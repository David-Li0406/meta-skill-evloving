# Notion Property Types Reference

Complete reference for all 24 database property types with JSON structures.

## Core Properties

### Title (Required)

Every database page must have exactly one title property.

```python
{"title": [{"text": {"content": "Page Title"}}]}
```

### Rich Text

Multi-line text with formatting support.

```python
{"rich_text": [{"text": {"content": "Description text"}}]}

# With formatting
{"rich_text": [{
    "type": "text",
    "text": {"content": "Bold text"},
    "annotations": {"bold": True}
}]}
```

### Number

Numeric values (integers or decimals).

```python
{"number": 42}
{"number": 3.14159}
{"number": None}  # Clear value
```

## Selection Properties

### Select

Single choice from predefined options.

```python
{"select": {"name": "High"}}
{"select": None}  # Clear selection
```

### Multi-Select

Multiple choices from predefined options.

```python
{"multi_select": [
    {"name": "python"},
    {"name": "api"},
    {"name": "automation"}
]}
{"multi_select": []}  # Clear all
```

### Status

Built-in status property with groups (To Do, In Progress, Complete).

```python
{"status": {"name": "In Progress"}}
{"status": {"name": "Done"}}
```

## Date & Time

### Date

Single date or date range.

```python
# Single date
{"date": {"start": "2025-12-23"}}

# Date with time
{"date": {"start": "2025-12-23T14:30:00"}}

# Date range
{"date": {
    "start": "2025-12-23",
    "end": "2025-12-31"
}}

# With timezone
{"date": {
    "start": "2025-12-23T14:30:00",
    "time_zone": "America/New_York"
}}
```

## Boolean & URL

### Checkbox

Boolean true/false.

```python
{"checkbox": True}
{"checkbox": False}
```

### URL

Web links.

```python
{"url": "https://example.com"}
{"url": None}  # Clear
```

### Email

Email addresses.

```python
{"email": "user@example.com"}
```

### Phone Number

Phone numbers (stored as string).

```python
{"phone_number": "+1-555-123-4567"}
```

## Relations & Rollups

### Relation

Links to pages in another database.

```python
# Single relation
{"relation": [{"id": "page-uuid-here"}]}

# Multiple relations
{"relation": [
    {"id": "page-1-uuid"},
    {"id": "page-2-uuid"}
]}

# Clear relations
{"relation": []}
```

### Rollup

Aggregates data from related pages. **Read-only** - computed automatically.

```json
{
  "rollup": {
    "type": "number",
    "number": 42,
    "function": "sum"
  }
}
```

## People & Files

### People

User assignments.

```python
{"people": [{"id": "user-uuid"}]}
{"people": []}  # Clear
```

### Files

File attachments (external URLs only via API).

```python
{"files": [{
    "type": "external",
    "name": "document.pdf",
    "external": {"url": "https://example.com/doc.pdf"}
}]}
```

## Auto-Generated (Read-Only)

These are computed automatically and cannot be set via API:

| Property           | Description                 |
| ------------------ | --------------------------- |
| `created_time`     | Page creation timestamp     |
| `created_by`       | User who created the page   |
| `last_edited_time` | Last modification timestamp |
| `last_edited_by`   | User who last edited        |
| `unique_id`        | Auto-increment ID           |

### Formula

Computed from other properties. **Read-only**.

```json
{
  "formula": {
    "type": "string",
    "string": "Computed Value"
  }
}
```

## Property Builder Helpers

Use helpers from `create_page.py`:

```python
from scripts.create_page import (
    title_property,
    rich_text_property,
    select_property,
    multi_select_property,
    date_property,
    checkbox_property,
    number_property,
    url_property,
    status_property,
    relation_property,
)

properties = {
    "Name": title_property("Task Title"),
    "Description": rich_text_property("Task description"),
    "Priority": select_property("High"),
    "Tags": multi_select_property(["api", "python"]),
    "Due Date": date_property("2025-12-31"),
    "Done": checkbox_property(False),
    "Score": number_property(85),
    "Link": url_property("https://example.com"),
    "Status": status_property("In Progress"),
    "Related": relation_property(["page-id-1", "page-id-2"]),
}
```

## Common Errors

| Error              | Cause                              | Fix                                 |
| ------------------ | ---------------------------------- | ----------------------------------- |
| `validation_error` | Property doesn't exist in database | Check database schema               |
| `validation_error` | Wrong property type                | Match type to schema                |
| `validation_error` | Select option doesn't exist        | Create option first or use existing |

## Edge Cases (from Testing)

### Empty and Null Values

- Empty strings create empty content (valid for title/rich_text)
- Empty arrays clear multi-select and relation properties
- None clears number/date properties

```python
title_property("")          # Creates empty title - valid
multi_select_property([])   # Clears all selections - valid
number_property(None)       # Clears number value - valid
```

### Unicode Support

All Unicode characters preserved in text properties:

```python
title_property("Task 🚀")           # Emoji preserved
title_property("日本語テキスト")      # CJK characters preserved
rich_text_property("Café résumé")   # Accented characters preserved
```

### Numeric Edge Cases

```python
number_property(0)      # Zero is valid (not treated as falsy)
number_property(-42)    # Negative numbers valid
number_property(3.14159)  # Float precision preserved
```

_Verified in: `test_property_builders.py::TestPropertyBuildersEdgeCases`_
