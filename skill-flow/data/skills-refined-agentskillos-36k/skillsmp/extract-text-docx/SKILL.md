---
name: extract-text-docx
description: Extract text from DOCX files using python-docx. Use this skill when you need to read the contents of a Microsoft Word file (.docx) into plain text for analysis or processing.
---

# Extract Text from DOCX

## Overview

This skill extracts text from modern Microsoft Word documents (`.docx`). It retrieves text from paragraphs and tables.

## Prerequisites

This skill requires the `python-docx` library.

```bash
pip install python-docx
```

## Usage

### Extract Text Script

**Syntax:**

```bash
python3 .agent/skills/extract-text-docx/scripts/extract_docx.py <path_to_docx>
```

**Arguments:**

*   `path_to_docx`: Absolute path to the .docx file.

**Example:**

```bash
python3 .agent/skills/extract-text-docx/scripts/extract_docx.py /Users/user/resume.docx
```
