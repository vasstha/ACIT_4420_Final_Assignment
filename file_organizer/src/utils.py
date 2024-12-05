import logging

def log_function_call(func):
    """
    Decorator to log function calls.
    """
    def wrapper(*args, **kwargs):
        logging.info(f"Function {func.__name__} called with args: {args}, kwargs: {kwargs}")
        return func(*args, **kwargs)
    return wrapper
