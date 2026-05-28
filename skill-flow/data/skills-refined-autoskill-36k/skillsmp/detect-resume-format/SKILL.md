---
name: detect-resume-format
description: Detect the format of a resume file (PDF, DOCX, TXT) based on file content (magic numbers) or extension. Use prior to selecting a parser.
---

# Detect Resume Format

## Overview

This skill identifies the file type of a document, returning a simple identifier string (`pdf`, `docx`, `txt`, or `unknown`). It prioritizes content inspection (using `python-magic`) and falls back to file extensions.

## Prerequisites

Optional: `python-magic` for accurate content-based detection.

```bash
pip install python-magic
```

## Usage

### Detection Script

**Syntax:**

```bash
python3 .agent/skills/detect-resume-format/scripts/detect_format.py <file_path>
```

**Example:**

```bash
# Returns "pdf"
python3 .agent/skills/detect-resume-format/scripts/detect_format.py /path/to/resume.pdf
```
