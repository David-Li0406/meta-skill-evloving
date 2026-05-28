---
name: pptx
description: Work with PowerPoint presentations (PPTX/PPT) - read slides, extract content, create presentations, convert formats, and generate slide decks. Use when the user asks to work with PowerPoint files or presentations.
allowed-tools: Read, Bash, Write
---

# PowerPoint (PPTX) Processing Skill

When working with PowerPoint presentations, follow these guidelines:

## 1. Reading & Extracting from PPTX

**Extract text content**:
```python
from pptx import Presentation

# Load presentation
prs = Presentation('presentation.pptx')

# Extract all text
for slide_num, slide in enumerate(prs.slides, 1):
    print(f"\n=== Slide {slide_num} ===")
    for shape in slide.shapes:
        if hasattr(shape, 'text'):
            print(shape.text)
```

**Extract with structure**:
```python
from pptx import Presentation

prs = Presentation('presentation.pptx')

for slide_num, slide in enumerate(prs.slides, 1):
    print(f"\nSlide {slide_num}:")

    # Title
    if slide.shapes.title:
        print(f"  Title: {slide.shapes.title.text}")

    # Content
    for shape in slide.shapes:
        if shape.has_text_frame:
            for paragraph in shape.text_frame.paragraphs:
                if paragraph.text:
                    print(f"    - {paragraph.text}")
```

**Extract images**:
```python
from pptx import Presentation
import os

prs = Presentation('presentation.pptx')
os.makedirs('extracted_images', exist_ok=True)

image_count = 0
for slide in prs.slides:
    for shape in slide.shapes:
        if shape.shape_type == 13:  # Picture
            image = shape.image
            image_bytes = image.blob
            image_filename = f'extracted_images/image_{image_count}.{image.ext}'
            with open(image_filename, 'wb') as f:
                f.write(image_bytes)
            image_count += 1

print(f"Extracted {image_count} images")
```

**Extract notes**:
```python
from pptx import Presentation

prs = Presentation('presentation.pptx')

for slide_num, slide in enumerate(prs.slides, 1):
    notes_slide = slide.notes_slide
    notes = notes_slide.notes_text_frame.text if notes_slide else ''
    if notes:
        print(f"Slide {slide_num} notes: {notes}")
```

## 2. Creating PPTX Files

**Create simple presentation**:
```python
from pptx import Presentation
from pptx.util import Inches, Pt

# Create presentation
prs = Presentation()

# Title slide
title_slide_layout = prs.slide_layouts[0]
slide = prs.slides.add_slide(title_slide_layout)
title = slide.shapes.title
subtitle = slide.placeholders[1]
title.text = "Presentation Title"
subtitle.text = "Your Name\n2026-01-22"

# Content slide
bullet_slide_layout = prs.slide_layouts[1]
slide = prs.slides.add_slide(bullet_slide_layout)
shapes = slide.shapes
title_shape = shapes.title
body_shape = shapes.placeholders[1]

title_shape.text = 'Key Points'
text_frame = body_shape.text_frame
text_frame.text = 'First point'

p = text_frame.add_paragraph()
p.text = 'Second point'
p.level = 0

p = text_frame.add_paragraph()
p.text = 'Sub-point'
p.level = 1

# Save
prs.save('presentation.pptx')
```

**Create from template**:
```python
from pptx import Presentation

# Load template
prs = Presentation('template.pptx')

# Add slides using template layouts
for i in range(5):
    slide_layout = prs.slide_layouts[1]  # Use content layout
    slide = prs.slides.add_slide(slide_layout)
    slide.shapes.title.text = f"Slide {i+1}"

prs.save('from_template.pptx')
```

**Add images and charts**:
```python
from pptx import Presentation
from pptx.util import Inches
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

prs = Presentation()

# Add image slide
blank_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_layout)

# Add title
title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.5))
title_box.text = "Image Slide"

# Add image
img_path = 'image.jpg'
left = Inches(2)
top = Inches(1.5)
slide.shapes.add_picture(img_path, left, top, width=Inches(5))

# Add chart slide
slide = prs.slides.add_slide(blank_layout)

# Create chart data
chart_data = CategoryChartData()
chart_data.categories = ['Q1', 'Q2', 'Q3', 'Q4']
chart_data.add_series('Sales', (10, 15, 13, 20))

# Add chart
x, y, cx, cy = Inches(1), Inches(1.5), Inches(8), Inches(4.5)
chart = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data
).chart
chart.has_legend = True

prs.save('presentation.pptx')
```

## 3. Converting PPTX

**PPTX to PDF**:
```bash
# Using LibreOffice
libreoffice --headless --convert-to pdf presentation.pptx

# With output directory
libreoffice --headless --convert-to pdf --outdir ./output presentation.pptx
```

**PPTX to Images (PNG/JPG)**:
```bash
# Using LibreOffice (converts to PDF first, then images)
libreoffice --headless --convert-to pdf presentation.pptx
pdftoppm presentation.pdf slides -png

# Or using Python
```

```python
from pptx import Presentation
import subprocess

# Convert to PDF first
subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', 'presentation.pptx'])

# Then PDF to images
subprocess.run(['pdftoppm', '-png', '-r', '300', 'presentation.pdf', 'slides'])
```

**PPTX to HTML**:
```bash
# Using pandoc (preserves content, not design)
pandoc presentation.pptx -o output.html

# Using LibreOffice
libreoffice --headless --convert-to html presentation.pptx
```

**PPT to PPTX**:
```bash
# Using LibreOffice
libreoffice --headless --convert-to pptx presentation.ppt
```

## 4. Modifying Presentations

**Add slide to existing presentation**:
```python
from pptx import Presentation

# Load existing
prs = Presentation('existing.pptx')

# Add new slide
slide_layout = prs.slide_layouts[1]
slide = prs.slides.add_slide(slide_layout)
slide.shapes.title.text = "New Slide"

# Save
prs.save('existing.pptx')
```

**Replace text globally**:
```python
from pptx import Presentation

def replace_text_in_presentation(pptx_path, search, replace):
    prs = Presentation(pptx_path)

    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                text_frame = shape.text_frame
                for paragraph in text_frame.paragraphs:
                    for run in paragraph.runs:
                        if search in run.text:
                            run.text = run.text.replace(search, replace)

    prs.save(pptx_path)

replace_text_in_presentation('presentation.pptx', '{NAME}', 'John Doe')
```

**Delete slides**:
```python
from pptx import Presentation
from lxml import etree

def delete_slide(prs, index):
    # Get slide
    slide = prs.slides[index]

    # Remove from slide list
    rId = prs.slides._sldIdLst[index].rId
    prs.part.drop_rel(rId)
    del prs.slides._sldIdLst[index]

prs = Presentation('presentation.pptx')
delete_slide(prs, 2)  # Delete 3rd slide (0-indexed)
prs.save('presentation.pptx')
```

## 5. Formatting & Styling

**Text formatting**:
```python
from pptx import Presentation
from pptx.util import Pt, Inches
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[6])

# Add text box
textbox = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(8), Inches(1))
text_frame = textbox.text_frame

# Add paragraph
p = text_frame.paragraphs[0]
run = p.add_run()
run.text = "Formatted Text"

# Font styling
font = run.font
font.name = 'Arial'
font.size = Pt(32)
font.bold = True
font.italic = False
font.color.rgb = RGBColor(255, 0, 0)

# Paragraph alignment
p.alignment = PP_ALIGN.CENTER

prs.save('formatted.pptx')
```

**Slide background**:
```python
from pptx import Presentation
from pptx.util import Inches
from pptx.enum.dml import MSO_THEME_COLOR

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[6])

# Solid color background
background = slide.background
fill = background.fill
fill.solid()
fill.fore_color.rgb = RGBColor(0, 102, 204)

# Or image background
fill.background()
fill.fore_color.theme_color = MSO_THEME_COLOR.BACKGROUND_1

prs.save('backgrounds.pptx')
```

**Table formatting**:
```python
from pptx import Presentation
from pptx.util import Inches
from pptx.enum.text import PP_ALIGN

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[6])

# Add table
rows, cols = 4, 3
left, top, width, height = Inches(1), Inches(1.5), Inches(8), Inches(3)
table = slide.shapes.add_table(rows, cols, left, top, width, height).table

# Set column widths
table.columns[0].width = Inches(3)
table.columns[1].width = Inches(2.5)
table.columns[2].width = Inches(2.5)

# Add data
headers = ['Product', 'Sales', 'Profit']
data = [
    ['Product A', '$1,000', '$300'],
    ['Product B', '$1,500', '$450'],
    ['Product C', '$800', '$200']
]

# Headers
for i, header in enumerate(headers):
    cell = table.cell(0, i)
    cell.text = header
    cell.text_frame.paragraphs[0].font.bold = True
    cell.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

# Data
for i, row_data in enumerate(data, 1):
    for j, value in enumerate(row_data):
        table.cell(i, j).text = value

prs.save('table.pptx')
```

## 6. Analyzing Presentations

**Get presentation info**:
```python
from pptx import Presentation

prs = Presentation('presentation.pptx')

print(f"Slides: {len(prs.slides)}")
print(f"Slide size: {prs.slide_width} x {prs.slide_height}")

# Layout info
print(f"\nAvailable layouts:")
for i, layout in enumerate(prs.slide_layouts):
    print(f"  {i}: {layout.name}")

# Slide content summary
for slide_num, slide in enumerate(prs.slides, 1):
    shapes_count = len(slide.shapes)
    text_count = sum(1 for s in slide.shapes if s.has_text_frame)
    image_count = sum(1 for s in slide.shapes if s.shape_type == 13)

    print(f"\nSlide {slide_num}:")
    print(f"  Shapes: {shapes_count}, Text: {text_count}, Images: {image_count}")
```

## 7. Common Workflows

### Generate presentation from data
```python
from pptx import Presentation
from pptx.util import Inches
import json

# Load data
with open('data.json') as f:
    data = json.load(f)

prs = Presentation()

# Title slide
title_slide = prs.slides.add_slide(prs.slide_layouts[0])
title_slide.shapes.title.text = data['title']
title_slide.placeholders[1].text = data['subtitle']

# Content slides
for section in data['sections']:
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = section['title']

    text_frame = slide.placeholders[1].text_frame
    for point in section['points']:
        p = text_frame.add_paragraph() if text_frame.text else text_frame.paragraphs[0]
        p.text = point
        p.level = 0

prs.save('generated.pptx')
```

### Merge presentations
```python
from pptx import Presentation

def merge_presentations(output_file, *input_files):
    prs = Presentation(input_files[0])

    for pptx_file in input_files[1:]:
        source_prs = Presentation(pptx_file)
        for slide in source_prs.slides:
            # Copy slide (simplified - doesn't preserve all formatting)
            slide_layout = prs.slide_layouts[6]  # Blank
            new_slide = prs.slides.add_slide(slide_layout)

            for shape in slide.shapes:
                # Copy each shape (basic implementation)
                pass  # Full implementation would need detailed shape copying

    prs.save(output_file)

# Usage
merge_presentations('merged.pptx', 'pres1.pptx', 'pres2.pptx')
```

### Extract speaker notes to document
```python
from pptx import Presentation

prs = Presentation('presentation.pptx')

with open('speaker_notes.txt', 'w') as f:
    for slide_num, slide in enumerate(prs.slides, 1):
        notes_slide = slide.notes_slide
        notes = notes_slide.notes_text_frame.text if notes_slide else ''

        # Title
        title = slide.shapes.title.text if slide.shapes.title else f"Slide {slide_num}"

        f.write(f"=== {title} ===\n")
        if notes:
            f.write(f"{notes}\n\n")
        else:
            f.write("(No notes)\n\n")
```

## Tools Required

Install necessary tools:

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get install python3-pip libreoffice poppler-utils
pip3 install python-pptx Pillow
```

**macOS**:
```bash
brew install libreoffice poppler
pip3 install python-pptx Pillow
```

**Windows**:
```powershell
pip install python-pptx Pillow
# Install LibreOffice manually
```

## Security Notes

- ✅ Validate file paths and extensions
- ✅ Check file sizes before processing
- ✅ Be cautious with macro-enabled presentations (.pptm)
- ✅ Sanitize user input in text replacements
- ✅ Validate image sources
- ✅ Don't execute embedded scripts
- ✅ Scan files from untrusted sources

## When to Use This Skill

Use `/pptx` when the user:
- Wants to read or extract content from PowerPoint files
- Needs to create presentations from data or templates
- Wants to convert PPTX to other formats (PDF, images, HTML)
- Asks to modify existing presentations
- Needs to extract speaker notes or images
- Wants to merge or split presentations
- Asks to generate slide decks programmatically
- Needs to analyze presentation structure

Always confirm before overwriting existing presentation files.
