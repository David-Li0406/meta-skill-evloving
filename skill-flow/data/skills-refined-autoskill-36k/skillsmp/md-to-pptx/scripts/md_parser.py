#!/usr/bin/env python3
"""
Markdown Parser Module for md-to-pptx

Parses Markdown content and extracts structured slide data.
Supports: headings, paragraphs, lists, code blocks, tables, images.
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class ContentType(Enum):
    """Types of content elements."""
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    BULLET_LIST = "bullet_list"
    NUMBERED_LIST = "numbered_list"
    CODE_BLOCK = "code_block"
    TABLE = "table"
    IMAGE = "image"
    CHART_DATA = "chart_data"


@dataclass
class ContentElement:
    """Represents a single content element."""
    type: ContentType
    content: Any
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SlideData:
    """Represents data for a single slide."""
    title: str = ""
    subtitle: str = ""
    elements: List[ContentElement] = field(default_factory=list)
    layout_hint: str = "content"  # title, content, two_column, image, chart
    notes: str = ""


class MarkdownParser:
    """Parse Markdown content into structured slide data."""

    def __init__(self):
        self.slides: List[SlideData] = []
        self.current_slide: Optional[SlideData] = None
        self.warnings: List[str] = []

    def parse(self, markdown_text: str) -> List[SlideData]:
        """
        Parse Markdown text and return list of SlideData.

        Args:
            markdown_text: Raw Markdown content

        Returns:
            List of SlideData objects representing slides
        """
        self.slides = []
        self.current_slide = None
        self.warnings = []

        lines = markdown_text.split('\n')
        i = 0

        while i < len(lines):
            line = lines[i]

            # Check for code block
            if line.strip().startswith('```'):
                i = self._parse_code_block(lines, i)
                continue

            # Check for table
            if '|' in line and i + 1 < len(lines) and '|' in lines[i + 1]:
                if re.match(r'^\s*\|?\s*[-:]+\s*\|', lines[i + 1]):
                    i = self._parse_table(lines, i)
                    continue

            # Check for heading
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if heading_match:
                level = len(heading_match.group(1))
                text = heading_match.group(2).strip()
                self._handle_heading(level, text)
                i += 1
                continue

            # Check for image
            img_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', line.strip())
            if img_match:
                alt_text = img_match.group(1)
                img_path = img_match.group(2)
                self._add_image(img_path, alt_text)
                i += 1
                continue

            # Check for bullet list
            if re.match(r'^\s*[-*+]\s+', line):
                i = self._parse_bullet_list(lines, i)
                continue

            # Check for numbered list
            if re.match(r'^\s*\d+\.\s+', line):
                i = self._parse_numbered_list(lines, i)
                continue

            # Regular paragraph
            if line.strip():
                self._add_paragraph(line.strip())

            i += 1

        # Finalize last slide
        if self.current_slide:
            self.slides.append(self.current_slide)

        # Post-process: determine layout hints
        self._determine_layouts()

        return self.slides

    def _ensure_slide(self):
        """Ensure there's a current slide to add content to."""
        if self.current_slide is None:
            self.current_slide = SlideData(title="Untitled")

    def _handle_heading(self, level: int, text: str):
        """Handle heading elements - create new slides for H1/H2."""
        if level <= 2:
            # Start new slide
            if self.current_slide:
                self.slides.append(self.current_slide)

            self.current_slide = SlideData(title=text)

            if level == 1:
                self.current_slide.layout_hint = "title"
        else:
            # Add as content heading
            self._ensure_slide()
            self.current_slide.elements.append(ContentElement(
                type=ContentType.HEADING,
                content=text,
                metadata={"level": level}
            ))

    def _add_paragraph(self, text: str):
        """Add paragraph content."""
        self._ensure_slide()

        # Check if this looks like a subtitle (first content after title slide)
        if (self.current_slide.layout_hint == "title" and
            not self.current_slide.subtitle and
            not self.current_slide.elements):
            self.current_slide.subtitle = text
        else:
            self.current_slide.elements.append(ContentElement(
                type=ContentType.PARAGRAPH,
                content=text
            ))

    def _add_image(self, path: str, alt_text: str = ""):
        """Add image content."""
        self._ensure_slide()

        # Only support local images
        if path.startswith(('http://', 'https://', 'data:')):
            self.warnings.append(f"Skipped non-local image: {path}")
            return

        self.current_slide.elements.append(ContentElement(
            type=ContentType.IMAGE,
            content=path,
            metadata={"alt_text": alt_text}
        ))

    def _parse_bullet_list(self, lines: List[str], start: int) -> int:
        """Parse bullet list and return next line index."""
        self._ensure_slide()
        items = []
        i = start

        while i < len(lines):
            match = re.match(r'^(\s*)[-*+]\s+(.+)$', lines[i])
            if match:
                indent = len(match.group(1))
                text = match.group(2).strip()
                items.append({"text": text, "indent": indent // 2})
                i += 1
            elif lines[i].strip() == "":
                i += 1
                # Check if list continues
                if i < len(lines) and re.match(r'^\s*[-*+]\s+', lines[i]):
                    continue
                break
            else:
                break

        if items:
            self.current_slide.elements.append(ContentElement(
                type=ContentType.BULLET_LIST,
                content=items
            ))

        return i

    def _parse_numbered_list(self, lines: List[str], start: int) -> int:
        """Parse numbered list and return next line index."""
        self._ensure_slide()
        items = []
        i = start

        while i < len(lines):
            match = re.match(r'^(\s*)\d+\.\s+(.+)$', lines[i])
            if match:
                indent = len(match.group(1))
                text = match.group(2).strip()
                items.append({"text": text, "indent": indent // 2})
                i += 1
            elif lines[i].strip() == "":
                i += 1
                if i < len(lines) and re.match(r'^\s*\d+\.\s+', lines[i]):
                    continue
                break
            else:
                break

        if items:
            self.current_slide.elements.append(ContentElement(
                type=ContentType.NUMBERED_LIST,
                content=items
            ))

        return i

    def _parse_code_block(self, lines: List[str], start: int) -> int:
        """Parse code block and return next line index."""
        self._ensure_slide()

        # Extract language from opening fence
        first_line = lines[start].strip()
        language = first_line[3:].strip() if len(first_line) > 3 else ""

        code_lines = []
        i = start + 1

        while i < len(lines):
            if lines[i].strip().startswith('```'):
                i += 1
                break
            code_lines.append(lines[i])
            i += 1

        self.current_slide.elements.append(ContentElement(
            type=ContentType.CODE_BLOCK,
            content='\n'.join(code_lines),
            metadata={"language": language}
        ))

        return i

    def _parse_table(self, lines: List[str], start: int) -> int:
        """Parse Markdown table and return next line index."""
        self._ensure_slide()

        headers = []
        rows = []
        i = start

        # Parse header row
        header_line = lines[i].strip()
        if header_line.startswith('|'):
            header_line = header_line[1:]
        if header_line.endswith('|'):
            header_line = header_line[:-1]
        headers = [cell.strip() for cell in header_line.split('|')]
        i += 1

        # Skip separator row
        if i < len(lines) and re.match(r'^\s*\|?\s*[-:]+', lines[i]):
            i += 1

        # Parse data rows
        while i < len(lines):
            line = lines[i].strip()
            if not line or not '|' in line:
                break

            if line.startswith('|'):
                line = line[1:]
            if line.endswith('|'):
                line = line[:-1]

            cells = [cell.strip() for cell in line.split('|')]
            rows.append(cells)
            i += 1

        self.current_slide.elements.append(ContentElement(
            type=ContentType.TABLE,
            content={"headers": headers, "rows": rows}
        ))

        return i

    def _determine_layouts(self):
        """Determine appropriate layout for each slide based on content."""
        for slide in self.slides:
            if slide.layout_hint == "title":
                continue

            has_image = any(e.type == ContentType.IMAGE for e in slide.elements)
            has_table = any(e.type == ContentType.TABLE for e in slide.elements)
            has_chart = any(e.type == ContentType.CHART_DATA for e in slide.elements)
            has_code = any(e.type == ContentType.CODE_BLOCK for e in slide.elements)

            element_count = len(slide.elements)

            if has_chart:
                slide.layout_hint = "chart"
            elif has_image and element_count <= 3:
                slide.layout_hint = "image"
            elif has_table or has_code:
                slide.layout_hint = "content"
            elif element_count > 4:
                slide.layout_hint = "two_column"
            else:
                slide.layout_hint = "content"

    def get_warnings(self) -> List[str]:
        """Return any warnings generated during parsing."""
        return self.warnings


def parse_markdown(markdown_text: str) -> tuple[List[SlideData], List[str]]:
    """
    Convenience function to parse Markdown text.

    Args:
        markdown_text: Raw Markdown content

    Returns:
        Tuple of (slides, warnings)
    """
    parser = MarkdownParser()
    slides = parser.parse(markdown_text)
    return slides, parser.get_warnings()


if __name__ == "__main__":
    # Test with sample markdown
    sample_md = """
# My Presentation

A sample presentation

## Introduction

This is the introduction slide.

- Point 1
- Point 2
- Point 3

## Code Example

Here's some code:

```python
def hello():
    print("Hello, World!")
```

## Data Table

| Name | Value |
|------|-------|
| A    | 100   |
| B    | 200   |

## Conclusion

Thank you!
"""

    slides, warnings = parse_markdown(sample_md)

    print(f"Parsed {len(slides)} slides:")
    for i, slide in enumerate(slides):
        print(f"\n--- Slide {i+1}: {slide.title} ({slide.layout_hint}) ---")
        if slide.subtitle:
            print(f"  Subtitle: {slide.subtitle}")
        for elem in slide.elements:
            print(f"  - {elem.type.value}: {str(elem.content)[:50]}...")

    if warnings:
        print(f"\nWarnings: {warnings}")
