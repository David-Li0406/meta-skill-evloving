#!/usr/bin/env python3
"""
Gemini Imagen API - Image Generation Script

This script generates images using Google's Gemini Imagen API.
Supports multiple models, aspect ratios, and customizable output.
"""

import requests
import json
import base64
import sys
import argparse
from datetime import datetime
from pathlib import Path
from PIL import Image
from io import BytesIO


def generate_images(
    api_key: str,
    prompt: str,
    model: str = "imagen-4.0-fast-generate-001",
    num_images: int = 1,
    aspect_ratio: str = "1:1",
    output_dir: str = ".",
    verbose: bool = True
) -> list[str]:
    """
    Generate images using Gemini Imagen API.

    Args:
        api_key: Gemini API key
        prompt: Text description of the image to generate
        model: Model to use (imagen-4.0-fast-generate-001, imagen-4.0-generate-001, imagen-4.0-ultra-generate-001)
        num_images: Number of images to generate (1-4)
        aspect_ratio: Image aspect ratio (1:1, 3:4, 4:3, 9:16, 16:9)
        output_dir: Directory to save generated images
        verbose: Print progress messages

    Returns:
        List of paths to generated image files
    """
    if verbose:
        print(f"🎨 Generating {num_images} image(s) with Gemini Imagen API")
        print(f"   Model: {model}")
        print(f"   Prompt: {prompt}")
        print(f"   Aspect Ratio: {aspect_ratio}\n")

    # API endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:predict?key={api_key}"

    # Request payload
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": num_images,
            "aspectRatio": aspect_ratio
        }
    }

    try:
        # Make API request
        if verbose:
            print("📡 Sending request to Gemini API...")

        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )

        # Check response status
        if response.status_code != 200:
            error_msg = f"API Error {response.status_code}: {response.text}"
            print(f"❌ {error_msg}", file=sys.stderr)
            sys.exit(1)

        # Parse response
        result = response.json()

        if verbose:
            print("✅ Response received!\n")

        # Extract and save images
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        saved_files = []

        if "predictions" in result:
            for i, prediction in enumerate(result["predictions"]):
                if "bytesBase64Encoded" in prediction:
                    # Decode base64 image
                    image_data = base64.b64decode(prediction["bytesBase64Encoded"])
                    image = Image.open(BytesIO(image_data))

                    # Generate filename
                    filename = f"gemini_image_{timestamp}_{i+1}.png"
                    filepath = output_path / filename

                    # Save image
                    image.save(filepath)
                    saved_files.append(str(filepath))

                    if verbose:
                        print(f"✅ Saved: {filepath}")
                        print(f"   Size: {image.size}")
        else:
            print("❌ No images found in API response", file=sys.stderr)
            sys.exit(1)

        if verbose:
            print(f"\n🎉 Generated {len(saved_files)} image(s) successfully!")

        return saved_files

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Gemini Imagen API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "A robot painting" --api-key YOUR_KEY
  %(prog)s "Sunset over mountains" --model imagen-4.0-ultra-generate-001 --num 2
  %(prog)s "City skyline" --aspect-ratio 16:9 --output ./images
        """
    )

    parser.add_argument(
        "prompt",
        help="Text description of the image to generate"
    )
    parser.add_argument(
        "--api-key",
        required=True,
        help="Gemini API key"
    )
    parser.add_argument(
        "--model",
        default="imagen-4.0-fast-generate-001",
        choices=[
            "imagen-4.0-fast-generate-001",
            "imagen-4.0-generate-001",
            "imagen-4.0-ultra-generate-001"
        ],
        help="Model to use (default: imagen-4.0-fast-generate-001)"
    )
    parser.add_argument(
        "--num",
        type=int,
        default=1,
        choices=[1, 2, 3, 4],
        help="Number of images to generate (default: 1)"
    )
    parser.add_argument(
        "--aspect-ratio",
        default="1:1",
        choices=["1:1", "3:4", "4:3", "9:16", "16:9"],
        help="Image aspect ratio (default: 1:1)"
    )
    parser.add_argument(
        "--output",
        default=".",
        help="Output directory for generated images (default: current directory)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress messages"
    )

    args = parser.parse_args()

    generate_images(
        api_key=args.api_key,
        prompt=args.prompt,
        model=args.model,
        num_images=args.num,
        aspect_ratio=args.aspect_ratio,
        output_dir=args.output,
        verbose=not args.quiet
    )


if __name__ == "__main__":
    main()
