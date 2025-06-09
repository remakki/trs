from pydub import AudioSegment
from pydub.silence import detect_silence


def get_split_ms(audio_bytes: bytes, sample_rate=16000) -> int:
    """
    Calculate the index in milliseconds where the last silence occurs in the audio bytes.
    This function uses the pydub library to analyze the audio data and detect silences.
    :param audio_bytes: Bytes representing the audio data.
    :param sample_rate: Sample rate of the audio (default is 16000).
    :return: The index in milliseconds where the last silence occurs.
    """
    audio = AudioSegment(
        data=audio_bytes,
        sample_width=2,
        frame_rate=sample_rate,
        channels=1,
    )

    silences = detect_silence(
        audio,
        min_silence_len=300,
        silence_thresh=-40,
    )

    if not silences:
        return 0

    last_silence = silences[-1]
    return sum(last_silence) // 2
