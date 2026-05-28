#!/usr/bin/env python3
"""
Export HTML to JPEG/PNG for The Calm CTO brand assets.

Usage:
    python3 export_image.py input.html output.jpg
    python3 export_image.py input.html output.jpg --twitter
    python3 export_image.py input.html output.png --width 1080 --height 1080
    python3 export_image.py input.html output.jpg --quality 90 --scale 2

The --twitter flag generates an additional image optimized for Twitter cards
(1200x600, 2:1 aspect ratio) with '-twitter' suffix in the filename.

Requirements:
    pip install playwright Pillow --break-system-packages
    playwright install chromium
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Standard dimensions
OG_WIDTH = 1200
OG_HEIGHT = 630
TWITTER_WIDTH = 1200
TWITTER_HEIGHT = 600  # 2:1 aspect ratio


async def capture_screenshot(page, width, height, quality, scale, is_jpeg):
    """Capture a screenshot at the specified dimensions."""
    from PIL import Image
    import io

    screenshot_options = {
        'type': 'jpeg' if is_jpeg else 'png',
        'clip': {
            'x': 0,
            'y': 0,
            'width': width,
            'height': height,
        },
    }

    if is_jpeg:
        screenshot_options['quality'] = quality

    screenshot_bytes = await page.screenshot(**screenshot_options)

    # Resize back to target dimensions if scaled
    if scale > 1:
        img = Image.open(io.BytesIO(screenshot_bytes))
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        return img
    else:
        return Image.open(io.BytesIO(screenshot_bytes))


def save_image(img, output_file, is_jpeg, quality):
    """Save image to file."""
    if is_jpeg:
        img.save(str(output_file), 'JPEG', quality=quality)
    else:
        img.save(str(output_file), 'PNG')

    size_kb = output_file.stat().st_size / 1024
    print(f"Exported: {output_file.name}")
    print(f"   Size: {img.width} x {img.height}px ({size_kb:.1f} KB)")


async def export_image(
    input_path: str,
    output_path: str,
    width: int = OG_WIDTH,
    height: int = OG_HEIGHT,
    quality: int = 95,
    scale: float = 2.0,
    twitter: bool = False,
):
    """Render HTML file to image using Playwright."""

    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("Error: playwright not installed.")
        print("Run: pip install playwright --break-system-packages")
        print("Then: playwright install chromium")
        sys.exit(1)

    try:
        from PIL import Image
    except ImportError:
        print("Error: Pillow not installed.")
        print("Run: pip install Pillow --break-system-packages")
        sys.exit(1)

    input_file = Path(input_path).resolve()
    output_file = Path(output_path).resolve()

    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)

    # Determine output format
    output_format = output_file.suffix.lower()
    if output_format not in ['.jpg', '.jpeg', '.png']:
        print(f"Error: Unsupported output format: {output_format}")
        print("Supported formats: .jpg, .jpeg, .png")
        sys.exit(1)

    is_jpeg = output_format in ['.jpg', '.jpeg']

    async with async_playwright() as p:
        browser = await p.chromium.launch()

        # --- Export main OG image ---
        page = await browser.new_page(
            viewport={'width': width, 'height': height},
            device_scale_factor=scale,
        )

        await page.goto(f'file://{input_file}')
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(0.5)

        img = await capture_screenshot(page, width, height, quality, scale, is_jpeg)
        save_image(img, output_file, is_jpeg, quality)

        # --- Export Twitter image if requested ---
        if twitter:
            # Inject CSS to adjust dimensions for Twitter (2:1 ratio)
            await page.add_style_tag(content=f'''
                body, body > div:first-child {{
                    height: {TWITTER_HEIGHT}px !important;
                    min-height: {TWITTER_HEIGHT}px !important;
                    max-height: {TWITTER_HEIGHT}px !important;
                }}
            ''')

            # Update viewport for Twitter dimensions
            await page.set_viewport_size({
                'width': TWITTER_WIDTH,
                'height': TWITTER_HEIGHT
            })

            await asyncio.sleep(0.3)

            # Generate Twitter output filename
            twitter_output = output_file.parent / f"{output_file.stem}-twitter{output_file.suffix}"

            img_twitter = await capture_screenshot(
                page, TWITTER_WIDTH, TWITTER_HEIGHT, quality, scale, is_jpeg
            )
            save_image(img_twitter, twitter_output, is_jpeg, quality)

        await browser.close()


def main():
    parser = argparse.ArgumentParser(
        description='Export HTML to JPEG/PNG image',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 export_image.py header.html header.jpg
  python3 export_image.py header.html header.jpg --twitter
  python3 export_image.py quote.html quote.png --width 1080 --height 1080
  python3 export_image.py stats.html stats.jpg --quality 85 --scale 1

The --twitter flag generates an additional image at 1200x600 (2:1 ratio)
for Twitter cards, saved with '-twitter' suffix (e.g., header-twitter.jpg).
        """
    )

    parser.add_argument('input', help='Input HTML file')
    parser.add_argument('output', help='Output image file (.jpg, .jpeg, or .png)')
    parser.add_argument('--width', type=int, default=OG_WIDTH, help=f'Canvas width (default: {OG_WIDTH})')
    parser.add_argument('--height', type=int, default=OG_HEIGHT, help=f'Canvas height (default: {OG_HEIGHT})')
    parser.add_argument('--quality', type=int, default=95, help='JPEG quality 1-100 (default: 95)')
    parser.add_argument('--scale', type=float, default=2.0, help='Device scale for retina (default: 2.0)')
    parser.add_argument('--twitter', action='store_true', help='Also generate Twitter card image (1200x600)')

    args = parser.parse_args()

    asyncio.run(export_image(
        args.input,
        args.output,
        width=args.width,
        height=args.height,
        quality=args.quality,
        scale=args.scale,
        twitter=args.twitter,
    ))


if __name__ == '__main__':
    main()
