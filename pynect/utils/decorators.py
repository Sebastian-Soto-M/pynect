import logging
import time
from functools import wraps
from typing import Optional

from .utils import configure_logger


def timeit(
    logger: Optional[logging.Logger] = None,
    level: int = logging.DEBUG,  # Default to DEBUG level
):
    def decorator(func):
        if (lgr := logger) is None:
            lgr = configure_logger(func.__module__)
        func_name = func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            start_time = time.time()
            end_time = time.time()
            elapsed_time = end_time - start_time
            message = f"{func_name} took {elapsed_time*1000:.4f}ms"
            lgr.log(level, message)  # Use the specified log level
            return result
        wrapper.__name__ = func_name
        wrapper.__doc__ = func.__doc__
        return wrapper
    return decorator
