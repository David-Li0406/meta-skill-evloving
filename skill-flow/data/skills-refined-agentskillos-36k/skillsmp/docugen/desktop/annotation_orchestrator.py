"""Annotation placement orchestrator for desktop element identification.

Coordinates element identification, caching, fallback, and rendering to
produce annotated screenshots with pixel-perfect element highlighting.
"""

import io
import logging
import time
from typing import Optional, Union

from PIL import Image

from .annotation_cache import ElementCache, make_cache_key
from .annotation_config import AnnotationConfig
from .annotation_renderer import render_element_annotation
from .element_metadata import ElementMetadata
from .platform_router import get_element_metadata
from .platform_utils import get_dpi_scale

logger = logging.getLogger(__name__)

# Module-level cache instance
_element_cache = ElementCache()


def annotate_screenshot(
    image: Union[Image.Image, bytes],
    interaction_coords: tuple[int, int],
    platform: str,
    config: Optional[AnnotationConfig] = None,
    app_name: Optional[str] = None,
) -> bytes:
    """Annotate screenshot with identified element bounds.

    Main entry point for desktop element annotation. Coordinates element
    identification (via accessibility or visual analysis), caching, fallback,
    and rendering to produce an annotated screenshot.

    Args:
        image: PIL Image or bytes to annotate.
        interaction_coords: (x, y) screen coordinates of user interaction.
        platform: Platform identifier ('windows', 'macos', 'linux').
        config: Optional annotation configuration (uses defaults if None).
        app_name: Optional application name for caching.

    Returns:
        Annotated image as PNG bytes.
    """
    start_time = time.perf_counter()

    # Load config
    cfg = config or AnnotationConfig()

    # Convert image to PIL if bytes
    if isinstance(image, bytes):
        image = Image.open(io.BytesIO(image))

    # Get DPI scale factor
    dpi_scale = get_dpi_scale()

    # Get element metadata (with caching if enabled)
    element = _get_element_with_cache(
        interaction_coords,
        platform,
        app_name,
        cfg,
    )

    # Decide: use identified bounds or fallback to visual
    if element and element["confidence"] >= cfg.confidence_threshold:
        bounds = element["bounds"]
        source = element["source"]
        element_name = element.get("name", "Unknown")
        element_type = element.get("type", "unknown")
        logger.info(
            "Element ID: source=%s confidence=%.2f bounds=%s name=%s",
            source,
            element["confidence"],
            bounds,
            element_name,
        )
    else:
        # Fallback to visual analysis or simple click indicator
        if element:
            logger.warning(
                "Fallback to visual: reason=low_confidence (%.2f < %.2f)",
                element["confidence"],
                cfg.confidence_threshold,
            )
        else:
            logger.warning("Fallback to visual: reason=element_id_failed")

        # Attempt visual fallback
        element = _fallback_to_visual(image, interaction_coords)

        if element:
            bounds = element["bounds"]
            source = "visual_fallback"
            element_name = element.get("name", "Element")
            element_type = element.get("type", "unknown")
        else:
            # Last resort: simple click indicator (no element identification)
            logger.warning("Visual fallback failed; using click indicator only")
            bounds = {
                "x": interaction_coords[0] - 10,
                "y": interaction_coords[1] - 10,
                "width": 20,
                "height": 20,
            }
            source = "click_indicator"
            element_name = "Click"
            element_type = "indicator"

    # Get element-specific style
    style = cfg.get_style_for_type(element_type)

    # Render annotations
    render_start = time.perf_counter()
    annotated_bytes = render_element_annotation(
        image,
        bounds,
        element_name,
        element_type,
        style,
        dpi_scale,
    )
    render_time_ms = (time.perf_counter() - render_start) * 1000

    total_time_ms = (time.perf_counter() - start_time) * 1000
    element_query_time_ms = total_time_ms - render_time_ms

    logger.info(
        "Performance: element_query=%dms render=%dms total=%dms",
        int(element_query_time_ms),
        int(render_time_ms),
        int(total_time_ms),
    )

    return annotated_bytes


def _get_element_with_cache(
    coords: tuple[int, int],
    platform: str,
    app_name: Optional[str],
    config: AnnotationConfig,
) -> Optional[ElementMetadata]:
    """Get element metadata with optional caching.

    Args:
        coords: (x, y) screen coordinates.
        platform: Platform identifier.
        app_name: Application name for cache key.
        config: Annotation configuration.

    Returns:
        ElementMetadata or None if identification fails.
    """
    # Check cache if enabled
    if config.enable_cache:
        cache_key = make_cache_key(platform, app_name, coords[0], coords[1])
        cached = _element_cache.get(cache_key)
        if cached is not None:
            return cached

    # Query element identifier with timeout
    element = _query_element_with_timeout(coords, config.element_query_timeout_ms)

    # Cache successful results
    if element and config.enable_cache:
        cache_key = make_cache_key(platform, app_name, coords[0], coords[1])
        _element_cache.put(cache_key, element)

    return element


def _query_element_with_timeout(
    coords: tuple[int, int],
    timeout_ms: int,
) -> Optional[ElementMetadata]:
    """Query element identifier with timeout enforcement.

    Args:
        coords: (x, y) screen coordinates.
        timeout_ms: Timeout in milliseconds.

    Returns:
        ElementMetadata or None if timeout or failure.
    """
    import threading

    result = [None]
    error = [None]

    def query_thread():
        try:
            # Call platform router (no screenshot_path for pure accessibility)
            element = get_element_metadata(coords[0], coords[1], screenshot_path=None)
            result[0] = element
        except Exception as e:
            error[0] = e

    thread = threading.Thread(target=query_thread, daemon=True)
    thread.start()
    thread.join(timeout=timeout_ms / 1000.0)

    if thread.is_alive():
        logger.error(
            "Element ID timeout: platform=? coords=%s timeout=%dms",
            coords,
            timeout_ms,
        )
        return None

    if error[0]:
        logger.error("Element ID exception: %s", error[0])
        return None

    return result[0]


def _fallback_to_visual(
    image: Image.Image,
    coords: tuple[int, int],
) -> Optional[ElementMetadata]:
    """Fallback to visual analysis using Claude Vision.

    Args:
        image: PIL Image to analyze.
        coords: (x, y) click coordinates.

    Returns:
        ElementMetadata or None if visual analysis fails.
    """
    try:
        # Save image to temporary file for visual_analyzer
        import tempfile
        from pathlib import Path

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            image.save(tmp, format="PNG")
            tmp_path = Path(tmp.name)

        # Import and call visual analyzer
        from .visual_analyzer import analyze_screenshot

        elements = analyze_screenshot(str(tmp_path), click_coords=coords)

        # Clean up temp file
        tmp_path.unlink()

        if elements and len(elements) > 0:
            # Return first (closest/best) match
            elem = elements[0]
            # Ensure it's properly typed as ElementMetadata
            return {
                "bounds": elem["bounds"],
                "name": elem.get("name", "Element"),
                "type": elem.get("type", "unknown"),
                "confidence": elem.get("confidence", 0.5),
                "source": "visual",
                "app_name": None,
                "platform": "unknown",
            }

        return None

    except Exception as e:
        logger.error("Visual fallback failed: %s", e)
        return None


def get_cache() -> ElementCache:
    """Access the module-level element cache for stats or clearing.

    Returns:
        ElementCache instance used by annotate_screenshot.
    """
    return _element_cache
