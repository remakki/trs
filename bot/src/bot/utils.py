import os
from datetime import datetime

from src import log


def to_normal_time(seconds: float) -> str:
    """
    Convert seconds since epoch to a human-readable date and time format.

    :param seconds: Seconds since epoch

    :return: Formatted date and time string in the format "DD-MM-YYYY HH:MM:SS"
    """

    return datetime.fromtimestamp(seconds).strftime("%H:%M:%S")

def delete_file(file: str) -> None:
    """
    Delete file if it exists.

    :param file: Path to the file to be deleted
    :return: None
    """
    try:
        if os.path.exists(file):
            os.remove(file)
            log.info(f"File {file} deleted successfully.")
        else:
            log.warning(f"File {file} not found for deletion.")
    except Exception as e:
        log.error(f"Error while deleting file {file}: {e}")
