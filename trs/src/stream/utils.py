import os
import wave
import uuid
from pathlib import Path


def write_bytes_to_wav(
    audio_bytes: bytes,
    sample_rate: int = 16000,
    sample_width: int = 2,
    channels: int = 1,
    output_dir: str = "tmp",
) -> Path:
    """
    Write audio bytes to a WAV file.
    :param audio_bytes: Bytes representing the audio data.
    :param sample_rate: Sample rate of the audio (default is 16000).
    :param sample_width: Width of each sample in bytes (default is 2).
    :param channels: Number of audio channels (default is 1).
    :param output_dir: Directory where the WAV file will be saved.
    :return: Path to the created WAV file.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    filename = Path(output_dir) / f"{uuid.uuid4()}.wav"

    with wave.open(str(filename), "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_bytes)

    return filename


def delete_file(path: str) -> None:
    """
    Deletes a file at the specified path.
    :param path: Path to the file to be deleted.
    :return: None
    """
    try:
        os.remove(path)
    except FileNotFoundError:
        pass
