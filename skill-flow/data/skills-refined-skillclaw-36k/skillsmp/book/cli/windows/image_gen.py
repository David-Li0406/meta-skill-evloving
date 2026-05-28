# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
#     "python-dotenv>=1.0.0",
# ]
# ///
"""
Image generation using Gemini Nano Banana Pro API.

Can be used as:
1. Module: from image_gen import generate_image, edit_image
2. Standalone: uv run image_gen.py new --path "output.png" "prompt"
               uv run image_gen.py edit --path "input.png" "edit instructions"

Examples:
    uv run image_gen.py new --path "figures/flowchart.png" "A process flowchart"
    uv run image_gen.py edit --path "figures/chart.png" "Add a legend"
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def get_api_key(provided_key: str | None = None) -> str | None:
    """Get API key from argument first, then environment."""
    if provided_key:
        return provided_key
    return os.environ.get("GEMINI_API_KEY")


def generate_image(
    prompt: str,
    output_path: Path,
    resolution: str = "1K",
    echo=print,
    error_style=None
) -> int:
    """
    Generate a new image from a text prompt.

    Args:
        prompt: Text description of the image to generate
        output_path: Path where to save the generated image
        resolution: Image resolution (1K, 2K, or 4K)
        echo: Function for normal output
        error_style: Function for error messages

    Returns:
        0 on success, 1 on error
    """
    if error_style is None:
        error_style = echo

    api_key = get_api_key()
    if not api_key:
        error_style("Error: No API key found.")
        error_style("Please set GEMINI_API_KEY in .env file or environment.")
        return 1

    # Import here after checking API key to avoid slow import on error
    from google import genai
    from google.genai import types
    from PIL import Image as PILImage

    # Ensure output directory exists
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    echo(f"Generating image: {output_path}")
    echo(f"Resolution: {resolution}")
    echo(f"Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                image_config=types.ImageConfig(
                    image_size=resolution
                )
            )
        )

        # Process response and save image
        image_saved = False
        for part in response.parts:
            if part.text is not None:
                echo(f"Model response: {part.text}")
            elif part.inline_data is not None:
                from io import BytesIO

                image_data = part.inline_data.data
                if isinstance(image_data, str):
                    import base64
                    image_data = base64.b64decode(image_data)

                image = PILImage.open(BytesIO(image_data))

                # Ensure RGB mode for PNG
                if image.mode == 'RGBA':
                    rgb_image = PILImage.new('RGB', image.size, (255, 255, 255))
                    rgb_image.paste(image, mask=image.split()[3])
                    rgb_image.save(str(output_path), 'PNG')
                elif image.mode == 'RGB':
                    image.save(str(output_path), 'PNG')
                else:
                    image.convert('RGB').save(str(output_path), 'PNG')
                image_saved = True

        if image_saved:
            echo(f"Image saved: {output_path.resolve()}")
            return 0
        else:
            error_style("Error: No image was generated in the response.")
            return 1

    except Exception as e:
        error_style(f"Error generating image: {e}")
        return 1


def edit_image(
    prompt: str,
    image_path: Path,
    resolution: str | None = None,
    echo=print,
    error_style=None
) -> int:
    """
    Edit an existing image with a text prompt.

    Args:
        prompt: Text instructions for editing the image
        image_path: Path to the image to edit (will be overwritten)
        resolution: Image resolution (1K, 2K, 4K) or None for auto-detect
        echo: Function for normal output
        error_style: Function for error messages

    Returns:
        0 on success, 1 on error
    """
    if error_style is None:
        error_style = echo

    api_key = get_api_key()
    if not api_key:
        error_style("Error: No API key found.")
        error_style("Please set GEMINI_API_KEY in .env file or environment.")
        return 1

    image_path = Path(image_path)
    if not image_path.exists():
        error_style(f"Error: Image not found: {image_path}")
        return 1

    # Import here after checking API key to avoid slow import on error
    from google import genai
    from google.genai import types
    from PIL import Image as PILImage

    echo(f"Editing image: {image_path}")

    try:
        # Load input image
        input_image = PILImage.open(image_path)
        echo(f"Loaded image: {input_image.size[0]}x{input_image.size[1]}")

        # Auto-detect resolution if not specified
        output_resolution = resolution
        if output_resolution is None:
            width, height = input_image.size
            max_dim = max(width, height)
            if max_dim >= 3000:
                output_resolution = "4K"
            elif max_dim >= 1500:
                output_resolution = "2K"
            else:
                output_resolution = "1K"
            echo(f"Auto-detected resolution: {output_resolution}")
        else:
            echo(f"Resolution: {output_resolution}")

        echo(f"Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[input_image, prompt],
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                image_config=types.ImageConfig(
                    image_size=output_resolution
                )
            )
        )

        # Process response and save image (overwrite original)
        image_saved = False
        for part in response.parts:
            if part.text is not None:
                echo(f"Model response: {part.text}")
            elif part.inline_data is not None:
                from io import BytesIO

                image_data = part.inline_data.data
                if isinstance(image_data, str):
                    import base64
                    image_data = base64.b64decode(image_data)

                image = PILImage.open(BytesIO(image_data))

                # Ensure RGB mode for PNG
                if image.mode == 'RGBA':
                    rgb_image = PILImage.new('RGB', image.size, (255, 255, 255))
                    rgb_image.paste(image, mask=image.split()[3])
                    rgb_image.save(str(image_path), 'PNG')
                elif image.mode == 'RGB':
                    image.save(str(image_path), 'PNG')
                else:
                    image.convert('RGB').save(str(image_path), 'PNG')
                image_saved = True

        if image_saved:
            echo(f"Image saved: {image_path.resolve()}")
            return 0
        else:
            error_style("Error: No image was generated in the response.")
            return 1

    except Exception as e:
        error_style(f"Error editing image: {e}")
        return 1


def main():
    """Standalone entry point with subcommands."""
    parser = argparse.ArgumentParser(
        description="Generate and edit images using Gemini Nano Banana Pro API"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # New image command
    new_parser = subparsers.add_parser("new", help="Generate a new image")
    new_parser.add_argument(
        "--path", "-p",
        required=True,
        help="Output path for the image (e.g., figures/flowchart.png)"
    )
    new_parser.add_argument(
        "--resolution", "-r",
        choices=["1K", "2K", "4K"],
        default="1K",
        help="Image resolution: 1K (default), 2K, or 4K"
    )
    new_parser.add_argument(
        "prompt",
        help="Text description of the image to generate"
    )

    # Edit image command
    edit_parser = subparsers.add_parser("edit", help="Edit an existing image")
    edit_parser.add_argument(
        "--path", "-p",
        required=True,
        help="Path to image to edit (will be overwritten)"
    )
    edit_parser.add_argument(
        "--resolution", "-r",
        choices=["1K", "2K", "4K"],
        default=None,
        help="Output resolution (auto-detected from input if not specified)"
    )
    edit_parser.add_argument(
        "prompt",
        help="Text instructions for editing the image"
    )

    args = parser.parse_args()

    if args.command == "new":
        return_code = generate_image(
            prompt=args.prompt,
            output_path=Path(args.path),
            resolution=args.resolution
        )
    elif args.command == "edit":
        return_code = edit_image(
            prompt=args.prompt,
            image_path=Path(args.path),
            resolution=args.resolution
        )
    else:
        parser.print_help()
        return_code = 1

    sys.exit(return_code)


if __name__ == "__main__":
    main()
