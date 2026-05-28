---
name: docx
description: Use this skill when you need to create, edit, or analyze professional documents in .docx format, including tasks like tracked changes, comments, and text extraction.
---

# DOCX Creation, Editing, and Analysis

## Overview

A .docx file is a ZIP archive containing XML files and resources. This skill allows you to create, edit, or analyze Word documents using various tools and workflows tailored for different tasks.

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
To read the text contents of a document, convert the document to markdown using Pandoc, which preserves document structure and can show tracked changes:

```bash
# Convert document to markdown with tracked changes
pandoc --track-changes=all path-to-file.docx -o output.md
# Options: --track-changes=accept/reject/all
```

### Raw XML Access
For comments, complex formatting, document structure, embedded media, and metadata, unpack the document and read its raw XML contents.

#### Unpacking a File
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
1. **MANDATORY - READ ENTIRE FILE**: Read [`docx-js.md`](docx-js.md).