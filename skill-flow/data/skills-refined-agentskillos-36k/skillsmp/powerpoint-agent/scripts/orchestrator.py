"""Main orchestrator for PowerPoint presentation generation."""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .slide_generator import (
    generate_slide_batch,
    generate_slide_batch_with_validation,
    generate_slide_batch_with_rolling_refs,
)
from .pptx_generator import create_pptx_with_metadata, get_pptx_info
from .utils import (
    ensure_output_dirs,
    get_project_root,
    list_reference_images,
    validate_prerequisites,
)


@dataclass
class SlideContent:
    """Configuration for a single slide.

    Attributes:
        title: Short title displayed on slide.
        bullet_points: Brief points shown on slide (3-4 items, 3-6 words each).
        visual_description: Description of icon/graphic for the slide.
        is_title_slide: If True, display logo prominently.
    """

    title: str
    bullet_points: list[str] = field(default_factory=list)
    visual_description: str = ""
    is_title_slide: bool = False


@dataclass
class PPTXConfig:
    """Configuration for the entire PowerPoint presentation."""

    slides: list[SlideContent]
    output_path: str = "./output/presentation.pptx"

    # Static reference images (logos, brand colors, style examples)
    reference_images: list[str] = field(default_factory=list)
    reference_urls: list[str] = field(default_factory=list)

    # Rolling style references - feed previous slides to maintain consistency
    use_rolling_references: bool = True
    rolling_reference_count: int = 1  # How many previous slides to include (1-2)

    # Validation options
    validate_slides: bool = True
    max_validation_attempts: int = 3

    # Presentation metadata
    presentation_title: Optional[str] = None
    presentation_author: Optional[str] = None


def create_powerpoint(config: PPTXConfig) -> str:
    """Create a complete PowerPoint presentation with AI-generated slide images.

    Workflow:
    1. Generate slide images using Nano Banana Pro
       - Uses static reference images for brand consistency
       - Optionally uses rolling references (previous slides)
       - Optionally validates with Claude Haiku 4.5
    2. Create PPTX with full-slide images
       - 16:9 widescreen format
       - Titles in speaker notes for accessibility

    Args:
        config: PPTXConfig with slides and settings.

    Returns:
        Path to the final PPTX file.

    Raises:
        EnvironmentError: If prerequisites are not met.
        RuntimeError: If generation fails.
    """
    # Validate prerequisites
    prereqs = validate_prerequisites()
    if not prereqs["fal_key"]:
        raise EnvironmentError(
            "FAL_KEY not configured. Add your API key to .env file.\n"
            "Get your key at: https://fal.ai/dashboard/keys"
        )
    if not prereqs["python_pptx"]:
        raise EnvironmentError(
            "python-pptx not installed. Run: pip install python-pptx"
        )

    # Setup directories
    output_path = Path(config.output_path)
    work_dir = str(output_path.parent)
    dirs = ensure_output_dirs(work_dir)
    slides_dir = str(dirs["slides"])

    # Prepare slide data
    slide_defs = [
        {
            "title": s.title,
            "bullet_points": s.bullet_points,
            "visual_description": s.visual_description,
            "is_title_slide": s.is_title_slide,
        }
        for s in config.slides
    ]

    # Check for reference images
    has_static_refs = bool(config.reference_images or config.reference_urls)
    has_rolling_refs = config.use_rolling_references

    # ===== STEP 1: Generate slide images =====
    print("=" * 60)
    print("STEP 1: Generating slide images (Nano Banana Pro)")
    if config.validate_slides:
        print("        With AI validation (Claude Haiku 4.5)")
    if has_static_refs:
        print("        Using static reference images for brand consistency")
        print(f"        Local refs: {len(config.reference_images)}")
        print(f"        URL refs: {len(config.reference_urls)}")
    if has_rolling_refs:
        print(f"        Using rolling references (last {config.rolling_reference_count} slide(s))")
    print("=" * 60)

    if config.validate_slides:
        slide_images = generate_slide_batch_with_validation(
            slides=slide_defs,
            output_dir=slides_dir,
            reference_images=config.reference_images if config.reference_images else None,
            reference_urls=config.reference_urls if config.reference_urls else None,
            validate=True,
            max_validation_attempts=config.max_validation_attempts,
            use_rolling_references=config.use_rolling_references,
            rolling_reference_count=config.rolling_reference_count,
        )
    elif config.use_rolling_references:
        slide_images = generate_slide_batch_with_rolling_refs(
            slides=slide_defs,
            output_dir=slides_dir,
            static_reference_images=config.reference_images if config.reference_images else None,
            static_reference_urls=config.reference_urls if config.reference_urls else None,
            use_rolling_references=True,
            rolling_reference_count=config.rolling_reference_count,
        )
    else:
        slide_images = generate_slide_batch(
            slides=slide_defs,
            output_dir=slides_dir,
            reference_images=config.reference_images if config.reference_images else None,
            reference_urls=config.reference_urls if config.reference_urls else None,
        )

    # ===== STEP 2: Create PowerPoint =====
    print("\n" + "=" * 60)
    print("STEP 2: Creating PowerPoint presentation (python-pptx)")
    print("        16:9 widescreen format (10\" x 5.625\")")
    print("        Full-slide images with titles in notes")
    print("=" * 60)

    # Build metadata for slides
    slides_metadata = [
        {
            "title": s.title,
            "bullet_points": s.bullet_points,
        }
        for s in config.slides
    ]

    pptx_path = create_pptx_with_metadata(
        image_paths=slide_images,
        output_path=config.output_path,
        slides_metadata=slides_metadata,
        presentation_title=config.presentation_title,
        presentation_author=config.presentation_author,
    )

    # Get info about created file
    info = get_pptx_info(pptx_path)

    print("\n" + "=" * 60)
    print(f"COMPLETE! PowerPoint saved to: {pptx_path}")
    print(f"  Slides: {info['slide_count']}")
    print(f"  Size: {info['width_inches']}\" x {info['height_inches']}\"")
    print(f"  Aspect: {info['aspect_ratio']}")
    print("=" * 60)

    return pptx_path


def run_from_json(json_path: str) -> str:
    """Create presentation from a JSON configuration file.

    JSON format:
    {
        "title": "Presentation Title",
        "author": "Author Name",
        "reference_images": ["./Reference Images/logo.png"],
        "reference_urls": [],
        "output_path": "./output/presentation.pptx",
        "validate_slides": true,
        "use_rolling_references": true,
        "rolling_reference_count": 1,
        "slides": [
            {
                "title": "Slide Title",
                "bullet_points": ["Point 1", "Point 2"],
                "visual_description": "Description of visuals",
                "is_title_slide": false
            }
        ]
    }

    Args:
        json_path: Path to JSON configuration file.

    Returns:
        Path to the final PPTX file.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    slides = []
    for i, s in enumerate(data["slides"]):
        bullet_points = s.get("bullet_points", [])
        if not bullet_points and s.get("title"):
            # Backwards compatibility: if no bullet points, use empty list
            bullet_points = []

        slides.append(SlideContent(
            title=s["title"],
            bullet_points=bullet_points,
            visual_description=s.get("visual_description", s.get("visual", "")),
            is_title_slide=s.get("is_title_slide", i == 0),
        ))

    config = PPTXConfig(
        slides=slides,
        output_path=data.get("output_path", "./output/presentation.pptx"),
        reference_images=data.get("reference_images", []),
        reference_urls=data.get("reference_urls", []),
        use_rolling_references=data.get("use_rolling_references", True),
        rolling_reference_count=data.get("rolling_reference_count", 1),
        validate_slides=data.get("validate_slides", True),
        max_validation_attempts=data.get("max_validation_attempts", 3),
        presentation_title=data.get("title"),
        presentation_author=data.get("author"),
    )

    return create_powerpoint(config)


def create_simple_powerpoint(
    topic: str,
    slides_content: list[dict],
    reference_images: Optional[list[str]] = None,
    output_path: str = "./output/presentation.pptx",
    validate_slides: bool = True,
    use_rolling_references: bool = True,
) -> str:
    """Simplified interface for creating a PowerPoint presentation.

    Args:
        topic: Topic/title of the presentation.
        slides_content: List of dicts with 'title', 'bullet_points', 'visual_description'.
        reference_images: List of paths to reference images.
        output_path: Path for output PPTX.
        validate_slides: Whether to validate slides with Claude.
        use_rolling_references: Whether to use previous slides as references.

    Returns:
        Path to the final PPTX file.
    """
    slides = []
    for i, s in enumerate(slides_content):
        bullet_points = s.get("bullet_points", [])

        slides.append(SlideContent(
            title=s["title"],
            bullet_points=bullet_points,
            visual_description=s.get("visual_description", s.get("visual", "")),
            is_title_slide=s.get("is_title_slide", i == 0),
        ))

    config = PPTXConfig(
        slides=slides,
        output_path=output_path,
        reference_images=reference_images or [],
        validate_slides=validate_slides,
        use_rolling_references=use_rolling_references,
        presentation_title=topic,
    )

    return create_powerpoint(config)


def estimate_cost(num_slides: int) -> dict:
    """Estimate the cost of generating a PowerPoint presentation.

    Args:
        num_slides: Number of slides in presentation.

    Returns:
        Dictionary with cost breakdown.
    """
    slide_cost = num_slides * 0.15  # Nano Banana Pro
    validation_cost = num_slides * 0.001  # Claude Haiku 4.5 (optional)

    total_without_validation = slide_cost
    total_with_validation = slide_cost + validation_cost

    return {
        "slides": f"${slide_cost:.2f}",
        "validation": f"${validation_cost:.3f} (optional)",
        "total_without_validation": f"${total_without_validation:.2f}",
        "total_with_validation": f"${total_with_validation:.2f}",
        "breakdown": {
            "slide_count": num_slides,
            "per_slide_cost": "$0.15",
            "per_validation_cost": "$0.001",
        },
    }
