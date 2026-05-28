"""Centralized annotation configuration for desktop element annotation.

Defines styling, behavior flags, and performance thresholds for the
annotation pipeline. Supports element type-specific styling and
confidence-based visual cues.
"""

from dataclasses import dataclass, field


@dataclass
class AnnotationConfig:
    """Configuration for desktop element annotation rendering.

    Centralizes all annotation styling, behavior flags, and performance
    thresholds. Supports element type-specific styling (e.g., buttons vs inputs)
    and confidence-based visual cues.

    Attributes:
        highlight_color: RGBA tuple for element bounding box (default: orange-red).
        label_bg_color: RGBA tuple for label background (default: orange-red).
        label_text_color: RGB tuple for label text (default: white).
        box_width: Bounding box line width in pixels.
        label_font_size: Label text font size in pixels.
        label_padding: Padding inside label background in pixels.
        arrow_width: Arrow line width in pixels.
        confidence_threshold: Minimum confidence to use element identification (0.8).
        enable_cache: Enable element metadata caching (default: True).
        cache_size: Maximum cache entries (default: 100).
        element_query_timeout_ms: Timeout for element identification in milliseconds.
        type_styles: Element type-specific style overrides {type: {color, width, ...}}.
    """

    # Colors (RGBA for highlight/label_bg, RGB for label text)
    highlight_color: tuple[int, int, int, int] = (255, 87, 51, 180)  # Orange-red
    label_bg_color: tuple[int, int, int, int] = (255, 87, 51, 230)  # Orange-red
    label_text_color: tuple[int, int, int] = (255, 255, 255)  # White

    # Dimensions
    box_width: int = 3
    label_font_size: int = 14
    label_padding: int = 4
    arrow_width: int = 3

    # Behavior
    confidence_threshold: float = 0.8
    enable_cache: bool = True
    cache_size: int = 100
    element_query_timeout_ms: int = 100

    # Element type-specific styles (optional overrides)
    # Example: {"button": {"highlight_color": (0, 255, 0, 180)}}
    type_styles: dict[str, dict] = field(default_factory=dict)

    def get_style_for_type(self, element_type: str) -> dict:
        """Get effective style for a specific element type.

        Merges type-specific overrides with default values.

        Args:
            element_type: Element type (button, input, link, etc.).

        Returns:
            Dict with effective style values for this element type.
        """
        default_style = {
            "highlight_color": self.highlight_color,
            "label_bg_color": self.label_bg_color,
            "label_text_color": self.label_text_color,
            "box_width": self.box_width,
            "label_font_size": self.label_font_size,
            "label_padding": self.label_padding,
            "arrow_width": self.arrow_width,
        }

        # Merge type-specific overrides
        type_override = self.type_styles.get(element_type, {})
        return {**default_style, **type_override}
