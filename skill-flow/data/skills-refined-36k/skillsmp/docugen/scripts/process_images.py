#!/usr/bin/env python3
"""
process_images.py - Image optimization and formatting for DocuGen

This script optimizes screenshot images for documentation:
- Compress PNG files to reduce size
- Convert formats if needed
- Resize large images
- Crop to relevant regions using element bounding boxes
- Combine multi-action screenshots when changes are minimal (NFR-2)
- Ensure consistent naming

Usage:
    python process_images.py <input_dir> [--output-dir <dir>] [--max-width 1200]

Options:
    --output-dir    Directory for processed images (default: same as input)
    --max-width     Maximum image width in pixels (default: 1200)
    --max-size      Maximum file size in KB (default: 200)
    --format        Output format: png, jpg (default: png)
    --crop          Crop to element region (requires --elements JSON)
    --elements      JSON file with element bounding boxes
    --combine       Combine similar screenshots (SSIM > threshold)

Dependencies:
    - PIL/Pillow
    - scikit-image (optional, for SSIM combining)
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any

try:
    from PIL import Image
    DEPS_AVAILABLE = True
except ImportError:
    DEPS_AVAILABLE = False

# Optional SSIM support for combining similar screenshots
try:
    from skimage.metrics import structural_similarity as ssim
    import numpy as np
    SSIM_AVAILABLE = True
except ImportError:
    SSIM_AVAILABLE = False


def get_file_size_kb(path: Path) -> float:
    """Get file size in kilobytes."""
    return path.stat().st_size / 1024


def crop_to_element(
    img: Image.Image,
    bounding_box: Dict[str, int],
    padding: int = 50,
    context_ratio: float = 0.3
) -> Image.Image:
    """
    Crop image to focus on element while preserving context.

    Args:
        img: PIL Image object
        bounding_box: Dict with x, y, width, height keys
        padding: Minimum padding around element in pixels
        context_ratio: Ratio of context to include around element (0.0-1.0)

    Returns:
        Cropped PIL Image
    """
    x = bounding_box.get('x', 0)
    y = bounding_box.get('y', 0)
    w = bounding_box.get('width', 100)
    h = bounding_box.get('height', 100)

    # Calculate crop region with context
    img_w, img_h = img.size

    # Add context based on element size
    context_w = int(w * context_ratio)
    context_h = int(h * context_ratio)

    # Calculate crop bounds with padding and context
    left = max(0, x - padding - context_w)
    top = max(0, y - padding - context_h)
    right = min(img_w, x + w + padding + context_w)
    bottom = min(img_h, y + h + padding + context_h)

    # Ensure minimum size
    min_size = 200
    if right - left < min_size:
        center_x = (left + right) // 2
        left = max(0, center_x - min_size // 2)
        right = min(img_w, center_x + min_size // 2)

    if bottom - top < min_size:
        center_y = (top + bottom) // 2
        top = max(0, center_y - min_size // 2)
        bottom = min(img_h, center_y + min_size // 2)

    return img.crop((left, top, right, bottom))


def calculate_ssim(img1: Image.Image, img2: Image.Image) -> float:
    """
    Calculate SSIM between two images.

    Args:
        img1: First PIL Image
        img2: Second PIL Image

    Returns:
        SSIM score (0-1, higher = more similar)
    """
    if not SSIM_AVAILABLE:
        return 0.0  # Can't calculate without scikit-image

    # Convert to grayscale numpy arrays
    arr1 = np.array(img1.convert('L'))
    arr2 = np.array(img2.convert('L'))

    # Resize if dimensions don't match
    if arr1.shape != arr2.shape:
        img2_resized = img2.resize(img1.size)
        arr2 = np.array(img2_resized.convert('L'))

    score, _ = ssim(arr1, arr2, full=True)
    return score


def combine_similar_screenshots(
    images: List[Tuple[Path, Image.Image]],
    threshold: float = 0.95
) -> List[Tuple[List[Path], Image.Image]]:
    """
    Combine screenshots that are very similar (multi-action screenshots).

    When SSIM > threshold, combine into a single screenshot using the last
    image (which shows the final state after all actions).

    Args:
        images: List of (path, image) tuples
        threshold: SSIM threshold above which to combine (default 0.95)

    Returns:
        List of (source_paths, combined_image) tuples
    """
    if not SSIM_AVAILABLE or len(images) < 2:
        return [([path], img) for path, img in images]

    result = []
    current_group_paths = [images[0][0]]
    current_image = images[0][1]

    for i in range(1, len(images)):
        path, img = images[i]
        similarity = calculate_ssim(current_image, img)

        if similarity > threshold:
            # Similar - add to current group
            current_group_paths.append(path)
            current_image = img  # Use latest image
        else:
            # Different - save current group and start new one
            result.append((current_group_paths, current_image))
            current_group_paths = [path]
            current_image = img

    # Don't forget the last group
    result.append((current_group_paths, current_image))

    return result


def load_element_data(elements_path: Path) -> Dict[str, Dict[str, int]]:
    """
    Load element bounding boxes from JSON file.

    Expected format:
    {
        "step-01.png": {"x": 100, "y": 200, "width": 150, "height": 40},
        "step-02.png": {"x": 300, "y": 150, "width": 200, "height": 50}
    }

    Or session format:
    {
        "steps": [
            {"screenshot": "step-01.png", "boundingBox": {...}}
        ]
    }
    """
    if not elements_path.exists():
        return {}

    with open(elements_path) as f:
        data = json.load(f)

    # Handle session format
    if 'steps' in data:
        return {
            Path(step.get('screenshot', '')).name: step.get('boundingBox', {})
            for step in data['steps']
            if step.get('screenshot') and step.get('boundingBox')
        }

    return data


def optimize_image(
    input_path: Path,
    output_path: Path,
    max_width: int = 1200,
    max_size_kb: int = 200,
    output_format: str = 'png',
    bounding_box: Dict[str, int] = None,
    crop_padding: int = 50
) -> dict:
    """
    Optimize an image for documentation use.

    Args:
        input_path: Path to input image
        output_path: Path to save optimized image
        max_width: Maximum width in pixels
        max_size_kb: Target maximum file size in KB
        output_format: Output format (png or jpg)
        bounding_box: Optional dict with x, y, width, height for cropping
        crop_padding: Padding around cropped element in pixels

    Returns:
        Dict with optimization results
    """
    img = Image.open(input_path)
    original_size = get_file_size_kb(input_path)
    original_dimensions = img.size

    # Crop to element region if bounding box provided
    cropped = False
    if bounding_box:
        img = crop_to_element(img, bounding_box, padding=crop_padding)
        cropped = True

    # Resize if too wide
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

    # Convert mode if needed
    if output_format == 'jpg' and img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    elif output_format == 'png' and img.mode == 'P':
        img = img.convert('RGBA')

    # Save with optimization
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_format == 'png':
        img.save(output_path, 'PNG', optimize=True)
    else:
        # Start with quality 85, reduce if needed
        quality = 85
        img.save(output_path, 'JPEG', quality=quality, optimize=True)

        # Reduce quality if file is still too large
        while get_file_size_kb(output_path) > max_size_kb and quality > 30:
            quality -= 10
            img.save(output_path, 'JPEG', quality=quality, optimize=True)

    final_size = get_file_size_kb(output_path)

    return {
        'input': str(input_path),
        'output': str(output_path),
        'original_size_kb': round(original_size, 2),
        'final_size_kb': round(final_size, 2),
        'original_dimensions': original_dimensions,
        'final_dimensions': img.size,
        'reduction_percent': round((1 - final_size / original_size) * 100, 1) if original_size > 0 else 0,
        'cropped': cropped
    }


def process_directory(
    input_dir: Path,
    output_dir: Optional[Path],
    max_width: int,
    max_size_kb: int,
    output_format: str,
    element_data: Dict[str, Dict[str, int]] = None,
    crop_padding: int = 50,
    combine_threshold: float = None
) -> list:
    """
    Process all images in a directory.

    Args:
        input_dir: Directory containing images
        output_dir: Output directory (or None to overwrite)
        max_width: Maximum image width
        max_size_kb: Maximum file size
        output_format: Output format
        element_data: Dict mapping filenames to bounding boxes for cropping
        crop_padding: Padding around cropped elements
        combine_threshold: If set, combine similar screenshots (SSIM > threshold)

    Returns:
        List of optimization results
    """
    if output_dir is None:
        output_dir = input_dir

    if element_data is None:
        element_data = {}

    results = []
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}

    # Collect all images
    image_paths = sorted([
        p for p in input_dir.iterdir()
        if p.suffix.lower() in image_extensions
    ])

    # Handle combining similar screenshots
    if combine_threshold is not None and SSIM_AVAILABLE:
        images = [(p, Image.open(p)) for p in image_paths]
        combined_groups = combine_similar_screenshots(images, combine_threshold)

        for paths, combined_img in combined_groups:
            # Use the last path for naming (shows final state)
            output_name = paths[-1].stem + '.' + output_format
            output_path = output_dir / output_name

            # Get bounding box if available
            bbox = element_data.get(paths[-1].name)

            try:
                # Save combined image and then optimize
                temp_path = output_dir / f"_temp_{paths[-1].name}"
                combined_img.save(temp_path)

                result = optimize_image(
                    temp_path,
                    output_path,
                    max_width,
                    max_size_kb,
                    output_format,
                    bounding_box=bbox,
                    crop_padding=crop_padding
                )

                temp_path.unlink()  # Clean up temp file

                result['combined_from'] = [str(p) for p in paths]
                results.append(result)

                if len(paths) > 1:
                    print(f"Combined: {[p.name for p in paths]} -> {output_path.name} "
                          f"({result['final_size_kb']}KB)")
                else:
                    print(f"Processed: {paths[0].name} -> {output_path.name} "
                          f"({result['final_size_kb']}KB, {result['reduction_percent']}% reduction)")

            except Exception as e:
                print(f"Error processing {paths[-1].name}: {e}", file=sys.stderr)
                results.append({
                    'input': str(paths[-1]),
                    'error': str(e)
                })
    else:
        # Standard processing without combining
        for input_path in image_paths:
            output_name = input_path.stem + '.' + output_format
            output_path = output_dir / output_name

            # Get bounding box if available
            bbox = element_data.get(input_path.name)

            try:
                result = optimize_image(
                    input_path,
                    output_path,
                    max_width,
                    max_size_kb,
                    output_format,
                    bounding_box=bbox,
                    crop_padding=crop_padding
                )
                results.append(result)
                crop_info = " (cropped)" if result.get('cropped') else ""
                print(f"Processed: {input_path.name} -> {output_path.name} "
                      f"({result['final_size_kb']}KB, {result['reduction_percent']}% reduction){crop_info}")
            except Exception as e:
                print(f"Error processing {input_path.name}: {e}", file=sys.stderr)
                results.append({
                    'input': str(input_path),
                    'error': str(e)
                })

    return results


def main():
    parser = argparse.ArgumentParser(
        description='Optimize images for documentation'
    )
    parser.add_argument('input_dir', type=Path, help='Directory containing images')
    parser.add_argument('--output-dir', type=Path, help='Output directory')
    parser.add_argument('--max-width', type=int, default=1200, help='Maximum width (default: 1200)')
    parser.add_argument('--max-size', type=int, default=200, help='Maximum size in KB (default: 200)')
    parser.add_argument('--format', choices=['png', 'jpg'], default='png', help='Output format')
    parser.add_argument('--json', action='store_true', help='Output results as JSON')
    parser.add_argument(
        '--elements',
        type=Path,
        help='JSON file with element bounding boxes for cropping'
    )
    parser.add_argument(
        '--crop-padding',
        type=int,
        default=50,
        help='Padding around cropped elements in pixels (default: 50)'
    )
    parser.add_argument(
        '--combine',
        type=float,
        metavar='THRESHOLD',
        help='Combine similar screenshots with SSIM > threshold (e.g., 0.95)'
    )

    args = parser.parse_args()

    if not DEPS_AVAILABLE:
        print("Error: PIL/Pillow not installed.", file=sys.stderr)
        print("Run: pip install pillow", file=sys.stderr)
        sys.exit(2)

    if args.combine and not SSIM_AVAILABLE:
        print("Warning: scikit-image not installed, --combine disabled.", file=sys.stderr)
        print("Run: pip install scikit-image", file=sys.stderr)
        args.combine = None

    if not args.input_dir.exists():
        print(f"Error: Input directory not found: {args.input_dir}", file=sys.stderr)
        sys.exit(2)

    if not args.input_dir.is_dir():
        print(f"Error: Not a directory: {args.input_dir}", file=sys.stderr)
        sys.exit(2)

    # Load element data for cropping
    element_data = {}
    if args.elements:
        element_data = load_element_data(args.elements)
        print(f"Loaded bounding boxes for {len(element_data)} elements")

    results = process_directory(
        args.input_dir,
        args.output_dir,
        args.max_width,
        args.max_size,
        args.format,
        element_data=element_data,
        crop_padding=args.crop_padding,
        combine_threshold=args.combine
    )

    if args.json:
        import json
        print(json.dumps(results, indent=2))
    else:
        # Summary
        successful = [r for r in results if 'error' not in r]
        if successful:
            total_original = sum(r['original_size_kb'] for r in successful)
            total_final = sum(r['final_size_kb'] for r in successful)
            print(f"\nProcessed {len(successful)} images")
            print(f"Total size: {total_original:.1f}KB -> {total_final:.1f}KB")
            if total_original > 0:
                print(f"Overall reduction: {(1 - total_final/total_original) * 100:.1f}%")


if __name__ == '__main__':
    main()
