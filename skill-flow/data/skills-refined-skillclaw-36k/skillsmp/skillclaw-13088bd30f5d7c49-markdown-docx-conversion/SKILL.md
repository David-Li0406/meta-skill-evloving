---
name: markdown-docx-conversion
description: Use this skill to convert between Markdown and Microsoft Word (.docx) formats, enabling easy document creation and editing across both platforms.
---

# Skill body

## Overview

This skill allows you to convert Microsoft Word (.docx) files to Markdown format and vice versa. Use it when you need to import Word documents into Markdown for version control or export Markdown content to Word for editing and formatting.

## Installation Required

```bash
cd .claude/skills/markdown-docx-conversion
npm install
```

**Dependencies:** `mammoth`, `turndown`, `@truto/turndown-plugin-gfm`, `markdown-docx`

## Conversion from DOCX to Markdown

### Quick Start

```bash
# Basic conversion
node .claude/skills/markdown-docx-conversion/scripts/convert-docx-to-markdown.cjs \
  --file ./document.docx

# Custom output path
node .claude/skills/markdown-docx-conversion/scripts/convert-docx-to-markdown.cjs \
  --file ./doc.docx \
  --output ./output/doc.md

# Extract images to directory
node .claude/skills/markdown-docx-conversion/scripts/convert-docx-to-markdown.cjs \
  --file ./doc.docx \
  --output ./output/doc.md \
  --images ./output/images/
```

### CLI Options

| Option | Required | Description |
| ------ | -------- | ----------- |
| `--file <path>` | Yes | Input DOCX file |
| `--output <path>` | No | Output Markdown path (default: input name + .md) |
| `--images <dir>` | No | Directory for extracted images (default: inline base64) |

### Supported Elements

- Headings (H1-H6)
- Paragraphs and emphasis (bold, italic, strikethrough)
- Ordered and unordered lists
- Tables (GFM format)
- Links
- Images (extracted or base64)
- Code blocks (requires Word "Code" style)
- Blockquotes

### Known Limitations

- Nested lists and tables may have formatting issues.
- Some complex formatting may be simplified.

## Conversion from Markdown to DOCX

### Quick Start

```bash
# Basic conversion
node .claude/skills/markdown-docx-conversion/scripts/convert-markdown-to-docx.cjs \
  --file ./README.md

# Custom output path
node .claude/skills/markdown-docx-conversion/scripts/convert-markdown-to-docx.cjs \
  --file ./doc.md \
  --output ./output/doc.docx
```

### CLI Options

| Option | Required | Description |
| ------ | -------- | ----------- |
| `--file <path>` | Yes | Input Markdown file |
| `--output <path>` | No | Output DOCX path (default: input name + .docx) |

### Default Styling

Uses markdown-docx default styling for professional formatting.

## Troubleshooting

- **Dependencies not found:** Run `npm install` in the skill directory.
- **Empty output:** Ensure the input file contains actual text.
- **Image not loading:** Check the path for images in Markdown.

## Task Planning Notes

- Always plan and break tasks into smaller steps.
- Add a final review task to ensure quality and completeness.