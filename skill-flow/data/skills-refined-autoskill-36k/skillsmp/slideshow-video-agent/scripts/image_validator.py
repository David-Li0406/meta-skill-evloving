"""Validate generated slide images using Claude Haiku 4.5 with structured outputs."""

import base64
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Callable

import anthropic

from .utils import get_anthropic_key


@dataclass
class ValidationResult:
    """Result of slide image validation."""

    is_valid: bool
    text_quality: str  # "good", "acceptable", "poor"
    text_issues: list[str]
    graphics_quality: str  # "good", "acceptable", "poor"
    graphics_issues: list[str]
    overall_score: int  # 1-10
    recommendation: str  # "approve", "regenerate", "manual_review"
    details: str


# JSON schema for structured output
VALIDATION_SCHEMA = {
    "name": "slide_validation",
    "description": "Validation result for a generated slide image",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "is_valid": {
                "type": "boolean",
                "description": "Whether the slide passes validation"
            },
            "text_quality": {
                "type": "string",
                "enum": ["good", "acceptable", "poor"],
                "description": "Quality of text rendering"
            },
            "text_issues": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of text-related issues found"
            },
            "graphics_quality": {
                "type": "string",
                "enum": ["good", "acceptable", "poor"],
                "description": "Quality of graphics/icons"
            },
            "graphics_issues": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of graphics-related issues found"
            },
            "overall_score": {
                "type": "integer",
                "description": "Overall quality score from 1-10"
            },
            "recommendation": {
                "type": "string",
                "enum": ["approve", "regenerate", "manual_review"],
                "description": "Recommended action"
            },
            "details": {
                "type": "string",
                "description": "Detailed explanation of validation result"
            }
        },
        "required": [
            "is_valid",
            "text_quality",
            "text_issues",
            "graphics_quality",
            "graphics_issues",
            "overall_score",
            "recommendation",
            "details"
        ],
        "additionalProperties": False
    }
}


def _encode_image_base64(image_path: str) -> str:
    """Encode image file to base64 string.

    Args:
        image_path: Path to image file.

    Returns:
        Base64-encoded image string.
    """
    with open(image_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def _get_media_type(image_path: str) -> str:
    """Get media type from image file extension.

    Args:
        image_path: Path to image file.

    Returns:
        Media type string (e.g., "image/png").
    """
    ext = Path(image_path).suffix.lower()
    media_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }
    return media_types.get(ext, "image/png")


def validate_slide_image(
    image_path: str,
    expected_title: str,
    expected_bullet_points: Optional[list[str]] = None,
) -> ValidationResult:
    """Validate a generated slide image using Claude Haiku 4.5.

    Checks for:
    - Text is correct English (not gibberish or AI artifacts)
    - Graphics are clear symbols (not alien lettering)
    - Overall quality and readability

    Args:
        image_path: Path to the slide image to validate.
        expected_title: The title that should appear on the slide.
        expected_bullet_points: Optional list of bullet points that should appear.

    Returns:
        ValidationResult with validation details.
    """
    client = anthropic.Anthropic(api_key=get_anthropic_key())

    # Encode image
    image_data = _encode_image_base64(image_path)
    media_type = _get_media_type(image_path)

    # Build validation prompt
    bullet_info = ""
    if expected_bullet_points:
        bullets = "\n".join(f"  - {bp}" for bp in expected_bullet_points)
        bullet_info = f"\n- Expected bullet points:\n{bullets}"

    prompt = f"""Analyze this presentation slide image for quality issues.

Expected content:
- Title: "{expected_title}"{bullet_info}

Check for these issues:
1. TEXT QUALITY:
   - Is the title readable and correctly spelled?
   - Are any bullet points readable and correctly spelled?
   - Is there any gibberish, corrupted text, or AI artifacts?
   - Is there any "alien lettering" or nonsense characters?

2. GRAPHICS QUALITY:
   - Are icons/symbols clear and recognizable?
   - Are there any distorted or corrupted graphics?
   - Is the overall visual design professional?

3. OVERALL ASSESSMENT:
   - Would this slide be acceptable in a professional presentation?
   - Score from 1-10 (10 = perfect, 7+ = acceptable, <7 = needs regeneration)

Provide your validation result as JSON."""

    # Call Claude Haiku 4.5
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            }
        ],
        tools=[
            {
                "name": "slide_validation",
                "description": "Submit the validation result for the slide image",
                "input_schema": VALIDATION_SCHEMA["schema"],
            }
        ],
        tool_choice={"type": "tool", "name": "slide_validation"},
    )

    # Extract tool use response
    for block in response.content:
        if block.type == "tool_use" and block.name == "slide_validation":
            result_data = block.input
            return ValidationResult(
                is_valid=result_data["is_valid"],
                text_quality=result_data["text_quality"],
                text_issues=result_data["text_issues"],
                graphics_quality=result_data["graphics_quality"],
                graphics_issues=result_data["graphics_issues"],
                overall_score=result_data["overall_score"],
                recommendation=result_data["recommendation"],
                details=result_data["details"],
            )

    # Fallback if no tool use found
    return ValidationResult(
        is_valid=False,
        text_quality="poor",
        text_issues=["Validation failed - no structured response"],
        graphics_quality="poor",
        graphics_issues=[],
        overall_score=0,
        recommendation="regenerate",
        details="Failed to get structured validation response from Claude",
    )


def validate_slide_with_retry(
    generate_func: Callable[[], str],
    expected_title: str,
    expected_bullet_points: Optional[list[str]] = None,
    max_attempts: int = 3,
    min_score: int = 7,
) -> tuple[str, ValidationResult]:
    """Generate and validate a slide, retrying if validation fails.

    Args:
        generate_func: Callable that generates a slide and returns the image path.
        expected_title: Expected title for validation.
        expected_bullet_points: Expected bullet points for validation.
        max_attempts: Maximum generation attempts (default: 3).
        min_score: Minimum acceptable quality score (default: 7).

    Returns:
        Tuple of (image_path, validation_result).
    """
    best_result = None
    best_path = None
    best_score = -1

    for attempt in range(1, max_attempts + 1):
        print(f"    Validation attempt {attempt}/{max_attempts}...")

        # Generate the slide
        image_path = generate_func()

        # Validate it
        result = validate_slide_image(
            image_path,
            expected_title,
            expected_bullet_points,
        )

        print(f"    Score: {result.overall_score}/10 - {result.recommendation}")

        # Track best result
        if result.overall_score > best_score:
            best_score = result.overall_score
            best_result = result
            best_path = image_path

        # Check if acceptable
        if result.overall_score >= min_score and result.recommendation != "regenerate":
            print(f"    Validation passed!")
            return image_path, result

        # Log issues
        if result.text_issues:
            print(f"    Text issues: {result.text_issues}")
        if result.graphics_issues:
            print(f"    Graphics issues: {result.graphics_issues}")

        if attempt < max_attempts:
            print(f"    Regenerating slide...")

    # All attempts completed - return best result
    print(f"    Using best attempt (score: {best_score})")
    return best_path, best_result
