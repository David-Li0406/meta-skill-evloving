#!/usr/bin/env python3
"""
detect_step.py - SSIM-based step boundary detection for DocuGen

This script compares consecutive screenshots using Structural Similarity Index (SSIM)
to determine when a meaningful visual change has occurred, indicating a step boundary.

Usage:
    python detect_step.py <before_image> <after_image> [--threshold 0.90]

Returns:
    Exit code 0 if significant change detected (SSIM < threshold)
    Exit code 1 if no significant change (SSIM >= threshold)
    Prints SSIM score to stdout

Dependencies:
    - scikit-image
    - PIL/Pillow
    - numpy
"""

import argparse
import os
import sys
from pathlib import Path

# Default threshold, can be overridden via SSIM_THRESHOLD environment variable
DEFAULT_THRESHOLD = float(os.environ.get('SSIM_THRESHOLD', '0.90'))

try:
    from skimage.metrics import structural_similarity as ssim
    from PIL import Image
    import numpy as np
    DEPS_AVAILABLE = True
except ImportError:
    DEPS_AVAILABLE = False


def load_image_as_grayscale(image_path: Path) -> np.ndarray:
    """Load an image and convert to grayscale numpy array."""
    img = Image.open(image_path).convert('L')
    return np.array(img)


def compare_images(before_path: Path, after_path: Path) -> float:
    """
    Compare two images using SSIM.

    Args:
        before_path: Path to the "before" screenshot
        after_path: Path to the "after" screenshot

    Returns:
        SSIM score between 0 and 1 (1 = identical)
    """
    before = load_image_as_grayscale(before_path)
    after = load_image_as_grayscale(after_path)

    # Resize if dimensions don't match
    if before.shape != after.shape:
        # Resize after to match before
        after_img = Image.fromarray(after)
        after_img = after_img.resize((before.shape[1], before.shape[0]))
        after = np.array(after_img)

    score, _ = ssim(before, after, full=True)
    return score


def is_significant_change(ssim_score: float, threshold: float = 0.90) -> bool:
    """
    Determine if the SSIM score indicates a significant visual change.

    Args:
        ssim_score: SSIM similarity score
        threshold: Scores below this indicate significant change

    Returns:
        True if change is significant (new step boundary)
    """
    return ssim_score < threshold


def main():
    parser = argparse.ArgumentParser(
        description='Detect step boundaries using SSIM comparison'
    )
    parser.add_argument('before', type=Path, help='Path to before screenshot')
    parser.add_argument('after', type=Path, help='Path to after screenshot')
    parser.add_argument(
        '--threshold',
        type=float,
        default=DEFAULT_THRESHOLD,
        help=f'SSIM threshold (default: {DEFAULT_THRESHOLD}, or set SSIM_THRESHOLD env var). Lower = more sensitive'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output result as JSON'
    )

    args = parser.parse_args()

    if not DEPS_AVAILABLE:
        print("Error: Required dependencies not installed.", file=sys.stderr)
        print("Run: pip install scikit-image pillow numpy", file=sys.stderr)
        sys.exit(2)

    if not args.before.exists():
        print(f"Error: Before image not found: {args.before}", file=sys.stderr)
        sys.exit(2)

    if not args.after.exists():
        print(f"Error: After image not found: {args.after}", file=sys.stderr)
        sys.exit(2)

    score = compare_images(args.before, args.after)
    is_step = is_significant_change(score, args.threshold)

    if args.json:
        import json
        from datetime import datetime
        result = {
            'ssim_score': round(score, 4),
            'threshold': args.threshold,
            'is_significant_change': is_step,
            'before': str(args.before),
            'after': str(args.after),
            'timestamp': datetime.now().isoformat(),
            'confidence': round(1 - score, 4)  # Higher confidence = more different
        }
        print(json.dumps(result))
    else:
        print(f"SSIM: {score:.4f}")
        print(f"Threshold: {args.threshold}")
        print(f"Significant change: {is_step}")

    sys.exit(0 if is_step else 1)


if __name__ == '__main__':
    main()
