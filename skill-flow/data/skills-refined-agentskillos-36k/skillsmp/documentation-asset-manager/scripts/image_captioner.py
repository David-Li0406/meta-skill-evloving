#!/usr/bin/env python3
"""
Generate AI captions for images using Claude Code native vision
Supports downloading from URLs or local files
Uses subprocess to call claude for native vision analysis
"""

import requests
import json
import sys
import os
import subprocess
import tempfile
from pathlib import Path
from io import BytesIO
from PIL import Image

class ImageCaptioner:
    def __init__(self):
        """Initialize - no API key needed, uses Claude Code native"""
        pass

    def download_image(self, url):
        """Download image from URL"""
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.content

    def load_local_image(self, path):
        """Load image from local file"""
        with open(path, 'rb') as f:
            return f.read()

    def save_temp_image(self, image_data):
        """Save image data to temporary file"""
        try:
            img = Image.open(BytesIO(image_data))
            suffix = f'.{img.format.lower()}' if img.format else '.png'
        except Exception:
            suffix = '.png'

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        temp_file.write(image_data)
        temp_file.close()
        return temp_file.name

    def generate_caption(self, image_source, caption_type='alt_text', is_url=True):
        """
        Generate caption for image using Claude Code native vision

        Args:
            image_source: URL or file path to image
            caption_type: 'alt_text', 'descriptive', or 'seo'
            is_url: True if image_source is URL, False if local file

        Returns:
            dict with caption and metadata
        """
        prompts = {
            'alt_text': (
                "Generate concise, accessible alt text (40-80 characters) for this "
                "documentation screenshot. Focus on what the image shows and its purpose. "
                "Do NOT use phrases like 'screenshot of' or 'image showing' - just describe "
                "the content directly. Be specific about UI elements visible."
            ),
            'descriptive': (
                "Generate a CONCISE description of EXACTLY 100-200 characters total (count carefully!). "
                "Include only the most essential UI elements visible and key functionality shown. "
                "Be brief and specific. STOP at 200 characters maximum - this is a hard limit."
            ),
            'seo': (
                "Generate SEO-optimized description (60-120 characters) for this documentation screenshot. "
                "Include: what Tallyfy feature is shown, specific UI elements visible, and the "
                "user action being documented. Use relevant keywords for documentation search. "
                "Format naturally for search engines."
            )
        }

        prompt_text = prompts.get(caption_type, prompts['alt_text'])
        temp_file = None

        try:
            # Get image as local file
            if is_url:
                image_data = self.download_image(image_source)
                temp_file = self.save_temp_image(image_data)
                image_path = temp_file
            else:
                image_path = image_source

            # Create Claude Code prompt that explicitly reads the image
            full_prompt = f"""You are a caption generator. Read the image at this path: {image_path}

This is a Tallyfy product screenshot showing workflow management UI, process templates, task management, approval flows, form builders, or automation rules.

Your task: {prompt_text}

CRITICAL OUTPUT REQUIREMENTS:
- Output ONLY the caption text itself
- Do NOT include any greetings, explanations, or commentary
- Do NOT use phrases like "Here is the caption:" or "Caption:"
- Do NOT use markdown formatting, quotes, or code blocks
- Just output the raw caption text and nothing else

Begin your response with the caption text directly, no preamble."""

            # Write prompt to temp file for claude command
            prompt_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
            prompt_file.write(full_prompt)
            prompt_file.close()

            # Call claude with prompt file - Claude will use Read tool to view the image
            result = subprocess.run(
                ['claude', '-p', prompt_file.name, '--dangerously-skip-permissions'],
                capture_output=True,
                text=True,
                timeout=120
            )

            # Cleanup prompt file
            os.unlink(prompt_file.name)

            if result.returncode == 0:
                caption = result.stdout.strip()

                # Remove any common prefixes/formatting
                for prefix in ['Caption:', 'Alt text:', 'Description:', 'SEO:', '```', '"', "'"]:
                    if caption.startswith(prefix):
                        caption = caption[len(prefix):].strip()
                    if caption.endswith(prefix):
                        caption = caption[:-len(prefix)].strip()

                # Post-processing: Enforce length limits as safety net
                if caption_type == 'descriptive' and len(caption) > 200:
                    # Truncate to 197 chars + ellipsis to enforce 200 char limit
                    caption = caption[:197] + "..."
                elif caption_type == 'alt_text' and len(caption) > 80:
                    # Truncate alt text if too long
                    caption = caption[:77] + "..."
                elif caption_type == 'seo' and len(caption) > 120:
                    # Truncate SEO if too long
                    caption = caption[:117] + "..."

                return {
                    'success': True,
                    'caption': caption,
                    'caption_type': caption_type,
                    'image_source': image_source,
                    'model': 'claude-code-native'
                }
            else:
                return {
                    'success': False,
                    'error': f'Claude command failed: {result.stderr}',
                    'image_source': image_source,
                    'caption_type': caption_type
                }

        except requests.RequestException as e:
            return {
                'success': False,
                'error': f'Failed to download image: {str(e)}',
                'image_source': image_source,
                'caption_type': caption_type
            }

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Claude command timed out',
                'image_source': image_source,
                'caption_type': caption_type
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'image_source': image_source,
                'caption_type': caption_type
            }

        finally:
            # Cleanup temp file if created
            if temp_file and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except Exception:
                    pass

    def generate_all_captions(self, image_source, is_url=True):
        """Generate all three caption types for an image"""
        captions = {}
        all_success = True

        for caption_type in ['alt_text', 'descriptive', 'seo']:
            result = self.generate_caption(image_source, caption_type, is_url)

            if result['success']:
                captions[caption_type] = result['caption']
            else:
                captions[caption_type] = ''
                captions[f'{caption_type}_error'] = result['error']
                all_success = False

        return {
            'success': all_success,
            'captions': captions,
            'image_source': image_source
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate AI captions for images')
    parser.add_argument('--url', help='Image URL')
    parser.add_argument('--file', help='Local image file')
    parser.add_argument('--type', choices=['alt_text', 'descriptive', 'seo', 'all'],
                       default='all', help='Caption type to generate')
    parser.add_argument('--output', help='Output JSON file')

    args = parser.parse_args()

    if not args.url and not args.file:
        parser.error('Either --url or --file is required')

    try:
        captioner = ImageCaptioner()

        image_source = args.url if args.url else args.file
        is_url = bool(args.url)

        if args.type == 'all':
            result = captioner.generate_all_captions(image_source, is_url)
        else:
            result = captioner.generate_caption(image_source, args.type, is_url)

        print(json.dumps(result, indent=2))

        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(result, indent=2))

        sys.exit(0 if result['success'] else 1)

    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e)
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == '__main__':
    main()
