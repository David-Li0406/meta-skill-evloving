# Database Schema Recommendations

Your current "new day" database has a minimal schema with only a `Name` property. For effective Claude Code integration, consider adding these properties:

## Recommended Schema Extension

### For Trading/Research Notes

```
Property Name    | Type          | Purpose
-----------------|---------------|----------------------------------
Name             | title         | Note title (existing)
Content          | rich_text     | Main note content
Type             | select        | trading, research, idea, todo
Date             | date          | Entry timestamp
Tags             | multi_select  | ETH, BTC, DeFi, Technical, etc.
Priority         | select        | high, medium, low
Status           | status        | Not Started, In Progress, Done
Source           | url           | Reference link
```

### For Daily Journal

```
Property Name    | Type          | Purpose
-----------------|---------------|----------------------------------
Name             | title         | Day/entry title
Mood             | select        | 😊 Good, 😐 Neutral, 😟 Bad
Summary          | rich_text     | Day summary
Lessons          | rich_text     | Key learnings
Tomorrow         | rich_text     | Next day plans
```

## How to Add Properties in Notion

1. Open the database
2. Click "+ Add a property" 
3. Choose property type
4. Name the property exactly as shown (case-sensitive for API)

## Updated Script Usage

After adding properties, use the extended save command:

```python
# Example: Save with multiple properties
create_page(
    database_id="your_db_id",
    title="ETH Analysis 2024-01-04",
    content="Main analysis content here...",
    properties={
        "Type": {
            "select": {"name": "research"}
        },
        "Tags": {
            "multi_select": [
                {"name": "ETH"},
                {"name": "Technical"}
            ]
        },
        "Priority": {
            "select": {"name": "high"}
        }
    }
)
```

## Property Type Reference

| Type | API Format |
|------|------------|
| title | `{"title": [{"text": {"content": "value"}}]}` |
| rich_text | `{"rich_text": [{"text": {"content": "value"}}]}` |
| select | `{"select": {"name": "option_name"}}` |
| multi_select | `{"multi_select": [{"name": "tag1"}, {"name": "tag2"}]}` |
| date | `{"date": {"start": "2024-01-04"}}` |
| url | `{"url": "https://example.com"}` |
| checkbox | `{"checkbox": true}` |
| number | `{"number": 42}` |
