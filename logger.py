import logging
import os


def setup_logger(name: str, log_file: str = "app.log", level=logging.INFO):
    """
    Set up a logger with console and file handlers.

    Args:
        name (str): Name of the logger (usually __name__).
        log_file (str): Path to the log file.
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers if called multiple times
    if not logger.handlers:
        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(filename)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        # File handler
        fh = logging.FileHandler(log_file, mode="a")
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
