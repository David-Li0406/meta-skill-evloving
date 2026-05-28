#!/usr/bin/env python3
"""
Nano-Banana PPT Slide Image Generator

This script generates presentation slide images using the Gemini Image Generation API
(Nano Banana Pro - gemini-3-pro-image-preview) from a JSON slide outline file.

Usage:
    python Generate_Slides.py <json_file> [--output-dir <directory>] [--slides <numbers>]

Examples:
    python Generate_Slides.py slides.json
    python Generate_Slides.py slides.json --output-dir ./output
    python Generate_Slides.py slides.json --slides 5          # Generate only slide 5
    python Generate_Slides.py slides.json --slides 5,7,9      # Generate slides 5, 7, and 9
    python Generate_Slides.py slides.json --slides 1-5        # Generate slides 1 through 5
"""

import argparse
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

# Enable real-time output (disable buffering)
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)


# Constants
MODEL = "gemini-3-pro-image-preview"  # Nano Banana Pro (highest quality)
ASPECT_RATIO = "16:9"
IMAGE_SIZE = "2K"
MAX_RETRIES = 10  # Reduced from 50 for faster failure detection
RETRY_DELAY_SECONDS = 5  # Delay for quota/rate limit errors
EMPTY_RESPONSE_RETRIES = 5  # Max retries for empty responses (sensitive content)
MAX_WORKERS = 20  # Maximum parallel threads
BATCH_SIZE = 20  # Process slides in batches to respect API rate limits
BATCH_DELAY_SECONDS = 30  # Wait between batches (Gemini API: 20 RPM)

# Default style guide for backward compatibility (used when JSON has no style_guide)
DEFAULT_STYLE_GUIDE = {
    "slide_prefix": "Create a professional presentation slide image",
    "layer4_specs": "16:9 aspect ratio, 1920x1080 resolution. All Korean text clearly readable.",
    "design_system": {
        "color_palette": {
            "background": "Light warm background (#F5F5DC)",
            "text": "#111111 dark text",
            "accent_primary": "#2D7D9A teal",
            "accent_secondary": "#E57373 coral",
            "sub": "#F0F0F0 light gray",
        },
        "typography": {
            "headings": "Bold sans-serif, large scale",
            "body": "Regular sans-serif, readable",
        },
        "layout": {
            "header": "Top 8% - left-aligned section title, sub color background, thin accent_primary line below",
            "content": "Middle 84%",
            "footer": "Bottom 8% - right-aligned page number, sub color background, thin accent_primary line above",
        },
        "mood": "Professional and clean",
        "illustration": "Modern illustration style with clear visual hierarchy",
    },
}


def build_final_prompt(slide_prompt: str, style_guide: dict, has_template: bool = False) -> str:
    """Build final prompt by prepending style guide as context.

    The nano_banana_prompt contains only slide content (title, text, visuals).
    This function prepends the design system context so the AI generates
    consistent visuals across all slides.

    Args:
        slide_prompt: The nano_banana_prompt containing slide content only.
        style_guide: Dictionary with design_system and technical specs.
        has_template: Whether a template image is provided as reference.

    Returns:
        Complete prompt with style context prepended to slide content.
    """
    ds = style_guide.get("design_system", {})
    cp = ds.get("color_palette", {})
    tp = ds.get("typography", {})
    ly = ds.get("layout", {})

    # Build template instruction if template is provided
    template_instruction = ""
    if has_template:
        template_instruction = """

CRITICAL - Template Reference:
The first reference image is the template (template.png).
You MUST maintain the EXACT header and footer layout from this template:
- Header bar: Same position, size, background color, and accent line
- Footer bar: Same position, size, background color, and accent line
- Header text style: Use the EXACT same font, size, and color as "[SECTION TITLE]" in the template
- Footer text style: Use the EXACT same font, size, and color as "[Page X/Y]" in the template
- Replace "[SECTION TITLE]" with the actual section title from the slide content
- Replace "[Page X/Y]" with the actual page number (e.g., "1/15")
- Content area: Fill with slide content while preserving template structure
DO NOT modify or reinterpret the template structure or text styles."""

    style_context = f"""{style_guide.get('slide_prefix', 'Create a professional presentation slide image')}.

Design System:
- Background: {cp.get('background', '')}
- Text color: {cp.get('text', '')}
- Accent primary: {cp.get('accent_primary', '')}
- Accent secondary: {cp.get('accent_secondary', '')}
- Sub color: {cp.get('sub', '')}
- Typography headings: {tp.get('headings', '')}
- Typography body: {tp.get('body', '')}
- Layout header: {ly.get('header', '')}
- Layout content: {ly.get('content', '')}
- Layout footer: {ly.get('footer', '')}
- Mood: {ds.get('mood', '')}
- Illustration style: {ds.get('illustration', '')}

Technical: {style_guide.get('layer4_specs', '')}{template_instruction}

Slide Content:"""

    return f"{style_context}\n{slide_prompt}"


class SlideGenerator:
    """Generates slide images using the Gemini Image Generation API."""

    def __init__(self, api_keys: list[str]):
        """Initialize the generator with API credentials.

        Args:
            api_keys: List of Google API keys for Gemini (for rotation on quota errors).
        """
        if not api_keys:
            raise ValueError("At least one API key is required")
        self.api_keys = api_keys
        self.current_key_index = 0
        self._local = threading.local()  # Thread-local storage for clients
        self._lock = threading.Lock()  # Lock for key index rotation
        self.model = MODEL
        print(f"[API Keys] Loaded {len(self.api_keys)} API key(s) for rotation")
        print(f"[Thread-Safe] Using thread-local clients for parallel processing")

    def _get_client(self) -> genai.Client:
        """Get the client for the current thread.

        Each thread gets its own client instance to avoid connection conflicts
        during parallel API key rotation.

        Returns:
            The Gemini client for this thread.
        """
        if not hasattr(self._local, 'client'):
            # Create a new client for this thread
            with self._lock:
                key_index = self.current_key_index
            self._local.client = genai.Client(api_key=self.api_keys[key_index])
            self._local.key_index = key_index
        return self._local.client

    def _rotate_api_key(self) -> bool:
        """Rotate to the next API key for the current thread.

        Returns:
            True if successfully rotated to a new key, False if all keys exhausted.
        """
        current_thread_index = getattr(self._local, 'key_index', 0)
        next_index = (current_thread_index + 1) % len(self.api_keys)

        # If we've cycled back to the first key, all keys are exhausted
        if next_index == 0 and current_thread_index != 0:
            return False

        # Update thread-local client with new key
        self._local.client = genai.Client(api_key=self.api_keys[next_index])
        self._local.key_index = next_index

        # Also update global index for new threads (with lock)
        with self._lock:
            self.current_key_index = next_index

        print(f"  [API Key Rotation] Thread switched to key {next_index + 1}/{len(self.api_keys)}")
        return True

    def _reset_api_key_cycle(self) -> None:
        """Reset API key cycle to start from the first key for the current thread."""
        self._local.client = genai.Client(api_key=self.api_keys[0])
        self._local.key_index = 0

        # Also reset global index (with lock)
        with self._lock:
            self.current_key_index = 0

        print(f"  [API Key Reset] Thread starting new cycle from key 1/{len(self.api_keys)}")

    def generate_slide_image(
        self, prompt: str, slide_number: int, reference_images: list[str] | None = None
    ) -> tuple[Any | None, str | None]:
        """Generate a single slide image from a prompt and optional reference images.

        Args:
            prompt: The text prompt for image generation.
            slide_number: The slide number (for logging).
            reference_images: Optional list of image file paths to use as reference.

        Returns:
            A tuple of (image, failure_reason).
            - If successful: (PIL Image, None)
            - If failed: (None, failure_reason_string)
        """
        empty_response_count = 0  # Track empty responses separately

        # Load reference images once before retry loop
        loaded_images: list[Image.Image] = []
        if reference_images:
            for img_path in reference_images:
                try:
                    img = Image.open(img_path)
                    loaded_images.append(img)
                    print(f"  [Reference Image] Loaded: {Path(img_path).name}")
                except Exception as e:
                    print(f"  [Warning] Failed to load reference image {img_path}: {e}")

        for attempt in range(MAX_RETRIES):
            try:
                if loaded_images:
                    print(f"  [Attempt {attempt + 1}/{MAX_RETRIES}] Generating image with {len(loaded_images)} reference(s)...")
                else:
                    print(f"  [Attempt {attempt + 1}/{MAX_RETRIES}] Generating image...")

                # Build contents: prompt first, then reference images
                contents: list[str | Image.Image] = [prompt]
                contents.extend(loaded_images)

                # Configure the request for Nano Banana Pro
                # Use TEXT+IMAGE modalities when reference images are provided
                response_modalities = ["TEXT", "IMAGE"] if loaded_images else ["IMAGE"]
                config = types.GenerateContentConfig(
                    response_modalities=response_modalities,
                    image_config=types.ImageConfig(
                        aspect_ratio=ASPECT_RATIO,
                        image_size=IMAGE_SIZE,
                    ),
                )

                # Use thread-local client
                client = self._get_client()
                response = client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=config,
                )

                # Check for empty response (common with sensitive content)
                if response.parts is None:
                    empty_response_count += 1

                    # Try to get detailed feedback from response
                    feedback_info = ""
                    if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                        feedback_info = f" | Feedback: {response.prompt_feedback}"
                    if hasattr(response, 'candidates') and response.candidates:
                        for candidate in response.candidates:
                            if hasattr(candidate, 'finish_reason'):
                                feedback_info += f" | Finish: {candidate.finish_reason}"
                            if hasattr(candidate, 'safety_ratings') and candidate.safety_ratings:
                                blocked = [r for r in candidate.safety_ratings if hasattr(r, 'blocked') and r.blocked]
                                if blocked:
                                    feedback_info += f" | Blocked by: {blocked}"

                    if empty_response_count >= EMPTY_RESPONSE_RETRIES:
                        print(f"  [Empty Response] Max retries ({EMPTY_RESPONSE_RETRIES}) reached")
                        reason = feedback_info.strip(" |") if feedback_info else "Unknown - API returned empty response"
                        print(f"  [Reason] {reason}")
                        print(f"  [Skipped] Slide {slide_number} skipped due to repeated empty responses")
                        return (None, reason)
                    print(f"  [Empty Response] ({empty_response_count}/{EMPTY_RESPONSE_RETRIES}){feedback_info}, retrying...")
                    time.sleep(3)
                    continue

                # Extract image from response
                for part in response.parts:
                    if part.inline_data is not None:
                        image = part.as_image()
                        return (image, None)  # Success

                print(f"  [Warning] No image generated for slide {slide_number}")
                return (None, "No image in response parts")

            except Exception as e:
                error_message = str(e)

                # Check for safety filter block
                if "blocked" in error_message.lower() or "safety" in error_message.lower():
                    print(f"  [Safety Filter] Slide {slide_number} blocked by safety filter")
                    print(f"    Error: {error_message[:200]}")
                    return (None, f"SAFETY_FILTER: {error_message[:200]}")

                # Check for rate limit or quota error
                if "rate" in error_message.lower() or "quota" in error_message.lower():
                    # Try rotating to next API key
                    if len(self.api_keys) > 1:
                        if self._rotate_api_key():
                            print(f"  [Quota/Rate Limit] Rotated API key, retrying immediately...")
                            continue
                        else:
                            # All keys exhausted, wait and reset cycle
                            print(f"  [All Keys Exhausted] Waiting {RETRY_DELAY_SECONDS}s before resetting cycle...")
                            time.sleep(RETRY_DELAY_SECONDS)
                            self._reset_api_key_cycle()
                            continue
                    else:
                        # Only one key, wait before retry
                        print(f"  [Rate Limit/Quota] Waiting {RETRY_DELAY_SECONDS} seconds before retry...")
                        time.sleep(RETRY_DELAY_SECONDS)
                        continue

                # Other errors - shorter retry delay
                if attempt < MAX_RETRIES - 1:
                    print(f"  [Error] {error_message[:200]}")
                    short_delay = 5  # 5 seconds for non-quota errors
                    print(f"  [Retry] Waiting {short_delay} seconds...")
                    time.sleep(short_delay)
                else:
                    print(f"  [Failed] Slide {slide_number} failed after {MAX_RETRIES} attempts")
                    print(f"    Error: {error_message[:300]}")
                    return (None, f"MAX_RETRIES_EXCEEDED: {error_message[:200]}")

        return (None, "Unknown error - all retries exhausted")


def parse_slide_numbers(slides_arg: str) -> set[int]:
    """Parse the --slides argument into a set of slide numbers.

    Supports formats:
        - Single number: "5"
        - Comma-separated: "5,7,9"
        - Range: "1-5"
        - Mixed: "1-3,5,7-9"

    Args:
        slides_arg: The raw --slides argument string.

    Returns:
        A set of slide numbers to generate.
    """
    result: set[int] = set()

    for part in slides_arg.split(","):
        part = part.strip()
        if "-" in part:
            # Range format: "1-5"
            start, end = part.split("-", 1)
            try:
                start_num = int(start.strip())
                end_num = int(end.strip())
                result.update(range(start_num, end_num + 1))
            except ValueError:
                print(f"Warning: Invalid range '{part}', skipping...")
        else:
            # Single number
            try:
                result.add(int(part))
            except ValueError:
                print(f"Warning: Invalid slide number '{part}', skipping...")

    return result


def load_slides_json(json_path: str) -> dict[str, Any]:
    """Load and parse the slides JSON file.

    Args:
        json_path: Path to the JSON file.

    Returns:
        The parsed JSON data.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def create_output_directory(json_path: str, output_dir: str | None = None) -> Path:
    """Create the output directory for generated images.

    Args:
        json_path: Path to the input JSON file.
        output_dir: Optional custom output directory.

    Returns:
        The Path object for the output directory.
    """
    if output_dir:
        output_path = Path(output_dir)
    else:
        # Create directory based on JSON filename
        json_name = Path(json_path).stem
        output_path = Path(json_path).parent / f"{json_name}_images"

    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def generate_single_slide(
    generator: SlideGenerator,
    slide: dict[str, Any],
    index: int,
    total_slides: int,
    output_dir: Path,
    global_reference_images: list[str] | None = None,
    style_guide: dict[str, str] | None = None,
    has_template: bool = False,
) -> tuple[int, bool, str, str | None, str | None]:
    """Generate a single slide image (for parallel execution).

    Args:
        generator: The SlideGenerator instance.
        slide: The slide data dictionary.
        index: The slide index (0-based).
        total_slides: Total number of slides.
        output_dir: The output directory for images.
        global_reference_images: Optional list of global reference image paths.
        style_guide: Optional style guide dict with design_system for context prepending.
        has_template: Whether a template image is provided as the first reference.

    Returns:
        A tuple of (page_number, success, message, failure_reason, title).
        - failure_reason is None if successful
        - title is included for error reporting
    """
    page = slide.get("page", index + 1)
    title = slide.get("title", f"Slide {page}")
    prompt = slide.get("nano_banana_prompt", "")

    # Build final prompt by prepending style guide context (use DEFAULT_STYLE_GUIDE if none provided)
    effective_style = style_guide if style_guide else DEFAULT_STYLE_GUIDE
    prompt = build_final_prompt(prompt, effective_style, has_template)

    if not prompt:
        return (page, False, f"[Slide {page:02d}] Skipped - No prompt found", "NO_PROMPT", title)

    # Collect reference images: slide-specific first, then global
    reference_images: list[str] = []
    slide_refs = slide.get("reference_images", [])
    if slide_refs:
        reference_images.extend(slide_refs)
    if global_reference_images:
        reference_images.extend(global_reference_images)

    ref_info = f" (refs: {len(reference_images)})" if reference_images else ""
    print(f"[Slide {page:02d}/{total_slides}] {title}{ref_info} - Starting...")

    image, failure_reason = generator.generate_slide_image(
        prompt, page, reference_images if reference_images else None
    )

    if image is not None:
        # Save the image
        filename = f"slide_{page:03d}.png"
        filepath = output_dir / filename
        image.save(str(filepath))
        return (page, True, f"[Slide {page:02d}] Success - Saved to {filename}", None, title)
    else:
        return (page, False, f"[Slide {page:02d}] Failed - Could not generate image", failure_reason, title)


def generate_all_slides(
    generator: SlideGenerator,
    slides_data: dict[str, Any],
    output_dir: Path,
    target_slides: set[int] | None = None,
    template_path: Path | None = None,
) -> tuple[int, int, list[int], float, list[dict[str, Any]]]:
    """Generate images for all slides in parallel.

    Args:
        generator: The SlideGenerator instance.
        slides_data: The parsed slides JSON data.
        output_dir: The output directory for images.
        target_slides: Optional set of specific slide numbers to generate.
                       If None, all slides are generated.
        template_path: Optional path to template image. If provided, it will be
                       prepended to global_reference_images for consistent styling.

    Returns:
        A tuple of (success_count, failure_count, failed_slide_numbers, elapsed_time, failure_details).
        failure_details is a list of dicts with {page, title, reason} for each failed slide.
    """
    all_slides = slides_data.get("slides", [])

    # Extract style_guide for design_system context prepending (None = use defaults)
    style_guide = slides_data.get("style_guide", None)
    if style_guide:
        print(f"[Style Guide] Using custom style_guide from JSON")
        ds = style_guide.get("design_system", {})
        if ds:
            cp = ds.get("color_palette", {})
            print(f"  - design_system.color_palette: {len(cp)} colors")
            print(f"    background: {cp.get('background', 'N/A')}")
            print(f"    accent_primary: {cp.get('accent_primary', 'N/A')}")
            print(f"  - design_system.mood: {ds.get('mood', 'N/A')}")
            print(f"  - design_system.illustration: {ds.get('illustration', 'N/A')[:50]}...")
        print(f"  - layer4_specs: {style_guide.get('layer4_specs', 'N/A')[:50]}...")
    else:
        print(f"[Style Guide] Using DEFAULT_STYLE_GUIDE (no style_guide in JSON)")

    # Extract global reference images (applied to all slides)
    # Note: style_guide.reference_images is NOT used (v8.1 change - text-based style guide preferred)
    global_reference_images = slides_data.get("reference_images", [])

    # Prepend template image to global_reference_images if provided
    has_template = template_path is not None and template_path.exists()
    if has_template:
        global_reference_images = [str(template_path)] + global_reference_images
        print(f"[Template] Using template image: {template_path}")

    if global_reference_images:
        print(f"[Global Reference] Found {len(global_reference_images)} global reference image(s)")

    # Filter slides if target_slides is specified
    if target_slides:
        slides = [
            slide for slide in all_slides
            if slide.get("page", all_slides.index(slide) + 1) in target_slides
        ]
        print(f"\n[Filter] Targeting specific slides: {sorted(target_slides)}")
        print(f"[Filter] Found {len(slides)} matching slides out of {len(all_slides)} total")
    else:
        slides = all_slides
    total_slides = len(slides)
    success_count = 0
    failure_count = 0
    failed_slides: list[int] = []
    failure_details: list[dict[str, Any]] = []  # Detailed failure info

    # Split slides into batches to respect API rate limits
    batches = [slides[i:i+BATCH_SIZE] for i in range(0, total_slides, BATCH_SIZE)]
    total_batches = len(batches)

    print(f"\n{'=' * 60}")
    print(f"Starting BATCHED PARALLEL image generation")
    print(f"Total slides: {total_slides}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Total batches: {total_batches}")
    print(f"Batch delay: {BATCH_DELAY_SECONDS} seconds")
    print(f"Output directory: {output_dir}")
    print(f"Model: {generator.model}")
    print(f"Max workers: {MAX_WORKERS}")
    print(f"Max retries: {MAX_RETRIES}")
    print(f"Retry delay: {RETRY_DELAY_SECONDS} seconds")
    print(f"{'=' * 60}\n")

    start_time = time.time()

    # Process each batch sequentially
    for batch_num, batch in enumerate(batches, 1):
        batch_start_time = time.time()
        batch_size = len(batch)

        print(f"\n{'=' * 60}")
        print(f"BATCH {batch_num}/{total_batches}: Processing {batch_size} slides")
        print(f"{'=' * 60}\n")

        # Use ThreadPoolExecutor for parallel execution within this batch
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Submit tasks for this batch only
            future_to_slide = {
                executor.submit(
                    generate_single_slide,
                    generator,
                    slide,
                    i,
                    total_slides,
                    output_dir,
                    global_reference_images if global_reference_images else None,
                    style_guide,  # Pass style_guide for {{variable}} substitution
                    has_template,  # Pass template flag for explicit instruction
                ): slide
                for i, slide in enumerate(batch, start=(batch_num-1)*BATCH_SIZE)
            }

            # Process completed tasks as they finish
            for future in as_completed(future_to_slide):
                try:
                    page, success, message, failure_reason, title = future.result()
                    print(message)

                    if success:
                        success_count += 1
                    else:
                        failure_count += 1
                        failed_slides.append(page)
                        failure_details.append({
                            "page": page,
                            "title": title,
                            "reason": failure_reason
                        })

                except Exception as e:
                    slide = future_to_slide[future]
                    page = slide.get("page", "?")
                    title = slide.get("title", f"Slide {page}")
                    print(f"[Slide {page}] Exception: {e}")
                    failure_count += 1
                    if isinstance(page, int):
                        failed_slides.append(page)
                        failure_details.append({
                            "page": page,
                            "title": title,
                            "reason": f"EXCEPTION: {str(e)[:200]}"
                        })

        batch_elapsed = time.time() - batch_start_time
        print(f"\n[Batch {batch_num}] Completed in {batch_elapsed:.1f} seconds")
        print(f"[Batch {batch_num}] Success: {success_count}, Failed: {failure_count}")

        # Wait before next batch (except for last batch)
        if batch_num < total_batches:
            print(f"\n[Wait] Pausing {BATCH_DELAY_SECONDS} seconds before next batch...")
            print(f"[Wait] This prevents API rate limit (Gemini: 20 RPM)")
            time.sleep(BATCH_DELAY_SECONDS)
            print(f"[Wait] Resuming batch {batch_num + 1}/{total_batches}...\n")

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Sort failed slides for consistent output
    failed_slides.sort()
    failure_details.sort(key=lambda x: x["page"])

    return success_count, failure_count, failed_slides, elapsed_time, failure_details


def print_summary(
    success_count: int,
    failure_count: int,
    failed_slides: list[int],
    elapsed_time: float,
    output_dir: Path,
) -> None:
    """Print a summary of the generation process.

    Args:
        success_count: Number of successfully generated images.
        failure_count: Number of failed generations.
        failed_slides: List of slide numbers that failed.
        elapsed_time: Total time taken in seconds.
        output_dir: The output directory.
    """
    total = success_count + failure_count
    print(f"\n{'=' * 60}")
    print("Generation Complete!")
    print(f"{'=' * 60}")
    print(f"Total slides processed: {total}")
    print(f"Successful: {success_count}")
    print(f"Failed: {failure_count}")
    print(f"Total time: {elapsed_time:.1f} seconds")
    if total > 0:
        print(f"Average time per slide: {elapsed_time / total:.1f} seconds")
    print(f"Output directory: {output_dir}")

    if failed_slides:
        print(f"\nFailed slides: {failed_slides}")

    print(f"{'=' * 60}\n")


def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Generate PPT slide images using Nano-Banana Pro (gemini-3-pro-image-preview)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python Generate_Slides.py slides.json
    python Generate_Slides.py slides.json --output-dir ./output
    python Generate_Slides.py slides.json --slides 5          # Generate only slide 5
    python Generate_Slides.py slides.json --slides 5,7,9      # Generate slides 5, 7, and 9
    python Generate_Slides.py slides.json --slides 1-5        # Generate slides 1 through 5
    python Generate_Slides.py slides.json --slides 1-3,5,7-9  # Mixed format
        """,
    )
    parser.add_argument(
        "json_file",
        help="Path to the JSON file containing slide outlines",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        help="Output directory for generated images (default: based on JSON filename)",
    )
    parser.add_argument(
        "--env-file",
        "-e",
        default=None,
        help="Path to .env file containing GOOGLE_API_KEY",
    )
    parser.add_argument(
        "--slides",
        "-s",
        default=None,
        help="Specific slide numbers to generate (e.g., '5', '5,7,9', '1-5', '1-3,5,7-9')",
    )
    parser.add_argument(
        "--template",
        "-t",
        default=None,
        help="Path to template image to use as reference for all slides (auto-detects template.png in JSON directory if not specified)",
    )

    args = parser.parse_args()

    # Validate input file
    if not os.path.exists(args.json_file):
        print(f"Error: JSON file not found: {args.json_file}")
        sys.exit(1)

    # Load environment variables
    env_file = args.env_file
    if env_file is None:
        # Try to find .env in same directory as JSON file or current directory
        json_dir = Path(args.json_file).parent
        possible_env_paths = [
            json_dir / ".env",
            Path.cwd() / ".env",
            Path(__file__).parent / ".env",
        ]
        for env_path in possible_env_paths:
            if env_path.exists():
                env_file = str(env_path)
                break

    if env_file:
        load_dotenv(env_file)
        print(f"Loaded environment from: {env_file}")

    # Get API keys (support both GOOGLE_API_KEYS and GOOGLE_API_KEY)
    api_keys_str = os.getenv("GOOGLE_API_KEYS")
    api_keys: list[str] = []

    if api_keys_str:
        # Parse comma-separated keys
        api_keys = [key.strip() for key in api_keys_str.split(",") if key.strip()]
        print(f"[Config] Found {len(api_keys)} API keys in GOOGLE_API_KEYS")
    else:
        # Fallback to single key
        single_key = os.getenv("GOOGLE_API_KEY")
        if single_key:
            api_keys = [single_key.strip()]
            print("[Config] Using single API key from GOOGLE_API_KEY")

    if not api_keys:
        print("Error: No API keys found in environment variables")
        print("Please set GOOGLE_API_KEYS (comma-separated) or GOOGLE_API_KEY in your .env file")
        sys.exit(1)

    # Load slides data
    try:
        slides_data = load_slides_json(args.json_file)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        sys.exit(1)

    # Create output directory
    output_dir = create_output_directory(args.json_file, args.output_dir)

    # Parse target slides if specified
    target_slides: set[int] | None = None
    if args.slides:
        target_slides = parse_slide_numbers(args.slides)
        if not target_slides:
            print("Error: No valid slide numbers found in --slides argument")
            sys.exit(1)
        print(f"Target slides: {sorted(target_slides)}")

    # Determine template path (explicit argument or auto-detect)
    template_path: Path | None = None
    if args.template:
        template_path = Path(args.template)
        if not template_path.exists():
            print(f"Warning: Template file not found: {template_path}")
            template_path = None
    else:
        # Auto-detect template.png in JSON directory
        auto_template = Path(args.json_file).parent / "template.png"
        if auto_template.exists():
            template_path = auto_template
            print(f"[Auto-detect] Found template image: {template_path}")

    # Initialize generator with API key rotation support
    generator = SlideGenerator(api_keys=api_keys)

    # Generate all slides (or specific slides if target_slides is set)
    success_count, failure_count, failed_slides, elapsed_time, failure_details = generate_all_slides(
        generator=generator,
        slides_data=slides_data,
        output_dir=output_dir,
        target_slides=target_slides,
        template_path=template_path,
    )

    # Print summary
    print_summary(
        success_count=success_count,
        failure_count=failure_count,
        failed_slides=failed_slides,
        elapsed_time=elapsed_time,
        output_dir=output_dir,
    )

    # Save failure details to JSON file if there are failures
    if failure_details:
        failure_report = {
            "source_json": args.json_file,
            "output_dir": str(output_dir),
            "total_processed": success_count + failure_count,
            "success_count": success_count,
            "failure_count": failure_count,
            "failed_slides": failure_details
        }
        failure_json_path = output_dir / "FAILURES.json"
        with open(failure_json_path, "w", encoding="utf-8") as f:
            json.dump(failure_report, f, ensure_ascii=False, indent=2)
        print(f"\n[Failure Report] Saved to: {failure_json_path}")

        # Also print JSON to stdout for easy parsing by commands
        print("\n--- FAILURE_REPORT_JSON_START ---")
        print(json.dumps(failure_report, ensure_ascii=False))
        print("--- FAILURE_REPORT_JSON_END ---")

    # Return exit code based on success
    if failure_count > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
