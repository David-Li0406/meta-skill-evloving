#!/usr/bin/env python3
"""
Data Structures for Direct Markdown to HTML Conversion.

Defines the core data structures used in the new direct conversion pipeline:
ParsedDocument -> SlideSpec[] -> DirectGenerator -> HTML
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class SlideType(Enum):
    """Types of slides that can be generated."""
    TITLE = "title"
    EXECUTIVE_SUMMARY = "executive_summary"
    DATA_VISUALIZATION = "data_viz"
    CONCEPTUAL = "conceptual"
    CONTENT = "content"
    CONCLUSIONS = "conclusions"


@dataclass
class SlideSpec:
    """Single slide specification for direct HTML generation.

    Attributes:
        slide_type: The type of slide (determines rendering method)
        title: Slide title
        content: Main content text
        chart_type: Optional chart type (e.g., 'bar', 'line', 'pie')
        data_points: Optional list of data points for chart visualization
        conceptual_type: Optional conceptual viz type (e.g., 'pyramid', 'cycle')
        key_points: Optional list of key insight points
        layout: Optional layout hint (e.g., 'two-column', 'full-width')
        source_section: Optional reference to source section title
        slide_number: Position in presentation (0-indexed)
    """
    slide_type: SlideType
    title: str
    content: str
    chart_type: Optional[str] = None
    data_points: Optional[List[Dict[str, Any]]] = None
    conceptual_type: Optional[str] = None
    key_points: Optional[List[str]] = None
    layout: Optional[str] = None
    source_section: Optional[str] = None
    slide_number: int = 0

    def __post_init__(self):
        """Set default values for mutable fields."""
        if self.data_points is None:
            self.data_points = []
        if self.key_points is None:
            self.key_points = []


@dataclass
class SlidePlan:
    """Complete slide plan for a presentation.

    Attributes:
        title: Presentation title
        slides: List of slide specifications
        total_slides: Total number of slides
    """
    title: str
    slides: List[SlideSpec] = field(default_factory=list)

    @property
    def total_slides(self) -> int:
        """Get total number of slides."""
        return len(self.slides)

    def add_slide(self, slide: SlideSpec) -> None:
        """Add a slide with automatic numbering."""
        slide.slide_number = len(self.slides)
        self.slides.append(slide)
