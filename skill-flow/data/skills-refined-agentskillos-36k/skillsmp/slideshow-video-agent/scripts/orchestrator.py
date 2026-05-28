"""Main orchestrator for slideshow video generation."""

import os
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .slide_generator import generate_slide_batch, generate_slide_batch_with_validation
from .voiceover import (
    generate_voiceover_batch,
    generate_combined_voiceover,
    generate_narrations_with_timing,
    concatenate_with_gaps,
    VOICES,
    is_valid_voice,
)
from .transition_generator import generate_transitions_batch, TRANSITION_STYLES
from .transition_validator import (
    validate_transition,
    validate_transitions_batch,
    TransitionValidationResult,
)
from .video_assembler import (
    assemble_slideshow,
    assemble_slideshow_with_single_audio,
    assemble_slideshow_narration_driven,
    add_audio_to_video,
    get_duration,
)
from .utils import (
    ensure_output_dirs,
    get_project_root,
    list_reference_images,
    validate_prerequisites,
)


@dataclass
class Slide:
    """Configuration for a single slide.

    Slides have two types of text content:
    - bullet_points: Brief summaries shown ON the slide (3-4 items, 3-6 words each)
    - narration: Fuller script spoken in voiceover (more detailed than slide text)

    The visual_description describes the graphic style (line-art icons, not photos).
    The transition_prompt describes how THIS slide animates into the NEXT slide.
    """

    title: str
    bullet_points: list[str]  # Brief text shown on slide (3-4 items max)
    narration: str            # Fuller script for voiceover
    visual_description: str   # Graphic/icon description (line-art style)
    is_title_slide: bool = False  # If True, display logo prominently
    transition_prompt: Optional[str] = None  # Custom animation for transition to next slide


@dataclass
class PresentationConfig:
    """Configuration for the entire presentation."""

    slides: list[Slide]
    output_path: str = "./output/presentation.mp4"
    voice: str = "George"
    transition_style: str = "cinematic"

    # Reference images for brand consistency
    reference_images: list[str] = field(default_factory=list)  # Local paths
    reference_urls: list[str] = field(default_factory=list)  # URLs

    # Slide validation options
    validate_slides: bool = True  # Use Claude to validate slides
    max_validation_attempts: int = 3  # Max regeneration attempts per slide

    # Transition validation options
    validate_transitions: bool = True  # Use Claude to validate transition frames
    max_transition_attempts: int = 3  # Max regeneration attempts per transition


def create_slideshow_video(config: PresentationConfig) -> str:
    """Create a complete slideshow video with optional reference images.

    Reference images (logos, color palettes, style guides) will be used
    to ensure all slides match your brand identity.

    Args:
        config: PresentationConfig with slides and settings.

    Returns:
        Path to the final video.

    Raises:
        EnvironmentError: If prerequisites are not met.
        RuntimeError: If video generation fails.
    """
    # Validate prerequisites
    prereqs = validate_prerequisites()
    if not prereqs["fal_key"]:
        raise EnvironmentError(
            "FAL_KEY not configured. Add your API key to .env file.\n"
            "Get your key at: https://fal.ai/dashboard/keys"
        )
    if not prereqs["ffmpeg"]:
        raise EnvironmentError(
            "FFmpeg not installed. See workflow_guide.md for installation."
        )

    # Validate voice
    if not is_valid_voice(config.voice):
        print(f"Warning: Voice '{config.voice}' not recognized. Using 'George'.")
        config.voice = "George"

    # Validate transition style
    if config.transition_style not in TRANSITION_STYLES:
        print(f"Warning: Style '{config.transition_style}' not recognized. Using 'cinematic'.")
        config.transition_style = "cinematic"

    # Setup directories
    work_dir = str(Path(config.output_path).parent) or "."
    dirs = ensure_output_dirs(work_dir)
    slides_dir = str(dirs["slides"])
    audio_dir = str(dirs["audio"])
    transitions_dir = str(dirs["transitions"])
    temp_dir = str(dirs["temp"])

    # Prepare slide data with new format
    slide_defs = [
        {
            "title": s.title,
            "bullet_points": s.bullet_points,
            "visual_description": s.visual_description,
            "is_title_slide": s.is_title_slide,
        }
        for s in config.slides
    ]
    narrations = [s.narration for s in config.slides]

    # Check for reference images
    has_refs = bool(config.reference_images or config.reference_urls)

    # ===== STEP 1: Generate slide images =====
    print("=" * 60)
    print("STEP 1: Generating STATIC slide images (Nano Banana Pro)")
    if config.validate_slides:
        print("        With AI validation (Claude Haiku 4.5)")
    if has_refs:
        print("        Using reference images for brand consistency")
        print(f"        Local refs: {len(config.reference_images)}")
        print(f"        URL refs: {len(config.reference_urls)}")
    print("=" * 60)

    if config.validate_slides:
        slide_images = generate_slide_batch_with_validation(
            slides=slide_defs,
            output_dir=slides_dir,
            reference_images=config.reference_images if config.reference_images else None,
            reference_urls=config.reference_urls if config.reference_urls else None,
            validate=True,
            max_validation_attempts=config.max_validation_attempts,
        )
    else:
        slide_images = generate_slide_batch(
            slides=slide_defs,
            output_dir=slides_dir,
            reference_images=config.reference_images if config.reference_images else None,
            reference_urls=config.reference_urls if config.reference_urls else None,
        )

    # ===== STEP 2: Generate individual narrations with timing =====
    print("\n" + "=" * 60)
    print("STEP 2: Generating INDIVIDUAL narrations (Eleven Labs v3)")
    print(f"        Voice: {config.voice}")
    print("        Measuring per-slide durations for timing")
    print("=" * 60)

    narration_clips, narration_durations = generate_narrations_with_timing(
        narrations=narrations,
        output_dir=audio_dir,
        voice=config.voice,
    )

    # ===== STEP 3: Generate transitions =====
    # Extract custom transition prompts from slides (all but last slide)
    custom_prompts = [s.transition_prompt for s in config.slides[:-1]]
    has_custom_prompts = any(p is not None for p in custom_prompts)

    print("\n" + "=" * 60)
    print("STEP 3: Generating ANIMATED transitions (Kling O1 Reference-to-Video)")
    print("        Morphing from each slide to the next")
    print("        Using FULL 5-second transitions (no trimming)")
    if has_custom_prompts:
        print("        Using CUSTOM transition prompts per slide")
    else:
        print(f"        Style: {config.transition_style}")
    print("=" * 60)

    transition_videos = generate_transitions_batch(
        slide_images,
        transitions_dir,
        config.transition_style,
        custom_prompts if has_custom_prompts else None,
    )

    # ===== STEP 4: Validate transitions (optional) =====
    if config.validate_transitions:
        print("\n" + "=" * 60)
        print("STEP 4: Validating transitions (Claude Haiku 4.5)")
        print("        Checking first/last frames match slides")
        print("=" * 60)

        transition_videos, validation_results = validate_transitions_batch(
            transition_videos=transition_videos,
            slide_images=slide_images,
            generate_funcs=None,  # No regeneration, just validate
            max_attempts=config.max_transition_attempts,
            temp_dir=temp_dir,
        )

        # Report validation results
        passed = sum(1 for r in validation_results if r.is_valid)
        print(f"  Validation: {passed}/{len(validation_results)} transitions passed")

    # ===== STEP 5: Get transition durations =====
    print("\n" + "=" * 60)
    print("STEP 5: Calculating video timing")
    print("=" * 60)

    transition_durations = [get_duration(t) for t in transition_videos]
    total_slide_time = sum(narration_durations)
    total_transition_time = sum(transition_durations)
    total_duration = total_slide_time + total_transition_time

    print(f"  Slide durations: {[f'{d:.1f}s' for d in narration_durations]}")
    print(f"  Transition durations: {[f'{d:.1f}s' for d in transition_durations]}")
    print(f"  Total video duration: {total_duration:.1f}s")

    # ===== STEP 6: Assemble video with per-slide durations =====
    print("\n" + "=" * 60)
    print("STEP 6: Assembling video (FFmpeg)")
    print("        Each slide displays for its narration duration")
    print("=" * 60)

    temp_silent_video = os.path.join(temp_dir, "silent_video.mp4")
    assemble_slideshow_narration_driven(
        slide_images=slide_images,
        slide_durations=narration_durations,
        transition_videos=transition_videos,
        output_path=temp_silent_video,
        temp_dir=temp_dir,
        cleanup=False,  # Keep temp files until we add audio
    )

    # ===== STEP 7: Create combined audio with silence gaps =====
    print("\n" + "=" * 60)
    print("STEP 7: Creating combined audio track")
    print("        Adding silence gaps for transitions")
    print("=" * 60)

    combined_audio = os.path.join(audio_dir, "narration_full.mp3")
    concatenate_with_gaps(
        audio_files=narration_clips,
        gap_durations=transition_durations,  # Silence during each transition
        output_path=combined_audio,
        temp_dir=temp_dir,
    )

    # ===== STEP 8: Add audio to final video =====
    print("\n" + "=" * 60)
    print("STEP 8: Adding audio to video")
    print("=" * 60)

    add_audio_to_video(temp_silent_video, combined_audio, config.output_path)
    final_video = config.output_path

    print("\n" + "=" * 60)
    print(f"COMPLETE! Video saved to: {final_video}")
    print("=" * 60)

    return final_video


def run_from_json(json_path: str) -> str:
    """Create presentation from a JSON configuration file.

    JSON format:
    {
        "title": "Presentation Title",
        "voice": "George",
        "transition_style": "cinematic",
        "reference_images": ["./Reference Images/logo.png"],
        "reference_urls": [],
        "output_path": "./output/presentation.mp4",
        "validate_slides": true,
        "validate_transitions": true,
        "slides": [
            {
                "title": "Slide Title",
                "bullet_points": ["Point 1", "Point 2"],
                "visual": "Description of visuals",
                "narration": "Voiceover script",
                "is_title_slide": false
            }
        ]
    }

    Args:
        json_path: Path to JSON configuration file.

    Returns:
        Path to the final video.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    slides = []
    for i, s in enumerate(data["slides"]):
        # Support both old format (visual_description) and new format (bullet_points)
        bullet_points = s.get("bullet_points")
        if bullet_points is None:
            # Backwards compatibility: use title as single bullet
            bullet_points = [s["title"]]

        slides.append(Slide(
            title=s["title"],
            bullet_points=bullet_points,
            narration=s["narration"],
            visual_description=s.get("visual", s.get("visual_description", "")),
            is_title_slide=s.get("is_title_slide", i == 0),
        ))

    config = PresentationConfig(
        slides=slides,
        output_path=data.get("output_path", "./output/presentation.mp4"),
        voice=data.get("voice", "George"),
        transition_style=data.get("transition_style", "cinematic"),
        reference_images=data.get("reference_images", []),
        reference_urls=data.get("reference_urls", []),
        validate_slides=data.get("validate_slides", True),
        max_validation_attempts=data.get("max_validation_attempts", 3),
        validate_transitions=data.get("validate_transitions", True),
        max_transition_attempts=data.get("max_transition_attempts", 3),
    )

    return create_slideshow_video(config)


def create_simple_presentation(
    topic: str,
    slides_content: list[dict],
    reference_images: Optional[list[str]] = None,
    voice: str = "George",
    transition_style: str = "cinematic",
    output_path: str = "./output/presentation.mp4",
    validate_slides: bool = True,
    validate_transitions: bool = True,
) -> str:
    """Simplified interface for creating a presentation.

    Args:
        topic: Topic/title of the presentation.
        slides_content: List of dicts with 'title', 'bullet_points', 'visual', and 'narration'.
        reference_images: List of paths to reference images.
        voice: Voice for narration.
        transition_style: Style for transitions.
        output_path: Path for output video.
        validate_slides: Whether to validate slides with Claude.
        validate_transitions: Whether to validate transition frames with Claude.

    Returns:
        Path to the final video.
    """
    slides = []
    for i, s in enumerate(slides_content):
        bullet_points = s.get("bullet_points")
        if bullet_points is None:
            bullet_points = [s["title"]]

        slides.append(Slide(
            title=s["title"],
            bullet_points=bullet_points,
            narration=s["narration"],
            visual_description=s.get("visual", ""),
            is_title_slide=s.get("is_title_slide", i == 0),
        ))

    config = PresentationConfig(
        slides=slides,
        output_path=output_path,
        voice=voice,
        transition_style=transition_style,
        reference_images=reference_images or [],
        validate_slides=validate_slides,
        validate_transitions=validate_transitions,
    )

    return create_slideshow_video(config)


def estimate_cost(num_slides: int, avg_narration_chars: int = 200) -> dict:
    """Estimate the cost of generating a presentation.

    Args:
        num_slides: Number of slides in presentation.
        avg_narration_chars: Average characters per narration.

    Returns:
        Dictionary with cost breakdown.
    """
    slide_cost = num_slides * 0.15
    transition_cost = (num_slides - 1) * 0.35
    voiceover_cost = (num_slides * avg_narration_chars / 1000) * 0.30

    total = slide_cost + transition_cost + voiceover_cost

    return {
        "slides": f"${slide_cost:.2f}",
        "transitions": f"${transition_cost:.2f}",
        "voiceovers": f"${voiceover_cost:.2f}",
        "total": f"${total:.2f}",
        "breakdown": {
            "slide_count": num_slides,
            "transition_count": num_slides - 1,
            "total_chars": num_slides * avg_narration_chars,
        },
    }
