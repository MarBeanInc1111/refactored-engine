import os
import re
import logging
import inspect

def setup_logger():
    # Set up a custom logger with a custom format for your logs
    # The format includes the following: timestamp, filename, line number, function name, log level, and message
    log_format = "%(asctime)s [%(filename)s:%(lineno)s - %(funcName)20s() ] %(levelname)s: %(message)s"

    # Create a file handler for logging
    # The log file is named 'debug.log' and located in the same directory as this script
    file_handler = logging.FileHandler(
        filename=os.path.join(os.path.dirname(__file__), 'debug.log'),
        mode='w',
        encoding='utf-8',
    )

    # Apply the custom format to the file handler
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)

    # Add a filter to the file handler to exclude sensitive fields from the log
    file_handler.addFilter(filter_sensitive_fields)

    # Create a logger and add the file handler
    logger = logging.getLogger()
    logger.addHandler(file_handler)

    # Set the log level based on the 'DEBUG' environment variable
    if os.getenv('DEBUG') == 'true':
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    return logger

# Define a list of sensitive fields that should be filtered from the log
SENSITIVE_FIELDS = ['--api-key', 'password']

def filter_sensitive_fields(record):
    # Replace sensitive fields in the log record with '*****'
    if hasattr(inspect, "currentframe"):
        # Get the current frame and the frame where the log call was made
        current_frame = inspect.currentframe()
        log_frame = current_frame.f_back

        # Get the code object and the local variables of the log frame
        code_obj = log_frame.f_code
        local_vars = log_frame.f_locals

        # Check if the log message or arguments contain sensitive fields
        if 'msg' in local_vars and any(field in local_vars['msg'] for field in SENSITIVE_FIELDS):
            record.msg = re.sub(r'\b(' + '|'.join(SENSITIVE_FIELDS) + r')\b', '*****', local_vars['msg'])

        if 'args' in local_vars and isinstance(local_vars['args'], dict) and any(field in local_vars['args'] for field in SENSITIVE_FIELDS):
            args = local_vars['args'].copy()
            for field in SENSITIVE_FIELDS:
                if field in args:
                    args[field] = '*****'
            record.args = args

        elif 'args' in local_vars and isinstance(local_vars['args'], tuple) and any(arg in SENSITIVE_FIELDS for arg in local_vars['args']):
            args_list = list(local_vars['args'])
            # Convert the tuple to a list and replace sensitive fields
            args_list = ['*****' if arg in SENSITIVE_FIELDS else arg for arg in args_list]
            record.args = tuple(args_list)

    # Remove ANSI escape sequences from the log message
    # This is necessary because some libraries (e.g. Peewee) may include escape sequences in their log messages
    if isinstance(record.msg, str):
        record.msg = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', record.msg)

    return True

# Create a logger instance
logger = setup_logger()

# Example usage
logger.debug("This is a debug message with --api-key in it", extra={'--api-key': 'secret-key'})
