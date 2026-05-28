---
name: pptx
description: "Use this skill for creating, editing, and analyzing PowerPoint presentations (.pptx files) including tasks like modifying content, working with layouts, and adding speaker notes."
---

# PPTX Creation, Editing, and Analysis

## Overview

A .pptx file is a ZIP archive containing XML files and resources. This skill allows you to create, edit, or analyze PowerPoint presentations programmatically.

## Reading and Analyzing Content

### Text Extraction

To read the text contents of a presentation, convert the document to markdown:

```bash
# Convert document to markdown
python -m markitdown path-to-file.pptx
```

### Raw XML Access

Raw XML access is required for comments, speaker notes, slide layouts, animations, design elements, and complex formatting. To access these features, unpack a presentation and read its raw XML contents.

#### Unpacking a File

```bash
python ooxml/scripts/unpack.py <office_file> <output_dir>
```

**Key File Structures:**
- `ppt/presentation.xml` - Main presentation metadata and slide references
- `ppt/slides/slide{N}.xml` - Individual slide contents
- `ppt/notesSlides/notesSlide{N}.xml` - Speaker notes for each slide
- `ppt/comments/modernComment_*.xml` - Comments for specific slides
- `ppt/slideLayouts/` - Layout templates for slides
- `ppt/slideMasters/` - Master slide templates
- `ppt/theme/` - Theme and styling information
- `ppt/media/` - Images and other media files

### Typography and Color Extraction

When given an example design to emulate, analyze the presentation's typography and colors using the following methods:

1. **Read Theme File**: Check `ppt/theme/theme1.xml` for colors and fonts.
2. **Sample Slide Content**: Examine `ppt/slides/slide1.xml` for actual font usage and colors.
3. **Search for Patterns**: Use grep to find color and font references across all XML files.

## Creating a New PowerPoint Presentation

### Without a Template

When creating a new PowerPoint presentation from scratch, use the **html2pptx** workflow to convert HTML slides to PowerPoint with accurate positioning.

#### Design Principles

- Analyze the content and choose appropriate design elements.
- Consider the subject matter, branding, and color palette.
- Use web-safe fonts and ensure readability with strong contrast.

#### Color Palette Selection

Choose colors creatively, ensuring they match the topic and maintain readability. Here are some example color palettes:

1. **Classic Blue**: Deep navy, slate gray, silver, off-white
2. **Teal & Coral**: Teal, deep teal, coral, white
3. **Bold Red**: Red, bright red, orange, yellow, green

### With a Template

To create a presentation that follows an existing template's design, duplicate and rearrange template slides before replacing placeholder content.

#### Workflow

1. **Extract Template Text and Create Visual Thumbnail Grid**:
   ```bash
   python -m markitdown template.pptx > template-content.md
   python scripts/thumbnail.py template.pptx
   ```

2. **Analyze Template and Save Inventory**:
   Create a template inventory file to understand slide layouts and design patterns.

3. **Create Presentation Outline**:
   Match layout structure to actual content and save the outline with content and template mapping.

4. **Duplicate, Reorder, and Delete Slides**:
   Use the `scripts/rearrange.py` script to create a new presentation with slides in the desired order.

5. **Extract All Text**:
   Use the `inventory.py` script to extract text from the presentation.

6. **Generate Replacement Text**:
   Create a JSON file with replacement text based on the inventory.

7. **Apply Replacements**:
   Use the `replace.py` script to apply new text to the presentation.

## Editing an Existing PowerPoint Presentation

To edit slides in an existing PowerPoint presentation, work with the raw Office Open XML (OOXML) format.

### Workflow

1. **Unpack the Presentation**:
   ```bash
   python ooxml/scripts/unpack.py <office_file> <output_dir>
   ```

2. **Edit the XML Files**:
   Modify the XML files as needed.

3. **Validate Changes**:
   Validate immediately after each edit to ensure no errors.

4. **Pack the Final Presentation**:
   ```bash
   python ooxml/scripts/pack.py <input_directory> <office_file>
   ```

## Creating Thumbnail Grids

To create visual thumbnail grids of PowerPoint slides for quick analysis and reference:

```bash
python scripts/thumbnail.py template.pptx [output_prefix]
```

## Converting Slides to Images

To visually analyze PowerPoint slides, convert them to images using a two-step process:

1. **Convert PPTX to PDF**:
   ```bash
   soffice --headless --convert-to pdf template.pptx
   ```

2. **Convert PDF Pages to JPEG Images**:
   ```bash
   pdftoppm -jpeg -r 150 template.pdf slide
   ```

## Best Practices

- Use slide layouts for consistency.
- Keep text minimal and use visuals.
- Save frequently during creation.

## Dependencies

Required dependencies (should already be installed):

- **markitdown**: `pip install "markitdown[pptx]"`
- **pptxgenjs**: `npm install -g pptxgenjs`
- **playwright**: `npm install -g playwright`
- **sharp**: `npm install -g sharp`
- **LibreOffice**: `sudo apt-get install libreoffice`
- **Poppler**: `sudo apt-get install poppler-utils`
- **defusedxml**: `pip install defusedxml`