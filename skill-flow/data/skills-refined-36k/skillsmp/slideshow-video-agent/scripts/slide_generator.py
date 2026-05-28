"""Generate presentation slides using Nano Banana Pro via fal.ai.

Supports both text-only and text + reference images for brand consistency.
"""

import os
from pathlib import Path
from typing import Optional

import fal_client
import requests

from .utils import get_fal_key, api_call_with_retry


# Ensure FAL_KEY is set
def _init_fal():
    """Initialize fal client with API key."""
    os.environ["FAL_KEY"] = get_fal_key()


def upload_reference_images(image_paths: list[str]) -> list[str]:
    """Upload local reference images to fal.ai storage.

    Args:
        image_paths: List of local file paths to reference images.

    Returns:
        List of fal.ai URLs for the uploaded images.
    """
    _init_fal()
    urls = []

    for path in image_paths:
        path_obj = Path(path)
        if not path_obj.exists():
            print(f"Warning: Reference image not found: {path}")
            continue

        with open(path, "rb") as f:
            # Determine mime type
            ext = path_obj.suffix.lower().lstrip(".")
            mime_types = {
                "png": "image/png",
                "jpg": "image/jpeg",
                "jpeg": "image/jpeg",
                "webp": "image/webp",
            }
            mime_type = mime_types.get(ext, "image/png")

            url = fal_client.upload(f.read(), mime_type)
            urls.append(url)
            print(f"  Uploaded: {path_obj.name}")

    return urls


def generate_slide(
    title: str,
    visual_description: str,
    slide_number: int,
    output_dir: str = "./slides",
    reference_images: Optional[list[str]] = None,
    reference_urls: Optional[list[str]] = None,
    bullet_points: Optional[list[str]] = None,
    is_title_slide: bool = False
) -> str:
    """Generate a static presentation slide image with minimal text design.

    Design principles:
    - Navy blue and white color scheme (from COP Logo)
    - Short title at top
    - 3-4 bullet points max (3-6 words each)
    - Single line-art icon on right side
    - NO photorealistic images, only graphics

    Can use EITHER:
    - Text prompt only (basic generation)
    - Text prompt + reference images (brand-consistent generation)

    Args:
        title: The slide title text.
        visual_description: Detailed description of slide visuals/graphics.
        slide_number: Slide number for filename.
        output_dir: Directory to save slide images.
        reference_images: Local paths to reference images (logos, colors, etc.).
        reference_urls: URLs of reference images (if already hosted).
        bullet_points: Optional list of brief bullet points to display (3-4 max).
        is_title_slide: If True, include the logo prominently.

    Returns:
        Path to the generated slide image.
    """
    _init_fal()

    # Format bullet points for prompt
    bullet_text = ""
    if bullet_points:
        bullets = "\n".join(f"  * {bp}" for bp in bullet_points[:4])  # Max 4
        bullet_text = f"""
- Bullet points (display these EXACTLY as shown, keep them SHORT):
{bullets}"""

    # Build different prompts for title slide vs content slides
    if is_title_slide:
        prompt = f"""Create a professional TITLE slide for a presentation:

LAYOUT:
- Clean white or light gray background
- The provided logo image should be displayed PROMINENTLY and CENTERED
- Title "{title}" below the logo in navy blue text
{bullet_text}

CRITICAL STYLE REQUIREMENTS:
- Navy blue (#1E3A5F) and white color scheme
- Professional, clean corporate design
- The logo should be the main focal point
- Aspect ratio: 16:9 widescreen format
- ALL text must be perfectly legible and correctly spelled
- NO photorealistic images - clean graphics only"""
    else:
        prompt = f"""Create a professional presentation slide with MINIMAL TEXT design:

LAYOUT:
- Clean white or light gray background with navy blue accents
- Title "{title}" at top in large, navy blue text
{bullet_text}
- Single LINE-ART icon on the right side representing: {visual_description}

CRITICAL STYLE REQUIREMENTS:
- Navy blue (#1E3A5F) and white color scheme
- Use ONLY simple line-art graphics (like hand-drawn icons)
- NO photorealistic images or photos
- NO complex illustrations
- Keep text MINIMAL - just title and brief bullet points
- Bullet points must be SHORT (3-6 words each)
- Graphics should be clean, simple navy blue line-art symbols
- Aspect ratio: 16:9 widescreen format
- ALL text must be perfectly legible and correctly spelled
- Match the style from reference images if provided

This should look like a clean, modern corporate slide with minimal text and a simple graphic icon."""

    # Determine which endpoint to use
    has_references = bool(reference_images or reference_urls)

    if has_references:
        # Use the edit endpoint with reference images
        image_urls = list(reference_urls or [])

        # Upload local images if provided
        if reference_images:
            uploaded_urls = upload_reference_images(reference_images)
            image_urls.extend(uploaded_urls)

        if not image_urls:
            print("Warning: No valid reference images found, using text-only generation")
            has_references = False

    if has_references:
        def _generate_with_refs():
            return fal_client.subscribe(
                "fal-ai/nano-banana-pro/edit",
                arguments={
                    "prompt": prompt,
                    "image_urls": image_urls,
                    "num_images": 1,
                    "aspect_ratio": "16:9",
                    "output_format": "png",
                },
            )

        result = api_call_with_retry(_generate_with_refs)
    else:
        def _generate_text_only():
            return fal_client.subscribe(
                "fal-ai/nano-banana-pro",
                arguments={
                    "prompt": prompt,
                    "num_images": 1,
                    "aspect_ratio": "16:9",
                    "output_format": "png",
                },
            )

        result = api_call_with_retry(_generate_text_only)

    # Download the generated image
    image_url = result["images"][0]["url"]

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"slide_{slide_number:02d}.png")

    response = requests.get(image_url)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path


def generate_slide_batch(
    slides: list[dict],
    output_dir: str = "./slides",
    reference_images: Optional[list[str]] = None,
    reference_urls: Optional[list[str]] = None
) -> list[str]:
    """Generate multiple slides, all using the same reference images for consistency.

    Args:
        slides: List of dicts with 'title' and 'visual_description'.
        output_dir: Directory to save slides.
        reference_images: Local paths to reference images (applied to ALL slides).
        reference_urls: URLs of reference images (applied to ALL slides).

    Returns:
        List of paths to generated slide images.
    """
    _init_fal()

    # Upload reference images once (reuse URLs for all slides)
    uploaded_urls = []
    if reference_images:
        print("Uploading reference images...")
        uploaded_urls = upload_reference_images(reference_images)

    all_refs = (reference_urls or []) + uploaded_urls

    paths = []
    total = len(slides)

    for i, slide in enumerate(slides, 1):
        print(f"Generating slide {i}/{total}: {slide['title']}")

        path = generate_slide(
            title=slide["title"],
            visual_description=slide.get("visual_description", ""),
            slide_number=i,
            output_dir=output_dir,
            reference_urls=all_refs if all_refs else None,
            bullet_points=slide.get("bullet_points"),
            is_title_slide=slide.get("is_title_slide", i == 1),
        )
        paths.append(path)
        print(f"  Saved: {path}")

    return paths


def generate_slide_batch_with_validation(
    slides: list[dict],
    output_dir: str = "./slides",
    reference_images: Optional[list[str]] = None,
    reference_urls: Optional[list[str]] = None,
    validate: bool = True,
    max_validation_attempts: int = 3,
) -> list[str]:
    """Generate multiple slides with AI validation.

    Uses Claude Haiku 4.5 to validate each slide for text quality and
    graphics clarity. Regenerates slides that fail validation.

    Args:
        slides: List of dicts with 'title', 'bullet_points', 'visual_description'.
        output_dir: Directory to save slides.
        reference_images: Local paths to reference images.
        reference_urls: URLs of reference images.
        validate: Whether to validate slides with Claude.
        max_validation_attempts: Max regeneration attempts per slide.

    Returns:
        List of paths to generated slide images.
    """
    _init_fal()

    # Upload reference images once
    uploaded_urls = []
    if reference_images:
        print("Uploading reference images...")
        uploaded_urls = upload_reference_images(reference_images)

    all_refs = (reference_urls or []) + uploaded_urls

    paths = []
    total = len(slides)

    for i, slide in enumerate(slides, 1):
        print(f"Generating slide {i}/{total}: {slide['title']}")

        if validate:
            from .image_validator import validate_slide_with_retry

            def gen_func():
                return generate_slide(
                    title=slide["title"],
                    visual_description=slide.get("visual_description", ""),
                    slide_number=i,
                    output_dir=output_dir,
                    reference_urls=all_refs if all_refs else None,
                    bullet_points=slide.get("bullet_points"),
                    is_title_slide=slide.get("is_title_slide", i == 1),
                )

            path, result = validate_slide_with_retry(
                generate_func=gen_func,
                expected_title=slide["title"],
                expected_bullet_points=slide.get("bullet_points"),
                max_attempts=max_validation_attempts,
            )
        else:
            path = generate_slide(
                title=slide["title"],
                visual_description=slide.get("visual_description", ""),
                slide_number=i,
                output_dir=output_dir,
                reference_urls=all_refs if all_refs else None,
                bullet_points=slide.get("bullet_points"),
                is_title_slide=slide.get("is_title_slide", i == 1),
            )

        paths.append(path)
        print(f"  Saved: {path}")

    return paths
