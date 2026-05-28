"""Hash-based cache for Claude Vision element identification responses.

Reduces redundant API calls by caching results keyed on screenshot
content hash. Cache entries expire after a configurable TTL.
"""

import hashlib
import logging
import time
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """A cached vision analysis result."""

    elements: list[dict]
    timestamp: float
    image_hash: str


class VisionCache:
    """In-memory cache for Claude Vision analysis results.

    Keys are SHA-256 hashes of screenshot image bytes. Entries expire
    after ttl_seconds (default: 300s / 5 minutes).
    """

    def __init__(self, ttl_seconds: float = 300.0, max_entries: int = 50):
        self._cache: dict[str, CacheEntry] = {}
        self._ttl = ttl_seconds
        self._max_entries = max_entries
        self._hits = 0
        self._misses = 0

    @property
    def hits(self) -> int:
        return self._hits

    @property
    def misses(self) -> int:
        return self._misses

    @property
    def size(self) -> int:
        return len(self._cache)

    def get(self, image_bytes: bytes) -> Optional[list[dict]]:
        """Look up cached elements for an image.

        Args:
            image_bytes: Raw screenshot bytes to look up.

        Returns:
            Cached element list if found and not expired, None otherwise.
        """
        key = self._hash(image_bytes)
        entry = self._cache.get(key)

        if entry is None:
            self._misses += 1
            return None

        if time.time() - entry.timestamp > self._ttl:
            del self._cache[key]
            self._misses += 1
            return None

        self._hits += 1
        return entry.elements

    def put(self, image_bytes: bytes, elements: list[dict]) -> None:
        """Store vision analysis results for an image.

        Args:
            image_bytes: Raw screenshot bytes as cache key.
            elements: Element identification results to cache.
        """
        if len(self._cache) >= self._max_entries:
            self._evict_oldest()

        key = self._hash(image_bytes)
        self._cache[key] = CacheEntry(
            elements=elements,
            timestamp=time.time(),
            image_hash=key,
        )

    def clear(self) -> None:
        """Clear all cached entries."""
        self._cache.clear()

    def _hash(self, image_bytes: bytes) -> str:
        """Compute SHA-256 hash of image bytes."""
        return hashlib.sha256(image_bytes).hexdigest()

    def _evict_oldest(self) -> None:
        """Remove the oldest cache entry."""
        if not self._cache:
            return
        oldest_key = min(self._cache, key=lambda k: self._cache[k].timestamp)
        del self._cache[oldest_key]
