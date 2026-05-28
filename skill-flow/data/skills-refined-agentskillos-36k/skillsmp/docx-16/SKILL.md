---
name: docx
description: "Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. Use when working with professional documents (.docx files) for creating new documents, modifying content, working with tracked changes, or adding comments."
---

# DOCX Creation, Editing, and Analysis

## Overview
A .docx file is essentially a ZIP archive containing XML files that you can read or edit.

## Workflow Decision Tree

### Reading/Analyzing Content
Use text extraction or raw XML access

### Creating New Document
Use docx-js workflow

### Editing Existing Document
- **Your own document + simple changes**: Basic OOXML editing
- **Someone else's document**: Redlining workflow (recommended)
- **Legal, academic, business docs**: Redlining workflow (required)

## Reading Content

### Text Extraction
Convert to markdown using pandoc:

```bash
# Convert document to markdown with tracked changes
pandoc --track-changes=all path-to-file.docx -o output.md
```

### Raw XML Access
Needed for: comments, complex formatting, document structure, embedded media.

```bash
# Unpack a file
python ooxml/scripts/unpack.py <input.docx> <output_dir>
```

Key file structures:
* `word/document.xml` - Main document contents
* `word/comments.xml` - Comments referenced in document.xml
* `word/media/` - Embedded images and media files
* Tracked changes use `<w:ins>` and `<w:del>` tags

## Creating New Documents

Use **docx-js** (JavaScript/TypeScript):

1. Create a JavaScript/TypeScript file using Document, Paragraph, TextRun components
2. Export as .docx using Packer.toBuffer()

```javascript
import { Document, Paragraph, TextRun, Packer } from "docx";

const doc = new Document({
  sections: [{
    properties: {},
    children: [
      new Paragraph({
        children: [new TextRun("Hello World")],
      }),
    ],
  }],
});

const buffer = await Packer.toBuffer(doc);
```

## Editing Existing Documents

Use the Document library (Python):

1. Unpack: `python ooxml/scripts/unpack.py <input.docx> <output_dir>`
2. Create and run a Python script using the Document library
3. Pack: `python ooxml/scripts/pack.py <unpacked_dir> <output.docx>`

## Redlining Workflow

For document review with tracked changes:

**Principle: Minimal, Precise Edits**
Only mark text that actually changes. Break replacements into:
[unchanged text] + [deletion] + [insertion] + [unchanged text]

### Workflow

1. **Get markdown representation**:
   ```bash
   pandoc --track-changes=all path-to-file.docx -o current.md
   ```

2. **Identify and group changes** into batches of 3-10

3. **Unpack the document**:
   ```bash
   python ooxml/scripts/unpack.py <input.docx> <output_dir>
   ```

4. **Implement changes in batches** using Document library

5. **Pack the document**:
   ```bash
   python ooxml/scripts/pack.py unpacked reviewed-document.docx
   ```

6. **Final verification**:
   ```bash
   pandoc --track-changes=all reviewed-document.docx -o verification.md
   ```

## Converting to Images

```bash
# Convert DOCX to PDF
soffice --headless --convert-to pdf document.docx

# Convert PDF pages to JPEG
pdftoppm -jpeg -r 150 document.pdf page
```

## Dependencies

- **pandoc**: Text extraction
- **docx**: Creating new documents (npm)
- **LibreOffice**: PDF conversion
- **Poppler**: PDF to image conversion
- **defusedxml**: Secure XML parsing
