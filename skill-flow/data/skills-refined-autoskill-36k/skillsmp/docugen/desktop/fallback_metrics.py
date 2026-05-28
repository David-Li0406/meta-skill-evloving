"""Metrics collection for accessibility API fallback behavior."""

import logging
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class MetricEntry:
    """Single metric entry for a fallback event."""

    timestamp: float
    app_name: Optional[str]
    platform: str
    source: str  # 'accessibility' or 'visual'
    success: bool
    latency_ms: float
    fallback_reason: Optional[str] = None


@dataclass
class AggregateStats:
    """Aggregated statistics for fallback behavior."""

    total_calls: int = 0
    accessibility_success: int = 0
    accessibility_failures: int = 0
    visual_fallbacks: int = 0
    avg_latency_ms: float = 0.0
    success_rate: float = 0.0
    fallback_rate: float = 0.0
    fallback_reasons: Dict[str, int] = field(default_factory=dict)


class MetricsCollector:
    """Collects and aggregates metrics for accessibility API fallback."""

    def __init__(self):
        self._entries: List[MetricEntry] = []
        self._app_entries: Dict[str, List[MetricEntry]] = defaultdict(list)
        self._cache_hits: int = 0
        self._cache_misses: int = 0

    def record_event(
        self,
        app_name: Optional[str],
        platform: str,
        source: str,
        success: bool,
        latency_ms: float,
        fallback_reason: Optional[str] = None,
    ):
        """Record a single fallback event."""
        entry = MetricEntry(
            timestamp=time.time(),
            app_name=app_name,
            platform=platform,
            source=source,
            success=success,
            latency_ms=latency_ms,
            fallback_reason=fallback_reason,
        )
        self._entries.append(entry)
        if app_name:
            self._app_entries[app_name].append(entry)

    def record_cache_hit(self):
        """Record a cache hit event."""
        self._cache_hits += 1

    def record_cache_miss(self):
        """Record a cache miss event."""
        self._cache_misses += 1

    def get_stats(self) -> AggregateStats:
        """Get aggregate statistics across all events."""
        if not self._entries:
            return AggregateStats()

        total = len(self._entries)
        accessibility_success = sum(
            1 for e in self._entries if e.source == "accessibility" and e.success
        )
        accessibility_failures = sum(
            1 for e in self._entries if e.source == "accessibility" and not e.success
        )
        visual_fallbacks = sum(1 for e in self._entries if e.source == "visual")

        avg_latency = sum(e.latency_ms for e in self._entries) / total

        fallback_reasons = defaultdict(int)
        for e in self._entries:
            if e.fallback_reason:
                fallback_reasons[e.fallback_reason] += 1

        success_rate = (accessibility_success + visual_fallbacks) / total if total > 0 else 0.0
        fallback_rate = visual_fallbacks / total if total > 0 else 0.0

        return AggregateStats(
            total_calls=total,
            accessibility_success=accessibility_success,
            accessibility_failures=accessibility_failures,
            visual_fallbacks=visual_fallbacks,
            avg_latency_ms=avg_latency,
            success_rate=success_rate,
            fallback_rate=fallback_rate,
            fallback_reasons=dict(fallback_reasons),
        )

    def get_app_stats(self, app_name: str) -> AggregateStats:
        """Get aggregate statistics for a specific application."""
        entries = self._app_entries.get(app_name, [])
        if not entries:
            return AggregateStats()

        total = len(entries)
        accessibility_success = sum(
            1 for e in entries if e.source == "accessibility" and e.success
        )
        accessibility_failures = sum(
            1 for e in entries if e.source == "accessibility" and not e.success
        )
        visual_fallbacks = sum(1 for e in entries if e.source == "visual")

        avg_latency = sum(e.latency_ms for e in entries) / total

        fallback_reasons = defaultdict(int)
        for e in entries:
            if e.fallback_reason:
                fallback_reasons[e.fallback_reason] += 1

        success_rate = (accessibility_success + visual_fallbacks) / total if total > 0 else 0.0
        fallback_rate = visual_fallbacks / total if total > 0 else 0.0

        return AggregateStats(
            total_calls=total,
            accessibility_success=accessibility_success,
            accessibility_failures=accessibility_failures,
            visual_fallbacks=visual_fallbacks,
            avg_latency_ms=avg_latency,
            success_rate=success_rate,
            fallback_rate=fallback_rate,
            fallback_reasons=dict(fallback_reasons),
        )

    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache hit/miss statistics."""
        total = self._cache_hits + self._cache_misses
        hit_rate = self._cache_hits / total if total > 0 else 0.0
        return {
            "hits": self._cache_hits,
            "misses": self._cache_misses,
            "hit_rate": hit_rate,
        }

    def reset(self):
        """Reset all metrics."""
        self._entries.clear()
        self._app_entries.clear()
        self._cache_hits = 0
        self._cache_misses = 0
        logger.debug("Metrics collector reset")
