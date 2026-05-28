#!/usr/bin/env python3
"""
Nano-Banana Template Image Generator

This script generates an empty presentation slide template image using the
Gemini Image Generation API from a JSON slide outline file's design_system.

The template contains only the header bar, footer bar, and background -
no text or content. This template can be used as a reference image when
generating actual slides to ensure consistent header/footer styling.

Usage:
    python Generate_Template.py <json_file> [--output <path>]

Examples:
    python Generate_Template.py Plan_Josh.json
    python Generate_Template.py Plan_Josh.json --output ./template.png
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

# Enable real-time output
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# Constants
MODEL = "gemini-3-pro-image-preview"
ASPECT_RATIO = "16:9"
IMAGE_SIZE = "2K"
MAX_RETRIES = 5
RETRY_DELAY_SECONDS = 5


def build_template_prompt(style_guide: dict) -> str:
    """Build a prompt for generating a template image with placeholder text.

    The template shows the layout structure (header bar, footer bar,
    accent lines, background) WITH placeholder text to establish text styling.

    Args:
        style_guide: The style_guide section from the JSON file.

    Returns:
        A prompt string for generating the template image.
    """
    ds = style_guide.get("design_system", {})
    cp = ds.get("color_palette", {})
    tp = ds.get("typography", {})
    ly = ds.get("layout", {})

    # Extract colors for use in requirements
    background = cp.get('background', '#FFFFFF white')
    accent = cp.get('accent_primary', '#B8282E crimson')
    text_color = cp.get('text', '#111111 dark')
    sub_color = cp.get('sub', '#F3F4F6 light gray')

    # Extract typography
    headings_style = tp.get('headings', 'Bold sans-serif, large scale')
    body_style = tp.get('body', 'Regular sans-serif, readable')

    # Extract layout descriptions
    header_desc = ly.get('header', 'Top 8% - bar with accent line below')
    content_desc = ly.get('content', 'Middle 84% - clean background')
    footer_desc = ly.get('footer', 'Bottom 8% - bar with accent line above')

    return f"""Create a presentation slide template image with placeholder text.

Design System:
- Background: {background}
- Accent primary: {accent}
- Text color: {text_color}
- Sub color (for bars): {sub_color}

Typography:
- Headings: {headings_style}
- Body: {body_style}

Layout Structure:
- Header: {header_desc}
- Content: {content_desc} - LEAVE COMPLETELY BLANK
- Footer: {footer_desc}

CRITICAL REQUIREMENTS:
1. Header area: Render the bar (sub color: {sub_color}) with accent line (accent: {accent}), AND include placeholder text "[SECTION TITLE]" left-aligned using heading typography ({headings_style}) in accent color ({accent})
2. Footer area: Render the bar (sub color: {sub_color}) with accent line (accent: {accent}), AND include placeholder text "[Page X/Y]" right-aligned using body typography ({body_style}) in text color ({text_color})
3. Content area: Completely blank, ONLY the background color ({background}) - nothing else
4. The placeholder text "[SECTION TITLE]" and "[Page X/Y]" must be clearly visible and establish the EXACT font style, size, and color for actual slides
5. 16:9 aspect ratio, 1920x1080 resolution
6. The result should look like a presentation slide template with header/footer structure and placeholder text
"""


def load_json(json_path: str) -> dict[str, Any]:
    """Load and parse the JSON file.

    Args:
        json_path: Path to the JSON file.

    Returns:
        The parsed JSON data.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def generate_template(client: genai.Client, prompt: str) -> Image.Image | None:
    """Generate a single template image using the Gemini API.

    Args:
        client: The Gemini API client.
        prompt: The prompt for image generation.

    Returns:
        The generated PIL Image, or None if generation failed.
    """
    for attempt in range(MAX_RETRIES):
        try:
            print(f"  [Attempt {attempt + 1}/{MAX_RETRIES}] Generating template image...")

            config = types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio=ASPECT_RATIO,
                    image_size=IMAGE_SIZE,
                ),
            )

            response = client.models.generate_content(
                model=MODEL,
                contents=[prompt],
                config=config,
            )

            # Check for empty response
            if response.parts is None:
                print(f"  [Empty Response] Attempt {attempt + 1}, retrying...")
                time.sleep(3)
                continue

            # Extract image from response
            for part in response.parts:
                if part.inline_data is not None:
                    image = part.as_image()
                    return image

            print(f"  [Warning] No image in response")
            time.sleep(3)

        except Exception as e:
            error_message = str(e)
            print(f"  [Error] {error_message[:200]}")

            if attempt < MAX_RETRIES - 1:
                print(f"  [Retry] Waiting {RETRY_DELAY_SECONDS} seconds...")
                time.sleep(RETRY_DELAY_SECONDS)
            else:
                print(f"  [Failed] Template generation failed after {MAX_RETRIES} attempts")
                return None

    return None


def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Generate an empty PPT template image using Nano-Banana Pro",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python Generate_Template.py Plan_Josh.json
    python Generate_Template.py Plan_Josh.json --output ./template.png
        """,
    )
    parser.add_argument(
        "json_file",
        help="Path to the JSON file containing slide outlines (with style_guide)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output file path for the template image (default: template.png in JSON directory)",
    )
    parser.add_argument(
        "--env-file",
        "-e",
        default=None,
        help="Path to .env file containing GOOGLE_API_KEY",
    )

    args = parser.parse_args()

    # Validate input file
    if not os.path.exists(args.json_file):
        print(f"Error: JSON file not found: {args.json_file}")
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path(args.json_file).parent / "template.png"

    # Load environment variables
    env_file = args.env_file
    if env_file is None:
        json_dir = Path(args.json_file).parent
        possible_env_paths = [
            json_dir / ".env",
            Path.cwd() / ".env",
            Path(__file__).parent / ".env",
        ]
        for env_path in possible_env_paths:
            if env_path.exists():
                env_file = str(env_path)
                break

    if env_file:
        load_dotenv(env_file)
        print(f"Loaded environment from: {env_file}")

    # Get API key
    api_key = os.getenv("GOOGLE_API_KEYS")
    if api_key:
        # Use first key from comma-separated list
        api_key = api_key.split(",")[0].strip()
    else:
        api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("Error: No API key found in environment variables")
        print("Please set GOOGLE_API_KEYS or GOOGLE_API_KEY in your .env file")
        sys.exit(1)

    # Load JSON data
    try:
        data = load_json(args.json_file)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        sys.exit(1)

    # Extract style_guide
    style_guide = data.get("style_guide", {})
    if not style_guide:
        print("Warning: No style_guide found in JSON, using defaults")

    # Print design system info
    ds = style_guide.get("design_system", {})
    cp = ds.get("color_palette", {})
    ly = ds.get("layout", {})
    print(f"\n{'=' * 60}")
    print("Template Generation")
    print(f"{'=' * 60}")
    print(f"Input: {args.json_file}")
    print(f"Output: {output_path}")
    print(f"Model: {MODEL}")
    print(f"\nDesign System:")
    print(f"  Background: {cp.get('background', 'N/A')}")
    print(f"  Accent: {cp.get('accent_primary', 'N/A')}")
    print(f"  Sub (bars): {cp.get('sub', 'N/A')}")
    print(f"\nLayout:")
    print(f"  Header: {ly.get('header', 'N/A')[:60]}...")
    print(f"  Footer: {ly.get('footer', 'N/A')[:60]}...")
    print(f"{'=' * 60}\n")

    # Build prompt
    prompt = build_template_prompt(style_guide)

    # Initialize client and generate
    client = genai.Client(api_key=api_key)
    print("Starting template generation...")

    image = generate_template(client, prompt)

    if image is not None:
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save image
        image.save(str(output_path))
        print(f"\n{'=' * 60}")
        print("Template Generated Successfully!")
        print(f"{'=' * 60}")
        print(f"Saved to: {output_path}")
        print(f"{'=' * 60}\n")
        sys.exit(0)
    else:
        print(f"\n{'=' * 60}")
        print("Template Generation Failed")
        print(f"{'=' * 60}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
