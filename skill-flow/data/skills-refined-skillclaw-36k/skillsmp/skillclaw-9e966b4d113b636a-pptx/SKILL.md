---
name: pptx
description: Use this skill when you need to create, edit, or analyze presentations (.pptx files) for tasks such as modifying content, working with layouts, or adding comments and speaker notes.
---

# PPTX Creation, Editing, and Analysis

## Overview

A user may ask you to create, edit, or analyze the contents of a .pptx file. A .pptx file is essentially a ZIP archive containing XML files and other resources that you can read or edit. You have different tools and workflows available for different tasks.

## Reading and Analyzing Content

### Text Extraction

If you just need to read the text contents of a presentation, you should convert the document to markdown:

```bash
# Convert document to markdown
python -m markitdown path-to-file.pptx
```

### Raw XML Access

You need raw XML access for comments, speaker notes, slide layouts, animations, design elements, and complex formatting. For any of these features, you'll need to unpack a presentation and read its raw XML contents.

#### Unpacking a File

```bash
python ooxml/scripts/unpack.py <office_file> <output_dir>
```

**Note**: The `unpack.py` script is located at `skills/pptx/ooxml/scripts/unpack.py` relative to the project root. If the script doesn't exist at this path, use `find . -name "unpack.py"` to locate it.

#### Key File Structures

- `ppt/presentation.xml` - Main presentation metadata and slide references
- `ppt/slides/slide{N}.xml` - Individual slide contents (slide1.xml, slide2.xml, etc.)
- `ppt/notesSlides/notesSlide{N}.xml` - Speaker notes for each slide
- `ppt/comments/modernComment_*.xml` - Comments for specific slides
- `ppt/slideLayouts/` - Layout templates for slides
- `ppt/slideMasters/` - Master slide templates
- `ppt/theme/` - Theme and styling information
- `ppt/media/` - Images and other media files

### Typography and Color Extraction

**When given an example design to emulate**: Always analyze the presentation's typography and colors first using the methods below:

1. **Read theme file**: Check `ppt/theme/theme1.xml` for colors (`<a:clrScheme>`) and fonts (`<a:fontScheme>`)
2. **Sample slide content**: Examine `ppt/slides/slide1.xml` for actual font usage (`<a:rPr>`) and colors
3. **Search for patterns**: Use grep to find color (`<a:solidFill>`, `<a:srgbClr>`) and font references across all XML files

## Creating a New PowerPoint Presentation

### Basic Creation

To create a new PowerPoint presentation, you can use the `python-pptx` library. Here’s a simple example:

```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()

# Add title slide
title_slide_layout = prs.slide_layouts[0]
slide = prs.slides.add_slide(title_slide_layout)
title = slide.shapes.title
subtitle = slide.placeholders[1]
title.text = "Hello, World!"
subtitle.text = "python-pptx demo"

# Add content slide
bullet_slide_layout = prs.slide_layouts[1]
slide = prs.slides.add_slide(bullet_slide_layout)
shapes = slide.shapes
title_shape = shapes.title
body_shape = shapes.placeholders[1]
title_shape.text = "Key Points"
tf = body_shape.text_frame
tf.text = "First bullet point"
p = tf.add_paragraph()
p.text = "Second bullet point"
p.level = 1

prs.save('presentation.pptx')
```

### Adding Images

To add images to your presentation:

```python
from pptx.util import Inches

blank_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_layout)

left = Inches(1)
top = Inches(1)
width = Inches(5)
slide.shapes.add_picture('image.png', left, top, width=width)
```

### Adding Tables

To add tables to your presentation:

```python
rows, cols = 3, 4
left = Inches(1)
top = Inches(2)
width = Inches(6)
height = Inches(1.5)

table = slide.shapes.add_table(rows, cols, left, top, width, height).table

# Set column widths
table.columns[0].width = Inches(2)

# Add content
table.cell(0, 0).text = "Header 1"
table.cell(1, 0).text = "Data 1"
```

### Editing Existing Presentations

To edit an existing presentation:

```python
prs = Presentation('existing.pptx')

# Access slides
for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame:
            print(shape.text_frame.text)

# Modify text
slide = prs.slides[0]
slide.shapes.title.text = "New Title"

prs.save('modified.pptx')
```

## Best Practices

- Use slide layouts for consistency.
- Keep text minimal and use visuals effectively.