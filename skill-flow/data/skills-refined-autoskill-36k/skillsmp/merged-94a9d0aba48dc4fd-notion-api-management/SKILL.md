---
name: notion-api-management
description: Use this skill to create, read, update, and manage pages, databases, and blocks in Notion using the Notion API.
---

# Notion API Management

Manage pages, databases, and content blocks in Notion workspaces using the Notion API.

## When to Use

- Create and update Notion pages
- Query and filter database entries
- Search across workspace content
- Append content blocks to pages
- Manage database schemas and properties

## Prerequisites

1. Create an integration at [Notion Integrations](https://notion.so/my-integrations).
2. Copy the API key (starts with `ntn_` or `secret_`).
3. Store it:
   ```bash
   mkdir -p ~/.config/notion
   echo "ntn_your_key_here" > ~/.config/notion/api_key
   ```
4. Share target pages/databases with your integration (click "..." → "Connect to" → your integration name).

## Setup

Before performing any Notion operations, check if the required environment variable is set:

```bash
[ -n "$NOTION_API_KEY" ] && echo "NOTION_API_KEY is set" || echo "NOTION_API_KEY is NOT set"
```

## Base Headers

All requests need the following headers:

```bash
-H "Authorization: Bearer ${NOTION_API_KEY}" \
-H "Notion-Version: 2025-09-03" \
-H "Content-Type: application/json"
```

## Common Operations

### Search for Pages and Databases

```bash
curl -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "page title"}'
```

### Create a Page Under a Parent Page

```bash
PARENT_PAGE_ID="<parent_page_id>"

curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"type": "page_id", "page_id": "'"${PARENT_PAGE_ID}"'"},
    "properties": {
      "title": {
        "title": [{"type": "text", "text": {"content": "My new page"}}]
      }
    },
    "children": [
      {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
          "rich_text": [{"type": "text", "text": {"content": "Hello from OpenHands."}}]
        }
      }
    ]
  }'
```

### Append Blocks to an Existing Page

```bash
PAGE_ID="<page_id>"

curl -s -X PATCH "https://api.notion.com/v1/blocks/${PAGE_ID}/children" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Appended section"}}]}
      }
    ]
  }'
```

### Query a Database

```bash
curl -X POST "https://api.notion.com/v1/databases/<your-database-id>/query" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {"property": "Status", "select": {"equals": "Active"}},
    "sorts": [{"property": "Date", "direction": "descending"}]
  }'
```

### Update Page Properties

```bash
curl -X PATCH "https://api.notion.com/v1/pages/<your-page-id>" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"Status": {"select": {"name": "Done"}}}}'
```

### Create a Database

```bash
curl -X POST "https://api.notion.com/v1/data_sources" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"page_id": "xxx"},
    "title": [{"text": {"content": "My Database"}}],
    "properties": {
      "Name": {"title": {}},
      "Status": {"select": {"options": [{"name": "Todo"}, {"name": "Done"}]}},
      "Date": {"date": {}}
    }
  }'
```

## Property Types

Common property formats for database items:
- **Title:** `{"title": [{"text": {"content": "..."}}]}`
- **Rich text:** `{"rich_text": [{"text": {"content": "..."}}]}`
- **Select:** `{"select": {"name": "Option"}}`
- **Multi-select:** `{"multi_select": [{"name": "A"}, {"name": "B"}]}`
- **Date:** `{"date": {"start": "2024-01-15", "end": "2024-01-16"}}`
- **Checkbox:** `{"checkbox": true}`
- **Number:** `{"number": 42}`
- **URL:** `{"url": "https://..."}`
- **Email:** `{"email": "a@b.com"}`
- **Relation:** `{"relation": [{"id": "page_id"}]}`

## Notes

- Page/database IDs are UUIDs (with or without dashes).
- The API cannot set database view filters — that's UI-only.
- Rate limit: ~3 requests/second average.
- Use `is_inline: true` when creating data sources to embed them in pages.

## Documentation

- [Notion API Documentation](https://developers.notion.com/reference)
- [Integration Settings](https://www.notion.so/profile/integrations)