from datetime import datetime


def to_normal_time(seconds: float) -> str:
    """
    Convert seconds since epoch to a human-readable date and time format.

    :param seconds: Seconds since epoch

    :return: Formatted date and time string in the format "DD-MM-YYYY HH:MM:SS"
    """

    return datetime.fromtimestamp(seconds).strftime("%H:%M:%S")
