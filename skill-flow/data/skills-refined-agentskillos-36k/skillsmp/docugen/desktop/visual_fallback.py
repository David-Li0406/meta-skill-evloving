"""Visual analysis integration layer for accessibility API fallback."""

import logging
from pathlib import Path
from typing import Optional, Dict

logger = logging.getLogger(__name__)


def analyze_with_fallback(
    screenshot_path: str | Path, x: int, y: int
) -> Optional[Dict]:
    """Convert visual analysis output to ElementMetadata format.

    Bridges the visual_analyzer.py output with the fallback system's
    expected ElementMetadata format.

    Args:
        screenshot_path: Path to screenshot image.
        x: X coordinate of click point.
        y: Y coordinate of click point.

    Returns:
        ElementMetadata dict with adjusted confidence, or None on failure.
    """
    try:
        from .visual_analyzer import analyze_screenshot_cached

        # Use cached analysis for performance
        elements = analyze_screenshot_cached(screenshot_path, click_coords=(x, y))

        if not elements:
            logger.debug("Visual analysis returned no elements at (%d, %d)", x, y)
            return None

        # Visual analysis may return multiple elements, select closest to coordinates
        if len(elements) > 1:
            element = _select_closest_element(elements, x, y)
        else:
            element = elements[0]

        # Adjust confidence score for visual analysis (typically lower than accessibility)
        if element.get("confidence", 0.0) > 0.7:
            element["confidence"] = 0.7  # Cap visual confidence

        # Ensure required fields exist
        element.setdefault("name", "Unknown")
        element.setdefault("type", "unknown")
        element.setdefault("bounds", {"x": x, "y": y, "width": 50, "height": 30})
        element["source"] = "visual"

        return element

    except ImportError:
        logger.error("visual_analyzer module not available for fallback")
        return None
    except Exception as e:
        logger.error("Visual fallback analysis failed: %s", e)
        return None


def _select_closest_element(elements: list[dict], x: int, y: int) -> dict:
    """Select the element closest to the specified coordinates.

    Args:
        elements: List of element dicts with bounds.
        x: Target X coordinate.
        y: Target Y coordinate.

    Returns:
        The closest element dict.
    """
    def distance_to_bounds(elem: dict) -> float:
        """Calculate distance from point to element bounds center."""
        bounds = elem.get("bounds", {})
        center_x = bounds.get("x", 0) + bounds.get("width", 0) / 2
        center_y = bounds.get("y", 0) + bounds.get("height", 0) / 2
        return ((center_x - x) ** 2 + (center_y - y) ** 2) ** 0.5

    return min(elements, key=distance_to_bounds)
