---
name: notion
description: Use this skill to interact with the Notion API for creating, reading, updating pages, databases, and blocks in your Notion workspace.
---

# Notion API

Manage pages, databases, and content blocks in Notion workspaces.

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

## API Basics

All requests need:
```bash
NOTION_KEY=$(cat ~/.config/notion/api_key)
```

### Common Operations

**Search for pages and data sources:**
```bash
curl -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "page title"}'
```

**Get page:**
```bash
curl "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03"
```

**Get page content (blocks):**
```bash
curl "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03"
```

**Create page in a data source:**
```bash
curl -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "xxx"},
    "properties": {
      "Name": {"title": [{"text": {"content": "New Item"}}]},
      "Status": {"select": {"name": "Todo"}}
    }
  }'
```

**Query a data source (database):**
```bash
curl -X POST "https://api.notion.com/v1/data_sources/{data_source_id}/query" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {"property": "Status", "select": {"equals": "Active"}},
    "sorts": [{"property": "Date", "direction": "descending"}]
  }'
```