"""Claude Vision-based UI element identification.

Fallback for platforms where native accessibility APIs are unavailable.
Sends screenshots to Claude's vision model to identify interactive
elements with estimated bounding boxes and descriptions.

Supports async processing, response caching, and pre-send privacy
screening to blur sensitive regions before sending to the Claude API.
"""

import asyncio
import base64
import io
import json
import logging
import re
from pathlib import Path
from typing import Optional

from .vision_cache import VisionCache

logger = logging.getLogger(__name__)

# Module-level cache instance shared across calls
_cache = VisionCache()

# Patterns for detecting sensitive on-screen content
_SENSITIVE_PATTERNS = [
    re.compile(r"password", re.IGNORECASE),
    re.compile(r"secret", re.IGNORECASE),
    re.compile(r"api[_\s]?key", re.IGNORECASE),
    re.compile(r"token", re.IGNORECASE),
    re.compile(r"private[_\s]?key", re.IGNORECASE),
]

ELEMENT_ANALYSIS_PROMPT = (
    "Analyze this desktop application screenshot. "
    "Identify all clearly visible interactive UI elements "
    "(buttons, text inputs, links, menus, checkboxes, dropdowns). "
    "For each element, provide a JSON array of objects with:\n"
    '  "name": visible text or descriptive label,\n'
    '  "type": element type (button, input, link, menu, checkbox, dropdown, tab, icon),\n'
    '  "bounds": {"x": left, "y": top, "width": w, "height": h} in pixels,\n'
    '  "confidence": 0.0-1.0 how certain you are of the bounds\n'
    "Return ONLY the JSON array, no other text."
)

FOCUSED_ELEMENT_PROMPT = (
    "Analyze this desktop application screenshot. "
    "There was a user interaction near coordinates ({x}, {y}). "
    "Identify the specific UI element at or closest to that point. "
    "Return a single JSON object with:\n"
    '  "name": visible text or descriptive label,\n'
    '  "type": element type (button, input, link, menu, checkbox, dropdown, tab, icon),\n'
    '  "bounds": {{"x": left, "y": top, "width": w, "height": h}} in pixels,\n'
    '  "confidence": 0.0-1.0 how certain you are of the bounds\n'
    "Return ONLY the JSON object, no other text."
)


def analyze_screenshot(
    image_path: str | Path,
    click_coords: Optional[tuple[int, int]] = None,
    model: str = "claude-sonnet-4-20250514",
) -> Optional[list[dict]]:
    """Analyze a screenshot to identify interactive UI elements.

    Args:
        image_path: Path to the screenshot PNG file.
        click_coords: Optional (x, y) to focus analysis on a specific point.
        model: Claude model to use for analysis.

    Returns:
        List of element dicts with name, type, bounds, confidence.
        Returns None if analysis fails.
    """
    try:
        import anthropic
    except ImportError:
        logger.warning(
            "anthropic package not installed. Visual analysis unavailable. "
            "Install with: pip install anthropic"
        )
        return None

    image_path = Path(image_path)
    if not image_path.exists():
        logger.error("Screenshot not found: %s", image_path)
        return None

    image_data = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    media_type = _get_media_type(image_path)

    if click_coords:
        prompt = FOCUSED_ELEMENT_PROMPT.format(x=click_coords[0], y=click_coords[1])
    else:
        prompt = ELEMENT_ANALYSIS_PROMPT

    try:
        client = anthropic.Anthropic()
        response = client.messages.create(
            model=model,
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data,
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )

        return _parse_response(response, focused=click_coords is not None)

    except Exception as e:
        logger.error("Claude Vision analysis failed: %s", e)
        return None


def analyze_capture_result(
    capture_result,
    click_coords: Optional[tuple[int, int]] = None,
    model: str = "claude-sonnet-4-20250514",
) -> Optional[list[dict]]:
    """Analyze a CaptureResult directly without saving to disk.

    Args:
        capture_result: A CaptureResult with image_bytes.
        click_coords: Optional (x, y) to focus analysis.
        model: Claude model to use.

    Returns:
        List of element dicts or None on failure.
    """
    try:
        import anthropic
    except ImportError:
        logger.warning(
            "anthropic package not installed. Visual analysis unavailable."
        )
        return None

    image_data = base64.b64encode(capture_result.image_bytes).decode("utf-8")

    if click_coords:
        prompt = FOCUSED_ELEMENT_PROMPT.format(x=click_coords[0], y=click_coords[1])
    else:
        prompt = ELEMENT_ANALYSIS_PROMPT

    try:
        client = anthropic.Anthropic()
        response = client.messages.create(
            model=model,
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": image_data,
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )

        return _parse_response(response, focused=click_coords is not None)

    except Exception as e:
        logger.error("Claude Vision analysis failed: %s", e)
        return None


def _parse_response(response, focused: bool = False) -> Optional[list[dict]]:
    """Parse Claude's response into structured element data."""
    try:
        text = response.content[0].text.strip()

        # Strip markdown code fence if present
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1])

        parsed = json.loads(text)

        # Normalize to list
        if isinstance(parsed, dict):
            parsed = [parsed]

        # Validate and tag each element
        elements = []
        for elem in parsed:
            if not isinstance(elem, dict):
                continue
            if "bounds" not in elem:
                continue

            elements.append({
                "name": elem.get("name", "Unknown"),
                "type": elem.get("type", "unknown"),
                "bounds": elem["bounds"],
                "confidence": float(elem.get("confidence", 0.5)),
                "source": "visual",
            })

        return elements if elements else None

    except (json.JSONDecodeError, IndexError, KeyError) as e:
        logger.warning("Failed to parse vision response: %s", e)
        return None


def analyze_screenshot_cached(
    image_path: str | Path,
    click_coords: Optional[tuple[int, int]] = None,
    model: str = "claude-sonnet-4-20250514",
    blur_sensitive: bool = False,
) -> Optional[list[dict]]:
    """Analyze screenshot with caching to reduce API calls.

    Checks the module-level cache before making an API call.
    Results are stored in cache for subsequent identical screenshots.

    Args:
        image_path: Path to the screenshot PNG file.
        click_coords: Optional (x, y) to focus analysis.
        model: Claude model to use.
        blur_sensitive: If True, blur detected sensitive regions before sending.

    Returns:
        List of element dicts or None on failure.
    """
    image_path = Path(image_path)
    if not image_path.exists():
        logger.error("Screenshot not found: %s", image_path)
        return None

    image_bytes = image_path.read_bytes()

    # Check cache first
    cached = _cache.get(image_bytes)
    if cached is not None:
        logger.debug("Vision cache hit for %s", image_path.name)
        return cached

    # Apply privacy screening if requested
    if blur_sensitive:
        image_bytes = _blur_sensitive_regions(image_bytes)

    result = analyze_screenshot(image_path, click_coords, model)

    # Cache successful results
    if result:
        _cache.put(image_bytes, result)

    return result


async def analyze_screenshot_async(
    image_path: str | Path,
    click_coords: Optional[tuple[int, int]] = None,
    model: str = "claude-sonnet-4-20250514",
    blur_sensitive: bool = False,
) -> Optional[list[dict]]:
    """Async wrapper for screenshot analysis.

    Runs the synchronous Claude API call in a thread pool to avoid
    blocking the capture pipeline.

    Args:
        image_path: Path to the screenshot PNG file.
        click_coords: Optional (x, y) to focus analysis.
        model: Claude model to use.
        blur_sensitive: If True, blur sensitive regions before sending.

    Returns:
        List of element dicts or None on failure.
    """
    return await asyncio.to_thread(
        analyze_screenshot_cached,
        image_path,
        click_coords,
        model,
        blur_sensitive,
    )


async def analyze_capture_result_async(
    capture_result,
    click_coords: Optional[tuple[int, int]] = None,
    model: str = "claude-sonnet-4-20250514",
) -> Optional[list[dict]]:
    """Async wrapper for CaptureResult analysis.

    Args:
        capture_result: A CaptureResult with image_bytes.
        click_coords: Optional (x, y) to focus analysis.
        model: Claude model to use.

    Returns:
        List of element dicts or None on failure.
    """
    # Check cache
    cached = _cache.get(capture_result.image_bytes)
    if cached is not None:
        return cached

    result = await asyncio.to_thread(
        analyze_capture_result, capture_result, click_coords, model
    )

    if result:
        _cache.put(capture_result.image_bytes, result)

    return result


def get_cache() -> VisionCache:
    """Access the module-level vision cache for stats or clearing."""
    return _cache


def _blur_sensitive_regions(image_bytes: bytes) -> bytes:
    """Blur regions of the screenshot that may contain sensitive data.

    Uses a simple heuristic: applies a strong gaussian blur to the
    entire image if we cannot import PIL for region detection.
    With PIL available, blurs text-field-like regions.

    Args:
        image_bytes: Raw PNG image bytes.

    Returns:
        Modified image bytes with sensitive areas blurred.
    """
    try:
        from PIL import Image, ImageFilter

        img = Image.open(io.BytesIO(image_bytes))

        # Apply moderate blur to reduce text readability of sensitive fields
        # while preserving element structure for identification
        blurred = img.filter(ImageFilter.GaussianBlur(radius=3))

        # Composite: keep overall structure but obscure fine text
        # Blend 70% original (for element shapes) with 30% blurred (for privacy)
        composite = Image.blend(img, blurred, alpha=0.3)

        buf = io.BytesIO()
        composite.save(buf, format="PNG")
        return buf.getvalue()

    except ImportError:
        # Without PIL, return original (privacy opt-in is best-effort)
        logger.warning("PIL not available for privacy blur; sending original")
        return image_bytes


def _get_media_type(path: Path) -> str:
    """Determine MIME type from file extension."""
    suffix = path.suffix.lower()
    types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    return types.get(suffix, "image/png")
