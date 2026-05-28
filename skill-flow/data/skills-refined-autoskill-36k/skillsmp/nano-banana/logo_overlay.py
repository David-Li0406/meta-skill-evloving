#!/usr/bin/env python3
# /// script
# dependencies = ["pillow"]
# ///
"""
Logo overlay utilities for brand-styled slide generation.

Provides precise logo compositing using Pillow for pixel-perfect
brand element placement.

IMPORTANT: This script MUST be run with uv when used standalone:
    uv run logo_overlay.py

When imported by other scripts (e.g., generate_images.py), it uses
the parent script's environment.
"""

from pathlib import Path
from typing import Tuple, Optional
from PIL import Image as PILImage

# Logo positioning presets for 16:9 slides
# Based on actual TrendLife PowerPoint template (slideLayout11-19)
#
# PowerPoint slide size: 12192000×6858000 EMU = 1280×720 pixels
# Logo at 1280×720: cx=1870738, cy=330262 EMU = 196.4×34.7px (5.66:1)
# Logo position at 1280×720: x=1072.6px, y=671.7px
#
# At 1920×1080 (scale 1.5x):
# Logo size: 294.6×52.0 pixels (15.34% of slide width, 5.66:1 aspect ratio)
#
# FINAL PADDING VALUES (calibrated via PowerPoint screenshot comparison):
# - Target (from PPT screenshot): visible content padding = (22, 20)
# - Initial setting attempt: (22, 20)
# - Actual measurement result: (27, 20)
# - Calibration offset: right -5px, bottom 0px
# - Final calibrated setting: (17, 20)
#
# Why calibration needed?
# - PowerPoint renders logo with specific anti-aliasing/edge handling
# - Our PIL-based measurement may detect edges slightly differently
# - Direct setting (22, 20) resulted in 5px extra right padding
# - Calibrated (17, 20) compensates for this measurement difference
#
# srcRect crop: l=0, t=1, r=38620, b=8728
# - Removes right 38.62% and bottom 8.73% from image3.png (12532×1490)
# - Result: 7692×1359 (5.66:1) - matches frame aspect ratio perfectly
# - With noChangeAspect=1, displays 100% of logo content (complete TRENDLIFE text)
LOGO_POSITIONS = {
    'title': {
        'position': 'bottom-right',
        'size_ratio': 0.1534,  # 294.6/1920 = 15.34% of slide width
        'padding': (17, 20),  # Calibrated to match PowerPoint visible content position
        'opacity': 1.0
    },
    'content': {
        'position': 'bottom-right',
        'size_ratio': 0.1534,  # Same size for all layouts (from template)
        'padding': (17, 20),
        'opacity': 1.0
    },
    'divider': {
        'position': 'bottom-right',
        'size_ratio': 0.1534,
        'padding': (17, 20),
        'opacity': 1.0
    },
    'end': {
        'position': 'bottom-right',  # All layouts use same position in template
        'size_ratio': 0.1534,
        'padding': (17, 20),
        'opacity': 1.0
    },
    'default': {
        'position': 'bottom-right',
        'size_ratio': 0.1534,
        'padding': (17, 20),
        'opacity': 1.0
    }
}


def calculate_logo_position(
    slide_width: int,
    slide_height: int,
    logo_width: int,
    logo_height: int,
    position: str,
    padding: Tuple[int, int]
) -> Tuple[int, int]:
    """
    Calculate logo position coordinates based on placement strategy.

    Args:
        slide_width: Slide width in pixels
        slide_height: Slide height in pixels
        logo_width: Logo width in pixels
        logo_height: Logo height in pixels
        position: Position strategy ('bottom-right', 'center-bottom', etc.)
        padding: (x_padding, y_padding) in pixels

    Returns:
        (x, y) coordinates for logo top-left corner
    """
    x_pad, y_pad = padding

    if position == 'bottom-right':
        x = slide_width - logo_width - x_pad
        y = slide_height - logo_height - y_pad
    elif position == 'center-bottom':
        x = (slide_width - logo_width) // 2
        y = slide_height - logo_height - y_pad
    elif position == 'top-right':
        x = slide_width - logo_width - x_pad
        y = y_pad
    elif position == 'top-left':
        x = x_pad
        y = y_pad
    else:
        # Default to bottom-right
        x = slide_width - logo_width - x_pad
        y = slide_height - logo_height - y_pad

    return (x, y)


def resize_logo_proportional(
    logo: PILImage.Image,
    target_width: int
) -> PILImage.Image:
    """
    Resize logo to match PowerPoint template display behavior.

    PowerPoint behavior (with noChangeAspect=1):
    - Logo file (after srcRect crop): 7692×1359 (5.66:1)
    - Frame size at 1080p: 294.6×52.0 (5.66:1)
    - Aspect ratios match perfectly → resize without cropping
    - Result: Displays 100% of logo content (complete TRENDLIFE text)

    Args:
        logo: PIL Image object (pre-cropped via srcRect to 5.66:1)
        target_width: Desired output width (295px at 1920×1080)

    Returns:
        Resized logo image maintaining native aspect ratio
    """
    # Calculate target height maintaining logo's native aspect ratio
    # For TrendLife logo: 7692×1359 = 5.66:1
    # At 295px width: height = 295 / 5.66 = 52px
    target_height = int(target_width * (logo.height / logo.width))

    return logo.resize(
        (target_width, target_height),
        PILImage.Resampling.LANCZOS
    )


def overlay_logo(
    background_path: Path,
    logo_path: Path,
    output_path: Path,
    layout_type: str = 'default',
    opacity: Optional[float] = None
) -> Path:
    """
    Overlay logo on generated slide image with precise positioning.

    Args:
        background_path: Path to generated slide image
        logo_path: Path to logo PNG with transparency
        output_path: Path for output image
        layout_type: Layout type ('title', 'content', 'divider', 'end', 'default')
        opacity: Optional opacity override (0.0-1.0)

    Returns:
        Path to output image

    Raises:
        FileNotFoundError: If background or logo file not found
        ValueError: If layout_type is invalid
    """
    # Validate inputs
    if not background_path.exists():
        raise FileNotFoundError(f"Background image not found: {background_path}")
    if not logo_path.exists():
        raise FileNotFoundError(f"Logo not found: {logo_path}")

    # Get positioning configuration
    if layout_type not in LOGO_POSITIONS:
        layout_type = 'default'

    config = LOGO_POSITIONS[layout_type]
    final_opacity = opacity if opacity is not None else config['opacity']

    # Load images
    background = PILImage.open(background_path).convert('RGBA')
    logo = PILImage.open(logo_path).convert('RGBA')

    # Calculate target logo size
    slide_width, slide_height = background.size
    target_logo_width = int(slide_width * config['size_ratio'])

    # Resize logo proportionally
    logo_resized = resize_logo_proportional(logo, target_logo_width)

    # Apply opacity if needed
    if final_opacity < 1.0:
        alpha = logo_resized.split()[3]  # Get alpha channel
        alpha = alpha.point(lambda p: int(p * final_opacity))
        logo_resized.putalpha(alpha)

    # Calculate position
    logo_width, logo_height = logo_resized.size
    position = calculate_logo_position(
        slide_width, slide_height,
        logo_width, logo_height,
        config['position'],
        config['padding']
    )

    # Composite logo onto background
    background.paste(logo_resized, position, logo_resized)

    # Convert back to RGB if saving as JPEG, keep RGBA for PNG/WebP
    if output_path.suffix.lower() in ['.jpg', '.jpeg']:
        background = background.convert('RGB')

    # Save with high quality
    if output_path.suffix.lower() == '.webp':
        background.save(output_path, 'WEBP', quality=95, lossless=True)
    elif output_path.suffix.lower() in ['.jpg', '.jpeg']:
        background.save(output_path, 'JPEG', quality=95, optimize=True)
    elif output_path.suffix.lower() == '.png':
        background.save(output_path, 'PNG', optimize=True)
    else:
        # Default to WebP
        background.save(output_path, 'WEBP', quality=95, lossless=True)

    return output_path


def detect_layout_type(prompt: str, slide_number: Optional[int] = None) -> str:
    """
    Detect layout type from prompt content for logo positioning.

    Args:
        prompt: User's slide prompt
        slide_number: Optional slide number (1-based)

    Returns:
        Layout type string ('title', 'content', 'divider', 'end', 'default')
    """
    prompt_lower = prompt.lower()

    # Title slide detection
    if any(word in prompt_lower for word in ['title slide', 'cover slide', 'opening']):
        return 'title'

    # End slide detection
    if any(word in prompt_lower for word in ['end slide', 'closing', 'thank you', 'conclusion']):
        return 'end'

    # Divider slide detection
    if any(word in prompt_lower for word in ['divider', 'section break', 'chapter']):
        return 'divider'

    # First slide is usually title
    if slide_number == 1:
        return 'title'

    # Default to content slide
    return 'content'
