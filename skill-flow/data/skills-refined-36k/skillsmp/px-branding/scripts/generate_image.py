#!/usr/bin/env python3
"""
AI Image Generation for PX Branding
Uses Google Gemini API to generate branded images.

Usage:
    python generate_image.py "prompt" output.png [--dry-run]
    python generate_image.py --summary
"""
import os
import sys
import json
import base64
import argparse
from datetime import datetime

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests")
    sys.exit(1)

# =============================================================================
# CONFIGURATION
# =============================================================================
TEMP_DIR = os.path.join(os.environ.get('TEMP', '/tmp'), 'px-branding')
LOG_FILE = os.path.join(TEMP_DIR, 'api_log.jsonl')

# Gemini API configuration
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
GEMINI_MODEL = 'gemini-2.0-flash-exp'
GEMINI_URL = f'https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent'

# Cost estimation (approximate)
COST_PER_IMAGE_1K = 0.134  # USD for 1K-2K resolution
COST_PER_IMAGE_4K = 0.24   # USD for 4K resolution

# PX Brand colors for prompts
PX_BRAND_PROMPT = """
Use these brand colors:
- Primary blue: #3399FF (vibrant, headers)
- Dark blue: #0F3D66 (accents, depth)
- Light blue: #D5E4F5 (backgrounds, soft elements)
- White: #FFFFFF (text, highlights)
Style: Modern, professional, clean, corporate but approachable.
"""


def ensure_temp_dir():
    """Ensure temp directory exists."""
    os.makedirs(TEMP_DIR, exist_ok=True)


def log_request(prompt, output_path, cost_estimate, success, error=None):
    """Log API request to JSONL file."""
    ensure_temp_dir()
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'prompt': prompt,
        'output_path': output_path,
        'cost_estimate_usd': cost_estimate,
        'success': success,
        'error': error
    }
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry) + '\n')


def get_usage_summary():
    """Read log file and return usage summary."""
    if not os.path.exists(LOG_FILE):
        return {'total_requests': 0, 'successful': 0, 'failed': 0, 'total_cost_usd': 0.0}

    total_requests = 0
    successful = 0
    failed = 0
    total_cost = 0.0

    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                total_requests += 1
                if entry.get('success'):
                    successful += 1
                    total_cost += entry.get('cost_estimate_usd', 0)
                else:
                    failed += 1
            except json.JSONDecodeError:
                continue

    return {
        'total_requests': total_requests,
        'successful': successful,
        'failed': failed,
        'total_cost_usd': total_cost,
        'total_cost_brl': total_cost * 6.0  # Approximate USD to BRL
    }


def generate_image(prompt, output_path, dry_run=False):
    """
    Generate an image using Gemini API.

    Args:
        prompt: Text description of the image
        output_path: Where to save the generated image
        dry_run: If True, only estimate cost without generating

    Returns:
        dict with success status and details
    """
    if not GEMINI_API_KEY:
        return {
            'success': False,
            'error': 'GEMINI_API_KEY environment variable not set'
        }

    # Enhance prompt with brand guidelines
    full_prompt = f"{prompt}\n\n{PX_BRAND_PROMPT}"

    cost_estimate = COST_PER_IMAGE_1K

    if dry_run:
        print(f"[DRY RUN] Would generate image:")
        print(f"  Prompt: {prompt[:100]}...")
        print(f"  Output: {output_path}")
        print(f"  Estimated cost: ${cost_estimate:.3f} USD (~R${cost_estimate * 6:.2f} BRL)")
        return {'success': True, 'dry_run': True, 'cost_estimate': cost_estimate}

    print(f"Generating image...")
    print(f"  Prompt: {prompt[:100]}...")
    print(f"  Output: {output_path}")

    try:
        headers = {
            'Content-Type': 'application/json'
        }

        payload = {
            'contents': [{
                'parts': [{
                    'text': full_prompt
                }]
            }],
            'generationConfig': {
                'responseModalities': ['image', 'text'],
                'responseMimeType': 'image/png'
            }
        }

        response = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=payload,
            timeout=120
        )

        if response.status_code != 200:
            error_msg = f"API error {response.status_code}: {response.text[:500]}"
            log_request(prompt, output_path, cost_estimate, False, error_msg)
            return {'success': False, 'error': error_msg}

        result = response.json()

        # Extract image from response
        candidates = result.get('candidates', [])
        if not candidates:
            error_msg = "No candidates in response"
            log_request(prompt, output_path, cost_estimate, False, error_msg)
            return {'success': False, 'error': error_msg}

        parts = candidates[0].get('content', {}).get('parts', [])
        image_data = None

        for part in parts:
            if 'inlineData' in part:
                image_data = part['inlineData'].get('data')
                break

        if not image_data:
            error_msg = "No image data in response"
            log_request(prompt, output_path, cost_estimate, False, error_msg)
            return {'success': False, 'error': error_msg}

        # Save image
        ensure_temp_dir()
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(output_path, 'wb') as f:
            f.write(base64.b64decode(image_data))

        log_request(prompt, output_path, cost_estimate, True)
        print(f"  Saved to: {output_path}")
        print(f"  Cost: ~${cost_estimate:.3f} USD")

        return {'success': True, 'output_path': output_path, 'cost': cost_estimate}

    except requests.exceptions.Timeout:
        error_msg = "Request timed out"
        log_request(prompt, output_path, cost_estimate, False, error_msg)
        return {'success': False, 'error': error_msg}
    except Exception as e:
        error_msg = str(e)
        log_request(prompt, output_path, cost_estimate, False, error_msg)
        return {'success': False, 'error': error_msg}


def main():
    parser = argparse.ArgumentParser(description='Generate AI images for PX branding')
    parser.add_argument('prompt', nargs='?', help='Image description')
    parser.add_argument('output', nargs='?', help='Output file path')
    parser.add_argument('--dry-run', action='store_true', help='Estimate cost only')
    parser.add_argument('--summary', action='store_true', help='Show usage summary')

    args = parser.parse_args()

    if args.summary:
        summary = get_usage_summary()
        print("=" * 50)
        print("PX Branding - AI Image Generation Summary")
        print("=" * 50)
        print(f"Total requests: {summary['total_requests']}")
        print(f"Successful: {summary['successful']}")
        print(f"Failed: {summary['failed']}")
        print(f"Total cost: ${summary['total_cost_usd']:.3f} USD (~R${summary['total_cost_brl']:.2f} BRL)")
        print("=" * 50)
        return

    if not args.prompt or not args.output:
        parser.print_help()
        sys.exit(1)

    result = generate_image(args.prompt, args.output, args.dry_run)

    if not result['success']:
        print(f"ERROR: {result.get('error', 'Unknown error')}")
        sys.exit(1)


if __name__ == '__main__':
    main()
