"""Debug helpers for reflect_sessions."""

from __future__ import annotations

import sys


def debug_print(*, enabled: bool, message: str) -> None:
    """Print a debug message when enabled.

    Args:
        enabled: Whether debug output is enabled.
        message: Message to print.
    """
    if enabled:
        print(message, file=sys.stderr)
