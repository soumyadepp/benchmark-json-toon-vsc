import time


def read_raw(path: str) -> str:
    """Reads raw text from a file.

    Args:
        path (str): The file path to read from.

    Returns:
        str: The content of the file as a string.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def calculate_latency(start_time: float) -> float:
    """Calculate the latency given a start time.

    Args:
        start_time (float): The start time in seconds.

    Returns:
        float: The latency in seconds.
    """
    return time.time() - start_time
