#!/usr/bin/env python3
"""
Logo generation with transparent background using Gemini + PIL.

This script generates high-quality logos by:
1. Using Gemini (google/gemini-3-pro-image-preview) with a chromakey background
2. Programmatically converting chromakey pixels to transparent using PIL

The chromakey approach uses green (#00FF00) as the background color, which
provides professional-quality edge detection without the "halo" artifacts
that occur with white background conversion. Green is preferred over magenta
because it avoids conflicts with purple/violet tones common in pixel art.

Usage:
    uv run --with requests --with pillow generate_logo.py "Your logo prompt" --output logo.png

Environment:
    SKILL_OPENROUTER_API_KEY - Required API key from https://openrouter.ai/keys

Dependencies: requests, pillow
"""

import argparse
import base64
import io
import math
import os
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests library required.", file=sys.stderr)
    print("Run with: uv run --with requests --with pillow generate_logo.py ...", file=sys.stderr)
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("Error: pillow library required.", file=sys.stderr)
    print("Run with: uv run --with requests --with pillow generate_logo.py ...", file=sys.stderr)
    sys.exit(1)


def parse_hex_color(hex_color: str) -> tuple:
    """Parse hex color string to RGB tuple.

    Args:
        hex_color: Color in format '#RRGGBB' or 'RRGGBB'

    Returns:
        Tuple of (R, G, B) values (0-255)
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


class OpenRouterClient:
    BASE_URL = "https://openrouter.ai/api/v1"

    def __init__(self, api_key: str):
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://claude.ai/claude-code",
            "X-Title": "Claude Code"
        }

    def _request(self, method: str, endpoint: str, payload: dict = None, max_retries: int = 3):
        """Make API request with retry logic."""
        url = endpoint if endpoint.startswith("http") else f"{self.BASE_URL}/{endpoint}"

        for attempt in range(max_retries):
            try:
                if method == "GET":
                    response = requests.get(url, headers=self.headers, timeout=120)
                else:
                    response = requests.post(url, headers=self.headers, json=payload, timeout=120)

                if response.status_code == 200:
                    return response.json()

                error = response.json().get("error", {})
                code = error.get("code", response.status_code)
                message = error.get("message", response.text)

                # Retryable errors
                if code in [408, 429, 502, 503] and attempt < max_retries - 1:
                    wait = min(2 ** attempt * 2, 30)
                    print(f"Retrying in {wait}s (attempt {attempt + 1}/{max_retries})...", file=sys.stderr)
                    time.sleep(wait)
                    continue

                # Non-retryable errors
                error_messages = {
                    400: "Bad request - check parameters",
                    401: "Invalid API key - check SKILL_OPENROUTER_API_KEY",
                    402: "Insufficient credits - add funds at openrouter.ai",
                    403: "Content flagged by moderation",
                    429: "Rate limited - wait before retrying"
                }
                msg = error_messages.get(code, message)
                raise Exception(f"OpenRouter error {code}: {msg}")

            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    continue
                raise Exception("Request timed out after retries")
            except requests.exceptions.RequestException as e:
                raise Exception(f"Network error: {e}")

        raise Exception("Max retries exceeded")

    def generate_image(self, model: str, prompt: str, aspect_ratio: str = "1:1",
                       size: str = "1K") -> list:
        """Generate image using chat completions endpoint."""
        image_config = {"aspect_ratio": aspect_ratio, "image_size": size}

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "modalities": ["image", "text"],
            "image_config": image_config,
            "n": 1
        }

        result = self._request("POST", "chat/completions", payload)
        images = result["choices"][0]["message"].get("images", [])
        return images


def convert_white_to_transparent(image_bytes: bytes, tolerance: int = 10) -> Image.Image:
    """Convert #ffffff (white) pixels to transparent.

    Args:
        image_bytes: Input image as bytes
        tolerance: Color tolerance for white detection (0-255)

    Returns:
        PIL Image with transparency
    """
    img = Image.open(io.BytesIO(image_bytes))

    # Convert to RGBA if not already
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # Get image dimensions
    width, height = img.size

    # Replace white pixels with transparent
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            # Check if pixel is white (within tolerance)
            if r >= 255 - tolerance and g >= 255 - tolerance and b >= 255 - tolerance:
                # Make transparent
                pixels[x, y] = (255, 255, 255, 0)

    return img


def chromakey_to_transparent(image_bytes: bytes, key_color: tuple = (0, 255, 0),
                              tolerance: int = 70) -> Image.Image:
    """Convert chromakey background to transparent with smooth edges.

    Uses color distance in RGB space to calculate alpha. This is the same
    technique used in professional film/TV green screen compositing.

    The algorithm:
    - Pure key color → fully transparent (alpha=0)
    - Blended pixels (anti-aliased edges) → proportional alpha based on distance
    - Non-key pixels → fully opaque (alpha=255)

    Args:
        image_bytes: Input image as bytes
        key_color: RGB tuple of the key color (default: green #00FF00)
        tolerance: Base tolerance for key color detection (default: 70)
                   Higher values = more aggressive transparency

    Returns:
        PIL Image with transparency applied
    """
    img = Image.open(io.BytesIO(image_bytes))

    # Convert to RGBA if not already
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    pixels = img.load()
    kr, kg, kb = key_color

    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]

            # Calculate Euclidean distance from key color in RGB space
            distance = math.sqrt((r - kr)**2 + (g - kg)**2 + (b - kb)**2)

            if distance < tolerance:
                # Pure key color or very close - fully transparent
                pixels[x, y] = (r, g, b, 0)
            elif distance < tolerance * 3:
                # Blended region (anti-aliased edges) - proportional alpha
                # This creates smooth transitions instead of hard edges
                alpha = int(255 * (distance - tolerance) / (tolerance * 2))
                pixels[x, y] = (r, g, b, min(255, alpha))
            # else: keep original alpha (fully opaque)

    return img


def compress_png(image_path: Path, quality: int = 80) -> tuple:
    """Compress PNG using pngquant if available.

    pngquant provides 60-80% compression with excellent alpha handling
    via premultiplied color space - the same technique used in professional
    image editing software.

    Args:
        image_path: Path to the PNG file to compress (modified in-place)
        quality: Quality setting 1-100 (default: 80)

    Returns:
        Tuple of (original_size, compressed_size) in bytes
    """
    import shutil
    import subprocess

    original_size = image_path.stat().st_size

    # Check for pngquant
    if not shutil.which("pngquant"):
        print("  pngquant not found, skipping compression", file=sys.stderr)
        print("  Install: brew install pngquant (macOS) or apt install pngquant (Linux)", file=sys.stderr)
        return original_size, original_size

    # Run pngquant in-place
    # Quality range: min-max, using quality-20 as min for flexibility
    quality_min = max(0, quality - 20)
    result = subprocess.run([
        "pngquant",
        "--quality", f"{quality_min}-{quality}",
        "--speed", "1",      # Best compression (slowest)
        "--strip",           # Remove metadata
        "--force",           # Overwrite output
        "--output", str(image_path),
        str(image_path)
    ], capture_output=True)

    if result.returncode != 0:
        # pngquant returns 99 if quality can't be achieved, which is OK
        if result.returncode != 99:
            stderr = result.stderr.decode().strip()
            if stderr:
                print(f"  pngquant warning: {stderr}", file=sys.stderr)
        return original_size, original_size

    compressed_size = image_path.stat().st_size
    return original_size, compressed_size


def main():
    parser = argparse.ArgumentParser(
        description="Logo generation with Gemini + programmatic transparency"
    )
    parser.add_argument("prompt", help="Logo description prompt")
    parser.add_argument("--output", "-o", default="logo.png", help="Output filename")
    parser.add_argument("--aspect", "-a", default="1:1", help="Aspect ratio (1:1, 16:9, etc)")
    parser.add_argument("--size", "-z", default="1K", help="Size (1K, 2K, 4K)")
    parser.add_argument("--model", "-m", default="google/gemini-3-pro-image-preview",
                        help="Model to use for generation")
    parser.add_argument("--tolerance", "-t", type=int, default=70,
                        help="Color tolerance for transparency (default 70 for chromakey, 10 for white)")
    parser.add_argument("--keep-original", action="store_true",
                        help="Keep original image before transparency conversion")

    # Chromakey options (new default approach)
    parser.add_argument("--key-color", "-k", default="#00FF00",
                        help="Chromakey color in hex (default: #00FF00 green)")
    parser.add_argument("--white-bg", action="store_true",
                        help="Use legacy white background approach instead of chromakey")

    # Compression options
    parser.add_argument("--compress", action="store_true", default=True,
                        help="Compress output PNG using pngquant (default: enabled)")
    parser.add_argument("--no-compress", dest="compress", action="store_false",
                        help="Skip PNG compression")
    parser.add_argument("--compress-quality", type=int, default=80,
                        help="pngquant quality 1-100 (default: 80)")

    args = parser.parse_args()

    # Get API key
    api_key = os.environ.get("SKILL_OPENROUTER_API_KEY")
    if not api_key:
        print("Error: SKILL_OPENROUTER_API_KEY environment variable not set", file=sys.stderr)
        print("Get your key at: https://openrouter.ai/keys", file=sys.stderr)
        sys.exit(1)

    client = OpenRouterClient(api_key)
    output_path = Path(args.output).resolve()

    try:
        # Determine background approach and enhance prompt accordingly
        if args.white_bg:
            # Legacy white background approach
            bg_color = "#ffffff"
            bg_name = "white"
            enhanced_prompt = f"{args.prompt}\n\nIMPORTANT: Use pure white (#ffffff) for the background only. Do not use white (#ffffff) anywhere else in the design - the logo/icon itself should use other colors."
        else:
            # Chromakey approach (default) - uses green for cleaner edge detection
            bg_color = args.key_color.upper()
            # Determine color name based on key color
            if bg_color == "#00FF00":
                bg_name = "green"
                avoid_colors = "green tones"
            elif bg_color == "#FF00FF":
                bg_name = "magenta"
                avoid_colors = "magenta or pink tones"
            else:
                bg_name = "chromakey"
                avoid_colors = f"colors similar to {bg_color}"
            enhanced_prompt = f"{args.prompt}\n\nIMPORTANT: Use pure {bg_name} ({bg_color}) for the background only. Do not use {avoid_colors} anywhere in the design itself - the logo/icon should use other colors."

        # Generate with Gemini
        print(f"Generating with {args.model}...", file=sys.stderr)
        print(f"  Background: {bg_name} ({bg_color})", file=sys.stderr)
        images = client.generate_image(
            args.model,
            enhanced_prompt,
            aspect_ratio=args.aspect,
            size=args.size
        )

        if not images:
            print("Error: No images generated", file=sys.stderr)
            sys.exit(1)

        # Get image data URL
        data_url = images[0]["image_url"]["url"]
        base64_data = data_url.split(",")[1]
        image_bytes = base64.b64decode(base64_data)

        print("✓ Image generation complete", file=sys.stderr)

        # Save original if requested
        if args.keep_original:
            original_path = output_path.parent / f"{output_path.stem}_original{output_path.suffix}"
            original_path.parent.mkdir(parents=True, exist_ok=True)
            with open(original_path, "wb") as f:
                f.write(image_bytes)
            print(f"  Saved original: {original_path}", file=sys.stderr)

        # Convert background to transparent
        if args.white_bg:
            # Legacy white background conversion
            print("Converting #ffffff to transparent...", file=sys.stderr)
            # Use lower tolerance for white (default was 10)
            tolerance = args.tolerance if args.tolerance != 70 else 10
            transparent_img = convert_white_to_transparent(image_bytes, tolerance=tolerance)
        else:
            # Chromakey conversion (default) - better edge handling
            print(f"Applying chromakey transparency ({bg_color})...", file=sys.stderr)
            key_rgb = parse_hex_color(args.key_color)
            transparent_img = chromakey_to_transparent(image_bytes, key_color=key_rgb,
                                                        tolerance=args.tolerance)
        print("✓ Transparency conversion complete", file=sys.stderr)

        # Save final output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        transparent_img.save(output_path, format='PNG')

        # Compress if enabled
        if args.compress:
            print("Compressing PNG...", file=sys.stderr)
            orig_size, comp_size = compress_png(output_path, args.compress_quality)
            if orig_size != comp_size:
                reduction = (1 - comp_size / orig_size) * 100
                print(f"✓ Compressed: {orig_size:,}B → {comp_size:,}B ({reduction:.1f}% reduction)", file=sys.stderr)

        print(f"✓ Saved logo: {output_path}", file=sys.stderr)
        print(f"\nSuccess! Transparent logo created at: {output_path}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
