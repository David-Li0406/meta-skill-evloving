---
name: markdown-to-docx
description: Use this skill to convert Markdown files to Microsoft Word (.docx) documents, suitable for generating editable documentation or exporting reports.
---

# markdown-to-docx

Convert Markdown files to Microsoft Word (.docx) documents.

## Installation Required

```bash
cd .claude/skills/markdown-to-docx
npm install
```

**Dependencies:** `markdown-docx` (uses docx internally)

## Quick Start

### Basic Conversion

```bash
node .claude/skills/markdown-to-docx/scripts/convert.cjs --file <input_path>
```

### Custom Output Path

```bash
node .claude/skills/markdown-to-docx/scripts/convert.cjs --file <input_path> --output <output_path>
```

## CLI Options

| Option | Required | Description |
| ------ | -------- | ----------- |
| `--file <path>` | Yes | Input Markdown file |
| `--output <path>` | No | Output DOCX path (default: input name + .docx) |

## Output Format (JSON)

```json
{
  "success": true,
  "input": "/path/to/input.md",
  "output": "/path/to/output.docx",
  "wordCount": 1523
}
```

## Supported Markdown Elements

- Headings (H1-H6)
- Paragraphs and emphasis (bold, italic)
- Ordered and unordered lists
- Code blocks
- Tables (GFM style)
- Links and images (local + URL)
- Blockquotes

## Default Styling

Uses markdown-docx default styling:

- Standard Word fonts
- Professional formatting
- Letter/A4 page size

## Troubleshooting

- **Dependencies not found:** Run `npm install` in skill directory.
- **Image not loading:** Ensure path is correct; URL images require network access (10s timeout).

## API Integration

To convert Markdown to Word using an API, follow these steps:

1. **Prepare Markdown**: Ensure content is in standard Markdown format.
2. **Run Script**: Execute the conversion script to call the conversion API.

### Example Usage

```bash
python scripts/convert.py <input_path> [template] [language]
```

### API Key Configuration

You can configure the API key in three ways:

1. **Environment Variable** (Highest Priority)
   ```bash
   export DEEP_SHARE_API_KEY="your_api_key_here"
   ```

2. **Skill Variable** (Medium Priority)
   Edit the `api_key` field in the YAML frontmatter of this Skill file.

3. **Trial Key** (Fallback): `f4e8fe6f-e39e-486f-b7e7-e037d2ec216f`

### Request Format

```json
{
  "content": "markdown text here",
  "filename": "output",
  "template_name": "templates",
  "language": "zh",
  "hard_line_breaks": false,
  "remove_hr": false
}
```

## Common Templates

**Chinese** (`language: "zh"`):
- `templates` - General purpose
- `论文` - Academic paper

**English** (`language: "en"`):
- `templates` - General purpose
- `article` - Article/report style

## User Communication

### On Success

Inform the user of successful conversion and provide the download URL.

### On Errors

Provide clear error messages and guidance on how to resolve issues.

## Tips

- Keep Markdown under 10MB.
- Use `https://` URLs for images.
- Validate Markdown content before conversion.

## Example Workflow

1. Save the Markdown content to a temporary file (e.g., `temp.md`).
2. Run the conversion script.
3. Handle the response and provide the download URL or error message.
4. Clean up temporary files.