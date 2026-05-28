"""Rate limiter for API clients."""

from __future__ import annotations

import time
from collections import deque


class RateLimiter:
    """Sliding window rate limiter with minimum interval.

    Ensures at most `max_requests` requests per `window_seconds`,
    and at least `min_interval` seconds between requests.
    """

    def __init__(
        self, max_requests: int, window_seconds: float, min_interval: float = 0
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.min_interval = min_interval
        self.timestamps: deque = deque()
        self.last_request: float = 0

    def wait(self):
        """Wait if necessary to respect rate limit."""
        now = time.monotonic()

        # Enforce minimum interval
        if self.min_interval > 0 and self.last_request > 0:
            elapsed = now - self.last_request
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
                now = time.monotonic()

        # Remove timestamps outside the window
        while self.timestamps and now - self.timestamps[0] >= self.window_seconds:
            self.timestamps.popleft()

        # If at limit, wait until oldest request exits the window
        if len(self.timestamps) >= self.max_requests:
            sleep_time = self.window_seconds - (now - self.timestamps[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
            self.timestamps.popleft()

        # Record this request
        now = time.monotonic()
        self.timestamps.append(now)
        self.last_request = now
