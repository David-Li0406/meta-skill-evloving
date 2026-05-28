"""Generate animated transitions between slides using Kling O1 Reference-to-Video.

Uses start and end frame images to create true morphing transitions where
graphics transform exactly from one slide to the next.
"""

import os

import fal_client
import requests

from .utils import get_fal_key, api_call_with_retry


# Critical frame requirements prefix/suffix for all prompts
FRAME_REQUIREMENT_PREFIX = (
    "CRITICAL REQUIREMENTS: The very first frame of this video MUST be visually "
    "identical to @Image1. The very last frame MUST be visually identical to @Image2. "
)
FRAME_REQUIREMENT_SUFFIX = (
    " Ensure frame 1 is exactly @Image1 and the final frame is exactly @Image2."
)

# Default transition prompt template using @Image1 (start) and @Image2 (end)
DEFAULT_TRANSITION_PROMPT = (
    FRAME_REQUIREMENT_PREFIX +
    "Starting from @Image1, smoothly morph and transform all elements into @Image2. "
    "The graphics, text, and icons should fluidly animate and reshape themselves, "
    "transitioning seamlessly from the first composition to the second. "
    "Maintain a professional, elegant motion with smooth morphing effects." +
    FRAME_REQUIREMENT_SUFFIX
)

# Available transition styles - these now describe HOW to morph between frames
# All styles include the critical frame requirements prefix and suffix
TRANSITION_STYLES = {
    "morph": (
        FRAME_REQUIREMENT_PREFIX +
        "Starting from @Image1, organically morph all graphics into @Image2. "
        "Line-art icons flow and reshape like ink in water, text elements dissolve "
        "and reform into the new positions, colors blend smoothly. The transformation "
        "should feel fluid and natural." +
        FRAME_REQUIREMENT_SUFFIX
    ),
    "cinematic": (
        FRAME_REQUIREMENT_PREFIX +
        "Starting from @Image1, elegantly transition to @Image2 with cinematic flair. "
        "Graphics gracefully dissolve with subtle light particles, elements morph "
        "and flow with smooth motion." +
        FRAME_REQUIREMENT_SUFFIX
    ),
    "zoom_blur": (
        FRAME_REQUIREMENT_PREFIX +
        "Starting from @Image1, rush toward @Image2 with dynamic motion blur. "
        "Graphics stretch and morph as they zoom, transforming mid-flight into "
        "the elements of @Image2." +
        FRAME_REQUIREMENT_SUFFIX
    ),
    "swipe": (
        FRAME_REQUIREMENT_PREFIX +
        "Starting from @Image1, smoothly swipe and morph into @Image2. "
        "Elements slide with 3D parallax depth while transforming shape, "
        "converging into the layout of @Image2." +
        FRAME_REQUIREMENT_SUFFIX
    ),
    "particles": (
        FRAME_REQUIREMENT_PREFIX +
        "Starting from @Image1, dissolve graphics into glowing particles that "
        "swirl and reform into @Image2. Icons break into dots that dance and "
        "coalesce into the new shapes." +
        FRAME_REQUIREMENT_SUFFIX
    ),
    "wave": (
        FRAME_REQUIREMENT_PREFIX +
        "Starting from @Image1, ripple and morph into @Image2. Wave effects "
        "distort and reshape the graphics, flowing and settling into the "
        "composition of @Image2." +
        FRAME_REQUIREMENT_SUFFIX
    ),
}

DEFAULT_STYLE = "morph"


def apply_frame_requirements(prompt: str) -> str:
    """Apply frame requirement prefix/suffix to a custom prompt if not already present.

    Ensures custom prompts also enforce first/last frame matching.

    Args:
        prompt: The original prompt.

    Returns:
        Prompt with frame requirements added if not already present.
    """
    has_prefix = "CRITICAL REQUIREMENTS" in prompt or "first frame" in prompt.lower()
    has_suffix = "final frame is exactly" in prompt.lower()

    if has_prefix and has_suffix:
        return prompt

    result = prompt
    if not has_prefix:
        result = FRAME_REQUIREMENT_PREFIX + result
    if not has_suffix:
        result = result + FRAME_REQUIREMENT_SUFFIX

    return result


def _init_fal():
    """Initialize fal client with API key."""
    os.environ["FAL_KEY"] = get_fal_key()


def generate_transition(
    from_slide_path: str,
    to_slide_path: str,
    transition_number: int,
    output_dir: str = "./transitions",
    transition_style: str = "morph",
    custom_prompt: str = None
) -> str:
    """Generate an animated transition morphing from one slide to another.

    Uses Kling O1 Reference-to-Video to create true start-to-end frame transitions
    where @Image1 (start slide) morphs exactly into @Image2 (end slide).

    Args:
        from_slide_path: Path to the starting slide image (@Image1).
        to_slide_path: Path to the destination slide image (@Image2).
        transition_number: Transition number for filename.
        output_dir: Directory to save transition videos.
        transition_style: Style of morphing animation (used if no custom_prompt).
        custom_prompt: Custom animation prompt (should reference @Image1 and @Image2).

    Returns:
        Path to the generated transition video.
    """
    _init_fal()

    # Upload both slides
    print(f"    Uploading start frame: {os.path.basename(from_slide_path)}")
    with open(from_slide_path, "rb") as f:
        from_url = fal_client.upload(f.read(), "image/png")

    print(f"    Uploading end frame: {os.path.basename(to_slide_path)}")
    with open(to_slide_path, "rb") as f:
        to_url = fal_client.upload(f.read(), "image/png")

    # Determine prompt
    if custom_prompt:
        # Apply frame requirements to custom prompts
        prompt = apply_frame_requirements(custom_prompt)
    else:
        if transition_style not in TRANSITION_STYLES:
            print(f"Warning: Style '{transition_style}' not recognized. Using '{DEFAULT_STYLE}'.")
            transition_style = DEFAULT_STYLE
        prompt = TRANSITION_STYLES[transition_style]

    def _generate():
        return fal_client.subscribe(
            "fal-ai/kling-video/o1/standard/reference-to-video",
            arguments={
                "prompt": prompt,
                "image_urls": [from_url, to_url],  # @Image1 and @Image2
                "duration": "5",
                "aspect_ratio": "16:9",
            },
        )

    print(f"    Generating morph transition...")
    result = api_call_with_retry(_generate)

    video_url = result["video"]["url"]

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"transition_{transition_number:02d}.mp4")

    response = requests.get(video_url)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path


def generate_transitions_batch(
    slide_images: list[str],
    output_dir: str = "./transitions",
    transition_style: str = "morph",
    custom_prompts: list[str] = None
) -> list[str]:
    """Generate transitions between all slides (n-1 transitions for n slides).

    Each transition morphs from slide[i] to slide[i+1] using both images
    as reference frames.

    Args:
        slide_images: List of paths to slide images.
        output_dir: Directory to save transition videos.
        transition_style: Style of morphing animation (fallback if no custom prompt).
        custom_prompts: Optional list of custom prompts for each transition.
                       Length should be len(slide_images) - 1.
                       Prompts should reference @Image1 (start) and @Image2 (end).

    Returns:
        List of paths to generated transition videos.
    """
    paths = []
    total = len(slide_images) - 1

    if total < 1:
        print("Warning: Need at least 2 slides to generate transitions.")
        return paths

    for i in range(total):
        # Get custom prompt for this transition if available
        custom_prompt = None
        if custom_prompts and i < len(custom_prompts):
            custom_prompt = custom_prompts[i]

        print(f"Generating transition {i + 1}/{total}: Slide {i + 1} -> Slide {i + 2}")
        if custom_prompt:
            print(f"  Using custom animation prompt")

        path = generate_transition(
            from_slide_path=slide_images[i],
            to_slide_path=slide_images[i + 1],
            transition_number=i + 1,
            output_dir=output_dir,
            transition_style=transition_style,
            custom_prompt=custom_prompt,
        )
        paths.append(path)
        print(f"  Saved: {path}")

    return paths


def list_transition_styles() -> dict[str, str]:
    """Get available transition styles and their descriptions.

    Returns:
        Dictionary mapping style names to descriptions.
    """
    return TRANSITION_STYLES.copy()
