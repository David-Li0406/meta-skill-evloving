"""Cross-platform timeout enforcement for accessibility API calls."""

import logging
import platform
import signal
import threading
from functools import wraps
from typing import Callable, TypeVar, Any

logger = logging.getLogger(__name__)

T = TypeVar("T")


class TimeoutError(Exception):
    """Raised when a function execution exceeds timeout."""

    pass


def with_timeout(timeout_ms: int) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator that enforces timeout on function execution.

    Uses signal.alarm() on Unix platforms and threading.Timer on Windows.

    Args:
        timeout_ms: Maximum execution time in milliseconds.

    Returns:
        Decorated function that raises TimeoutError on timeout.

    Example:
        @with_timeout(100)
        def slow_function():
            time.sleep(1)  # Will raise TimeoutError
    """
    timeout_seconds = timeout_ms / 1000.0

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        if platform.system() == "Windows":
            return _windows_timeout(func, timeout_seconds)
        else:
            return _unix_timeout(func, timeout_seconds)

    return decorator


def _unix_timeout(func: Callable[..., T], timeout_seconds: float) -> Callable[..., T]:
    """Unix implementation using signal.alarm()."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        def _timeout_handler(signum, frame):
            raise TimeoutError(f"Function {func.__name__} timed out after {timeout_seconds}s")

        # Set the alarm
        old_handler = signal.signal(signal.SIGALRM, _timeout_handler)
        signal.setitimer(signal.ITIMER_REAL, timeout_seconds)

        try:
            result = func(*args, **kwargs)
        finally:
            # Cancel the alarm and restore previous handler
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, old_handler)

        return result

    return wrapper


def _windows_timeout(func: Callable[..., T], timeout_seconds: float) -> Callable[..., T]:
    """Windows implementation using threading.Timer."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        result_container = {"result": None, "exception": None, "completed": False}

        def _target():
            try:
                result_container["result"] = func(*args, **kwargs)
                result_container["completed"] = True
            except Exception as e:
                result_container["exception"] = e
                result_container["completed"] = True

        thread = threading.Thread(target=_target, daemon=True)
        thread.start()
        thread.join(timeout=timeout_seconds)

        if not result_container["completed"]:
            # Thread is still running - timeout occurred
            raise TimeoutError(f"Function {func.__name__} timed out after {timeout_seconds}s")

        if result_container["exception"]:
            raise result_container["exception"]

        return result_container["result"]

    return wrapper
