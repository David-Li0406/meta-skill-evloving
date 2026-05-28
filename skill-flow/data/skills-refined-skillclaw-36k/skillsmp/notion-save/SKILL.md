---
name: notion-save
description: Save notes, ideas, and content directly to Notion database. Use when Claude needs to persist conversation insights, trading notes, research findings, or any content to Notion for later reference. Triggers on phrases like "save to notion", "记录到notion", "add to my notes database".
---

# Notion Save Skill

Save content directly to your Notion database via the official Notion API with full Markdown support.

## Features

- **Markdown formatting**: Headings, lists, tables, code blocks, bold/italic
- **File input**: Read content from .md files (recommended for long content)
- **Auto-chunking**: Handles content longer than Notion's block limits
- **Inline formatting**: Bold, italic, code, links are preserved

## Usage

### For long content (recommended): Use file input

```bash
# Write content to temp file first, then upload
python scripts/save_to_notion.py --title "Research Report" --file report.md --api-key "YOUR_KEY"
```

### For short content: Use inline

```bash
python scripts/save_to_notion.py --title "Quick Note" --content "# Title\n- Item 1\n- Item 2" --api-key "YOUR_KEY"
```

### List recent pages

```bash
python scripts/save_to_notion.py --list --api-key "YOUR_KEY"
```

## Markdown Support

| Element | Syntax | Notion Block Type |
|---------|--------|-------------------|
| Heading 1 | `# Title` | heading_1 |
| Heading 2 | `## Title` | heading_2 |
| Heading 3 | `### Title` | heading_3 |
| Bullet list | `- item` | bulleted_list_item |
| Numbered list | `1. item` | numbered_list_item |
| Code block | ` ```lang ` | code |
| Table | `\| col \| col \|` | table |
| Quote | `> text` | quote |
| Divider | `---` | divider |
| Bold | `**text**` | annotation |
| Italic | `*text*` | annotation |
| Code | `` `text` `` | annotation |
| Link | `[text](url)` | link |

## Claude Usage Pattern

When saving long research reports or conversation content:

1. Write content to a temp markdown file
2. Call the script with `--file` parameter
3. Delete temp file after success

Example:
```python
# In Claude's workflow:
# 1. Write content to temp file
with open('temp_report.md', 'w', encoding='utf-8') as f:
    f.write(markdown_content)

# 2. Call save script
python scripts/save_to_notion.py --title "Report Title" --file temp_report.md --api-key "KEY"
```

## Configuration

- Default database ID: `2decc7dd-3404-8002-a7e7-d64733a75885`
- API key can be passed via `--api-key` or `NOTION_API_KEY` env var

## Error Handling

- 401 error: Invalid API key
- 404 error: Database not shared with integration
- Validation error: Check property names match database schema
