import logging
from logging.handlers import RotatingFileHandler

def setup_logger(log_file="app.log", log_level=logging.INFO):
    """
    Sets up a logger with console and file handlers.
    """
    # Create a logger
    logger = logging.getLogger("data_migration_logger")
    logger.setLevel(log_level)

    # Prevent multiple handlers if logger already exists
    if logger.hasHandlers():
        return logger

    # Format for logs
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Console handler (logs will show up in terminal)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (logs will be saved to a file with rotation)
    file_handler = RotatingFileHandler(log_file, maxBytes=1048576, backupCount=5)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
