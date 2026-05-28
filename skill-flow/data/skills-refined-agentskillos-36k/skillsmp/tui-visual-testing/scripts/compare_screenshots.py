#!/usr/bin/env python3
"""
Compare two screenshots and report differences.

This script compares a golden (expected) screenshot against an actual screenshot
and reports the percentage difference. Optionally generates a diff image.

Usage:
    python compare_screenshots.py <golden-file> <actual-file> [options]

Options:
    --threshold PERCENT    Acceptable difference percentage (default: 0.1)
    --output FILE          Save diff image to file
    --fail-on-diff         Exit with code 1 if different
    --verbose              Show detailed comparison info

Requirements:
    pip install Pillow

Example:
    python compare_screenshots.py golden/main_view.png /tmp/screenshot.png --fail-on-diff
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageDraw
except ImportError:
    print("Error: Pillow is required. Install with: pip install Pillow", file=sys.stderr)
    sys.exit(1)


def calculate_difference(img1: Image, img2: Image) -> tuple[float, Image]:
    """Calculate the difference between two images.

    Returns:
        A tuple of (difference_percentage, diff_image)
    """
    # Ensure same mode
    if img1.mode != img2.mode:
        img2 = img2.convert(img1.mode)

    # Handle size differences
    if img1.size != img2.size:
        # Create a new image with the larger dimensions
        max_width = max(img1.width, img2.width)
        max_height = max(img1.height, img2.height)

        # Expand both images to the same size
        new_img1 = Image.new(img1.mode, (max_width, max_height), (0, 0, 0))
        new_img2 = Image.new(img2.mode, (max_width, max_height), (0, 0, 0))

        new_img1.paste(img1, (0, 0))
        new_img2.paste(img2, (0, 0))

        img1 = new_img1
        img2 = new_img2

    # Calculate pixel difference
    diff = ImageChops.difference(img1, img2)

    # Convert to grayscale for analysis
    diff_gray = diff.convert('L')

    # Count different pixels
    total_pixels = img1.width * img1.height
    different_pixels = sum(1 for pixel in diff_gray.getdata() if pixel > 0)

    difference_percent = (different_pixels / total_pixels) * 100

    return difference_percent, diff


def create_diff_visualization(
    golden: Image,
    actual: Image,
    diff: Image
) -> Image:
    """Create a side-by-side visualization of the difference.

    Layout: | Golden | Actual | Diff |
    """
    # Ensure same size
    max_width = max(golden.width, actual.width, diff.width)
    max_height = max(golden.height, actual.height, diff.height)

    # Create visualization
    padding = 10
    label_height = 25
    total_width = (max_width * 3) + (padding * 4)
    total_height = max_height + label_height + (padding * 2)

    viz = Image.new('RGB', (total_width, total_height), (50, 50, 50))
    draw = ImageDraw.Draw(viz)

    # Add labels
    labels = ['Golden', 'Actual', 'Diff (highlighted)']
    for i, label in enumerate(labels):
        x = padding + i * (max_width + padding)
        draw.text((x, 5), label, fill=(200, 200, 200))

    # Paste images
    y = label_height

    # Golden
    viz.paste(golden, (padding, y))

    # Actual
    viz.paste(actual, (padding * 2 + max_width, y))

    # Diff (enhance visibility)
    diff_enhanced = diff.copy()
    # Make differences more visible by increasing contrast
    diff_data = list(diff_enhanced.getdata())
    enhanced_data = []
    for pixel in diff_data:
        if isinstance(pixel, tuple):
            # If any channel is different, highlight in red
            if any(c > 0 for c in pixel):
                enhanced_data.append((255, 0, 0))
            else:
                enhanced_data.append(pixel)
        else:
            enhanced_data.append((255, 0, 0) if pixel > 0 else (0, 0, 0))

    if diff_enhanced.mode != 'RGB':
        diff_enhanced = diff_enhanced.convert('RGB')

    diff_highlight = Image.new('RGB', diff.size)
    diff_highlight.putdata(enhanced_data)

    viz.paste(diff_highlight, (padding * 3 + max_width * 2, y))

    return viz


def compare_screenshots(
    golden_path: str,
    actual_path: str,
    threshold: float = 0.1,
    output_path: str = None,
    verbose: bool = False
) -> tuple[bool, float]:
    """Compare two screenshots.

    Args:
        golden_path: Path to the golden (expected) image
        actual_path: Path to the actual image
        threshold: Acceptable difference percentage
        output_path: Optional path to save diff image
        verbose: Print detailed information

    Returns:
        A tuple of (is_same, difference_percentage)
    """
    # Load images
    golden = Image.open(golden_path)
    actual = Image.open(actual_path)

    if verbose:
        print(f"Golden: {golden.size}, mode={golden.mode}")
        print(f"Actual: {actual.size}, mode={actual.mode}")

    # Check for size differences
    size_differs = golden.size != actual.size
    if size_differs and verbose:
        print(f"Warning: Image sizes differ!")
        print(f"  Golden: {golden.size}")
        print(f"  Actual: {actual.size}")

    # Calculate difference
    diff_percent, diff_img = calculate_difference(golden, actual)

    if verbose:
        print(f"Difference: {diff_percent:.4f}%")
        print(f"Threshold: {threshold}%")

    # Save diff visualization if requested
    if output_path:
        viz = create_diff_visualization(golden, actual, diff_img)
        viz.save(output_path)
        if verbose:
            print(f"Diff image saved to: {output_path}")

    # Determine if images are effectively the same
    is_same = diff_percent <= threshold

    return is_same, diff_percent


def main():
    parser = argparse.ArgumentParser(
        description='Compare two screenshots and report differences'
    )
    parser.add_argument('golden', help='Path to golden (expected) image')
    parser.add_argument('actual', help='Path to actual image')
    parser.add_argument(
        '--threshold', type=float, default=0.1,
        help='Acceptable difference percentage (default: 0.1)'
    )
    parser.add_argument('--output', help='Save diff image to file')
    parser.add_argument(
        '--fail-on-diff', action='store_true',
        help='Exit with code 1 if different'
    )
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    # Validate inputs
    golden_path = Path(args.golden)
    actual_path = Path(args.actual)

    if not golden_path.exists():
        print(f"Error: Golden file not found: {args.golden}", file=sys.stderr)
        sys.exit(1)

    if not actual_path.exists():
        print(f"Error: Actual file not found: {args.actual}", file=sys.stderr)
        sys.exit(1)

    # Compare
    is_same, diff_percent = compare_screenshots(
        str(golden_path),
        str(actual_path),
        threshold=args.threshold,
        output_path=args.output,
        verbose=args.verbose
    )

    # Output result
    if is_same:
        print(f"PASS: Images match (difference: {diff_percent:.4f}%)")
        sys.exit(0)
    else:
        print(f"FAIL: Images differ by {diff_percent:.4f}% (threshold: {args.threshold}%)")
        if args.fail_on_diff:
            sys.exit(1)
        sys.exit(0)


if __name__ == '__main__':
    main()
