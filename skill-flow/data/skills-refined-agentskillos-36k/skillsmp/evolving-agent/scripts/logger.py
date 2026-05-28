"""
Logging utility for Evolving Programming Agent.

Provides centralized logging configuration for all scripts.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


# Default log file location
DEFAULT_LOG_FILE = Path.home() / '.config' / 'evolving-agent.log'


def setup_logging(
    level: str = 'INFO',
    log_file: str | None = None,
    console_output: bool = True
) -> logging.Logger:
    """
    Setup logging for the evolving agent.

    Args:
        level: Log level (DEBUG, INFO, WARN, ERROR)
        log_file: Path to log file (uses default if None)
        console_output: Whether to output to console

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger('evolving-agent')
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Remove existing handlers
    logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler
    log_path = Path(log_file) if log_file else DEFAULT_LOG_FILE
    log_path.parent.mkdir(parents=True, exist_ok=True)

    file_handler = logging.FileHandler(str(log_path), encoding='utf-8')

    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


def get_logger(name: str = 'evolving-agent') -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)

    # Setup default logging if not configured
    if not logger.handlers:
        setup_logging()

    return logger


def log_execution(logger: logging.Logger, func_name: str):
    """
    Decorator to log function execution.

    Args:
        logger: Logger instance
        func_name: Function name (optional, defaults to __name__)

    Returns:
        Decorated function
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.debug(f"Executing: {func_name}")
            try:
                result = func(*args, **kwargs)
                logger.debug(f"Completed: {func_name}")
                return result
            except Exception as e:
                logger.error(f"Error in {func_name}: {e}", exc_info=True)
                raise
        return wrapper
    return decorator


if __name__ == '__main__':
    # Test logging
    logger = setup_logging(level='DEBUG')
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    print(f"Logs written to: {DEFAULT_LOG_FILE}")
