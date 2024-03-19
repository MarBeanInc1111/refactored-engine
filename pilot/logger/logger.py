import os
import re
import logging

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
sensitive_fields = ['--api-key', 'password']


def filter_sensitive_fields(record):
    # Replace sensitive fields in the log record with '*****'
    if isinstance(record.args, dict):  # check if args is a dictionary
        args = record.args.copy()
        for field in sensitive_fields:
            if field in args:
                args[field] = '*****'
        record.args = args

    elif isinstance(record.args, tuple):  # check if args is a tuple
        args_list = list(record.args)
        # Convert the tuple to a list and replace sensitive fields
        args_list = ['*****' if arg in sensitive_fields else arg for arg in args_list]
        record.args = tuple(args_list)

    # Remove ANSI escape sequences from the log message
    # This is necessary because some libraries (e.g. Peewee) may include escape sequences in their log messages
    if isinstance(record.msg, str):
        record.msg = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', record.msg)

    return True


# Create a logger instance
logger = setup_logger()
