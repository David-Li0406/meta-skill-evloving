---
name: resume-format
description: Apply headers, sections, and final formatting to output. Converts structured JSON resume data into a readable Markdown format.
---

# Resume Format

## Overview

This skill formats a structured JSON resume into a human-readable document (Markdown). Future versions may support DOCX or PDF generation.

## Usage

### Format Script

**Syntax:**

```bash
python3 .agent/skills/resume-format/scripts/format_resume.py <resume.json>
```

**Output:**
Markdown formatted text.

**Example:**

```bash
python3 .agent/skills/resume-format/scripts/format_resume.py resume.json > resume.md
```
