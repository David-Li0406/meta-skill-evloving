# Notion Block Types Reference

Complete reference for all block types with JSON structures.

## Text Blocks

### Paragraph

```python
{
    "type": "paragraph",
    "paragraph": {
        "rich_text": [{"type": "text", "text": {"content": "Paragraph text"}}]
    }
}
```

### Headings

```python
# Heading 1 (largest)
{"type": "heading_1", "heading_1": {"rich_text": [{"type": "text", "text": {"content": "H1"}}]}}

# Heading 2
{"type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "H2"}}]}}

# Heading 3 (smallest)
{"type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "H3"}}]}}
```

### Quote

```python
{
    "type": "quote",
    "quote": {
        "rich_text": [{"type": "text", "text": {"content": "Quoted text"}}]
    }
}
```

### Callout

```python
{
    "type": "callout",
    "callout": {
        "rich_text": [{"type": "text", "text": {"content": "Important note"}}],
        "icon": {"type": "emoji", "emoji": "💡"}
    }
}
```

## List Blocks

### Bulleted List Item

```python
{
    "type": "bulleted_list_item",
    "bulleted_list_item": {
        "rich_text": [{"type": "text", "text": {"content": "List item"}}]
    }
}
```

### Numbered List Item

```python
{
    "type": "numbered_list_item",
    "numbered_list_item": {
        "rich_text": [{"type": "text", "text": {"content": "Step 1"}}]
    }
}
```

### To-Do

```python
{
    "type": "to_do",
    "to_do": {
        "rich_text": [{"type": "text", "text": {"content": "Task item"}}],
        "checked": False
    }
}
```

## Container Blocks

### Toggle

Collapsible content with nested children.

```python
{
    "type": "toggle",
    "toggle": {
        "rich_text": [{"type": "text", "text": {"content": "Click to expand"}}],
        "children": [
            {"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Hidden content"}}]}}
        ]
    }
}
```

### Column List & Columns

Multi-column layouts.

```python
{
    "type": "column_list",
    "column_list": {
        "children": [
            {"type": "column", "column": {"children": [...]}},
            {"type": "column", "column": {"children": [...]}}
        ]
    }
}
```

## Code & Technical

### Code Block

```python
{
    "type": "code",
    "code": {
        "rich_text": [{"type": "text", "text": {"content": "print('hello')"}}],
        "language": "python"
    }
}
```

Supported languages: `python`, `javascript`, `typescript`, `java`, `c`, `cpp`, `csharp`, `go`, `rust`, `ruby`, `php`, `swift`, `kotlin`, `sql`, `bash`, `shell`, `json`, `yaml`, `markdown`, `html`, `css`, and more.

### Equation

LaTeX math equations.

```python
{
    "type": "equation",
    "equation": {
        "expression": "E = mc^2"
    }
}
```

## Media Blocks

### Image

```python
{
    "type": "image",
    "image": {
        "type": "external",
        "external": {"url": "https://example.com/image.png"}
    }
}
```

### Video

```python
{
    "type": "video",
    "video": {
        "type": "external",
        "external": {"url": "https://youtube.com/watch?v=..."}
    }
}
```

### File

```python
{
    "type": "file",
    "file": {
        "type": "external",
        "external": {"url": "https://example.com/document.pdf"}
    }
}
```

### Bookmark

```python
{
    "type": "bookmark",
    "bookmark": {
        "url": "https://example.com"
    }
}
```

## Structural Blocks

### Divider

Horizontal line separator.

```python
{"type": "divider", "divider": {}}
```

### Table of Contents

Auto-generated from headings.

```python
{"type": "table_of_contents", "table_of_contents": {}}
```

### Breadcrumb

Navigation path.

```python
{"type": "breadcrumb", "breadcrumb": {}}
```

## Embed Blocks

### Embed

Generic embed for supported services.

```python
{
    "type": "embed",
    "embed": {
        "url": "https://twitter.com/..."
    }
}
```

### PDF

```python
{
    "type": "pdf",
    "pdf": {
        "type": "external",
        "external": {"url": "https://example.com/doc.pdf"}
    }
}
```

## Database Blocks

### Child Database

Inline database.

```python
{
    "type": "child_database",
    "child_database": {
        "title": "Task List"
    }
}
```

### Child Page

Nested page.

```python
{
    "type": "child_page",
    "child_page": {
        "title": "Sub-page Title"
    }
}
```

## Block Builder Helpers

Use helpers from `add_blocks.py`:

```python
from scripts.add_blocks import (
    paragraph,
    heading,
    bullet,
    numbered,
    todo,
    code_block,
    divider,
    callout,
    quote,
    toggle,
    table_of_contents,
    bookmark,
)

blocks = [
    heading("Introduction", level=1),
    paragraph("Welcome to the guide."),
    divider(),
    heading("Steps", level=2),
    numbered("First step"),
    numbered("Second step"),
    callout("Important tip!", emoji="💡"),
    code_block("print('done')", language="python"),
]
```

## Nesting Rules

| Block Type           | Can Have Children  |
| -------------------- | ------------------ |
| `toggle`             | Yes                |
| `bulleted_list_item` | Yes (nested lists) |
| `numbered_list_item` | Yes (nested lists) |
| `to_do`              | Yes                |
| `quote`              | Yes                |
| `callout`            | Yes                |
| `column`             | Yes                |
| `paragraph`          | No                 |
| `heading_*`          | No                 |
| `code`               | No                 |
| `divider`            | No                 |

## Constraints (from Testing)

### Block Limits

- Max **1000 blocks** per `append_blocks()` call
- Exceeding limit raises `ValueError`

```python
# For large content, batch into multiple calls
for i in range(0, len(blocks), 1000):
    append_blocks(client, page_id, blocks[i:i+1000])
```

### Heading Levels

- Only levels 1, 2, 3 valid
- Level 4+ or 0 raises `ValueError`

```python
heading("Valid", level=3)   # OK
heading("Invalid", level=4)  # Raises ValueError
```

### Content Preservation

- Multiline code preserved exactly (whitespace, newlines)
- Unicode emoji in callout icons preserved
- Toggle blocks without children omit the `children` key

```python
code_block("def f():\n    return 42")  # Newlines preserved
callout("Note", emoji="🚀")             # Emoji preserved
toggle("Empty toggle")                  # No children key in output
```

_Verified in: `test_block_builders.py::TestBlockBuildersInvalidInputs`_
