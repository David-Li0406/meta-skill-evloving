"""Validate transition videos using Claude Haiku 4.5 to verify first/last frames match slides."""

import base64
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

import anthropic

from .utils import get_anthropic_key, get_ffmpeg_path


@dataclass
class TransitionValidationResult:
    """Result of transition video validation."""

    is_valid: bool
    first_frame_match: str  # "exact", "close", "different"
    last_frame_match: str   # "exact", "close", "different"
    first_frame_issues: list[str]
    last_frame_issues: list[str]
    overall_score: int  # 1-10
    recommendation: str  # "approve", "regenerate"
    details: str


# JSON schema for structured output
VALIDATION_SCHEMA = {
    "name": "transition_validation",
    "description": "Validation result for a transition video's first and last frames",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "is_valid": {
                "type": "boolean",
                "description": "Whether the transition passes validation"
            },
            "first_frame_match": {
                "type": "string",
                "enum": ["exact", "close", "different"],
                "description": "How well the first frame matches the source slide"
            },
            "last_frame_match": {
                "type": "string",
                "enum": ["exact", "close", "different"],
                "description": "How well the last frame matches the destination slide"
            },
            "first_frame_issues": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of issues with first frame matching"
            },
            "last_frame_issues": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of issues with last frame matching"
            },
            "overall_score": {
                "type": "integer",
                "description": "Overall quality score from 1-10"
            },
            "recommendation": {
                "type": "string",
                "enum": ["approve", "regenerate"],
                "description": "Recommended action"
            },
            "details": {
                "type": "string",
                "description": "Detailed explanation of validation result"
            }
        },
        "required": [
            "is_valid",
            "first_frame_match",
            "last_frame_match",
            "first_frame_issues",
            "last_frame_issues",
            "overall_score",
            "recommendation",
            "details"
        ],
        "additionalProperties": False
    }
}


def extract_frames(
    video_path: str,
    output_dir: Optional[str] = None
) -> tuple[str, str]:
    """Extract first and last frames from a video file.

    Args:
        video_path: Path to the video file.
        output_dir: Directory for output frames. Defaults to video's directory.

    Returns:
        Tuple of (first_frame_path, last_frame_path).

    Raises:
        RuntimeError: If FFmpeg fails to extract frames.
    """
    ffmpeg = get_ffmpeg_path()
    video_dir = Path(video_path).parent
    video_stem = Path(video_path).stem

    if output_dir is None:
        output_dir = str(video_dir)
    else:
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    first_frame = os.path.join(output_dir, f"{video_stem}_first_frame.png")
    last_frame = os.path.join(output_dir, f"{video_stem}_last_frame.png")

    # Extract first frame
    result = subprocess.run(
        [
            ffmpeg, "-y",
            "-i", video_path,
            "-vframes", "1",
            "-q:v", "2",
            first_frame,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg failed extracting first frame: {result.stderr}")

    # Extract last frame using -sseof (seek from end)
    result = subprocess.run(
        [
            ffmpeg, "-y",
            "-sseof", "-0.1",  # Seek to 0.1 seconds before end
            "-i", video_path,
            "-vframes", "1",
            "-q:v", "2",
            last_frame,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg failed extracting last frame: {result.stderr}")

    return first_frame, last_frame


def _encode_image_base64(image_path: str) -> str:
    """Encode image file to base64 string."""
    with open(image_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def _get_media_type(image_path: str) -> str:
    """Get media type from image file extension."""
    ext = Path(image_path).suffix.lower()
    media_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }
    return media_types.get(ext, "image/png")


def validate_transition(
    video_path: str,
    from_slide_path: str,
    to_slide_path: str,
    temp_dir: Optional[str] = None,
    cleanup_frames: bool = True,
) -> TransitionValidationResult:
    """Validate a transition video using Claude Haiku 4.5.

    Checks that:
    - First frame matches the source slide (from_slide)
    - Last frame matches the destination slide (to_slide)

    Args:
        video_path: Path to the transition video.
        from_slide_path: Path to the source slide image.
        to_slide_path: Path to the destination slide image.
        temp_dir: Directory for temporary frame extraction.
        cleanup_frames: Whether to delete extracted frames after validation.

    Returns:
        TransitionValidationResult with validation details.
    """
    client = anthropic.Anthropic(api_key=get_anthropic_key())

    # Extract frames from video
    first_frame, last_frame = extract_frames(video_path, temp_dir)

    try:
        # Encode all images
        first_frame_data = _encode_image_base64(first_frame)
        last_frame_data = _encode_image_base64(last_frame)
        from_slide_data = _encode_image_base64(from_slide_path)
        to_slide_data = _encode_image_base64(to_slide_path)

        first_media = _get_media_type(first_frame)
        last_media = _get_media_type(last_frame)
        from_media = _get_media_type(from_slide_path)
        to_media = _get_media_type(to_slide_path)

        prompt = """Analyze this transition video's first and last frames for quality.

I will show you 4 images:
1. SOURCE SLIDE - The slide the transition should START from
2. FIRST FRAME - The actual first frame extracted from the transition video
3. DESTINATION SLIDE - The slide the transition should END on
4. LAST FRAME - The actual last frame extracted from the transition video

Your task is to determine:
1. Does the FIRST FRAME match the SOURCE SLIDE? (exact, close, or different)
2. Does the LAST FRAME match the DESTINATION SLIDE? (exact, close, or different)

Match criteria:
- "exact": The frames are visually identical (same layout, text, graphics, colors)
- "close": The frames are very similar but have minor differences (slight color shift, minor element position changes)
- "different": The frames are noticeably different (different content, missing elements, extra elements, wrong layout)

A valid transition should have:
- First frame: exact or close match to source slide
- Last frame: exact or close match to destination slide

Score guidelines:
- 9-10: Both frames are exact matches
- 7-8: Both frames are close matches, or one exact + one close
- 5-6: One frame matches well but the other has issues
- 1-4: One or both frames are different from their expected slides

Provide your validation result as JSON."""

        # Build message with all 4 images
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "SOURCE SLIDE (transition should start from this):"},
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": from_media,
                                "data": from_slide_data,
                            },
                        },
                        {"type": "text", "text": "FIRST FRAME (extracted from transition video):"},
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": first_media,
                                "data": first_frame_data,
                            },
                        },
                        {"type": "text", "text": "DESTINATION SLIDE (transition should end on this):"},
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": to_media,
                                "data": to_slide_data,
                            },
                        },
                        {"type": "text", "text": "LAST FRAME (extracted from transition video):"},
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": last_media,
                                "data": last_frame_data,
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
            tools=[
                {
                    "name": "transition_validation",
                    "description": "Submit the validation result for the transition video",
                    "input_schema": VALIDATION_SCHEMA["schema"],
                }
            ],
            tool_choice={"type": "tool", "name": "transition_validation"},
        )

        # Extract tool use response
        for block in response.content:
            if block.type == "tool_use" and block.name == "transition_validation":
                result_data = block.input
                return TransitionValidationResult(
                    is_valid=result_data["is_valid"],
                    first_frame_match=result_data["first_frame_match"],
                    last_frame_match=result_data["last_frame_match"],
                    first_frame_issues=result_data["first_frame_issues"],
                    last_frame_issues=result_data["last_frame_issues"],
                    overall_score=result_data["overall_score"],
                    recommendation=result_data["recommendation"],
                    details=result_data["details"],
                )

        # Fallback if no tool use found
        return TransitionValidationResult(
            is_valid=False,
            first_frame_match="different",
            last_frame_match="different",
            first_frame_issues=["Validation failed - no structured response"],
            last_frame_issues=[],
            overall_score=0,
            recommendation="regenerate",
            details="Failed to get structured validation response from Claude",
        )

    finally:
        # Clean up extracted frames if requested
        if cleanup_frames:
            for frame in [first_frame, last_frame]:
                if os.path.exists(frame):
                    os.remove(frame)


def validate_transition_with_retry(
    generate_func: Callable[[], str],
    from_slide_path: str,
    to_slide_path: str,
    max_attempts: int = 3,
    min_score: int = 7,
    temp_dir: Optional[str] = None,
) -> tuple[str, TransitionValidationResult]:
    """Generate and validate a transition, retrying if validation fails.

    Args:
        generate_func: Callable that generates a transition and returns the video path.
        from_slide_path: Path to source slide for validation.
        to_slide_path: Path to destination slide for validation.
        max_attempts: Maximum generation attempts (default: 3).
        min_score: Minimum acceptable quality score (default: 7).
        temp_dir: Directory for temporary frame extraction.

    Returns:
        Tuple of (video_path, validation_result).
    """
    best_result = None
    best_path = None
    best_score = -1

    for attempt in range(1, max_attempts + 1):
        print(f"    Validation attempt {attempt}/{max_attempts}...")

        # Generate the transition
        video_path = generate_func()

        # Validate it
        result = validate_transition(
            video_path,
            from_slide_path,
            to_slide_path,
            temp_dir=temp_dir,
        )

        print(f"    Score: {result.overall_score}/10 - {result.recommendation}")
        print(f"    First frame: {result.first_frame_match}, Last frame: {result.last_frame_match}")

        # Track best result
        if result.overall_score > best_score:
            best_score = result.overall_score
            best_result = result
            best_path = video_path

        # Check if acceptable
        if result.overall_score >= min_score and result.recommendation != "regenerate":
            print(f"    Validation passed!")
            return video_path, result

        # Log issues
        if result.first_frame_issues:
            print(f"    First frame issues: {result.first_frame_issues}")
        if result.last_frame_issues:
            print(f"    Last frame issues: {result.last_frame_issues}")

        if attempt < max_attempts:
            print(f"    Regenerating transition...")

    # All attempts completed - return best result
    print(f"    Using best attempt (score: {best_score})")
    return best_path, best_result


def validate_transitions_batch(
    transition_videos: list[str],
    slide_images: list[str],
    generate_funcs: Optional[list[Callable[[], str]]] = None,
    max_attempts: int = 3,
    min_score: int = 7,
    temp_dir: Optional[str] = None,
) -> tuple[list[str], list[TransitionValidationResult]]:
    """Validate all transitions in a batch.

    Args:
        transition_videos: List of paths to transition videos.
        slide_images: List of paths to slide images (n slides).
        generate_funcs: Optional list of functions to regenerate each transition.
                       If None, validation only reports without regeneration.
        max_attempts: Maximum regeneration attempts per transition.
        min_score: Minimum acceptable quality score.
        temp_dir: Directory for temporary frame extraction.

    Returns:
        Tuple of (validated_video_paths, validation_results).
    """
    validated_videos = []
    results = []
    num_transitions = len(transition_videos)

    print(f"Validating {num_transitions} transitions...")

    for i, video in enumerate(transition_videos):
        from_slide = slide_images[i]
        to_slide = slide_images[i + 1]

        print(f"\nValidating transition {i + 1}/{num_transitions}:")

        if generate_funcs and i < len(generate_funcs):
            # Can regenerate if needed
            video_path, result = validate_transition_with_retry(
                generate_func=generate_funcs[i],
                from_slide_path=from_slide,
                to_slide_path=to_slide,
                max_attempts=max_attempts,
                min_score=min_score,
                temp_dir=temp_dir,
            )
            validated_videos.append(video_path)
        else:
            # Just validate without regeneration
            result = validate_transition(
                video, from_slide, to_slide, temp_dir=temp_dir
            )
            validated_videos.append(video)

            print(f"  Score: {result.overall_score}/10 - {result.recommendation}")
            print(f"  First frame: {result.first_frame_match}, Last frame: {result.last_frame_match}")

        results.append(result)

    return validated_videos, results
