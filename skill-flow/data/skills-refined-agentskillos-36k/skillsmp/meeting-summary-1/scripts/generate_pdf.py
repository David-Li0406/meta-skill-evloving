#!/usr/bin/env python3
"""
Generate a professional PDF from a meeting summary markdown file.

Usage:
    python generate_pdf.py <input_markdown> [output_pdf]

If output_pdf is not specified, creates PDF in same directory as input with .pdf extension.
"""

import sys
import re
import os
import urllib.request
import zipfile
from pathlib import Path

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, HRFlowable, ListFlowable, ListItem, KeepTogether
    )
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("Error: reportlab not installed. Run: pip install reportlab")
    sys.exit(1)

# Font configuration
FONTS_DIR = Path.home() / ".claude" / "fonts"
IBM_PLEX_FONTS = {
    "IBMPlexSans": "IBMPlexSans-Regular.ttf",
    "IBMPlexSans-Bold": "IBMPlexSans-Bold.ttf",
    "IBMPlexSans-Italic": "IBMPlexSans-Italic.ttf",
    "IBMPlexSans-BoldItalic": "IBMPlexSans-BoldItalic.ttf",
}


def setup_fonts():
    """Download and register IBM Plex fonts if not present."""
    FONTS_DIR.mkdir(parents=True, exist_ok=True)

    # Check if fonts already exist
    fonts_present = all((FONTS_DIR / f).exists() for f in IBM_PLEX_FONTS.values())

    if not fonts_present:
        print("Downloading IBM Plex fonts...")
        zip_url = "https://github.com/IBM/plex/releases/download/v6.4.0/IBM-Plex-Sans.zip"
        zip_path = FONTS_DIR / "ibm-plex-sans.zip"

        try:
            urllib.request.urlretrieve(zip_url, zip_path)
            with zipfile.ZipFile(zip_path, 'r') as zf:
                for font_file in IBM_PLEX_FONTS.values():
                    for name in zf.namelist():
                        if name.endswith(font_file):
                            # Extract just the font file
                            data = zf.read(name)
                            (FONTS_DIR / font_file).write_bytes(data)
                            break
            zip_path.unlink()  # Clean up zip
            print("Fonts installed successfully.")
        except Exception as e:
            print(f"Warning: Could not download fonts ({e}). Using defaults.")
            return False

    # Register fonts with reportlab
    try:
        for font_name, font_file in IBM_PLEX_FONTS.items():
            font_path = FONTS_DIR / font_file
            if font_path.exists():
                pdfmetrics.registerFont(TTFont(font_name, str(font_path)))

        # Register font family for bold/italic handling
        from reportlab.pdfbase.pdfmetrics import registerFontFamily
        registerFontFamily(
            'IBMPlexSans',
            normal='IBMPlexSans',
            bold='IBMPlexSans-Bold',
            italic='IBMPlexSans-Italic',
            boldItalic='IBMPlexSans-BoldItalic'
        )
        return True
    except Exception as e:
        print(f"Warning: Could not register fonts ({e}). Using defaults.")
        return False


# Initialize fonts
USE_IBM_PLEX = setup_fonts()
BODY_FONT = 'IBMPlexSans' if USE_IBM_PLEX else 'Helvetica'
BOLD_FONT = 'IBMPlexSans-Bold' if USE_IBM_PLEX else 'Helvetica-Bold'
ITALIC_FONT = 'IBMPlexSans-Italic' if USE_IBM_PLEX else 'Helvetica-Oblique'

# Colors
PRIMARY_COLOR = HexColor("#1a365d")   # Dark blue
ACCENT_COLOR = HexColor("#2b6cb0")    # Medium blue
LIGHT_BG = HexColor("#f7fafc")        # Light gray background
TABLE_BORDER = HexColor("#8a9aad")    # Medium gray for table borders (visible but not heavy)
TEXT_GRAY = HexColor("#4a5568")       # Gray for quotes
FOOTER_GRAY = HexColor("#718096")     # Lighter gray for footer


def create_styles():
    """Create all paragraph styles for the PDF."""
    styles = getSampleStyleSheet()

    custom_styles = {
        # Title page styles
        'TitleMain': ParagraphStyle(
            'TitleMain',
            fontName=BOLD_FONT,
            fontSize=32,
            textColor=PRIMARY_COLOR,
            spaceAfter=6,
            alignment=TA_CENTER,
            leading=38
        ),
        'MetaField': ParagraphStyle(
            'MetaField',
            fontName=BODY_FONT,
            fontSize=11,
            alignment=TA_CENTER,
            spaceAfter=6,
            leading=14
        ),
        'CustomTitle': ParagraphStyle(
            'CustomTitle',
            fontName=BOLD_FONT,
            fontSize=28,
            textColor=PRIMARY_COLOR,
            spaceAfter=6,
            alignment=TA_CENTER
        ),
        'Subtitle': ParagraphStyle(
            'Subtitle',
            fontName=BODY_FONT,
            fontSize=12,
            textColor=ACCENT_COLOR,
            alignment=TA_CENTER,
            spaceAfter=20
        ),
        'Meta': ParagraphStyle(
            'Meta',
            fontName=BODY_FONT,
            alignment=TA_CENTER,
            fontSize=11
        ),
        'CustomH1': ParagraphStyle(
            'CustomH1',
            fontName=BOLD_FONT,
            fontSize=20,
            textColor=PRIMARY_COLOR,
            spaceBefore=28,
            spaceAfter=12
        ),
        'CustomH2': ParagraphStyle(
            'CustomH2',
            fontName=BOLD_FONT,
            fontSize=14,
            textColor=ACCENT_COLOR,
            spaceBefore=20,
            spaceAfter=10
        ),
        'CustomH3': ParagraphStyle(
            'CustomH3',
            fontName=BOLD_FONT,
            fontSize=12,
            textColor=ACCENT_COLOR,
            spaceBefore=16,
            spaceAfter=8
        ),
        'CustomBody': ParagraphStyle(
            'CustomBody',
            fontName=BODY_FONT,
            fontSize=10,
            leading=15,
            spaceAfter=10
        ),
        'Bullet': ParagraphStyle(
            'Bullet',
            fontName=BODY_FONT,
            fontSize=10,
            leading=15,
            leftIndent=20,
            bulletIndent=10,
            spaceAfter=6
        ),
        'Quote': ParagraphStyle(
            'Quote',
            fontName=ITALIC_FONT,
            fontSize=10,
            leading=15,
            leftIndent=30,
            rightIndent=30,
            textColor=TEXT_GRAY,
            spaceBefore=8,
            spaceAfter=12
        ),
        'Footer': ParagraphStyle(
            'Footer',
            fontName=BODY_FONT,
            alignment=TA_CENTER,
            fontSize=9,
            textColor=FOOTER_GRAY
        )
    }

    return custom_styles


def make_table_style():
    """Create consistent table styling."""
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), BOLD_FONT),
        ('FONTNAME', (0, 1), (-1, -1), BODY_FONT),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, TABLE_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ])


def extract_title_page(content):
    """Extract title and metadata for special title page treatment.

    Returns (title, metadata_list, remaining_content) where:
    - title: The main document title (from first # heading)
    - metadata_list: List of (label, value) tuples for metadata fields
    - remaining_content: Content after the title page section
    """
    lines = content.split('\n')
    title = None
    metadata = []
    content_start_idx = 0

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines at the start
        if not line:
            i += 1
            continue

        # First # heading is the title
        if line.startswith('# ') and title is None:
            title = line[2:].strip()
            i += 1
            continue

        # If we have a title, look for metadata lines like "**Label:** Value"
        if title is not None:
            # Check for metadata pattern: **Label:** Value or **Label**: Value
            meta_match = re.match(r'^\*\*([^*]+)\*\*:?\s*(.+)$', line)
            if meta_match:
                label = meta_match.group(1).strip().rstrip(':')
                value = meta_match.group(2).strip()
                metadata.append((label, value))
                i += 1
                continue

            # Horizontal rule signals end of title page section
            if re.match(r'^---+$', line):
                content_start_idx = i + 1
                break

            # Any other heading signals end of title section
            if line.startswith('#'):
                content_start_idx = i
                break

        i += 1

    # If we consumed everything without finding content start
    if content_start_idx == 0:
        content_start_idx = i

    remaining_content = '\n'.join(lines[content_start_idx:])
    return title, metadata, remaining_content


def build_title_page(title, metadata, styles):
    """Build the title page flowables."""
    elements = []

    if not title:
        return elements

    # Add some top spacing
    elements.append(Spacer(1, 0.5*inch))

    # Main title - can be multi-line, split on newline or " - "
    title_parts = re.split(r'\s+-\s+|\n', title, maxsplit=1)
    if len(title_parts) == 2:
        # Two-line title (e.g., "Company Name" + "Meeting Type")
        elements.append(Paragraph(title_parts[0].strip(), styles['TitleMain']))
        elements.append(Paragraph(title_parts[1].strip(), styles['TitleMain']))
    else:
        elements.append(Paragraph(title, styles['TitleMain']))

    # Horizontal rule under title
    elements.append(Spacer(1, 0.15*inch))
    elements.append(HRFlowable(
        width="35%",
        thickness=2,
        color=PRIMARY_COLOR,
        spaceBefore=0,
        spaceAfter=0,
        hAlign='CENTER'
    ))
    elements.append(Spacer(1, 0.4*inch))

    # Metadata fields, each on own line, centered
    for label, value in metadata:
        # Format: **Label:** Value
        meta_text = f'<b>{label}:</b> {value}'
        elements.append(Paragraph(meta_text, styles['MetaField']))

    # Large spacer before content
    elements.append(Spacer(1, 0.8*inch))

    return elements


def parse_markdown_table(lines):
    """Parse a markdown table into rows."""
    rows = []
    for line in lines:
        if line.strip().startswith('|') and not re.match(r'^\|[\s\-:|]+\|$', line):
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            rows.append(cells)
    return rows


def clean_markdown_formatting(text):
    """Convert markdown formatting to reportlab markup."""
    # Bold: **text** or __text__ -> <b>text</b>
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.+?)__', r'<b>\1</b>', text)
    # Italic: *text* or _text_ -> <i>text</i>
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'(?<![_\w])_([^_]+?)_(?![_\w])', r'<i>\1</i>', text)
    # Inline code: `text` -> text (just remove backticks)
    text = re.sub(r'`(.+?)`', r'\1', text)
    return text


def parse_markdown(content, styles):
    """Parse markdown content and convert to reportlab flowables."""
    story = []
    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Horizontal rule
        if re.match(r'^---+$', line):
            story.append(HRFlowable(width="100%", thickness=1, color=LIGHT_BG, spaceBefore=10, spaceAfter=10))
            i += 1
            continue

        # H1 heading
        if line.startswith('# '):
            text = clean_markdown_formatting(line[2:])
            story.append(Paragraph(text, styles['CustomH1']))
            story.append(HRFlowable(width="100%", thickness=1, color=LIGHT_BG, spaceBefore=0, spaceAfter=10))
            i += 1
            continue

        # H2 heading
        if line.startswith('## '):
            text = clean_markdown_formatting(line[3:])
            story.append(Paragraph(text, styles['CustomH2']))
            i += 1
            continue

        # H3 heading
        if line.startswith('### '):
            text = clean_markdown_formatting(line[4:])
            story.append(Paragraph(text, styles['CustomH3']))
            i += 1
            continue

        # Table detection
        if line.startswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i])
                i += 1

            rows = parse_markdown_table(table_lines)
            if rows:
                num_cols = len(rows[0]) if rows else 0
                if num_cols > 0:
                    available_width = 6.5 * inch

                    # Calculate column widths based on content length
                    col_char_counts = [0] * num_cols
                    for row in rows:
                        for j, cell in enumerate(row):
                            if j < num_cols:
                                col_char_counts[j] = max(col_char_counts[j], len(cell))

                    total_chars = sum(col_char_counts) or 1
                    col_widths = [(count / total_chars) * available_width for count in col_char_counts]

                    # Ensure minimum column width based on content type
                    # First column (often names) needs more space to avoid breaking
                    min_width_first = 1.1 * inch
                    min_width_other = 0.7 * inch

                    for j in range(num_cols):
                        min_w = min_width_first if j == 0 else min_width_other
                        if col_widths[j] < min_w:
                            col_widths[j] = min_w

                    # Re-normalize so total equals available width
                    current_total = sum(col_widths)
                    scale = available_width / current_total
                    col_widths = [w * scale for w in col_widths]

                    # Create cell style for wrapping text (word boundaries only)
                    cell_style = ParagraphStyle(
                        'TableCell',
                        fontName=BODY_FONT,
                        fontSize=9,
                        leading=11,
                    )
                    header_style = ParagraphStyle(
                        'TableHeader',
                        fontName=BOLD_FONT,
                        fontSize=10,
                        leading=12,
                        textColor=colors.white,
                    )

                    # Convert cells to Paragraphs for proper wrapping
                    formatted_rows = []
                    for row_idx, row in enumerate(rows):
                        formatted_row = []
                        for cell in row:
                            cleaned_cell = clean_markdown_formatting(cell)
                            if row_idx == 0:
                                formatted_row.append(Paragraph(cleaned_cell, header_style))
                            else:
                                formatted_row.append(Paragraph(cleaned_cell, cell_style))
                        formatted_rows.append(formatted_row)

                    t = Table(formatted_rows, colWidths=col_widths, splitByRow=False)
                    t.setStyle(make_table_style())
                    # Keep entire table on one page - splitByRow=False prevents row splitting,
                    # KeepTogether moves the whole table to next page if it doesn't fit
                    story.append(KeepTogether([t, Spacer(1, 0.15*inch)]))
            continue

        # Bullet points
        if re.match(r'^[\-\*]\s', line):
            text = clean_markdown_formatting(line[2:])
            story.append(Paragraph(f"• {text}", styles['Bullet']))
            i += 1
            continue

        # Numbered lists
        if re.match(r'^\d+\.\s', line):
            text = clean_markdown_formatting(re.sub(r'^\d+\.\s', '', line))
            # Keep the number
            num = re.match(r'^(\d+)\.\s', line).group(1)
            story.append(Paragraph(f"{num}. {text}", styles['Bullet']))
            i += 1
            continue

        # Blockquote
        if line.startswith('>'):
            text = clean_markdown_formatting(line[1:].strip())
            story.append(Paragraph(text, styles['Quote']))
            i += 1
            continue

        # Code block - skip
        if line.startswith('```'):
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                i += 1
            i += 1
            continue

        # Regular paragraph
        text = clean_markdown_formatting(line)
        story.append(Paragraph(text, styles['CustomBody']))
        i += 1

    return story


def get_versioned_output_path(base_path):
    """Get next available versioned path if base already exists.

    Example: Summary.pdf exists → returns Summary_v2.pdf
             Summary_v2.pdf exists → returns Summary_v3.pdf

    Args:
        base_path: The default output path (e.g., "Meeting Summary.pdf")

    Returns:
        Path object - either base_path if it doesn't exist, or next versioned path
    """
    base_path = Path(base_path)
    if not base_path.exists():
        return base_path

    # Find existing versions
    stem = base_path.stem  # "Summary"
    suffix = base_path.suffix  # ".pdf"
    parent = base_path.parent

    # Check for _vN pattern in existing files
    pattern = f"{stem}_v*.pdf"
    existing = list(parent.glob(pattern))

    if not existing:
        # First version after original
        return parent / f"{stem}_v2{suffix}"

    # Find highest version number
    max_version = 1
    version_re = re.compile(rf"{re.escape(stem)}_v(\d+)\.pdf$")
    for path in existing:
        match = version_re.match(path.name)
        if match:
            max_version = max(max_version, int(match.group(1)))

    return parent / f"{stem}_v{max_version + 1}{suffix}"


def generate_pdf(input_path, output_path=None):
    """Generate PDF from markdown file.

    If output_path is not specified and the default PDF already exists,
    a versioned filename will be used (e.g., Summary_v2.pdf) to preserve
    the existing file.
    """
    input_path = Path(input_path)

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    # Determine output path with versioning support
    if output_path is None:
        base_output = input_path.with_suffix('.pdf')
        output_path = get_versioned_output_path(base_output)
        is_versioned = output_path != base_output
    else:
        output_path = Path(output_path)
        is_versioned = False

    # Read markdown content
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Create document
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    # Create styles
    styles = create_styles()

    # Extract title page content and build it separately
    title, metadata, remaining_content = extract_title_page(content)
    story = build_title_page(title, metadata, styles)

    # Parse remaining content
    story.extend(parse_markdown(remaining_content, styles))

    # Add footer
    story.append(Spacer(1, 0.5*inch))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT_COLOR, spaceBefore=20, spaceAfter=10))
    story.append(Paragraph("Generated with Revtelligent Meeting Summary", styles['Footer']))

    # Build PDF
    doc.build(story)
    if is_versioned:
        print(f"PDF created: {output_path} (previous version preserved)")
    else:
        print(f"PDF created: {output_path}")
    return output_path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    generate_pdf(input_file, output_file)
