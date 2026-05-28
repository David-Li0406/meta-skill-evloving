#!/usr/bin/env python3
"""
Gemini Image Generator
Generate images using Google Gemini AI.
"""
import argparse
import base64
import io
import os
import sys

from google import genai
from google.genai import types
from PIL import Image


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Google Gemini.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --prompt "A cat in space" --output cat.png
  %(prog)s --prompt "Same style but blue" --reference input.png --output blue.png
        """
    )
    parser.add_argument(
        "--prompt",
        required=True,
        help="Text prompt describing the image to generate"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output file path for the generated image"
    )
    parser.add_argument(
        "--reference",
        help="Optional reference image path for style/content guidance"
    )
    args = parser.parse_args()

    # Get API key from environment
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.", file=sys.stderr)
        print("Set it with:", file=sys.stderr)
        print("  Unix: export GEMINI_API_KEY='your-api-key'", file=sys.stderr)
        print("  PowerShell: $env:GEMINI_API_KEY = 'your-api-key'", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    # Build content list
    contents = [args.prompt]

    # Add reference image if provided
    if args.reference:
        try:
            reference_image = Image.open(args.reference)
            contents.append(reference_image)
            print(f"Using reference image: {args.reference}")
        except FileNotFoundError:
            print(f"Error: Reference image '{args.reference}' not found.", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error loading reference image: {e}", file=sys.stderr)
            sys.exit(1)

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    print("Generating image...")

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["Text", "Image"],
            )
        )
    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        sys.exit(1)

    # Process response
    image_saved = False
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(f"Model response: {part.text}")
        elif part.inline_data is not None:
            try:
                # Get the raw bytes directly
                image_bytes = part.inline_data.data
                
                # If it's a string (base64), decode it
                if isinstance(image_bytes, str):
                    image_bytes = base64.b64decode(image_bytes)
                
                # Open and save the image
                generated_image = Image.open(io.BytesIO(image_bytes))
                generated_image.save(args.output)
                print(f"Image saved to: {args.output}")
                image_saved = True
            except Exception as e:
                print(f"Error processing image data: {e}", file=sys.stderr)
                # Try saving raw data for debugging
                debug_path = args.output + ".debug.bin"
                with open(debug_path, "wb") as f:
                    if isinstance(part.inline_data.data, str):
                        f.write(part.inline_data.data.encode())
                    else:
                        f.write(part.inline_data.data)
                print(f"Raw data saved to {debug_path} for debugging")

    if not image_saved:
        print("Warning: No image was generated in the response.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
