"""Pure rendering functions for desktop element annotations.

Stateless PIL-based functions to draw annotations on screenshots:
bounding boxes, labels, arrows. All functions accept explicit DPI scale
factor and apply it uniformly to coordinates, dimensions, and fonts.
"""

import io
import logging
from typing import Optional, Union

from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)


def draw_bounding_box(
    image: Image.Image,
    bounds: dict[str, int],
    color: tuple[int, int, int, int],
    width: int,
    dpi_scale: float = 1.0,
) -> Image.Image:
    """Draw element bounding box on image.

    Args:
        image: PIL Image to draw on (modified in place).
        bounds: Element bounds {x, y, width, height} in screen pixels.
        color: RGBA tuple for box color.
        width: Line width in pixels.
        dpi_scale: DPI scale factor (e.g., 2.0 for Retina).

    Returns:
        Modified image (same object as input).
    """
    draw = ImageDraw.Draw(image, "RGBA")

    # Apply DPI scaling
    x = int(bounds["x"] * dpi_scale)
    y = int(bounds["y"] * dpi_scale)
    w = int(bounds["width"] * dpi_scale)
    h = int(bounds["height"] * dpi_scale)
    scaled_width = int(width * dpi_scale)

    # Draw rectangle
    draw.rectangle(
        [(x, y), (x + w, y + h)],
        outline=color,
        width=scaled_width,
    )

    return image


def draw_label(
    image: Image.Image,
    text: str,
    position: tuple[int, int],
    bg_color: tuple[int, int, int, int],
    text_color: tuple[int, int, int],
    font_size: int,
    padding: int,
    dpi_scale: float = 1.0,
) -> Image.Image:
    """Draw text label with background on image.

    Args:
        image: PIL Image to draw on (modified in place).
        text: Label text.
        position: (x, y) top-left corner of label in screen pixels.
        bg_color: RGBA tuple for label background.
        text_color: RGB tuple for label text.
        font_size: Font size in pixels.
        padding: Padding inside label background in pixels.
        dpi_scale: DPI scale factor.

    Returns:
        Modified image (same object as input).
    """
    draw = ImageDraw.Draw(image, "RGBA")

    # Apply DPI scaling
    x = int(position[0] * dpi_scale)
    y = int(position[1] * dpi_scale)
    scaled_font_size = int(font_size * dpi_scale)
    scaled_padding = int(padding * dpi_scale)

    # Load font (use default if custom font not available)
    try:
        font = ImageFont.truetype("Arial.ttf", scaled_font_size)
    except OSError:
        font = ImageFont.load_default()

    # Get text bounding box
    bbox = draw.textbbox((x, y), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Draw background rectangle
    bg_rect = [
        (x - scaled_padding, y - scaled_padding),
        (x + text_width + scaled_padding, y + text_height + scaled_padding),
    ]
    draw.rectangle(bg_rect, fill=bg_color)

    # Draw text
    draw.text((x, y), text, fill=text_color, font=font)

    return image


def draw_arrow(
    image: Image.Image,
    start: tuple[int, int],
    end: tuple[int, int],
    color: tuple[int, int, int],
    width: int,
    dpi_scale: float = 1.0,
) -> Image.Image:
    """Draw directional arrow on image.

    Args:
        image: PIL Image to draw on (modified in place).
        start: (x, y) arrow start point in screen pixels.
        end: (x, y) arrow end point in screen pixels.
        color: RGB tuple for arrow color.
        width: Line width in pixels.
        dpi_scale: DPI scale factor.

    Returns:
        Modified image (same object as input).
    """
    draw = ImageDraw.Draw(image, "RGBA")

    # Apply DPI scaling
    start_scaled = (int(start[0] * dpi_scale), int(start[1] * dpi_scale))
    end_scaled = (int(end[0] * dpi_scale), int(end[1] * dpi_scale))
    scaled_width = int(width * dpi_scale)

    # Draw line
    draw.line([start_scaled, end_scaled], fill=color, width=scaled_width)

    # TODO: Add arrowhead (future enhancement)

    return image


def calculate_label_position(
    element_bounds: dict[str, int],
    img_dims: tuple[int, int],
    label_size: tuple[int, int],
    padding: int = 4,
) -> tuple[int, int]:
    """Calculate optimal label position to avoid element overlap.

    Tries positions in order: above, below, left, right of element.
    Ensures label fits within image bounds.

    Args:
        element_bounds: Element bounds {x, y, width, height}.
        img_dims: Image dimensions (width, height).
        label_size: Label size (width, height) in pixels.
        padding: Minimum padding from element edge.

    Returns:
        (x, y) top-left corner for label placement.
    """
    elem_x = element_bounds["x"]
    elem_y = element_bounds["y"]
    elem_w = element_bounds["width"]
    elem_h = element_bounds["height"]
    label_w, label_h = label_size
    img_w, img_h = img_dims

    # Try above element
    if elem_y - label_h - padding >= 0:
        return (elem_x, elem_y - label_h - padding)

    # Try below element
    if elem_y + elem_h + padding + label_h <= img_h:
        return (elem_x, elem_y + elem_h + padding)

    # Try left of element
    if elem_x - label_w - padding >= 0:
        return (elem_x - label_w - padding, elem_y)

    # Try right of element
    if elem_x + elem_w + padding + label_w <= img_w:
        return (elem_x + elem_w + padding, elem_y)

    # Fallback: top-left corner of element (may overlap)
    return (elem_x, elem_y)


def validate_bounds(
    bounds: dict[str, int],
    img_dims: tuple[int, int],
) -> dict[str, int]:
    """Validate and clip element bounds to fit within image dimensions.

    Args:
        bounds: Element bounds {x, y, width, height}.
        img_dims: Image dimensions (width, height).

    Returns:
        Clipped bounds dict that fits within image.
    """
    img_w, img_h = img_dims

    # Clip coordinates to image bounds
    x = max(0, min(bounds["x"], img_w - 1))
    y = max(0, min(bounds["y"], img_h - 1))

    # Adjust width/height to fit within image
    max_w = img_w - x
    max_h = img_h - y
    width = min(bounds["width"], max_w)
    height = min(bounds["height"], max_h)

    clipped = {"x": x, "y": y, "width": width, "height": height}

    # Log warning if bounds were clipped
    if clipped != bounds:
        logger.warning(
            "Bounds clipped to fit image: original=%s clipped=%s",
            bounds,
            clipped,
        )

    return clipped


def render_element_annotation(
    image: Union[Image.Image, bytes],
    element_bounds: dict[str, int],
    element_name: str,
    element_type: str,
    style: dict,
    dpi_scale: float = 1.0,
) -> bytes:
    """Render complete element annotation (box + label) on image.

    High-level function that combines bounding box and label rendering.

    Args:
        image: PIL Image or bytes to annotate.
        element_bounds: Element bounds {x, y, width, height}.
        element_name: Element text or label.
        element_type: Element type (for styling).
        style: Style dict with color, width, font_size, padding.
        dpi_scale: DPI scale factor.

    Returns:
        Annotated image as PNG bytes.
    """
    # Convert bytes to PIL Image if needed
    if isinstance(image, bytes):
        image = Image.open(io.BytesIO(image))

    # Validate bounds fit within image
    validated_bounds = validate_bounds(element_bounds, image.size)

    # Draw bounding box
    draw_bounding_box(
        image,
        validated_bounds,
        style.get("highlight_color", (255, 87, 51, 180)),
        style.get("box_width", 3),
        dpi_scale,
    )

    # Calculate label position
    # Estimate label size (rough approximation)
    font_size = style.get("label_font_size", 14)
    padding = style.get("label_padding", 4)
    label_width = len(element_name) * font_size * 0.6  # Rough char width estimate
    label_height = font_size + padding * 2
    label_size = (int(label_width), int(label_height))

    label_pos = calculate_label_position(
        validated_bounds,
        image.size,
        label_size,
        padding,
    )

    # Draw label
    draw_label(
        image,
        element_name,
        label_pos,
        style.get("label_bg_color", (255, 87, 51, 230)),
        style.get("label_text_color", (255, 255, 255)),
        font_size,
        padding,
        dpi_scale,
    )

    # Convert to bytes
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()
