#!/usr/bin/env python3
"""
Nano Banana PRO Image Generation Script

Usage:
    python generate_image.py "prompt" output.png [options]
    
Options:
    --model MODEL      gemini-3-pro-image-preview (default) or gemini-2.5-flash-image
    --ratio RATIO      Aspect ratio (1:1, 16:9, etc.)
    --size SIZE        Resolution: 1K, 2K, 4K
    --search           Enable Google Search grounding
    --input FILE       Input image(s) for editing (can specify multiple)
    --json             Output full JSON response
"""

import os
import sys
import json
import base64
import argparse
import urllib.request
import urllib.error
from pathlib import Path

API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

def get_mime_type(filepath):
    """Determine MIME type from file extension."""
    ext = Path(filepath).suffix.lower()
    mime_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
    }
    return mime_types.get(ext, 'image/png')

def encode_image(filepath):
    """Read and base64 encode an image file."""
    with open(filepath, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def generate_image(
    prompt,
    output_path,
    model="gemini-3-pro-image-preview",
    aspect_ratio="1:1",
    image_size="2K",
    enable_search=False,
    input_images=None
):
    """Generate an image using Nano Banana PRO API."""
    
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    # Build parts array
    parts = [{"text": prompt}]
    
    # Add input images if provided
    if input_images:
        for img_path in input_images:
            mime_type = get_mime_type(img_path)
            img_data = encode_image(img_path)
            parts.append({
                "inline_data": {
                    "mime_type": mime_type,
                    "data": img_data
                }
            })
    
    # Build request body
    request_body = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {
                "aspectRatio": aspect_ratio,
                "imageSize": image_size
            }
        }
    }
    
    # Add search tool if enabled
    if enable_search:
        request_body["tools"] = [{"google_search": {}}]
    
    # Make API request
    url = f"{API_BASE}/{model}:generateContent"
    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    data = json.dumps(request_body).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        raise RuntimeError(f"API Error ({e.code}): {error_body}")
    
    # Extract image data
    image_data = None
    text_response = None
    
    for part in result.get('candidates', [{}])[0].get('content', {}).get('parts', []):
        if 'inlineData' in part:
            image_data = part['inlineData']['data']
        elif 'text' in part:
            text_response = part['text']
    
    if not image_data:
        raise RuntimeError(f"No image in response. Text: {text_response}")
    
    # Save image
    with open(output_path, 'wb') as f:
        f.write(base64.b64decode(image_data))
    
    return {
        'output_path': output_path,
        'text_response': text_response,
        'full_response': result
    }

def main():
    parser = argparse.ArgumentParser(description='Generate images with Nano Banana PRO')
    parser.add_argument('prompt', help='Text prompt for image generation')
    parser.add_argument('output', help='Output file path')
    parser.add_argument('--model', default='gemini-3-pro-image-preview',
                       help='Model: gemini-3-pro-image-preview or gemini-2.5-flash-image')
    parser.add_argument('--ratio', default='1:1',
                       help='Aspect ratio (1:1, 16:9, 9:16, 4:3, etc.)')
    parser.add_argument('--size', default='2K',
                       help='Image size: 1K, 2K, or 4K')
    parser.add_argument('--search', action='store_true',
                       help='Enable Google Search grounding')
    parser.add_argument('--input', action='append', dest='inputs',
                       help='Input image(s) for editing (can use multiple times)')
    parser.add_argument('--json', action='store_true',
                       help='Output full JSON response')
    
    args = parser.parse_args()
    
    print(f"Generating image with {args.model}...")
    print(f"Prompt: {args.prompt}")
    print(f"Aspect Ratio: {args.ratio}, Size: {args.size}")
    
    result = generate_image(
        prompt=args.prompt,
        output_path=args.output,
        model=args.model,
        aspect_ratio=args.ratio,
        image_size=args.size,
        enable_search=args.search,
        input_images=args.inputs
    )
    
    print(f"\nImage saved to: {result['output_path']}")
    
    if result['text_response']:
        print(f"\nModel response:\n{result['text_response']}")
    
    if args.json:
        print(f"\nFull response:\n{json.dumps(result['full_response'], indent=2)}")

if __name__ == '__main__':
    main()
