#!/usr/bin/env python3
"""
Generate and edit images using Nano Banana Pro via OpenRouter API.

Supports various image generation models:
- google/gemini-3-pro-image-preview (default - generation and editing)
- black-forest-labs/flux.2-pro (generation and editing)
- black-forest-labs/flux.2-flex (generation)

For image editing, provide an input image along with an editing prompt.

Usage:
    # Generate a new image
    python generate_image.py "A beautiful sunset over mountains" -o sunset.png

    # Edit an existing image
    python generate_image.py "Make the sky purple" --input photo.jpg -o edited.png

    # Use a specific model
    python generate_image.py "Abstract art" -m "black-forest-labs/flux.2-pro" -o art.png
"""

import sys
import json
import base64
import argparse
import os
import urllib.request
import urllib.error
import socket
from pathlib import Path
from typing import Optional


def check_env_file() -> Optional[str]:
    """Check if .env file exists and contains OPENROUTER_API_KEY."""
    current_dir = Path.cwd()
    for parent in [current_dir] + list(current_dir.parents):
        env_file = parent / ".env"
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('OPENROUTER_API_KEY='):
                        api_key = line.split('=', 1)[1].strip().strip('"').strip("'")
                        if api_key:
                            return api_key
    return None


def load_image_as_base64(image_path: str) -> str:
    """Load an image file and return it as a base64 data URL."""
    path = Path(image_path)
    if not path.exists():
        print(f"❌ Error: Image file not found: {image_path}")
        sys.exit(1)

    ext = path.suffix.lower()
    mime_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
    }
    mime_type = mime_types.get(ext, 'image/png')

    with open(path, 'rb') as f:
        image_data = f.read()

    base64_data = base64.b64encode(image_data).decode('utf-8')
    return f"data:{mime_type};base64,{base64_data}"


def save_base64_image(base64_data: str, output_path: str) -> None:
    """Save base64 encoded image to file."""
    if ',' in base64_data:
        base64_data = base64_data.split(',', 1)[1]

    # Create output directory if needed
    output_dir = Path(output_path).parent
    if output_dir and not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    image_data = base64.b64decode(base64_data)
    with open(output_path, 'wb') as f:
        f.write(image_data)


def calculate_aspect_ratio(width: int, height: int) -> str:
    """Calculate aspect ratio string from width and height."""
    from math import gcd
    divisor = gcd(width, height)
    w_ratio = width // divisor
    h_ratio = height // divisor

    # Map to common aspect ratios for better model compatibility
    common_ratios = {
        (1, 1): "1:1",
        (16, 9): "16:9",
        (9, 16): "9:16",
        (4, 3): "4:3",
        (3, 4): "3:4",
        (3, 2): "3:2",
        (2, 3): "2:3",
        (2, 1): "2:1",
        (1, 2): "1:2",
    }

    if (w_ratio, h_ratio) in common_ratios:
        return common_ratios[(w_ratio, h_ratio)]

    return f"{w_ratio}:{h_ratio}"


def generate_image(
    prompt: str,
    model: str = "google/gemini-3-pro-image-preview",
    output_path: str = "generated_image.png",
    api_key: Optional[str] = None,
    input_image: Optional[str] = None,
    width: Optional[int] = None,
    height: Optional[int] = None
) -> dict:
    """
    Generate or edit an image using OpenRouter API.

    Uses Python stdlib only - no external dependencies required.

    Args:
        prompt: Text description of the image to generate, or editing instructions
        model: OpenRouter model ID (default: google/gemini-3-pro-image-preview)
        output_path: Path to save the generated image
        api_key: OpenRouter API key (will check .env and environment if not provided)
        input_image: Path to an input image for editing (optional)
        width: Target image width in pixels (optional, Gemini models only)
        height: Target image height in pixels (optional, Gemini models only)

    Returns:
        dict: Response from OpenRouter API
    """
    # Check for API key: param → env var → .env file
    if not api_key:
        api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        api_key = check_env_file()

    if not api_key:
        print("❌ Error: OPENROUTER_API_KEY not found!")
        print("\nPlease set the environment variable:")
        print("  export OPENROUTER_API_KEY=your-api-key-here")
        print("\nOr create a .env file in your project directory with:")
        print("  OPENROUTER_API_KEY=your-api-key-here")
        print("\nGet your API key from: https://openrouter.ai/keys")
        sys.exit(1)

    is_editing = input_image is not None

    print(f"\n{'='*50}")
    print(f"🍌 Nano Banana - {'Editing' if is_editing else 'Generating'} Image")
    print(f"{'='*50}")

    if is_editing:
        print(f"📷 Input: {input_image}")
        print(f"✏️  Edit: {prompt}")

        image_data_url = load_image_as_base64(input_image)
        message_content = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": image_data_url}}
        ]
    else:
        print(f"📝 Prompt: {prompt}")
        message_content = prompt

    print(f"🤖 Model: {model}")
    print(f"💾 Output: {output_path}")

    # Display dimension settings if specified
    if width and height:
        aspect_ratio = calculate_aspect_ratio(width, height)
        print(f"📐 Dimensions: {width}x{height} (aspect ratio: {aspect_ratio})")

        # Warn if using non-Gemini model with dimension controls
        if "gemini" not in model.lower():
            print(f"⚠️  Dimension control is optimized for Gemini models")
            print(f"   Model '{model}' may ignore dimension settings")

    print(f"{'='*50}\n")

    # Prepare request using stdlib
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/flight505/nano-banana",
        "X-Title": "Nano Banana Image Generator"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": message_content}],
        "modalities": ["image", "text"]
    }

    # Add dimension configuration if specified (Gemini models)
    if width and height:
        aspect_ratio = calculate_aspect_ratio(width, height)
        image_config = {
            "aspect_ratio": aspect_ratio
        }

        # Determine image size based on dimensions
        # OpenRouter Gemini models use: "1K", "2K", "4K"
        max_dim = max(width, height)
        if max_dim <= 512:
            image_config["image_size"] = "1K"  # ~1024px
        elif max_dim <= 1024:
            image_config["image_size"] = "2K"  # ~2048px
        else:
            image_config["image_size"] = "4K"  # ~4096px

        payload["image_config"] = image_config

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            response_body = response.read().decode("utf-8")
            result = json.loads(response_body)
    except urllib.error.HTTPError as e:
        error_body = ""
        try:
            error_body = e.read().decode("utf-8")
        except Exception:
            error_body = str(e)
        print(f"❌ API Error ({e.code}): {error_body}")
        sys.exit(1)
    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.timeout):
            print("❌ Request timed out after 120 seconds")
        else:
            print(f"❌ Connection error: {e.reason}")
        sys.exit(1)
    except socket.timeout:
        print("❌ Request timed out after 120 seconds")
        sys.exit(1)

    if result.get("choices"):
        message = result["choices"][0]["message"]
        images = []

        if message.get("images"):
            images = message["images"]
        elif message.get("content"):
            content = message["content"]
            if isinstance(content, list):
                for part in content:
                    if isinstance(part, dict) and part.get("type") == "image":
                        images.append(part)

        if images:
            image = images[0]
            if "image_url" in image:
                image_url = image["image_url"]["url"]
                save_base64_image(image_url, output_path)
                print(f"✅ Image saved to: {output_path}")
            elif "url" in image:
                save_base64_image(image["url"], output_path)
                print(f"✅ Image saved to: {output_path}")
            else:
                print(f"⚠️ Unexpected image format: {image}")
        else:
            print("⚠️ No image found in response")
            if message.get("content"):
                print(f"Response content: {message['content'][:500]}...")
    else:
        print("❌ No choices in response")
        print(f"Response: {json.dumps(result, indent=2)}")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Generate or edit images using Nano Banana Pro via OpenRouter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate with default model (Gemini 3 Pro Image Preview)
  python generate_image.py "A beautiful sunset over mountains" -o sunset.png

  # Generate with specific dimensions (256x256 square)
  python generate_image.py "A simple icon" -o icon.png --width 256 --height 256

  # Generate widescreen image (16:9 aspect ratio)
  python generate_image.py "Panoramic landscape" -o panorama.png --width 1024 --height 576

  # Use a specific model
  python generate_image.py "A cat in space" -m "black-forest-labs/flux.2-pro" -o cat.png

  # Edit an existing image
  python generate_image.py "Make the sky purple" --input photo.jpg -o edited.png

  # Edit with a specific model
  python generate_image.py "Add a hat to the person" --input portrait.png -m "black-forest-labs/flux.2-pro"

Popular image models:
  - google/gemini-3-pro-image-preview (default, high quality, generation + editing, supports dimensions)
  - black-forest-labs/flux.2-pro (fast, high quality, generation + editing)
  - black-forest-labs/flux.2-flex (development version, generation only)

Dimension Control:
  --width and --height parameters work best with Gemini models.
  The script calculates aspect ratio and maps dimensions to OpenRouter's image_config API.
  Common aspect ratios: 1:1 (square), 16:9 (widescreen), 4:3 (standard), 3:2 (photo)

Environment:
  OPENROUTER_API_KEY    OpenRouter API key (required)
        """
    )

    parser.add_argument("prompt", type=str,
                       help="Text description of the image, or editing instructions")
    parser.add_argument("--model", "-m", type=str, default="google/gemini-3-pro-image-preview",
                       help="OpenRouter model ID (default: google/gemini-3-pro-image-preview)")
    parser.add_argument("--output", "-o", type=str, default="generated_image.png",
                       help="Output file path (default: generated_image.png)")
    parser.add_argument("--input", "-i", type=str,
                       help="Input image path for editing (enables edit mode)")
    parser.add_argument("--api-key", type=str,
                       help="OpenRouter API key (will check environment if not provided)")
    parser.add_argument("--width", type=int,
                       help="Target image width in pixels (optional, works best with Gemini models)")
    parser.add_argument("--height", type=int,
                       help="Target image height in pixels (optional, works best with Gemini models)")

    args = parser.parse_args()

    # Validate dimensions if provided
    if (args.width and not args.height) or (args.height and not args.width):
        parser.error("Both --width and --height must be specified together")

    if args.width and args.width < 1:
        parser.error("Width must be positive")

    if args.height and args.height < 1:
        parser.error("Height must be positive")

    generate_image(
        prompt=args.prompt,
        model=args.model,
        output_path=args.output,
        api_key=args.api_key,
        input_image=args.input,
        width=args.width,
        height=args.height
    )


if __name__ == "__main__":
    main()
