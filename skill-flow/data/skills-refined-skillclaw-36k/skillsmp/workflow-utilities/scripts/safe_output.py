"""Safe cross-platform output utilities for Unicode characters.

Handles Windows console encoding issues (cp1252) by:
1. Attempting to reconfigure stdout to UTF-8
2. Providing ASCII fallbacks for special characters
"""

import sys
from typing import Any


# Try to reconfigure stdout to UTF-8 (Python 3.7+)
def _init_utf8():
    """Initialize UTF-8 encoding for stdout if possible."""
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            return True
        except Exception:
            pass
    return False


_UTF8_SUPPORTED = _init_utf8()


# Character mappings: Unicode -> ASCII fallback
SYMBOLS = {
    "checkmark": "✓" if _UTF8_SUPPORTED else "[OK]",
    "cross": "✗" if _UTF8_SUPPORTED else "[X]",
    "arrow": "→" if _UTF8_SUPPORTED else "->",
    "bullet": "•" if _UTF8_SUPPORTED else "*",
    "warning": "⚠" if _UTF8_SUPPORTED else "!",
}


def safe_print(*args: Any, **kwargs: Any) -> None:
    """Print with automatic fallback to ASCII on encoding errors."""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        # Convert to ASCII-safe string
        message = " ".join(str(arg) for arg in args)
        # Replace common Unicode characters
        message = message.replace("✓", "[OK]").replace("✗", "[X]").replace("→", "->").replace("•", "*").replace("⚠", "!")
        print(message, **kwargs)


def format_check(message: str) -> str:
    """Format a success message with checkmark."""
    return f"{SYMBOLS['checkmark']} {message}"


def format_cross(message: str) -> str:
    """Format an error message with cross."""
    return f"{SYMBOLS['cross']} {message}"


def format_arrow(left: str, right: str) -> str:
    """Format an arrow between two items."""
    return f"{left} {SYMBOLS['arrow']} {right}"


def format_warning(message: str) -> str:
    """Format a warning message."""
    return f"{SYMBOLS['warning']} {message}"


# Convenience functions
def print_success(message: str) -> None:
    """Print a success message."""
    safe_print(format_check(message))


def print_error(message: str) -> None:
    """Print an error message."""
    safe_print(format_cross(message))


def print_warning(message: str) -> None:
    """Print a warning message."""
    safe_print(format_warning(message))
