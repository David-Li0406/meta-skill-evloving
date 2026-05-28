---
name: docx
description: "Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. Use when working with professional documents (.docx files) for creating new documents, modifying content, working with tracked changes, adding comments, or any other document tasks."
---

# DOCX Creation, Editing, and Analysis

## Overview

A .docx file is essentially a ZIP archive containing XML files and other resources that can be read or edited. This skill provides various tools and workflows for creating, editing, and analyzing Word documents.

## Workflow Decision Tree

### Reading/Analyzing Content
- Use "Text extraction" or "Raw XML access" sections below.

### Creating New Document
- Use "Creating a new Word document" workflow.

### Editing Existing Document
- **Your own document + simple changes**: Use "Basic OOXML editing" workflow.
- **Someone else's document**: Use **"Redlining workflow"** (recommended default).
- **Legal, academic, business, or government docs**: Use **"Redlining workflow"** (required).

## Reading and Analyzing Content

### Text Extraction
To read the text contents of a document, convert the document to markdown using pandoc, which preserves document structure and can show tracked changes:

```bash
# Convert document to markdown with tracked changes
pandoc --track-changes=all path-to-file.docx -o output.md
# Options: --track-changes=accept/reject/all
```

### Raw XML Access
Raw XML access is required for comments, complex formatting, document structure, embedded media, and metadata. Unpack a document and read its raw XML contents:

```bash
python ooxml/scripts/unpack.py <office_file> <output_directory>
```

#### Key File Structures
- `word/document.xml`: Main document contents.
- `word/comments.xml`: Comments referenced in document.xml.
- `word/media/`: Embedded images and media files.
- Tracked changes use `<w:ins>` (insertions) and `<w:del>` (deletions) tags.

## Creating a New Word Document

When creating a new Word document from scratch, use **docx-js**, which allows you to create Word documents using JavaScript/TypeScript.

### Workflow
1. **MANDATORY - READ ENTIRE FILE**: Read [`docx-js.md`](docx-js.md) completely from start to finish. **NEVER set any range limits when reading this file.**
2. Create a JavaScript/TypeScript file using Document, Paragraph, TextRun components.
3. Export as .docx using Packer.toBuffer().

## Editing an Existing Word Document

When editing an existing Word document, use the **Document library** (a Python library for OOXML manipulation). The library automatically handles infrastructure setup and provides methods for document manipulation.

### Workflow
1. **MANDATORY - READ ENTIRE FILE**: Read [`ooxml.md`](ooxml.md) completely from start to finish. **NEVER set any range limits when reading this file.**
2. Unpack the document: `python ooxml/scripts/unpack.py <office_file> <output_directory>`.
3. Create and run a Python script using the Document library.
4. Pack the final document: `python ooxml/scripts/pack.py <input_directory> <office_file>`.

## Redlining Workflow for Document Review

This workflow allows planning comprehensive tracked changes using markdown before implementing them in OOXML. **CRITICAL**: For complete tracked changes, implement ALL changes systematically.

### Batching Strategy
Group related changes into batches of 3-10 changes for manageable debugging and efficiency.

### Principle: Minimal, Precise Edits
Only mark text that actually changes. Preserve the original run's RSID for unchanged text by extracting the `<w:r>` element from the original and reusing it.

### Tracked Changes Workflow
1. **Get markdown representation**: Convert document to markdown with tracked changes preserved:
   ```bash
   pandoc --track-changes=all path-to-file.docx -o current.md
   ```

2. **Identify and group changes**: Review the document and identify ALL changes needed, organizing them into logical batches.

3. **Read documentation and unpack**:
   - **MANDATORY - READ ENTIRE FILE**: Read [`ooxml.md`](ooxml.md) completely from start to finish.
   - **Unpack the document**: `python ooxml/scripts/unpack.py <file.docx> <dir>`.

4. **Implement changes in batches**: Group changes logically and implement them together in a single script.

5. **Pack the document**: After all batches are complete, convert the unpacked directory back to .docx:
   ```bash
   python ooxml/scripts/pack.py unpacked reviewed-document.docx
   ```

6. **Final verification**: Convert final document to markdown and verify ALL changes were applied correctly.

## Converting Documents to Images

To visually analyze Word documents, convert them to images using a two-step process:

1. **Convert DOCX to PDF**:
   ```bash
   soffice --headless --convert-to pdf document.docx
   ```

2. **Convert PDF pages to JPEG images**:
   ```bash
   pdftoppm -jpeg -r 150 document.pdf page
   ```

### Options
- `-r 150`: Sets resolution to 150 DPI.
- `-jpeg`: Output JPEG format (use `-png` for PNG if preferred).
- `-f N`: First page to convert.
- `-l N`: Last page to convert.
- `page`: Prefix for output files.

## Code Style Guidelines
**IMPORTANT**: When generating code for DOCX operations:
- Write concise code.
- Avoid verbose variable names and redundant operations.
- Avoid unnecessary print statements.

## Dependencies

Required dependencies (install if not available):
- **pandoc**: `sudo apt-get install pandoc` (for text extraction).
- **docx**: `npm install -g docx` (for creating new documents).
- **LibreOffice**: `sudo apt-get install libreoffice` (for PDF conversion).
- **Poppler**: `sudo apt-get install poppler-utils` (for pdftoppm to convert PDF to images).
- **defusedxml**: `pip install defusedxml` (for secure XML parsing).