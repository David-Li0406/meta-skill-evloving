#!/usr/bin/env python3
# /// script
# dependencies = ["google-genai", "pillow"]
# ///
"""
generate_images.py - Unified image generation with progress tracking

IMPORTANT: This script MUST be run with uv:
    uv run generate_images.py --config slides_config.json

DO NOT run with plain python (dependencies will not be found)

Usage:
    uv run generate_images.py --config <config_file>

Config format:
    {
        "slides": [
            {"number": 1, "prompt": "...", "style": "professional"},
            {"number": 2, "prompt": "...", "style": "data-viz"}
        ],
        "output_dir": "./output/",
        "format": "webp",
        "quality": 90
    }

Note: Model is set via NANO_BANANA_MODEL environment variable, not in config.

Output files (in system temp directory):
    - Progress: {temp_dir}/nano-banana-progress.json
    - Results: {temp_dir}/nano-banana-results.json
"""

import json
import sys
import os
import io
import tempfile
from pathlib import Path
from datetime import datetime, UTC
from typing import Dict, List, Tuple, Optional

from google import genai
from google.genai import types
from PIL import Image as PILImage

# Configure UTF-8 encoding for Windows console
if sys.platform == 'win32':
    # Force UTF-8 encoding for stdout/stderr on Windows
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Progress and results file paths (cross-platform)
TEMP_DIR = Path(tempfile.gettempdir())
PROGRESS_FILE = TEMP_DIR / "nano-banana-progress.json"
RESULTS_FILE = TEMP_DIR / "nano-banana-results.json"


def validate_output_dir(path_str: str) -> Path:
    """Validate that output_dir is a relative path.

    Args:
        path_str: Path string from config

    Returns:
        Path object if valid

    Raises:
        SystemExit: If path is absolute
    """
    path = Path(path_str)

    if path.is_absolute():
        print(
            f"Error: output_dir must be relative path, got: {path_str}\n"
            f"Use './dirname/' instead for cross-platform compatibility.",
            file=sys.stderr
        )
        sys.exit(1)

    return path


def load_config(config_path: str) -> Dict:
    """Load and validate configuration file.

    Args:
        config_path: Path to JSON configuration file

    Returns:
        Validated configuration dictionary

    Raises:
        SystemExit: If config is invalid or file not found
    """
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: Config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config file: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate required fields
    if 'slides' not in config or not isinstance(config['slides'], list):
        print("Error: Config must contain 'slides' array", file=sys.stderr)
        sys.exit(1)

    if not config['slides']:
        print("Error: 'slides' array is empty", file=sys.stderr)
        sys.exit(1)

    if 'output_dir' not in config:
        print("Error: Config must contain 'output_dir'", file=sys.stderr)
        sys.exit(1)

    # Validate output_dir is relative path
    validate_output_dir(config['output_dir'])

    # Validate each slide
    for i, slide in enumerate(config['slides']):
        if 'number' not in slide:
            print(f"Error: Slide {i} missing 'number' field", file=sys.stderr)
            sys.exit(1)
        if 'prompt' not in slide:
            print(f"Error: Slide {i} missing 'prompt' field", file=sys.stderr)
            sys.exit(1)

    return config


def write_progress(current: int, total: int, status: str,
                   completed: List[str], failed: List[int],
                   started_at: str) -> None:
    """Write progress to JSON file.

    Args:
        current: Current slide number being processed
        total: Total number of slides
        status: Current status message
        completed: List of completed slide paths
        failed: List of failed slide numbers
        started_at: ISO timestamp when batch started
    """
    try:
        progress = {
            "current": current,
            "total": total,
            "status": status,
            "completed": completed,
            "failed": failed,
            "started_at": started_at,
            "updated_at": datetime.now(UTC).isoformat() + 'Z'
        }

        # Write atomically (write to temp, then rename)
        temp_file = PROGRESS_FILE.with_suffix('.tmp')
        with open(temp_file, 'w') as f:
            json.dump(progress, f, indent=2)
        temp_file.replace(PROGRESS_FILE)

    except Exception as e:
        print(f"Warning: Failed to write progress file: {e}", file=sys.stderr)


def write_results(completed: List[Dict], failed: List[int],
                  errors: List[Dict], started_at: str) -> None:
    """Write final results to JSON file.

    Args:
        completed: List of completed slide info dicts
        failed: List of failed slide numbers
        errors: List of error info dicts
        started_at: ISO timestamp when batch started
    """
    try:
        completed_at = datetime.now(UTC).isoformat() + 'Z'
        started_dt = datetime.fromisoformat(started_at.rstrip('Z'))
        completed_dt = datetime.fromisoformat(completed_at.rstrip('Z'))
        duration = (completed_dt - started_dt).total_seconds()

        results = {
            "completed": len(completed),
            "failed": len(failed),
            "total": len(completed) + len(failed),
            "outputs": completed,
            "errors": errors,
            "started_at": started_at,
            "completed_at": completed_at,
            "duration_seconds": int(duration)
        }

        with open(RESULTS_FILE, 'w') as f:
            json.dump(results, f, indent=2)

    except Exception as e:
        print(f"Error: Failed to write results file: {e}", file=sys.stderr)
        sys.exit(1)


def detect_api_type(model: str) -> str:
    """Detect which API to use based on model name.

    Args:
        model: Model name string

    Returns:
        'imagen' or 'gemini'
    """
    return 'imagen' if 'imagen' in model.lower() else 'gemini'


def generate_slide_gemini(client: genai.Client, slide: Dict,
                          output_dir: Path, model: str,
                          output_format: str, quality: int) -> Tuple[bool, Optional[str], Optional[str]]:
    """Generate single slide using Gemini API.

    Args:
        client: Gemini client instance
        slide: Slide configuration dict
        output_dir: Output directory path
        model: Model name
        output_format: Output format (webp, png, jpeg)
        quality: Image quality (1-100)

    Returns:
        Tuple of (success, output_path, error_message)
    """
    try:
        # Build prompt with style if specified
        prompt = slide['prompt']
        if 'style' in slide:
            style = slide['style']
            if style == 'professional':
                prompt = f"Professional presentation slide: {prompt}. Clean, minimal design with clear typography."
            elif style == 'data-viz':
                prompt = f"Data visualization slide: {prompt}. Clear charts and graphs, professional color scheme."
            elif style == 'infographic':
                prompt = f"Infographic style: {prompt}. Visual storytelling with icons and illustrations."
            elif style == 'trendlife':
                # TrendLife brand style with colors (logo added later via overlay)
                prompt = f"{prompt}\n\nUse TrendLife brand colors for Trend Micro presentations:\n- IMPORTANT: Title text and all headings MUST be in Trend Red (#D71920)\n- Primary accents and highlights: Trend Red (#D71920)\n- Guardian Red (#6F0000) for supporting elements and depth\n- Neutral palette: Dark gray (#57585B), medium gray (#808285), light gray (#E7E6E6)\n- Black (#000000) for body text, white (#FFFFFF) for backgrounds\nKeep the design clean, professional, and suitable for corporate presentations.\nDO NOT include any logos or brand text - these will be added separately."

        # Determine if lossless is needed (for slides/diagrams)
        use_lossless = output_format == 'webp' and slide.get('style') in ['professional', 'data-viz', 'infographic', 'trendlife']

        # Get aspect ratio from slide config (default to 16:9 for slides)
        aspect_ratio = slide.get('aspect_ratio', '16:9')

        # Generate image
        config = types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size='2K'
            )
        )

        response = client.models.generate_content(
            model=model,
            contents=[prompt],
            config=config
        )

        # Save image
        if not response.candidates or not response.candidates[0].content.parts:
            return False, None, "No image generated in response"

        image_part = response.candidates[0].content.parts[0]
        if not hasattr(image_part, 'inline_data') or not image_part.inline_data:
            return False, None, "No image data in response"

        image_bytes = image_part.inline_data.data
        image = PILImage.open(io.BytesIO(image_bytes))

        # Save with appropriate format
        slide_num = slide['number']
        output_path = output_dir / f"slide-{slide_num:02d}.{output_format}"

        if output_format == 'webp':
            image.save(output_path, 'WEBP', quality=quality, lossless=use_lossless)
        elif output_format == 'png':
            image.save(output_path, 'PNG', optimize=True)
        elif output_format in ['jpeg', 'jpg']:
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')
            image.save(output_path, 'JPEG', quality=quality, optimize=True)
        else:
            return False, None, f"Unsupported format: {output_format}"

        # TrendLife Logo Overlay (MANDATORY for trendlife style)
        if slide.get('style') == 'trendlife':
            from logo_overlay import overlay_logo, detect_layout_type

            # Detect layout type from prompt
            layout_type = detect_layout_type(slide['prompt'], slide_number=slide['number'])

            # Logo path
            logo_path = Path(__file__).parent / 'assets/logos/trendlife-logo.png'

            # Create temporary path for overlay
            temp_output = output_path.with_stem(output_path.stem + '_with_logo')

            try:
                # Apply logo overlay
                overlay_logo(
                    background_path=output_path,
                    logo_path=logo_path,
                    output_path=temp_output,
                    layout_type=layout_type
                )

                # Replace original with logo version
                temp_output.replace(output_path)
            except Exception as e:
                # Log warning but don't fail the slide generation
                print(f"Warning: Logo overlay failed for slide {slide['number']}: {e}", file=sys.stderr)

        # Get file size
        size_kb = output_path.stat().st_size // 1024

        return True, str(output_path), None

    except Exception as e:
        return False, None, str(e)


def generate_slide_imagen(client: genai.Client, slide: Dict,
                          output_dir: Path, model: str,
                          output_format: str, quality: int) -> Tuple[bool, Optional[str], Optional[str]]:
    """Generate single slide using Imagen API.

    Args:
        client: Gemini client instance
        slide: Slide configuration dict
        output_dir: Output directory path
        model: Model name
        output_format: Output format (webp, png, jpeg)
        quality: Image quality (1-100)

    Returns:
        Tuple of (success, output_path, error_message)
    """
    try:
        # Build prompt with style if specified
        prompt = slide['prompt']
        if 'style' in slide:
            style = slide['style']
            if style == 'professional':
                prompt = f"Professional presentation slide: {prompt}. Clean, minimal design with clear typography."
            elif style == 'data-viz':
                prompt = f"Data visualization slide: {prompt}. Clear charts and graphs, professional color scheme."
            elif style == 'infographic':
                prompt = f"Infographic style: {prompt}. Visual storytelling with icons and illustrations."
            elif style == 'trendlife':
                # TrendLife brand style with colors (logo added later via overlay)
                prompt = f"{prompt}\n\nUse TrendLife brand colors for Trend Micro presentations:\n- IMPORTANT: Title text and all headings MUST be in Trend Red (#D71920)\n- Primary accents and highlights: Trend Red (#D71920)\n- Guardian Red (#6F0000) for supporting elements and depth\n- Neutral palette: Dark gray (#57585B), medium gray (#808285), light gray (#E7E6E6)\n- Black (#000000) for body text, white (#FFFFFF) for backgrounds\nKeep the design clean, professional, and suitable for corporate presentations.\nDO NOT include any logos or brand text - these will be added separately."

        # Get aspect ratio from slide config (default to 16:9 for slides)
        aspect_ratio = slide.get('aspect_ratio', '16:9')

        # Generate image using Imagen API
        response = client.models.generate_images(
            model=model,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio=aspect_ratio
            )
        )

        # Save image
        if not response.generated_images:
            return False, None, "No image generated in response"

        image = response.generated_images[0].image

        # Save with appropriate format
        slide_num = slide['number']
        output_path = output_dir / f"slide-{slide_num:02d}.{output_format}"

        use_lossless = output_format == 'webp' and slide.get('style') in ['professional', 'data-viz', 'infographic', 'trendlife']

        # Convert to PIL Image
        pil_image = PILImage.open(io.BytesIO(image.image_bytes))

        if output_format == 'webp':
            pil_image.save(output_path, 'WEBP', quality=quality, lossless=use_lossless)
        elif output_format == 'png':
            pil_image.save(output_path, 'PNG', optimize=True)
        elif output_format in ['jpeg', 'jpg']:
            if pil_image.mode in ('RGBA', 'LA', 'P'):
                pil_image = pil_image.convert('RGB')
            pil_image.save(output_path, 'JPEG', quality=quality, optimize=True)
        else:
            return False, None, f"Unsupported format: {output_format}"

        # TrendLife Logo Overlay (MANDATORY for trendlife style)
        if slide.get('style') == 'trendlife':
            from logo_overlay import overlay_logo, detect_layout_type

            # Detect layout type from prompt
            layout_type = detect_layout_type(slide['prompt'], slide_number=slide['number'])

            # Logo path
            logo_path = Path(__file__).parent / 'assets/logos/trendlife-logo.png'

            # Create temporary path for overlay
            temp_output = output_path.with_stem(output_path.stem + '_with_logo')

            try:
                # Apply logo overlay
                overlay_logo(
                    background_path=output_path,
                    logo_path=logo_path,
                    output_path=temp_output,
                    layout_type=layout_type
                )

                # Replace original with logo version
                temp_output.replace(output_path)
            except Exception as e:
                # Log warning but don't fail the slide generation
                print(f"Warning: Logo overlay failed for slide {slide['number']}: {e}", file=sys.stderr)

        return True, str(output_path), None

    except Exception as e:
        return False, None, str(e)


def main():
    """Main batch generation entry point."""
    # Parse arguments
    if len(sys.argv) != 3 or sys.argv[1] != '--config':
        print("Usage: uv run generate_batch.py --config <config_file>", file=sys.stderr)
        sys.exit(1)

    config_path = sys.argv[2]

    # Load configuration
    config = load_config(config_path)

    # Extract parameters
    slides = config['slides']
    output_dir = Path(config['output_dir'])

    # Priority: environment variable > default
    # Config file no longer includes model field to prevent hallucinations
    model = os.environ.get("NANO_BANANA_MODEL") or "gemini-3-pro-image-preview"
    output_format = config.get('format', 'webp').lower()
    quality = config.get('quality', 90)

    # Create output directory
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error: Cannot create output directory: {e}", file=sys.stderr)
        sys.exit(1)

    # Initialize API client
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY or GOOGLE_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    base_url = os.environ.get("GOOGLE_GEMINI_BASE_URL")

    try:
        if base_url:
            client = genai.Client(api_key=api_key, http_options={'base_url': base_url})
        else:
            client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Error: Failed to initialize API client: {e}", file=sys.stderr)
        sys.exit(1)

    # Detect API type
    api_type = detect_api_type(model)

    # Initialize tracking
    started_at = datetime.now(UTC).isoformat() + 'Z'
    completed = []
    failed = []
    errors = []

    # Process each slide sequentially
    for i, slide in enumerate(slides):
        slide_num = slide['number']
        status = f"generating slide {slide_num}..."

        # Update progress before starting
        write_progress(i, len(slides), status, [c['path'] for c in completed], failed, started_at)

        # Generate slide
        if api_type == 'gemini':
            success, output_path, error = generate_slide_gemini(
                client, slide, output_dir, model, output_format, quality
            )
        else:  # imagen
            success, output_path, error = generate_slide_imagen(
                client, slide, output_dir, model, output_format, quality
            )

        # Track result
        if success:
            size_kb = Path(output_path).stat().st_size // 1024
            completed.append({
                "slide": slide_num,
                "path": output_path,
                "size_kb": size_kb
            })
            print(f"✓ Slide {slide_num} completed: {output_path}")
        else:
            failed.append(slide_num)
            errors.append({
                "slide": slide_num,
                "error": error or "Unknown error",
                "timestamp": datetime.now(UTC).isoformat() + 'Z'
            })
            print(f"✗ Slide {slide_num} failed: {error}", file=sys.stderr)

    # Final progress update
    write_progress(len(slides), len(slides), "completed", [c['path'] for c in completed], failed, started_at)

    # Write results
    write_results(completed, failed, errors, started_at)

    # Print summary
    print(f"\n{'='*60}")
    print(f"Batch generation completed")
    print(f"{'='*60}")
    print(f"Completed: {len(completed)}/{len(slides)}")
    print(f"Failed: {len(failed)}/{len(slides)}")
    if completed:
        print(f"\nOutput directory: {output_dir}")
    if errors:
        print(f"\nErrors:")
        for err in errors:
            print(f"  Slide {err['slide']}: {err['error']}")

    # Cleanup temp files
    try:
        PROGRESS_FILE.unlink(missing_ok=True)
        RESULTS_FILE.unlink(missing_ok=True)
    except Exception:
        pass  # Ignore cleanup errors

    # Exit with appropriate code
    # Exit 0 if at least some slides completed, 1 if all failed
    sys.exit(0 if completed else 1)


if __name__ == '__main__':
    main()
