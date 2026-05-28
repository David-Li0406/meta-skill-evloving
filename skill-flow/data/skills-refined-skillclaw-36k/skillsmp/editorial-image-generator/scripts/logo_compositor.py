#!/usr/bin/env python3
"""
Logo Compositor for Article Images

Composites the real Tallyfy logo onto AI-generated images,
replacing the empty space left in the solution indicator area.

Uses PIL/Pillow for image processing.

Usage:
    python3 logo_compositor.py --image /path/to/image.jpg --output /path/to/output.jpg
    python3 logo_compositor.py --image /path/to/image.jpg  # outputs to same location with -with-logo suffix
"""

import argparse
import os
import sys
from pathlib import Path
from io import BytesIO
import requests

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Error: Pillow not installed. Run: pip3 install pillow")
    sys.exit(1)

# Constants
LOGO_URL = "https://tallyfy.com/wp-content/uploads/Logo-padded@2000x.png"
SCRIPT_DIR = Path(__file__).parent.parent
ASSETS_DIR = SCRIPT_DIR / "assets"
CACHED_LOGO_PATH = ASSETS_DIR / "tallyfy-logo.png"

# Default logo sizing and positioning
# Logo width as percentage of image width
# Increased from 9.17% to 12% for better visual balance with X indicator
LOGO_WIDTH_PERCENT = 0.12
DEFAULT_LOGO_WIDTH = 110  # fallback for 1200px wide images
SOLUTION_INDICATOR_MARGIN = 20  # margin from edges
ORANGE_COLOR_RANGE = {
    'r': (200, 255),
    'g': (80, 140),
    'b': (0, 80)
}


def download_logo(force_refresh: bool = False) -> Image.Image:
    """
    Download the Tallyfy logo from URL or use cached version.
    """
    # Check for cached logo
    if CACHED_LOGO_PATH.exists() and not force_refresh:
        print(f"Using cached logo: {CACHED_LOGO_PATH}")
        return Image.open(CACHED_LOGO_PATH).convert('RGBA')

    # Download logo
    print(f"Downloading logo from: {LOGO_URL}")
    try:
        response = requests.get(LOGO_URL, timeout=30)
        response.raise_for_status()

        logo = Image.open(BytesIO(response.content)).convert('RGBA')

        # Cache the logo
        ASSETS_DIR.mkdir(parents=True, exist_ok=True)
        logo.save(CACHED_LOGO_PATH, 'PNG')
        print(f"Logo cached to: {CACHED_LOGO_PATH}")

        return logo

    except requests.RequestException as e:
        print(f"Error downloading logo: {e}")
        raise


def is_orange_pixel(r: int, g: int, b: int) -> bool:
    """
    Check if a pixel is in the orange color range (for the X indicator).
    """
    return (
        ORANGE_COLOR_RANGE['r'][0] <= r <= ORANGE_COLOR_RANGE['r'][1] and
        ORANGE_COLOR_RANGE['g'][0] <= g <= ORANGE_COLOR_RANGE['g'][1] and
        ORANGE_COLOR_RANGE['b'][0] <= b <= ORANGE_COLOR_RANGE['b'][1]
    )


def find_solution_indicator(image: Image.Image) -> tuple:
    """
    Scan the bottom-right quadrant to find the solution indicator area.
    Returns (x, y) position for logo placement, or None if not found.

    The solution indicator pattern is: [Orange X] → [Arrow] → [Empty Space]
    We're looking for the orange X and then positioning the logo to its right.
    """
    width, height = image.size
    pixels = image.load()

    # Only scan bottom-right quadrant (last 30% of width and height)
    scan_start_x = int(width * 0.7)
    scan_start_y = int(height * 0.7)

    # Find orange pixels (the X indicator)
    orange_pixels = []
    for y in range(scan_start_y, height):
        for x in range(scan_start_x, width):
            try:
                pixel = pixels[x, y]
                if len(pixel) >= 3:
                    r, g, b = pixel[:3]
                    if is_orange_pixel(r, g, b):
                        orange_pixels.append((x, y))
            except (IndexError, TypeError):
                continue

    if not orange_pixels:
        print("Warning: Could not find orange X indicator in bottom-right quadrant")
        # Default to bottom-right corner with margin
        return (width - 150, height - 50)

    # Find the bounding box of orange pixels
    min_x = min(p[0] for p in orange_pixels)
    max_x = max(p[0] for p in orange_pixels)
    min_y = min(p[1] for p in orange_pixels)
    max_y = max(p[1] for p in orange_pixels)

    # Center of orange X
    center_x = (min_x + max_x) // 2
    center_y = (min_y + max_y) // 2

    print(f"Found orange X indicator at approximately ({center_x}, {center_y})")

    # Logo should be placed at the far right of the solution indicator area
    # Position it from the right edge of the image, vertically centered with the X
    # This ensures it covers any grey placeholder box that might exist
    logo_x = width - SOLUTION_INDICATOR_MARGIN  # Will be adjusted for logo width in composite_logo
    logo_y = center_y

    print(f"Positioning logo at right edge, vertically aligned with X at y={center_y}")
    return (logo_x, logo_y, center_x)  # Return X center for reference


def composite_logo(
    image_path: Path,
    output_path: Path = None,
    logo_width: int = None,
    position: tuple = None
) -> Path:
    """
    Composite the Tallyfy logo onto the image.

    Args:
        image_path: Path to the source image
        output_path: Path for the output image (optional)
        logo_width: Width to scale the logo to (optional, auto-calculated if None)
        position: (x, y) tuple for logo center position (optional, auto-detected if None)

    Returns:
        Path to the output image
    """
    # Load the source image
    print(f"Loading image: {image_path}")
    image = Image.open(image_path).convert('RGBA')
    img_width, img_height = image.size
    print(f"Image size: {img_width}x{img_height}")

    # Download/load logo
    logo = download_logo()
    logo_orig_width, logo_orig_height = logo.size
    print(f"Original logo size: {logo_orig_width}x{logo_orig_height}")

    # Calculate logo width proportionally to image size if not specified
    if logo_width is None:
        logo_width = int(img_width * LOGO_WIDTH_PERCENT)
        print(f"Auto-calculated logo width: {logo_width}px ({LOGO_WIDTH_PERCENT*100:.1f}% of {img_width}px)")

    # Scale logo to desired width while maintaining aspect ratio
    scale_factor = logo_width / logo_orig_width
    new_logo_height = int(logo_orig_height * scale_factor)
    logo_resized = logo.resize((logo_width, new_logo_height), Image.Resampling.LANCZOS)
    print(f"Resized logo to: {logo_width}x{new_logo_height}")

    # Find position if not provided
    if position is None:
        indicator_result = find_solution_indicator(image)
        if len(indicator_result) == 3:
            right_edge_x, logo_y, x_center = indicator_result
        else:
            right_edge_x, logo_y = indicator_result
            x_center = right_edge_x - 100
    else:
        right_edge_x, logo_y = position[0], position[1]

    # Position logo at right edge of image, right-aligned
    # Logo should end at (right_edge - margin), so it starts at (right_edge - margin - logo_width)
    paste_x = img_width - logo_width - SOLUTION_INDICATOR_MARGIN
    paste_y = logo_y - (new_logo_height // 2)

    # Ensure logo stays within image bounds
    if paste_y + new_logo_height > img_height:
        paste_y = img_height - new_logo_height - SOLUTION_INDICATOR_MARGIN
    if paste_y < 0:
        paste_y = SOLUTION_INDICATOR_MARGIN
    if paste_x < 0:
        paste_x = SOLUTION_INDICATOR_MARGIN

    print(f"Compositing logo at position: ({paste_x}, {paste_y})")

    # Create a copy to composite onto
    result = image.copy()

    # Paste logo with alpha channel as mask
    result.paste(logo_resized, (paste_x, paste_y), logo_resized)

    # Determine output path
    if output_path is None:
        stem = image_path.stem
        suffix = image_path.suffix
        output_path = image_path.parent / f"{stem}-with-logo{suffix}"

    # Convert back to RGB for JPEG output (remove alpha channel)
    if output_path.suffix.lower() in ['.jpg', '.jpeg']:
        # Create white background
        background = Image.new('RGB', result.size, (255, 255, 255))
        # Paste the result onto white background
        background.paste(result, mask=result.split()[3] if result.mode == 'RGBA' else None)
        result = background

    # Save result
    print(f"Saving result to: {output_path}")
    result.save(output_path, quality=95)

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Composite Tallyfy logo onto AI-generated images'
    )
    parser.add_argument(
        '--image',
        type=str,
        required=True,
        help='Path to the source image'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Path for the output image (optional)'
    )
    parser.add_argument(
        '--logo-width',
        type=int,
        default=None,
        help=f'Width to scale logo to (default: auto-calculated as ~9% of image width)'
    )
    parser.add_argument(
        '--position',
        type=str,
        help='Logo position as "x,y" (optional, auto-detected if not provided)'
    )
    parser.add_argument(
        '--refresh-logo',
        action='store_true',
        help='Force re-download of the logo from URL'
    )
    parser.add_argument(
        '--download-only',
        action='store_true',
        help='Only download and cache the logo, do not composite'
    )

    args = parser.parse_args()

    # Handle download-only mode
    if args.download_only:
        download_logo(force_refresh=True)
        print("Logo downloaded and cached successfully.")
        return 0

    # Validate image path
    image_path = Path(args.image)
    if not image_path.exists():
        print(f"Error: Image not found: {image_path}")
        return 1

    # Parse position if provided
    position = None
    if args.position:
        try:
            x, y = args.position.split(',')
            position = (int(x.strip()), int(y.strip()))
        except ValueError:
            print(f"Error: Invalid position format. Use 'x,y' (e.g., '1100,550')")
            return 1

    # Force logo refresh if requested
    if args.refresh_logo:
        download_logo(force_refresh=True)

    # Determine output path
    output_path = Path(args.output) if args.output else None

    try:
        result_path = composite_logo(
            image_path=image_path,
            output_path=output_path,
            logo_width=args.logo_width,
            position=position
        )
        print(f"\nSuccess! Logo composited image saved to: {result_path}")
        return 0

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
