#!/usr/bin/env python3
"""Standardized error handling utilities for all skills.

This module provides consistent error handling, logging, and status output
across all skill scripts in the workflow system.

Usage:
    from error_utils import error_exit, warn, success, fail, info

Example:
    from error_utils import error_exit, success, fail

    if not validate_input(data):
        error_exit("Invalid input format", code=1)

    success("Operation completed")
"""

import sys
from typing import NoReturn


def error_exit(message: str, code: int = 1) -> NoReturn:
    """Print error message to stderr and exit with code.

    Args:
        message: Error message to display
        code: Exit code (default: 1)

    Returns:
        Never returns (exits process)
    """
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(code)


def warn(message: str) -> None:
    """Print warning message to stderr.

    Args:
        message: Warning message to display
    """
    print(f"WARNING: {message}", file=sys.stderr)


def success(message: str) -> None:
    """Print success message with checkmark.

    Args:
        message: Success message to display
    """
    print(f"\u2713 {message}")


def fail(message: str) -> None:
    """Print failure message with X mark.

    Args:
        message: Failure message to display
    """
    print(f"\u2717 {message}")


def info(message: str) -> None:
    """Print informational message.

    Args:
        message: Info message to display
    """
    print(f"\u2192 {message}")


def progress(message: str) -> None:
    """Print progress indicator message.

    Args:
        message: Progress message to display
    """
    print(f"... {message}")


def header(title: str, width: int = 60) -> None:
    """Print formatted header line.

    Args:
        title: Header title
        width: Total width of header line (default: 60)
    """
    print("=" * width)
    print(title)
    print("=" * width)


def subheader(title: str) -> None:
    """Print formatted subheader.

    Args:
        title: Subheader title
    """
    print(f"\n[{title}]")


class StatusReporter:
    """Context manager for reporting operation status.

    Usage:
        with StatusReporter("Running tests") as status:
            result = run_tests()
            if result:
                status.success()
            else:
                status.fail("Tests failed")
    """

    def __init__(self, operation: str):
        """Initialize status reporter.

        Args:
            operation: Description of the operation being performed
        """
        self.operation = operation
        self._completed = False
        self._status = None

    def __enter__(self) -> "StatusReporter":
        """Enter context and print operation start."""
        progress(self.operation)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Exit context and print final status if not already reported."""
        if not self._completed:
            if exc_type is not None:
                fail(f"{self.operation} (exception: {exc_val})")
            else:
                warn(f"{self.operation} (no status reported)")
        return False  # Don't suppress exceptions

    def success(self, message: str | None = None) -> None:
        """Report success status.

        Args:
            message: Optional success message (defaults to operation name)
        """
        self._completed = True
        self._status = "success"
        success(message or self.operation)

    def fail(self, message: str | None = None) -> None:
        """Report failure status.

        Args:
            message: Optional failure message (defaults to operation name)
        """
        self._completed = True
        self._status = "fail"
        fail(message or self.operation)

    def skip(self, reason: str) -> None:
        """Report skipped status.

        Args:
            reason: Reason for skipping
        """
        self._completed = True
        self._status = "skip"
        warn(f"{self.operation} (skipped: {reason})")
