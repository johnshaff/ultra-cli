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



def redirect_nested_logs(func, *args, **kwargs):
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
        result = func(*args, **kwargs)
    stdout_val = stdout_buf.getvalue()
    stderr_val = stderr_buf.getvalue()
    
    if stdout_val:
        logging.info("%s output:\n%s", func.__name__, stdout_val)
    if stderr_val:
        logging.error("%s errors:\n%s", func.__name__, stderr_val)
    return result