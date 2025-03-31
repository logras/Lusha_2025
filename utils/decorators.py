# utils/decorators.py
import time
import logging

LOGGER = logging.getLogger(__name__)

def time_func(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        LOGGER.info(f"Function {func.__name__} took {duration:.4f} seconds")
        return result
    return wrapper