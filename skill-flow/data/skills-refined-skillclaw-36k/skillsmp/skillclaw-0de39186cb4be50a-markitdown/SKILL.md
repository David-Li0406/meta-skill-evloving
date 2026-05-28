---
name: markitdown
description: Use this skill when you need to convert various file formats, such as PDF, DOCX, PPTX, and more, into Markdown for efficient text processing and analysis.
---

# MarkItDown - File to Markdown Conversion

## Overview

MarkItDown is a powerful tool for converting a wide range of file formats into Markdown, which is ideal for LLM processing due to its token efficiency and structured format.

**Key Benefits**:
- Converts documents to clean, structured Markdown.
- Supports over 15 file formats including PDF, DOCX, PPTX, XLSX, images (with OCR), audio (with transcription), HTML, CSV, JSON, XML, ZIP, YouTube URLs, and EPubs.
- Optional AI-enhanced image descriptions and OCR for images and scanned documents.

## Basic Usage

```bash
# Convert to stdout
uvx markitdown input.pdf

# Save to file
uvx markitdown input.pdf -o output.md
uvx markitdown input.docx > output.md

# From stdin
cat input.pdf | uvx markitdown
```

## Options

```bash
-o OUTPUT      # Specify output file
-x EXTENSION   # Hint file extension (for stdin)
-m MIME_TYPE   # Hint MIME type
-c CHARSET     # Hint charset (e.g., UTF-8)
-d             # Use Azure Document Intelligence for better extraction
-e ENDPOINT    # Document Intelligence endpoint
--use-plugins  # Enable 3rd-party plugins
--list-plugins # Show installed plugins
```

## Supported Formats

| Format      | Description              |
|-------------|--------------------------|
| **PDF**     | Portable Document Format |
| **DOCX**    | Microsoft Word Document  |
| **PPTX**    | Microsoft PowerPoint     |
| **XLSX**    | Microsoft Excel          |
| **HTML**    | HyperText Markup Language|
| **CSV**     | Comma-Separated Values   |
| **JSON**    | JavaScript Object Notation|
| **XML**     | eXtensible Markup Language|
| **Images**  | Various formats with OCR |
| **Audio**   | Various formats with transcription |
| **ZIP**     | Compressed archive files  |
| **YouTube** | Video URLs               |
| **EPub**    | Electronic Publication    |

## Visual Enhancement with Scientific Schematics

When creating documents with this skill, consider adding scientific diagrams and schematics to enhance visual communication. If your document does not already contain schematics or diagrams, use the **scientific-schematics** skill to generate AI-powered publication-quality diagrams.

**How to generate schematics:**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

The AI will automatically:
- Create publication-quality images with proper formatting.
- Review and refine through multiple iterations.
- Ensure accessibility (colorblind-friendly, high contrast).
- Save outputs in the figures/ directory.

**When to add schematics:**
- Document conversion workflow diagrams
- File format architecture illustrations
- OCR processing pipeline diagrams
- Integration workflow visualizations
- System architecture diagrams
- Data flow diagrams
- Any complex concept that benefits from visualization