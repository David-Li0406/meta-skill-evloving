"""Core fallback manager for accessibility API failures.

Implements robust fallback mechanism that transitions from platform
accessibility APIs to visual element analysis when APIs are unavailable,
denied, or timeout.
"""

import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict

from .fallback_config import FallbackConfig
from .fallback_metrics import MetricsCollector
from .macos_permissions import check_accessibility_permission, get_permission_instructions
from .platform_utils import get_os
from .timeout_wrapper import with_timeout, TimeoutError
from .visual_fallback import analyze_with_fallback

logger = logging.getLogger(__name__)


@dataclass
class ElementMetadata:
    """Standardized element metadata from accessibility API or visual analysis."""

    name: str
    type: str
    bounds: Dict[str, int]  # x, y, width, height
    confidence_score: float
    source: str  # 'accessibility' or 'visual'
    fallback_used: bool
    fallback_reason: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary format for compatibility."""
        return {
            "name": self.name,
            "type": self.type,
            "bounds": self.bounds,
            "confidence": self.confidence_score,
            "source": self.source,
            "fallback_used": self.fallback_used,
            "fallback_reason": self.fallback_reason,
        }


class FallbackManager:
    """Manages fallback from accessibility APIs to visual analysis."""

    def __init__(self, config: Optional[FallbackConfig] = None):
        self._config = config or FallbackConfig.from_env()
        self._metrics = MetricsCollector()
        self._app_timeout_counts: Dict[str, int] = {}
        self._app_support_cache: Dict[str, bool] = {}
        self._cache_timestamps: Dict[str, float] = {}

    def get_element_metadata_with_fallback(
        self,
        x: int,
        y: int,
        platform: str,
        screenshot_path: Optional[str] = None,
        app_name: Optional[str] = None,
    ) -> Optional[ElementMetadata]:
        """Get element metadata with automatic fallback to visual analysis.

        Main interface for retrieving element metadata. Tries accessibility API
        first with timeout enforcement and permission checking, falls back to
        visual analysis on failure.

        Args:
            x: Screen X coordinate.
            y: Screen Y coordinate.
            platform: Platform identifier (windows, macos, linux).
            screenshot_path: Path to screenshot for visual fallback.
            app_name: Optional application name for metrics/caching.

        Returns:
            ElementMetadata or None if all methods fail.
        """
        start_time = time.time()

        # Check if app is cached as unsupported
        if app_name and self._is_app_cached_unsupported(app_name):
            logger.debug("App %s cached as unsupported, using visual fallback", app_name)
            self._metrics.record_cache_hit()
            return self._try_visual_fallback(
                x, y, screenshot_path, app_name, platform, "unsupported"
            )

        self._metrics.record_cache_miss()

        # Try accessibility API with fallback handling
        result = self._try_accessibility_api(x, y, platform, app_name)

        if result:
            latency_ms = (time.time() - start_time) * 1000
            self._metrics.record_event(
                app_name, platform, "accessibility", True, latency_ms
            )
            return result

        # Accessibility failed, try visual fallback
        if screenshot_path and self._config.visual_fallback_enabled:
            return self._try_visual_fallback(
                x, y, screenshot_path, app_name, platform, "error"
            )

        logger.warning("All element detection methods failed at (%d, %d)", x, y)
        return None

    def _try_accessibility_api(
        self,
        x: int,
        y: int,
        platform: str,
        app_name: Optional[str],
    ) -> Optional[ElementMetadata]:
        """Attempt to get element metadata via accessibility API.

        Wraps accessibility API calls with timeout, permission checking,
        and exception handling.

        Returns:
            ElementMetadata or None on failure.
        """
        # Check for exponential backoff
        if app_name and self._app_timeout_counts.get(app_name, 0) >= self._config.max_retries:
            logger.debug("App %s exceeded timeout threshold, skipping accessibility", app_name)
            return None

        # macOS permission check
        if platform == "macos":
            if not check_accessibility_permission():
                logger.warning(
                    "macOS accessibility permission denied. %s",
                    get_permission_instructions()
                )
                return None

        try:
            # Get backend and wrap with timeout
            element_dict = self._get_element_with_timeout(x, y, platform)

            if element_dict:
                # Reset timeout count on success
                if app_name:
                    self._app_timeout_counts[app_name] = 0

                return ElementMetadata(
                    name=element_dict.get("name", "Unknown"),
                    type=element_dict.get("type", "unknown"),
                    bounds=element_dict.get("bounds", {"x": x, "y": y, "width": 50, "height": 30}),
                    confidence_score=element_dict.get("confidence", 0.9),
                    source="accessibility",
                    fallback_used=False,
                )

        except TimeoutError:
            logger.info(
                "[FALLBACK] reason=timeout app=%s coords=(%d,%d) latency=%dms",
                app_name or "unknown",
                x,
                y,
                self._config.timeout_ms,
            )
            # Increment timeout count for exponential backoff
            if app_name:
                self._app_timeout_counts[app_name] = self._app_timeout_counts.get(app_name, 0) + 1
            return None

        except PermissionError:
            logger.warning(
                "[FALLBACK] reason=permission_denied app=%s coords=(%d,%d). %s",
                app_name or "unknown",
                x,
                y,
                get_permission_instructions(),
            )
            return None

        except Exception as e:
            logger.error(
                "[FALLBACK] reason=error app=%s coords=(%d,%d) error=%s",
                app_name or "unknown",
                x,
                y,
                str(e),
            )
            # Cache app as unsupported after persistent failures
            if app_name and "not found" in str(e).lower():
                self._cache_app_unsupported(app_name)
            return None

        return None

    def _get_element_with_timeout(self, x: int, y: int, platform: str) -> Optional[dict]:
        """Get element from accessibility API with timeout enforcement."""

        @with_timeout(self._config.timeout_ms)
        def _timed_get_element():
            from .platform_router import get_accessibility_backend

            backend = get_accessibility_backend()
            if backend is None:
                return None
            return backend.get_element_at_point(x, y)

        return _timed_get_element()

    def _try_visual_fallback(
        self,
        x: int,
        y: int,
        screenshot_path: Optional[str],
        app_name: Optional[str],
        platform: str,
        fallback_reason: str,
    ) -> Optional[ElementMetadata]:
        """Try visual analysis as fallback method."""
        if not screenshot_path:
            logger.debug("No screenshot provided for visual fallback")
            return None

        start_time = time.time()
        element_dict = analyze_with_fallback(screenshot_path, x, y)
        latency_ms = (time.time() - start_time) * 1000

        if element_dict:
            logger.info(
                "[FALLBACK] reason=%s app=%s coords=(%d,%d) latency=%.1fms source=visual",
                fallback_reason,
                app_name or "unknown",
                x,
                y,
                latency_ms,
            )

            self._metrics.record_event(
                app_name, platform, "visual", True, latency_ms, fallback_reason
            )

            return ElementMetadata(
                name=element_dict.get("name", "Unknown"),
                type=element_dict.get("type", "unknown"),
                bounds=element_dict.get("bounds", {"x": x, "y": y, "width": 50, "height": 30}),
                confidence_score=element_dict.get("confidence", 0.5),
                source="visual",
                fallback_used=True,
                fallback_reason=fallback_reason,
            )

        self._metrics.record_event(
            app_name, platform, "visual", False, latency_ms, fallback_reason
        )
        return None

    def _is_app_cached_unsupported(self, app_name: str) -> bool:
        """Check if app is cached as unsupported and cache is still valid."""
        if app_name not in self._app_support_cache:
            return False

        # Check if cache has expired
        timestamp = self._cache_timestamps.get(app_name, 0)
        if time.time() - timestamp > self._config.cache_ttl_seconds:
            # Cache expired, remove it
            del self._app_support_cache[app_name]
            del self._cache_timestamps[app_name]
            logger.debug("Cache expired for app %s", app_name)
            return False

        return not self._app_support_cache[app_name]

    def _cache_app_unsupported(self, app_name: str):
        """Mark app as unsupported in cache."""
        self._app_support_cache[app_name] = False
        self._cache_timestamps[app_name] = time.time()
        logger.debug("Cached app %s as unsupported (TTL: %ds)", app_name, self._config.cache_ttl_seconds)

    def get_metrics(self) -> MetricsCollector:
        """Access metrics collector for stats retrieval."""
        return self._metrics


# Global fallback manager instance
_manager: Optional[FallbackManager] = None


def get_element_metadata_with_fallback(
    x: int,
    y: int,
    platform: str,
    screenshot_path: Optional[str] = None,
    app_name: Optional[str] = None,
    config: Optional[FallbackConfig] = None,
) -> Optional[ElementMetadata]:
    """Convenience function to get element metadata with fallback.

    Uses a module-level singleton manager instance.

    Args:
        x: Screen X coordinate.
        y: Screen Y coordinate.
        platform: Platform identifier.
        screenshot_path: Optional screenshot for visual fallback.
        app_name: Optional app name for caching/metrics.
        config: Optional custom configuration.

    Returns:
        ElementMetadata or None.
    """
    global _manager
    if _manager is None or config is not None:
        _manager = FallbackManager(config)

    return _manager.get_element_metadata_with_fallback(
        x, y, platform, screenshot_path, app_name
    )
