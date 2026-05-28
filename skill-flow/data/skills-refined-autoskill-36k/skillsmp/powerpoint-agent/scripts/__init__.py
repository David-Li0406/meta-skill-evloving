"""PowerPoint Agent - Creates editable presentations with AI-generated slides.

This package provides tools to create professional PowerPoint presentations with:
- AI-generated slide images (Nano Banana Pro)
- Full-slide images in 16:9 widescreen format
- Brand consistency via reference images
- Rolling style references for consistent look across slides
- Optional AI validation (Claude Haiku 4.5)

Example usage:
    from scripts import PPTXConfig, SlideContent, create_powerpoint

    config = PPTXConfig(
        slides=[
            SlideContent(
                title="Welcome",
                bullet_points=["Point 1", "Point 2"],
                visual_description="Modern title slide with company branding",
                is_title_slide=True,
            ),
        ],
        reference_images=["./Reference Images/logo.png"],
        output_path="./output/presentation.pptx",
    )

    result = create_powerpoint(config)
"""

from .orchestrator import (
    PPTXConfig,
    SlideContent,
    create_powerpoint,
    run_from_json,
    create_simple_powerpoint,
    estimate_cost,
)

from .slide_generator import (
    generate_slide,
    generate_slide_batch,
    generate_slide_batch_with_rolling_refs,
    generate_slide_batch_with_validation,
    upload_reference_images,
)

from .image_validator import (
    validate_slide_image,
    validate_slide_with_retry,
    ValidationResult,
)

from .pptx_generator import (
    create_pptx_from_images,
    create_pptx_with_metadata,
    get_pptx_info,
    replace_slide_image,
    replace_multiple_slides,
)

from .utils import (
    validate_prerequisites,
    print_prerequisites_status,
    list_reference_images,
    get_reference_images_dir,
    get_anthropic_key,
)

__all__ = [
    # Main orchestrator
    "PPTXConfig",
    "SlideContent",
    "create_powerpoint",
    "run_from_json",
    "create_simple_powerpoint",
    "estimate_cost",
    # Slide generation
    "generate_slide",
    "generate_slide_batch",
    "generate_slide_batch_with_rolling_refs",
    "generate_slide_batch_with_validation",
    "upload_reference_images",
    # Image validation
    "validate_slide_image",
    "validate_slide_with_retry",
    "ValidationResult",
    # PPTX generation
    "create_pptx_from_images",
    "create_pptx_with_metadata",
    "get_pptx_info",
    "replace_slide_image",
    "replace_multiple_slides",
    # Utilities
    "validate_prerequisites",
    "print_prerequisites_status",
    "list_reference_images",
    "get_reference_images_dir",
    "get_anthropic_key",
]

__version__ = "1.0.0"
