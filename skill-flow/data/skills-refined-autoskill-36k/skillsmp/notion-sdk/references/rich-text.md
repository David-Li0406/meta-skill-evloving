# Rich Text Formatting Reference

Rich text is used in titles, paragraphs, headings, and most text-containing blocks.

## Basic Structure

Rich text is always an **array** of text objects:

```python
[
    {
        "type": "text",
        "text": {"content": "Hello, World!"}
    }
]
```

## Text Annotations

Apply formatting with annotations:

```python
{
    "type": "text",
    "text": {"content": "Formatted text"},
    "annotations": {
        "bold": True,
        "italic": False,
        "strikethrough": False,
        "underline": False,
        "code": False,
        "color": "default"
    }
}
```

### Available Colors

| Color     | Background Variant  |
| --------- | ------------------- |
| `default` | `default`           |
| `gray`    | `gray_background`   |
| `brown`   | `brown_background`  |
| `orange`  | `orange_background` |
| `yellow`  | `yellow_background` |
| `green`   | `green_background`  |
| `blue`    | `blue_background`   |
| `purple`  | `purple_background` |
| `pink`    | `pink_background`   |
| `red`     | `red_background`    |

Example with color:

```python
{
    "type": "text",
    "text": {"content": "Important"},
    "annotations": {
        "bold": True,
        "color": "red"
    }
}
```

## Links

Add hyperlinks to text:

```python
{
    "type": "text",
    "text": {
        "content": "Click here",
        "link": {"url": "https://example.com"}
    }
}
```

## Mentions

Reference other objects inline.

### User Mention

```python
{
    "type": "mention",
    "mention": {
        "type": "user",
        "user": {"id": "user-uuid"}
    }
}
```

### Page Mention

```python
{
    "type": "mention",
    "mention": {
        "type": "page",
        "page": {"id": "page-uuid"}
    }
}
```

### Database Mention

```python
{
    "type": "mention",
    "mention": {
        "type": "database",
        "database": {"id": "database-uuid"}
    }
}
```

### Date Mention

```python
{
    "type": "mention",
    "mention": {
        "type": "date",
        "date": {
            "start": "2025-12-23",
            "end": None
        }
    }
}
```

## Equations

Inline LaTeX math:

```python
{
    "type": "equation",
    "equation": {
        "expression": "x^2 + y^2 = z^2"
    }
}
```

## Combining Multiple Segments

Mix formatted and plain text:

```python
[
    {"type": "text", "text": {"content": "This is "}},
    {
        "type": "text",
        "text": {"content": "bold"},
        "annotations": {"bold": True}
    },
    {"type": "text", "text": {"content": " and "}},
    {
        "type": "text",
        "text": {"content": "italic"},
        "annotations": {"italic": True}
    },
    {"type": "text", "text": {"content": " text."}}
]
```

## Helper Function

From `add_blocks.py`:

```python
def _rich_text(text: str, bold: bool = False, italic: bool = False, code: bool = False) -> list:
    """Create rich_text array with optional formatting."""
    return [
        {
            "type": "text",
            "text": {"content": text},
            "annotations": {
                "bold": bold,
                "italic": italic,
                "code": code,
                "strikethrough": False,
                "underline": False,
                "color": "default",
            },
        }
    ]
```

## Character Limits

| Field        | Max Length       |
| ------------ | ---------------- |
| Text content | 2,000 characters |
| URL          | 2,000 characters |
| Email        | 200 characters   |
| Phone        | 200 characters   |

If you need longer text, split across multiple rich_text objects.

## Common Patterns

### Bold + Colored

```python
{
    "type": "text",
    "text": {"content": "WARNING"},
    "annotations": {
        "bold": True,
        "color": "red_background"
    }
}
```

### Code Inline

```python
{
    "type": "text",
    "text": {"content": "variable_name"},
    "annotations": {"code": True}
}
```

### Link with Formatting

```python
{
    "type": "text",
    "text": {
        "content": "Documentation",
        "link": {"url": "https://docs.example.com"}
    },
    "annotations": {"bold": True, "color": "blue"}
}
```
