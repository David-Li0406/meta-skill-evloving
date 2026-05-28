#!/usr/bin/env python3
"""
Recraft API Image Processor
Remove backgrounds and vectorize images using Recraft API.
"""
import argparse
import os
import sys
import requests

RECRAFT_API_BASE = "https://external.api.recraft.ai/v1"


def remove_background(input_path: str, output_path: str, api_key: str) -> bool:
    """Remove background from an image using Recraft API."""
    print(f"Removing background from: {input_path}")

    url = f"{RECRAFT_API_BASE}/images/removeBackground"
    headers = {"Authorization": f"Bearer {api_key}"}

    with open(input_path, "rb") as f:
        files = {"file": (os.path.basename(input_path), f, "image/png")}
        response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        data = response.json()
        if "image" in data and "url" in data["image"]:
            # Download the processed image
            img_response = requests.get(data["image"]["url"])
            if img_response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(img_response.content)
                print(f"Background removed, saved to: {output_path}")
                return True
        print(f"Unexpected response format: {data}")
        return False
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return False


def vectorize(input_path: str, output_path: str, api_key: str) -> bool:
    """Vectorize an image using Recraft API."""
    print(f"Vectorizing: {input_path}")

    url = f"{RECRAFT_API_BASE}/images/vectorize"
    headers = {"Authorization": f"Bearer {api_key}"}

    with open(input_path, "rb") as f:
        files = {"file": (os.path.basename(input_path), f, "image/png")}
        response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        data = response.json()
        if "image" in data and "url" in data["image"]:
            # Download the SVG
            img_response = requests.get(data["image"]["url"])
            if img_response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(img_response.content)
                print(f"Vectorized, saved to: {output_path}")
                return True
        print(f"Unexpected response format: {data}")
        return False
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Process images with Recraft API (remove background, vectorize).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --action remove-bg --input image.png --output nobg.png
  %(prog)s --action vectorize --input nobg.png --output vector.svg
        """
    )
    parser.add_argument(
        "--action",
        required=True,
        choices=["remove-bg", "vectorize"],
        help="Action to perform"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Input image path"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output file path"
    )
    args = parser.parse_args()

    api_key = os.environ.get("RECRAFT_API_KEY")
    if not api_key:
        print("Error: RECRAFT_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    # Create output directory if needed
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if args.action == "remove-bg":
        success = remove_background(args.input, args.output, api_key)
    elif args.action == "vectorize":
        success = vectorize(args.input, args.output, api_key)
    else:
        print(f"Unknown action: {args.action}")
        success = False

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
