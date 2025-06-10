import json
from datetime import timezone, datetime
from json import JSONDecodeError
from subprocess import Popen
from requests import HTTPError

from src import log
from src.api import AIClient, TranscriptionClient
from src.config import settings
from src.mq import RabbitMQ
from src.stream.detection import get_split_ms
from src.stream.ffmpeg import get_stream
from src.stream.schemas import Message
from src.stream.utils import write_bytes_to_wav, delete_file


class StreamService:
    """
    StreamService is responsible for processing audio streams, transcribing them,
    and interacting with AI and transcription clients to analyze the content.
    """

    def __init__(
        self,
        flow: str,
        sample_rate: int = 16000,
        flow_format: str = "s16le",
        sample_width: int = 2,
        chunk_duration: int = 30,
    ):
        self._flow = flow
        self._flow_format = flow_format
        self._stream: Popen[bytes] | None = None
        self._SAMPLE_RATE = sample_rate
        self._SAMPLE_WIDTH = sample_width
        self._CHUNK_DURATION = chunk_duration
        self._CHUNK_SIZE = sample_rate * chunk_duration * sample_width
        self._remaining_bytes = b""

        self._max_diff_time_for_last_message = 60 * 7

        self._messages: list[Message] = []
        self._time = datetime.now(timezone.utc).timestamp()

        self._ai_client = AIClient()
        self._transcription_client = TranscriptionClient()

    # TODO: Decompose this method into smaller methods for better readability and maintainability.
    def process(self) -> None:
        """
        Process the audio stream by reading data in chunks, transcribing it,
        and sending the results to the AI service for analysis.
        :return: None
        """
        self._stream = get_stream(
            flow=self._flow,
            sample_rate=self._SAMPLE_RATE,
            flow_format=self._flow_format,
        )

        with RabbitMQ() as mq:
            while True:
                if not self._stream:
                    raise RuntimeError("Failed to start stream process.")

                data = self._stream.stdout.read(self._CHUNK_SIZE)
                log.info(f"Chunk size readed: {len(data)} bytes")

                if not data:
                    try:
                        self._stream.terminate()
                    finally:
                        self._stream = get_stream(
                            flow=self._flow,
                            sample_rate=self._SAMPLE_RATE,
                            flow_format=self._flow_format,
                        )
                        self._time = datetime.now(timezone.utc).timestamp()
                        continue

                self._remaining_bytes += data

                split_ms = get_split_ms(self._remaining_bytes, self._SAMPLE_RATE)
                split_seconds = split_ms / 1000
                samples = int(split_seconds * self._SAMPLE_RATE)
                byte_index = samples * self._SAMPLE_WIDTH

                audio_bytes = self._remaining_bytes[:byte_index]
                self._remaining_bytes = self._remaining_bytes[byte_index:]

                if len(audio_bytes) == 0:
                    continue

                file_path = write_bytes_to_wav(audio_bytes)

                segments = []

                try:
                    log.info("Transcribing...")
                    segments = self._transcription_client.transcribe(str(file_path))
                except HTTPError as e:
                    log.error(e)

                delete_file(str(file_path))

                if not segments:
                    continue

                message = "\n".join(
                    f"[{self._time + segment['start']} - "
                    f"{self._time + segment['end']}] "
                    f"{segment['text']}"
                    for segment in segments
                )
                log.info(f"message: {message}")

                self._messages.append(
                    {
                        "content": message,
                        "start": self._time + segments[0]["start"],
                        "end": self._time + segments[-1]["end"],
                    }
                )

                self._time += split_seconds

                result: str | None = None

                try:
                    result = self._ai_client.chat_completions(
                        "trs-analyzer-main", self._messages
                    )
                except HTTPError as e:
                    log.error(f"HTTP error: {e}")

                if not result:
                    continue

                log.info(f"Chat result: {result}")

                if result.strip() == "-":
                    if (
                        self._messages[-1]["start"]
                        < self._time - self._max_diff_time_for_last_message
                    ):
                        self._messages = self._messages[1:]
                    continue

                if result.strip() == "wait":
                    continue

                result = (
                    result.replace("```json", "")
                    .replace("```text", "")
                    .replace("```", "")
                    .replace("“", '"')
                    .replace("”", '"')
                    .strip("`")
                )

                try:
                    result_json = json.loads(result)

                    mq.publish(settings.RABBITMQ_QUEUE, json.dumps(result_json))

                except JSONDecodeError as e:
                    log.error(f"JSONDecodeError: {e}")
                finally:
                    self._messages = []
