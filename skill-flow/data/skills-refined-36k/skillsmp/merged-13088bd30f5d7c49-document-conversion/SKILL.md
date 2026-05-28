---
name: document-conversion
description: Use this skill when converting between Microsoft Word (.docx) and Markdown formats for documentation, reports, or content management.
---

# document-conversion

This skill allows for the conversion of Microsoft Word (.docx) documents to Markdown format and vice versa.

## Installation Required

```bash
cd .claude/skills/document-conversion
npm install
```

**Dependencies:** 
- For DOCX to Markdown: `mammoth`, `turndown`, `@truto/turndown-plugin-gfm`
- For Markdown to DOCX: `markdown-docx`

## DOCX to Markdown Conversion

### Quick Start

```bash
# Basic conversion
node .claude/skills/document-conversion/scripts/docx-to-markdown.cjs \
  --file ./document.docx

# Custom output path
node .claude/skills/document-conversion/scripts/docx-to-markdown.cjs \
  --file ./doc.docx \
  --output ./output/doc.md

# Extract images to directory
node .claude/skills/document-conversion/scripts/docx-to-markdown.cjs \
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
- Code blocks
- Blockquotes

### Known Limitations

- Nested lists and tables may have formatting issues.
- Some complex formatting may be simplified.

## Markdown to DOCX Conversion

### Quick Start

```bash
# Basic conversion
node .claude/skills/document-conversion/scripts/markdown-to-docx.cjs \
  --file ./README.md

# Custom output path
node .claude/skills/document-conversion/scripts/markdown-to-docx.cjs \
  --file ./doc.md \
  --output ./output/doc.docx
```

### CLI Options

| Option | Required | Description |
| ------ | -------- | ----------- |
| `--file <path>` | Yes | Input Markdown file |
| `--output <path>` | No | Output DOCX path (default: input name + .docx) |

### Supported Markdown Elements

- Headings (H1-H6)
- Paragraphs and emphasis (bold, italic)
- Ordered and unordered lists
- Code blocks
- Tables (GFM style)
- Links and images (local + URL)
- Blockquotes

## API Integration for Markdown to DOCX

For advanced users, Markdown can also be converted to DOCX using an API.

### Conversion Steps

1. **Prepare Markdown**: Ensure content is in standard Markdown format.
2. **Run Script**: Execute the conversion script to call the conversion API.
3. **Get Result**: Receive a download URL or error message.

### Example Usage

```bash
python scripts/convert.py input.md [template] [language]
```

### API Key Configuration

You can configure the API key in three ways:
1. **Environment Variable** (Highest Priority)
   ```bash
   export DEEP_SHARE_API_KEY="your_api_key_here"
   ```
2. **Skill Variable** (Medium Priority)
   Edit the `api_key` field in the YAML frontmatter of this Skill file.
3. **Trial Key** (Fallback): Limited quota.

## Troubleshooting

- **Dependencies not found**: Run `npm install` in the skill directory.
- **Empty output**: Ensure the input file contains actual text.
- **Image not loading**: Ensure the path is correct; URL images require network access.

## Task Planning Notes

- Always plan and break tasks into smaller steps.
- Add a final review task to ensure quality and completeness.