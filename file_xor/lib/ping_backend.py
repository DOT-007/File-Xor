import time


def calc_response_time_ms(start: float, end: float) -> int:
    """Return the elapsed time between start and end in milliseconds."""
    return int((end - start) * 1000)
