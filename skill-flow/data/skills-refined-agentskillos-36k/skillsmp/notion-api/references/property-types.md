# Notion Property Types Reference

Quick reference for working with Notion property types when updating or creating items.

## Common Property Formats

### Title
```json
{ "title": [{ "text": { "content": "My Title" } }] }
```

### Rich Text
```json
{ "rich_text": [{ "text": { "content": "Some text content" } }] }
```

### Status
```json
{ "status": { "name": "Done" } }
```

### Select
```json
{ "select": { "name": "Option Name" } }
```
Clear: `{ "select": null }`

### Multi-Select
```json
{ "multi_select": [{ "name": "Tag1" }, { "name": "Tag2" }] }
```

### Date
Single date:
```json
{ "date": { "start": "2025-01-20" } }
```

Date range:
```json
{ "date": { "start": "2025-01-20", "end": "2025-01-25" } }
```

With time:
```json
{ "date": { "start": "2025-01-20T10:00:00.000Z" } }
```

### Number
```json
{ "number": 42 }
```

### Checkbox
```json
{ "checkbox": true }
```

### URL
```json
{ "url": "https://example.com" }
```

### Email
```json
{ "email": "user@example.com" }
```

### Phone
```json
{ "phone_number": "+1-555-1234" }
```

### People
By user ID:
```json
{ "people": [{ "id": "user-uuid-here" }] }
```

### Relation
By page ID:
```json
{ "relation": [{ "id": "page-uuid-here" }] }
```

### Files (External URLs)
```json
{
  "files": [{
    "type": "external",
    "name": "document.pdf",
    "external": { "url": "https://example.com/doc.pdf" }
  }]
}
```

## Read-Only Properties

These cannot be updated via API:
- `created_time`
- `created_by`
- `last_edited_time`
- `last_edited_by`
- `formula`
- `rollup`
- `unique_id`

## Status vs Select

- **Status**: Has built-in groupings (To-do, In progress, Complete), colored tags
- **Select**: Simple single-choice dropdown

Both update the same way: `{ "name": "Value" }`

## Getting User IDs

To assign people, you need their Notion user IDs. Get these from:
1. Reading an existing page with that person assigned
2. Notion API users endpoint: `GET /v1/users`

## Getting Page IDs for Relations

Page IDs can be extracted from Notion URLs:
- URL: `https://www.notion.so/workspace/Page-Title-abc123def456789`
- ID: Last 32 characters (with or without hyphens)

Or query the related database first to get IDs.
