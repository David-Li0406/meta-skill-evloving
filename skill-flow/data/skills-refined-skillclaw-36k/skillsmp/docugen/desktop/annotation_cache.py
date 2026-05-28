"""LRU cache for element metadata to reduce redundant accessibility API calls.

Caches element metadata keyed by (platform, app_name, coord_hash) to avoid
repeated queries when annotating similar screenshots.
"""

import logging
from collections import OrderedDict
from typing import Optional

from .element_metadata import ElementMetadata

logger = logging.getLogger(__name__)


class ElementCache:
    """LRU cache for element metadata with configurable size limit.

    Reduces redundant accessibility API calls by caching element metadata
    keyed by platform, app name, and coordinate hash (bucketed to 10px grid).

    Attributes:
        max_size: Maximum number of cached entries (default: 100).
    """

    def __init__(self, max_size: int = 100):
        """Initialize cache with size limit.

        Args:
            max_size: Maximum number of entries before LRU eviction.
        """
        self._cache: OrderedDict = OrderedDict()
        self._max_size = max_size
        self._stats = {"hits": 0, "misses": 0}

    def get(self, key: tuple) -> Optional[ElementMetadata]:
        """Retrieve cached element metadata.

        Moves accessed entry to end (most recently used).

        Args:
            key: Cache key tuple (platform, app_name, coord_hash).

        Returns:
            Cached ElementMetadata or None if not found.
        """
        if key in self._cache:
            self._stats["hits"] += 1
            # Move to end (most recently used)
            self._cache.move_to_end(key)
            logger.debug(
                "Cache hit for key=%s (hit_rate=%.2f%%)",
                key,
                self.hit_rate() * 100,
            )
            return self._cache[key]

        self._stats["misses"] += 1
        return None

    def put(self, key: tuple, value: ElementMetadata) -> None:
        """Store element metadata in cache.

        Evicts least recently used entry if cache is full.

        Args:
            key: Cache key tuple (platform, app_name, coord_hash).
            value: ElementMetadata to cache.
        """
        if key in self._cache:
            # Update existing entry and move to end
            self._cache.move_to_end(key)
        else:
            # Add new entry
            self._cache[key] = value

            # Evict LRU if over limit
            if len(self._cache) > self._max_size:
                evicted_key = next(iter(self._cache))
                del self._cache[evicted_key]
                logger.debug("Cache evicted LRU entry: %s", evicted_key)

    def hit_rate(self) -> float:
        """Calculate cache hit rate.

        Returns:
            Hit rate as fraction 0.0-1.0 (0 if no queries yet).
        """
        total = self._stats["hits"] + self._stats["misses"]
        if total == 0:
            return 0.0
        return self._stats["hits"] / total

    def clear(self) -> None:
        """Clear all cached entries and reset statistics."""
        self._cache.clear()
        self._stats = {"hits": 0, "misses": 0}
        logger.info("Cache cleared")

    def size(self) -> int:
        """Get current cache size.

        Returns:
            Number of cached entries.
        """
        return len(self._cache)

    def stats(self) -> dict:
        """Get cache statistics.

        Returns:
            Dict with hits, misses, hit_rate, and size.
        """
        return {
            "hits": self._stats["hits"],
            "misses": self._stats["misses"],
            "hit_rate": self.hit_rate(),
            "size": len(self._cache),
        }


def make_cache_key(platform: str, app_name: Optional[str], x: int, y: int) -> tuple:
    """Generate cache key from platform, app, and coordinates.

    Coordinates are bucketed to 10px grid to increase cache hit rate for
    nearby clicks on the same element.

    Args:
        platform: Platform identifier ('windows', 'macos', 'linux').
        app_name: Application name (e.g., 'Google Chrome') or None.
        x: Screen X coordinate.
        y: Screen Y coordinate.

    Returns:
        Cache key tuple (platform, app_name, coord_x_bucket, coord_y_bucket).
    """
    # Bucket coordinates to 10px grid to increase cache hits
    coord_x_bucket = x // 10
    coord_y_bucket = y // 10

    return (platform, app_name or "unknown", coord_x_bucket, coord_y_bucket)
