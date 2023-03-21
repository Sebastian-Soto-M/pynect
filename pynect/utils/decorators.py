import logging
import time
from functools import wraps


def timed(log=True):
    """Decorator that times the function it belongs to. You can set
    log to False if you want to print to standard output

    Args:
        log (bool, optional)
    """
    def timed_decorator(func):
        func_name = func.__name__
        logger = logging.getLogger(func_name).debug if log else print

        def _format_output(msg: str) -> str:
            divider = '-'*len(msg)
            return f'{divider}\n{msg}\n{divider}\n'

        @wraps(func)
        def wrapper_timer(*args, **kwargs):
            tic = time.perf_counter()
            logger(_format_output(f'Running: {func_name}'))
            value = func(*args, **kwargs)
            toc = time.perf_counter()
            elapsed_time = toc - tic
            logger(_format_output(f"Done: {elapsed_time:0.4f} seconds"))
            return elapsed_time, value
        return wrapper_timer
    return timed_decorator
