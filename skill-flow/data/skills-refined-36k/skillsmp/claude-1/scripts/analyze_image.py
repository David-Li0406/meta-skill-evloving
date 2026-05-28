#!/usr/bin/env python3
"""
Image analysis using Claude API.

Usage:
    uv run analyze_image.py image.png "Describe this image"
    uv run analyze_image.py image.jpg "What text is visible?" --model claude-3-5-haiku-20241022
    uv run analyze_image.py https://example.com/image.png "Analyze this chart"

Environment:
    ANTHROPIC_API_KEY must be set
"""

import argparse
import base64
import sys
from pathlib import Path
from anthropic import Anthropic, APIError, RateLimitError


def get_media_type(path: str) -> str:
    """Determine media type from file extension."""
    ext = Path(path).suffix.lower()
    media_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    return media_types.get(ext, "image/jpeg")


def analyze_image(
    image_source: str,
    prompt: str,
    model: str = "claude-sonnet-4-5-20250929",
    system: str | None = None,
    max_tokens: int = 1024,
) -> str:
    """
    Analyze an image using Claude API.

    Args:
        image_source: Path to local image file or URL
        prompt: Question or instruction about the image
        model: Model identifier
        system: Optional system prompt
        max_tokens: Maximum tokens to generate

    Returns:
        Analysis result as text
    """
    client = Anthropic()

    # Determine if source is URL or file
    is_url = image_source.startswith(("http://", "https://"))

    if is_url:
        image_content = {
            "type": "image",
            "source": {
                "type": "url",
                "url": image_source,
            },
        }
    else:
        # Load and encode local file
        image_path = Path(image_source)
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_source}")

        with open(image_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode("utf-8")

        image_content = {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": get_media_type(image_source),
                "data": image_data,
            },
        }

    # Build request
    params = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "user",
                "content": [
                    image_content,
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    }

    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message.content[0].text


def main():
    parser = argparse.ArgumentParser(description="Analyze images using Claude API")
    parser.add_argument("image", help="Path to image file or URL")
    parser.add_argument("prompt", help="Question or instruction about the image")
    parser.add_argument(
        "--model",
        "-m",
        default="claude-sonnet-4-5-20250929",
        help="Model to use (default: claude-sonnet-4-5-20250929)",
    )
    parser.add_argument(
        "--system",
        "-s",
        help="System prompt for context",
    )
    parser.add_argument(
        "--max-tokens",
        "-t",
        type=int,
        default=1024,
        help="Maximum tokens to generate (default: 1024)",
    )

    args = parser.parse_args()

    try:
        result = analyze_image(
            image_source=args.image,
            prompt=args.prompt,
            model=args.model,
            system=args.system,
            max_tokens=args.max_tokens,
        )
        print(result)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except RateLimitError:
        print("Rate limit exceeded. Please wait and try again.", file=sys.stderr)
        sys.exit(1)
    except APIError as e:
        print(f"API error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
