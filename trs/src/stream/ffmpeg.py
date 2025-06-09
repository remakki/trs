import subprocess


def get_stream(
    flow: str, sample_rate: int = 16000, flow_format: str = "s16le"
) -> subprocess.Popen:
    """
    Get a subprocess stream for the given flow.
    This function uses ffmpeg to convert the input flow into a raw audio stream.
    :param flow: The input flow, which can be a file path or a URL.
    :param sample_rate: The sample rate for the audio stream (default is 16000).
    :param flow_format: The format of the audio stream (default is "s16le" for 16-bit signed little-endian PCM).
    :return: subprocess.Popen object that streams the audio data.
    """
    return subprocess.Popen(
        [
            "ffmpeg",
            "-i",
            flow,
            "-ac",
            "1",
            "-ar",
            str(sample_rate),
            "-f",
            flow_format,
            "pipe:1",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        bufsize=10**8,
    )
