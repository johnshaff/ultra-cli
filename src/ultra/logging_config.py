# logging_config.py
import logging
import os
import io
from contextlib import redirect_stdout, redirect_stderr


def configure_logging(log_file="logs/transcribe.log", level=logging.DEBUG):
    os.makedirs("logs", exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove existing handlers to avoid multiple writes if configure_logging is called more than once
    root_logger.handlers = []

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s [%(name)s] [%(levelname)s] %(message)s"
    )
    file_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    
    # Set markdown-it logger to WARNING level to reduce verbose debug logs
    logging.getLogger('markdown_it').setLevel(logging.WARNING)



def redirect_nested_logs(func, *args, **kwargs):
    """
    Redirects stdout and stderr from a function call to the caller's logger.
    
    This function captures stdout and stderr from the called function and logs them.
    The caller should pass their logger explicitly or a module logger will be used.
    """
    logger = kwargs.pop('logger', logging.getLogger(__name__))
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
        result = func(*args, **kwargs)
    stdout_val = stdout_buf.getvalue()
    stderr_val = stderr_buf.getvalue()
    
    if stdout_val:
        logger.info("%s output:\n%s", func.__name__, stdout_val)
    if stderr_val:
        logger.error("%s errors:\n%s", func.__name__, stderr_val)
    return result