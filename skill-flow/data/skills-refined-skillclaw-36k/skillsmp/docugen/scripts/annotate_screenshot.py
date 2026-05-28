#!/usr/bin/env python3
"""
annotate_screenshot.py - PIL-based screenshot annotation for DocuGen

This script adds visual annotations to screenshots including:
- Highlight boxes around target elements
- Numbered step callouts
- Arrows pointing to elements
- Auto-blur for sensitive data

Usage:
    python annotate_screenshot.py <input_image> <output_image> --box x,y,w,h [options]

Options:
    --box x,y,w,h          Draw highlight box at coordinates
    --arrow x1,y1,x2,y2    Draw arrow from (x1,y1) to (x2,y2)
    --callout x,y,number   Add numbered callout at position
    --click x,y[,type]     Draw click indicator (type: single/double/right)
    --blur x,y,w,h         Blur region (for sensitive data)
    --style <style_file>   Load custom styles from JSON
    --elements <json>      Element metadata for auto-blur detection
    --auto-blur            Auto-detect and blur sensitive fields
    --smart                Smart auto-annotation (no config required!)
    --step <n>             Step number for smart annotation callout
    --scale <factor>       Scale factor for coordinates (e.g., 2.0 for Retina)
    --auto-scale           Auto-detect scale factor (default: enabled)
    --no-auto-scale        Disable auto-scale, use --scale value directly

Dependencies:
    - PIL/Pillow

Coordinate Systems:
    Playwright's boundingBox() returns CSS pixels, but screenshots may be
    captured at device pixel ratio (e.g., 2x on Retina displays). Use --scale
    to multiply coordinates by the devicePixelRatio, or --auto-scale to
    auto-detect the scale factor.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Tuple, List, Optional, Dict, Any

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    DEPS_AVAILABLE = True
except ImportError:
    DEPS_AVAILABLE = False


# Default annotation styles
DEFAULT_STYLES = {
    'highlight_color': (255, 87, 51, 180),      # Orange-red with alpha
    'highlight_width': 3,
    'arrow_color': (255, 87, 51),               # Orange-red
    'arrow_width': 3,
    'callout_bg_color': (255, 87, 51),          # Orange-red
    'callout_text_color': (255, 255, 255),      # White
    'callout_size': 24,
    'blur_strength': 15,
    # Click indicator styles (like Scribe/CleanShot)
    'click_color': (255, 87, 51),               # Orange-red
    'click_inner_radius': 8,                     # Inner circle radius
    'click_outer_radius': 20,                    # Outer ripple radius
    'click_ring_width': 2,                       # Ring stroke width
    'click_opacity': 200,                        # 0-255
}

# Patterns for detecting sensitive fields (FR-2.5)
SENSITIVE_PATTERNS = {
    'password': re.compile(r'password|passwd|pwd|secret', re.IGNORECASE),
    'ssn': re.compile(r'ssn|social.?security|tax.?id', re.IGNORECASE),
    'credit_card': re.compile(r'credit.?card|card.?number|cvv|cvc|expir', re.IGNORECASE),
    'api_key': re.compile(r'api.?key|access.?token|secret.?key|auth.?token', re.IGNORECASE),
    'email': re.compile(r'email|e-mail', re.IGNORECASE),
    'phone': re.compile(r'phone|tel|mobile', re.IGNORECASE),
}


def transform_bounding_box(
    bbox: Dict[str, Any],
    scale_factor: float = 1.0
) -> Tuple[int, int, int, int]:
    """
    Transform bounding box coordinates by scale factor.

    Playwright's boundingBox() returns CSS pixels, but screenshots may be
    captured at device pixel ratio (e.g., 2x on Retina). This function
    scales the coordinates to match the actual screenshot pixels.

    Args:
        bbox: Bounding box dict with x, y, width, height
        scale_factor: Device pixel ratio (e.g., 2.0 for Retina)

    Returns:
        Tuple of (x, y, width, height) in image pixels
    """
    return (
        int(bbox.get('x', 0) * scale_factor),
        int(bbox.get('y', 0) * scale_factor),
        int(bbox.get('width', 0) * scale_factor),
        int(bbox.get('height', 0) * scale_factor)
    )


def detect_scale_factor(
    elements: List[Dict[str, Any]],
    img_width: int,
    img_height: int
) -> float:
    """
    Auto-detect the scale factor by comparing bounding boxes to image size.

    The key insight: Playwright's boundingBox() returns CSS pixels, but screenshots
    may be captured at device pixel ratio. If scale factor is 2.0, the screenshot
    has 2x the pixels of the CSS coordinate space.

    Detection strategy:
    1. If any bbox extends BEYOND image bounds at scale 1.0 → need to scale DOWN (rare)
    2. If all bboxes are suspiciously small (< 25% of image) and image is large → likely HiDPI
    3. Check if doubling coordinates makes bboxes fit proportionally better

    Common scale factors:
    - 1.0: Standard displays, or screenshots taken with scale="css"
    - 2.0: Retina/HiDPI displays
    - 1.5, 1.25: Windows scaling

    Args:
        elements: List of element metadata with boundingBox
        img_width, img_height: Actual image dimensions

    Returns:
        Detected scale factor (defaults to 1.0 if uncertain)
    """
    if not elements:
        return 1.0

    # Collect all bounding boxes
    bboxes = []
    for elem in elements:
        if 'boundingBox' not in elem:
            continue
        bbox = elem['boundingBox']
        x = bbox.get('x', 0)
        y = bbox.get('y', 0)
        w = bbox.get('width', 0)
        h = bbox.get('height', 0)
        if w > 0 and h > 0:
            bboxes.append((x, y, w, h))

    if not bboxes:
        return 1.0

    # Check if coordinates fit at scale 1.0
    all_fit_at_1x = all(
        x + w <= img_width and y + h <= img_height
        for x, y, w, h in bboxes
    )

    # If coords don't fit at 1x, we might need to scale DOWN (unusual case)
    if not all_fit_at_1x:
        # Try common scales to see which makes them fit
        for scale in [0.5, 0.75, 1.0]:
            if all(
                x * scale + w * scale <= img_width and y * scale + h * scale <= img_height
                for x, y, w, h in bboxes
            ):
                print(f"Warning: Bounding boxes exceed image at scale 1.0, using {scale}", file=sys.stderr)
                return scale
        return 1.0

    # If coords fit at 1x, check if the image might be HiDPI (2x)
    # Heuristic: if image is large (>1500px) and coords seem to occupy
    # only a small portion of it, might need 2x scaling
    max_right = max(x + w for x, y, w, h in bboxes)
    max_bottom = max(y + h for x, y, w, h in bboxes)

    # Check if doubling would still fit and cover more of the image proportionally
    would_fit_at_2x = all(
        x * 2 + w * 2 <= img_width and y * 2 + h * 2 <= img_height
        for x, y, w, h in bboxes
    )

    if would_fit_at_2x:
        # Calculate coverage at 1x vs 2x
        coverage_1x = (max_right / img_width + max_bottom / img_height) / 2
        coverage_2x = (max_right * 2 / img_width + max_bottom * 2 / img_height) / 2

        # If 2x coverage is between 50-95% and 1x is under 50%, suggest 2x
        if coverage_1x < 0.5 and 0.5 <= coverage_2x <= 0.95:
            return 2.0

    # Default to 1.0 - most common case, especially with scale="css" screenshots
    return 1.0


def validate_bbox_in_image(
    bbox: Tuple[int, int, int, int],
    img_width: int,
    img_height: int
) -> bool:
    """
    Check if a bounding box fits within the image bounds.

    Args:
        bbox: (x, y, width, height) tuple
        img_width, img_height: Image dimensions

    Returns:
        True if bbox is valid and fits within image
    """
    x, y, w, h = bbox

    # Check for negative values
    if x < 0 or y < 0 or w <= 0 or h <= 0:
        return False

    # Check if bbox extends beyond image
    if x + w > img_width or y + h > img_height:
        return False

    return True


def detect_sensitive_fields(
    elements: List[Dict[str, Any]],
    scale_factor: float = 1.0
) -> List[Tuple[int, int, int, int]]:
    """
    Detect sensitive fields from element metadata and return their bounding boxes.

    Args:
        elements: List of element metadata dicts with keys:
            - selector: CSS selector
            - text: Visible text
            - ariaLabel: ARIA label
            - inputType: Input type attribute (e.g., 'password')
            - boundingBox: {x, y, width, height}
        scale_factor: Device pixel ratio for coordinate transformation

    Returns:
        List of (x, y, width, height) tuples for regions to blur (in image pixels)
    """
    blur_regions = []

    for elem in elements:
        is_sensitive = False

        # Check input type
        input_type = elem.get('inputType', '').lower()
        if input_type in ('password', 'hidden'):
            is_sensitive = True

        # Check selector, text, and aria label against patterns
        check_fields = [
            elem.get('selector', ''),
            elem.get('text', ''),
            elem.get('ariaLabel', ''),
            elem.get('placeholder', ''),
            elem.get('name', ''),
            elem.get('id', ''),
        ]

        for field in check_fields:
            if not field:
                continue
            for pattern_name, pattern in SENSITIVE_PATTERNS.items():
                if pattern.search(field):
                    is_sensitive = True
                    break

        if is_sensitive and 'boundingBox' in elem:
            # Transform coordinates using scale factor
            blur_regions.append(transform_bounding_box(elem['boundingBox'], scale_factor))

    return blur_regions


def load_styles(style_path: Optional[Path]) -> dict:
    """Load annotation styles from JSON file or use defaults."""
    styles = DEFAULT_STYLES.copy()
    if style_path and style_path.exists():
        with open(style_path) as f:
            custom = json.load(f)
            styles.update(custom)
    return styles


def draw_highlight_box(
    draw: ImageDraw.Draw,
    coords: Tuple[int, int, int, int],
    styles: dict
) -> None:
    """
    Draw a highlight box around a region.

    Args:
        draw: PIL ImageDraw object
        coords: (x, y, width, height) of the region
        styles: Style configuration dict
    """
    x, y, w, h = coords
    color = styles['highlight_color'][:3]  # RGB only for rectangle
    width = styles['highlight_width']

    # Draw rectangle outline
    draw.rectangle(
        [x, y, x + w, y + h],
        outline=color,
        width=width
    )


def draw_arrow(
    draw: ImageDraw.Draw,
    start: Tuple[int, int],
    end: Tuple[int, int],
    styles: dict
) -> None:
    """
    Draw an arrow from start to end point.

    Args:
        draw: PIL ImageDraw object
        start: (x, y) start position
        end: (x, y) end position (arrow head)
        styles: Style configuration dict
    """
    import math

    color = styles['arrow_color']
    width = styles['arrow_width']

    # Draw main line
    draw.line([start, end], fill=color, width=width)

    # Draw arrow head
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    arrow_length = 15
    arrow_angle = math.pi / 6  # 30 degrees

    left_x = end[0] - arrow_length * math.cos(angle - arrow_angle)
    left_y = end[1] - arrow_length * math.sin(angle - arrow_angle)
    right_x = end[0] - arrow_length * math.cos(angle + arrow_angle)
    right_y = end[1] - arrow_length * math.sin(angle + arrow_angle)

    draw.polygon(
        [end, (left_x, left_y), (right_x, right_y)],
        fill=color
    )


def draw_callout(
    img: Image.Image,
    draw: ImageDraw.Draw,
    position: Tuple[int, int],
    number: int,
    styles: dict
) -> None:
    """
    Draw a numbered callout circle.

    Args:
        img: PIL Image object
        draw: PIL ImageDraw object
        position: (x, y) center position
        number: Step number to display
        styles: Style configuration dict
    """
    x, y = position
    size = styles['callout_size']
    radius = size // 2

    # Draw circle background
    draw.ellipse(
        [x - radius, y - radius, x + radius, y + radius],
        fill=styles['callout_bg_color']
    )

    # Draw number text
    text = str(number)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size - 8)
    except OSError:
        font = ImageFont.load_default()

    # Center text in circle
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    text_x = x - text_w // 2
    text_y = y - text_h // 2 - 2

    draw.text((text_x, text_y), text, fill=styles['callout_text_color'], font=font)


def blur_region(
    img: Image.Image,
    coords: Tuple[int, int, int, int],
    styles: dict
) -> Image.Image:
    """
    Apply blur to a region of the image (for sensitive data).

    Args:
        img: PIL Image object
        coords: (x, y, width, height) of region to blur
        styles: Style configuration dict

    Returns:
        Modified image with blurred region
    """
    x, y, w, h = coords
    region = img.crop((x, y, x + w, y + h))
    blurred = region.filter(ImageFilter.GaussianBlur(styles['blur_strength']))
    img.paste(blurred, (x, y))
    return img


def draw_click_indicator(
    img: Image.Image,
    draw: ImageDraw.Draw,
    position: Tuple[int, int],
    styles: dict,
    click_type: str = 'single'
) -> None:
    """
    Draw a click indicator (ripple effect) at the specified position.
    Similar to Scribe/CleanShot click visualization.

    Args:
        img: PIL Image object
        draw: PIL ImageDraw object
        position: (x, y) center of click
        styles: Style configuration dict
        click_type: 'single', 'double', or 'right' for different styles
    """
    x, y = position
    color = styles.get('click_color', (255, 87, 51))
    inner_r = styles.get('click_inner_radius', 8)
    outer_r = styles.get('click_outer_radius', 20)
    ring_width = styles.get('click_ring_width', 2)
    opacity = styles.get('click_opacity', 200)

    # Create color with opacity
    if len(color) == 3:
        fill_color = (*color, opacity)
        ring_color = (*color, opacity // 2)
    else:
        fill_color = color
        ring_color = (*color[:3], color[3] // 2)

    # Draw outer ring (ripple effect)
    draw.ellipse(
        [x - outer_r, y - outer_r, x + outer_r, y + outer_r],
        outline=ring_color[:3],
        width=ring_width
    )

    # Draw middle ring for double-click
    if click_type == 'double':
        mid_r = (inner_r + outer_r) // 2
        draw.ellipse(
            [x - mid_r, y - mid_r, x + mid_r, y + mid_r],
            outline=ring_color[:3],
            width=ring_width
        )

    # Draw inner filled circle
    draw.ellipse(
        [x - inner_r, y - inner_r, x + inner_r, y + inner_r],
        fill=fill_color[:3]
    )

    # For right-click, add a small "R" indicator
    if click_type == 'right':
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10)
        except OSError:
            font = ImageFont.load_default()
        draw.text((x + inner_r + 2, y - 6), "R", fill=color[:3], font=font)


def normalize_desktop_element(element: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize a desktop element (from visual_analyzer or accessibility backend)
    to the Playwright-style format used by smart_annotate.

    Desktop elements use 'bounds' with {x, y, width, height}.
    Playwright elements use 'boundingBox' with {x, y, width, height}.

    Args:
        element: Desktop element dict with 'bounds', 'name', 'type', 'source'.

    Returns:
        Normalized element dict compatible with smart_annotate.
    """
    normalized = dict(element)

    # Convert 'bounds' to 'boundingBox' if needed
    if 'bounds' in normalized and 'boundingBox' not in normalized:
        normalized['boundingBox'] = normalized['bounds']

    # Map 'name' to 'text' for display
    if 'name' in normalized and 'text' not in normalized:
        normalized['text'] = normalized['name']

    # Map desktop 'type' to web-style tag/role
    type_to_tag = {
        'button': 'button',
        'input': 'input',
        'link': 'a',
        'checkbox': 'input',
        'dropdown': 'select',
        'menu': 'menuitem',
        'tab': 'tab',
    }
    if 'type' in normalized and 'tagName' not in normalized:
        normalized['tagName'] = type_to_tag.get(normalized['type'], 'div')

    # Mark as target so smart_annotate picks it up
    normalized['isTarget'] = True

    return normalized


def _draw_dashed_rectangle(
    draw: ImageDraw.Draw,
    coords: Tuple[int, int, int, int],
    color: Tuple[int, ...],
    width: int = 2,
    dash_length: int = 8,
    gap_length: int = 5,
) -> None:
    """
    Draw a dashed rectangle outline.

    PIL doesn't support dashed lines natively, so we draw short line segments.

    Args:
        draw: PIL ImageDraw object
        coords: (x, y, w, h) of the region
        color: Line color
        width: Line width
        dash_length: Length of each dash segment
        gap_length: Length of gaps between dashes
    """
    x, y, w, h = coords
    stride = dash_length + gap_length

    # Top edge
    pos = 0
    while pos < w:
        end = min(pos + dash_length, w)
        draw.line([(x + pos, y), (x + end, y)], fill=color, width=width)
        pos += stride

    # Bottom edge
    pos = 0
    while pos < w:
        end = min(pos + dash_length, w)
        draw.line([(x + pos, y + h), (x + end, y + h)], fill=color, width=width)
        pos += stride

    # Left edge
    pos = 0
    while pos < h:
        end = min(pos + dash_length, h)
        draw.line([(x, y + pos), (x, y + end)], fill=color, width=width)
        pos += stride

    # Right edge
    pos = 0
    while pos < h:
        end = min(pos + dash_length, h)
        draw.line([(x + w, y + pos), (x + w, y + end)], fill=color, width=width)
        pos += stride


def draw_desktop_element(
    img: Image.Image,
    draw: ImageDraw.Draw,
    element: Dict[str, Any],
    step_number: int,
    styles: dict,
    scale_factor: float = 1.0
) -> Image.Image:
    """
    Draw annotation for a desktop-captured element with source-aware styling.

    Accessibility-sourced elements get solid borders (precise bounds).
    Vision-sourced elements get dashed borders when confidence < 0.8,
    solid borders when confidence >= 0.8.

    Args:
        img: PIL Image object
        draw: PIL ImageDraw object
        element: Desktop element with 'bounds', 'source', 'confidence'
        step_number: Step number for callout
        styles: Style configuration
        scale_factor: DPI scale factor

    Returns:
        Annotated image
    """
    normalized = normalize_desktop_element(element)
    source = element.get('source', 'accessibility')
    confidence = element.get('confidence', 1.0)

    if 'boundingBox' not in normalized:
        return img

    # Get scaled coordinates
    x, y, w, h = transform_bounding_box(normalized['boundingBox'], scale_factor)
    if w < 5 or h < 5:
        return img

    # Source-aware styling
    if source == 'visual' and confidence < 0.8:
        # Low-confidence visual: dashed orange border
        color = (255, 165, 0)
        _draw_dashed_rectangle(draw, (x, y, w, h), color=color, width=2)
    elif source == 'visual':
        # High-confidence visual: solid orange border
        color = (255, 165, 0)
        draw.rectangle([x, y, x + w, y + h], outline=color, width=3)
    else:
        # Accessibility: solid red-orange border
        color = (255, 87, 51)
        draw.rectangle([x, y, x + w, y + h], outline=color, width=3)

    # Add element label above the box
    label = normalized.get('text', '') or normalized.get('title', '')
    if label:
        label_text = label[:40]  # Truncate long labels
        if source == 'visual' and confidence < 1.0:
            label_text += f" ({int(confidence * 100)}%)"

        try:
            font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12
            )
        except OSError:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), label_text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        label_y = max(0, y - text_h - 4)

        # Draw label background
        draw.rectangle(
            [x, label_y, x + text_w + 6, label_y + text_h + 4],
            fill=color,
        )
        draw.text(
            (x + 3, label_y + 2),
            label_text,
            fill=(255, 255, 255),
            font=font,
        )

    # Add step callout
    callout_x = x + w + 5
    callout_y = y
    draw_callout(img, draw, (callout_x, callout_y), step_number, styles)

    return img


def smart_annotate(
    img: Image.Image,
    draw: ImageDraw.Draw,
    elements: List[Dict[str, Any]],
    step_number: int,
    styles: dict,
    scale_factor: float = 1.0
) -> Image.Image:
    """
    Smart auto-annotation: automatically detect what to highlight and annotate.
    Requires NO manual configuration - just pass element metadata from Playwright.

    Smart detection logic:
    1. Find the "target" element (highest z-index, focused, or has action)
    2. Draw highlight box around target
    3. Add callout with step number
    4. Auto-blur any sensitive fields
    5. Optionally add arrow for small/hard-to-find elements

    Args:
        img: PIL Image object
        draw: PIL ImageDraw object
        elements: Element metadata from Playwright capture
        step_number: Step number for callout
        styles: Style configuration
        scale_factor: Device pixel ratio (e.g., 2.0 for Retina displays)

    Returns:
        Modified image with smart annotations
    """
    if not elements:
        return img

    # Find the target element (the one being interacted with)
    target = find_target_element(elements)
    if not target or 'boundingBox' not in target:
        return img

    # Transform bounding box coordinates using scale factor
    x, y, w, h = transform_bounding_box(target['boundingBox'], scale_factor)

    # Skip if element is too small to be meaningful (after scaling)
    if w < 5 or h < 5:
        return img

    # Validate that transformed coords fit within image
    img_width, img_height = img.size
    if not validate_bbox_in_image((x, y, w, h), img_width, img_height):
        print(f"Warning: Bounding box ({x}, {y}, {w}, {h}) extends beyond image "
              f"({img_width}x{img_height}). Check scale factor.", file=sys.stderr)
        # Clamp to image bounds
        x = max(0, min(x, img_width - 1))
        y = max(0, min(y, img_height - 1))
        w = min(w, img_width - x)
        h = min(h, img_height - y)

    # Auto-blur sensitive fields first (with scale factor)
    blur_regions = detect_sensitive_fields(elements, scale_factor)
    for coords in blur_regions:
        img = blur_region(img, coords, styles)
        draw = ImageDraw.Draw(img)

    # Draw highlight box around target element
    draw_highlight_box(draw, (x, y, w, h), styles)

    # Determine optimal callout position
    callout_pos = calculate_callout_position(x, y, w, h, img_width, img_height, styles)

    # Draw callout
    draw_callout(img, draw, callout_pos, step_number, styles)

    # Draw arrow from callout to element for small elements (use scaled dimensions)
    if w < 100 * scale_factor or h < 30 * scale_factor:
        # Point arrow to center of element
        element_center = (x + w // 2, y + h // 2)
        draw_arrow(draw, callout_pos, element_center, styles)

    # Add click indicator if this is a clickable element
    if is_clickable_element(target):
        click_pos = (x + w // 2, y + h // 2)
        draw_click_indicator(img, draw, click_pos, styles, 'single')

    return img


def find_target_element(elements: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Identify the target element from a list of captured elements.

    Priority order:
    1. Element marked as 'target' or 'focused'
    2. Element with an action (clicked, typed, etc.)
    3. Element with highest z-index
    4. First interactive element (button, input, link)
    5. First element with bounding box

    Args:
        elements: List of element metadata

    Returns:
        Target element dict or None
    """
    # Look for explicitly marked target
    for elem in elements:
        if elem.get('isTarget') or elem.get('focused'):
            return elem

    # Look for element with action
    for elem in elements:
        if elem.get('action') or elem.get('clicked') or elem.get('typed'):
            return elem

    # Sort by z-index if available
    with_zindex = [e for e in elements if 'zIndex' in e]
    if with_zindex:
        return max(with_zindex, key=lambda e: int(e.get('zIndex', 0)))

    # Look for interactive elements
    interactive_tags = {'button', 'input', 'a', 'select', 'textarea'}
    interactive_roles = {'button', 'link', 'textbox', 'checkbox', 'radio', 'combobox'}

    for elem in elements:
        tag = elem.get('tagName', '').lower()
        role = elem.get('role', '').lower()
        if tag in interactive_tags or role in interactive_roles:
            return elem

    # Fall back to first element with bounding box
    for elem in elements:
        if 'boundingBox' in elem:
            return elem

    return None


def calculate_callout_position(
    x: int, y: int, w: int, h: int,
    img_width: int, img_height: int,
    styles: dict
) -> Tuple[int, int]:
    """
    Calculate optimal callout position relative to target element.
    Avoids placing callout outside image bounds or overlapping the element.

    Args:
        x, y, w, h: Element bounding box
        img_width, img_height: Image dimensions
        styles: Style config (for callout size)

    Returns:
        (x, y) position for callout center
    """
    callout_radius = styles.get('callout_size', 24) // 2
    padding = 10

    # Preferred position: top-left of element, offset outward
    callout_x = x - callout_radius - padding
    callout_y = y - callout_radius - padding

    # Adjust if too close to left edge
    if callout_x < callout_radius + padding:
        # Place to the right of element instead
        callout_x = x + w + callout_radius + padding

    # Adjust if too close to top
    if callout_y < callout_radius + padding:
        # Place below instead
        callout_y = y + h + callout_radius + padding

    # Adjust if off right edge
    if callout_x > img_width - callout_radius - padding:
        callout_x = x - callout_radius - padding

    # Adjust if off bottom
    if callout_y > img_height - callout_radius - padding:
        callout_y = y - callout_radius - padding

    # Final bounds check
    callout_x = max(callout_radius + 5, min(img_width - callout_radius - 5, callout_x))
    callout_y = max(callout_radius + 5, min(img_height - callout_radius - 5, callout_y))

    return (callout_x, callout_y)


def is_clickable_element(element: Dict[str, Any]) -> bool:
    """
    Determine if an element is clickable based on its metadata.

    Args:
        element: Element metadata dict

    Returns:
        True if element appears to be clickable
    """
    # Check for click action
    if element.get('clicked') or element.get('action') == 'click':
        return True

    # Check tag name
    clickable_tags = {'button', 'a', 'input', 'select'}
    tag = element.get('tagName', '').lower()
    if tag in clickable_tags:
        return True

    # Check role
    clickable_roles = {'button', 'link', 'checkbox', 'radio', 'menuitem', 'tab'}
    role = element.get('role', '').lower()
    if role in clickable_roles:
        return True

    # Check for onclick attribute
    if element.get('onclick') or element.get('hasClickHandler'):
        return True

    return False


def parse_coords(coord_str: str) -> Tuple[int, ...]:
    """Parse comma-separated coordinates string."""
    return tuple(int(x.strip()) for x in coord_str.split(','))


def main():
    parser = argparse.ArgumentParser(
        description='Add annotations to screenshots'
    )
    parser.add_argument('input', type=Path, help='Input image path')
    parser.add_argument('output', type=Path, help='Output image path')
    parser.add_argument('--box', action='append', help='Highlight box: x,y,w,h')
    parser.add_argument('--arrow', action='append', help='Arrow: x1,y1,x2,y2')
    parser.add_argument('--callout', action='append', help='Callout: x,y,number')
    parser.add_argument('--blur', action='append', help='Blur region: x,y,w,h')
    parser.add_argument(
        '--click',
        action='append',
        help='Click indicator: x,y[,type] where type is single/double/right (default: single)'
    )
    parser.add_argument('--style', type=Path, help='Custom style JSON file')
    parser.add_argument(
        '--elements',
        type=Path,
        help='JSON file with element metadata for auto-blur detection (FR-2.5)'
    )
    parser.add_argument(
        '--auto-blur',
        action='store_true',
        help='Auto-detect and blur sensitive fields (requires --elements)'
    )
    parser.add_argument(
        '--smart',
        action='store_true',
        default=True,
        help='Smart auto-annotation: automatically detect target element, add highlight, callout, and blur sensitive data (default: enabled when --elements provided)'
    )
    parser.add_argument(
        '--no-smart',
        action='store_true',
        help='Disable smart annotation, use manual coordinates only'
    )
    parser.add_argument(
        '--step',
        type=int,
        default=1,
        help='Step number for smart annotation callout (default: 1)'
    )
    parser.add_argument(
        '--scale',
        type=float,
        default=1.0,
        help='Scale factor for coordinates (devicePixelRatio). Common values: 1.0 (standard), 2.0 (Retina/HiDPI)'
    )
    parser.add_argument(
        '--auto-scale',
        action='store_true',
        default=True,
        help='Auto-detect scale factor by comparing element bounding boxes to image dimensions (default: enabled)'
    )
    parser.add_argument(
        '--no-auto-scale',
        action='store_true',
        help='Disable auto-scale detection, use --scale value directly'
    )
    parser.add_argument(
        '--desktop',
        action='store_true',
        help='Use desktop element annotation with accessibility APIs (Windows/macOS)'
    )
    parser.add_argument(
        '--platform',
        type=str,
        choices=['windows', 'macos', 'linux'],
        help='Platform for desktop annotation (auto-detected if not specified)'
    )
    parser.add_argument(
        '--coords',
        type=str,
        help='Interaction coordinates for desktop annotation: x,y (required with --desktop)'
    )

    args = parser.parse_args()

    if not DEPS_AVAILABLE:
        print("Error: PIL/Pillow not installed.", file=sys.stderr)
        print("Run: pip install pillow", file=sys.stderr)
        sys.exit(2)

    if not args.input.exists():
        print(f"Error: Input image not found: {args.input}", file=sys.stderr)
        sys.exit(2)

    # Desktop annotation mode - use annotation_orchestrator
    if args.desktop:
        if not args.coords:
            print("Error: --coords required with --desktop", file=sys.stderr)
            sys.exit(2)

        try:
            x_str, y_str = args.coords.split(',')
            coords = (int(x_str), int(y_str))
        except (ValueError, AttributeError):
            print("Error: --coords must be in format x,y (e.g., 100,200)", file=sys.stderr)
            sys.exit(2)

        # Import desktop annotation
        try:
            from docugen.desktop import annotate_screenshot as desktop_annotate
            from docugen.desktop import AnnotationConfig
            from docugen.desktop.platform_utils import get_os
        except ImportError as e:
            print(f"Error: Desktop annotation unavailable: {e}", file=sys.stderr)
            sys.exit(2)

        # Determine platform
        platform = args.platform or get_os()

        # Read input image
        with open(args.input, 'rb') as f:
            image_bytes = f.read()

        # Annotate using desktop orchestrator
        config = AnnotationConfig()
        annotated_bytes = desktop_annotate(
            image_bytes,
            coords,
            platform,
            config=config,
        )

        # Write output
        with open(args.output, 'wb') as f:
            f.write(annotated_bytes)

        print(f"Desktop annotation complete: {args.output}")
        return

    styles = load_styles(args.style)
    img = Image.open(args.input).convert('RGBA')
    draw = ImageDraw.Draw(img)

    # Smart annotation mode - automatic everything (default when --elements provided)
    use_smart = args.smart and args.elements and not args.no_smart
    if use_smart:
        if not args.elements.exists():
            print(f"Error: Elements file not found: {args.elements}", file=sys.stderr)
            sys.exit(2)

        with open(args.elements) as f:
            elements_data = json.load(f)
            if isinstance(elements_data, list):
                elements = elements_data
            else:
                elements = elements_data.get('elements', [])

        # Determine scale factor
        scale_factor = args.scale
        img_width, img_height = img.size

        # Auto-scale is enabled by default unless --no-auto-scale is specified
        use_auto_scale = args.auto_scale and not args.no_auto_scale

        if use_auto_scale:
            detected_scale = detect_scale_factor(elements, img_width, img_height)
            if detected_scale != 1.0:
                print(f"Auto-detected scale factor: {detected_scale}")
                scale_factor = detected_scale
        elif scale_factor != 1.0:
            print(f"Using scale factor: {scale_factor}")

        img = smart_annotate(img, draw, elements, args.step, styles, scale_factor)

        # Save and exit - smart mode handles everything
        args.output.parent.mkdir(parents=True, exist_ok=True)
        img = img.convert('RGB')
        img.save(args.output, optimize=True)
        print(f"Smart annotated image saved: {args.output}")
        return

    # Auto-detect sensitive fields if requested (FR-2.5)
    auto_blur_regions = []
    if args.auto_blur and args.elements:
        if args.elements.exists():
            with open(args.elements) as f:
                elements_data = json.load(f)
                # Handle both list of elements or dict with 'elements' key
                if isinstance(elements_data, list):
                    elements = elements_data
                else:
                    elements = elements_data.get('elements', [])
                auto_blur_regions = detect_sensitive_fields(elements)
                print(f"Auto-detected {len(auto_blur_regions)} sensitive field(s) to blur")
        else:
            print(f"Warning: Elements file not found: {args.elements}", file=sys.stderr)

    # Apply auto-detected blur regions
    for coords in auto_blur_regions:
        img = blur_region(img, coords, styles)
        draw = ImageDraw.Draw(img)

    # Apply manual blur regions (before other annotations)
    if args.blur:
        for blur_spec in args.blur:
            coords = parse_coords(blur_spec)
            img = blur_region(img, coords, styles)
            draw = ImageDraw.Draw(img)  # Recreate draw after modification

    # Draw highlight boxes
    if args.box:
        for box_spec in args.box:
            coords = parse_coords(box_spec)
            draw_highlight_box(draw, coords, styles)

    # Draw arrows
    if args.arrow:
        for arrow_spec in args.arrow:
            coords = parse_coords(arrow_spec)
            start = (coords[0], coords[1])
            end = (coords[2], coords[3])
            draw_arrow(draw, start, end, styles)

    # Draw callouts
    if args.callout:
        for callout_spec in args.callout:
            parts = callout_spec.split(',')
            x, y = int(parts[0]), int(parts[1])
            number = int(parts[2])
            draw_callout(img, draw, (x, y), number, styles)

    # Draw click indicators (like Scribe/CleanShot)
    if args.click:
        for click_spec in args.click:
            parts = click_spec.split(',')
            x, y = int(parts[0]), int(parts[1])
            click_type = parts[2] if len(parts) > 2 else 'single'
            draw_click_indicator(img, draw, (x, y), styles, click_type)

    # Save output
    args.output.parent.mkdir(parents=True, exist_ok=True)
    img = img.convert('RGB')  # Convert back to RGB for PNG/JPG
    img.save(args.output, optimize=True)
    print(f"Annotated image saved: {args.output}")


if __name__ == '__main__':
    main()
