"""Centralized loguru configuration."""

import logging
import os
import sys

# Prevent litellm from installing a DEBUG StreamHandler at import time
os.environ.setdefault("LITELLM_LOG", "WARNING")
from pathlib import Path
from typing import Optional

from loguru import logger

# Remove loguru default handler, configure our own
logger.remove()

# Console sink -> stderr (don't pollute stdout)
# Default level is WARNING to avoid flooding the terminal;
# use setup_logging(console_level="DEBUG") for verbose output.
_CONSOLE_FORMAT = (
    "<green>{time:HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan> - "
    "<level>{message}</level>"
)
_console_sink_id: int = logger.add(
    sys.stderr,
    level="WARNING",
    format=_CONSOLE_FORMAT,
    colorize=True,
)

# Level mapping: FileLogger custom levels -> loguru levels
LEVEL_MAP = {
    "ok": "SUCCESS",
    "warn": "WARNING",
    "send": "INFO",
    "recv": "INFO",
    "tool": "INFO",
    "error": "ERROR",
}


def map_level(level: str) -> str:
    """Map custom log levels to loguru levels."""
    return LEVEL_MAP.get(level, level.upper())


class InterceptHandler(logging.Handler):
    """Route stdlib logging to loguru (intercepts uvicorn / litellm etc.)."""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging(console_level: str = "WARNING") -> None:
    """Install InterceptHandler and set console log level.

    Args:
        console_level: Log level for stderr console output (default WARNING).
                       Pass "DEBUG" for verbose terminal output.
    """
    global _console_sink_id
    # Swap console sink to the requested level
    logger.remove(_console_sink_id)
    _console_sink_id = logger.add(
        sys.stderr,
        level=console_level,
        format=_CONSOLE_FORMAT,
        colorize=True,
    )
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.WARNING, force=True)

    # Suppress liteLLM verbose debug output
    try:
        import litellm
        litellm.suppress_debug_info = True
        litellm.set_verbose = False
        litellm.num_retries = 3          # global retry default
        litellm.request_timeout = 600    # global timeout default (10min)
    except ImportError:
        pass

    # Always suppress liteLLM / httpx debug output regardless of -v flag
    _lib_level = logging.WARNING
    for name in ("LiteLLM", "litellm", "LiteLLM Proxy", "LiteLLM Router",
                 "httpx", "httpcore"):
        lg = logging.getLogger(name)
        lg.setLevel(_lib_level)
        lg.handlers.clear()
        lg.propagate = True


# -- FileLogger replacement utilities --

def add_file_sink(
    log_path: Path,
    level: str = "DEBUG",
    filter_key: Optional[str] = None,
) -> int:
    """Add a loguru file sink. Returns sink ID (for logger.remove())."""
    log_path.parent.mkdir(parents=True, exist_ok=True)

    if filter_key:
        sink_filter = lambda record: record["extra"].get("sink_key") == filter_key
    else:
        sink_filter = None

    return logger.add(
        str(log_path),
        level=level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        filter=sink_filter,
    )
