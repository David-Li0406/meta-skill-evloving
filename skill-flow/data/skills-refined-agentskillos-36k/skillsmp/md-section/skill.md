---
name: md-section
description: Extract a specific section from a Markdown file by heading name. Use this to efficiently read targeted documentation sections instead of loading entire files.
allowed-tools: Bash
---

# Markdown Section Extractor

Extracts a section from a Markdown file by heading name. Returns only the content between the specified heading and the next heading of equal or higher level.

## Usage

```bash
python3 /Users/mattgioe/aiq/scripts/md_section.py "<file_path>" "<heading_name>"
```

## Arguments

Parse the skill arguments as: `<file_path> <heading_name>`

Examples:
- `/md-section backend/README.md Installation` → extracts the "Installation" section
- `/md-section CLAUDE.md "Quick Reference"` → extracts the "Quick Reference" section
- `/md-section docs/architecture/OVERVIEW.md "Data Flow"` → extracts nested section

If the file path is relative, resolve it from `/Users/mattgioe/aiq`.

## Behavior

- Case-insensitive heading match
- Returns content from heading to next same/higher level heading
- Returns empty string if heading not found
- No metadata, just the section content

## When to Use

Use this skill when you need to:
- Read a specific section of documentation without loading the entire file
- Look up a particular topic in a large Markdown file
- Reduce token usage by fetching only relevant content
