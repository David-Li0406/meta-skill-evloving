---
name: metabase
description: Query and analyze data from Metabase, create/update questions and dashboards, access the Metabase REST API, and troubleshoot Metabase SQL queries. Use when user mentions Metabase, dashboards, metrics, or asks to fetch/analyze business intelligence data.
allowed-tools:
  - Bash
  - Read
  - Write
  - WebFetch
---

# Metabase Skill

This skill provides comprehensive Metabase integration for querying data, managing questions/dashboards, and troubleshooting.

## Authentication

Use these environment variables (already configured):

- `METABASE_URL`: Base URL for Metabase instance (usually `https://metabase.vessel.co`)
- `METABASE_API_KEY`: API key for authentication

**Important**: Always use simple double quotes for env vars: `"$METABASE_API_KEY"`

## Common Tasks

### 1. Query Data from Metabase Questions

To fetch data from an existing question:

```bash
curl -H "X-API-KEY: $METABASE_API_KEY" \
  "$METABASE_URL/api/card/{QUESTION_ID}/query/json"
```

To list available questions:

```bash
curl -H "X-API-KEY: $METABASE_API_KEY" \
  "$METABASE_URL/api/card"
```

### 2. Create/Update Questions

Create a new question:

```bash
curl -X POST \
  -H "X-API-KEY: $METABASE_API_KEY" \
  -H "Content-Type: application/json" \
  -d @- \
  "$METABASE_URL/api/card" <<'EOF'
{
  "name": "Question Name",
  "dataset_query": {
    "type": "native",
    "native": {
      "query": "SELECT * FROM table"
    },
    "database": 2
  },
  "display": "table",
  "visualization_settings": {}
}
EOF
```

Update existing question:

```bash
curl -X PUT \
  -H "X-API-KEY: $METABASE_API_KEY" \
  -H "Content-Type: application/json" \
  -d @- \
  "$METABASE_URL/api/card/{QUESTION_ID}" <<'EOF'
{
  "name": "Updated Question Name",
  "dataset_query": {
    "type": "native",
    "native": {
      "query": "SELECT * FROM updated_table"
    },
    "database": 2
  }
}
EOF
```

### 3. Access Metabase API

Key endpoints:

- **Cards (Questions)**: `/api/card` (list), `/api/card/{id}` (get/update)
- **Dashboards**: `/api/dashboard` (list), `/api/dashboard/{id}` (get)
- **Databases**: `/api/database` (list), `/api/database/{id}` (get)
- **Collections**: `/api/collection` (list)
- **Search**: `/api/search?q={query}`

### 4. Troubleshoot Queries

Check query execution:

```bash
curl -X POST \
  -H "X-API-KEY: $METABASE_API_KEY" \
  -H "Content-Type: application/json" \
  -d @- \
  "$METABASE_URL/api/dataset" <<'EOF'
{
  "type": "native",
  "native": {
    "query": "EXPLAIN ANALYZE SELECT ..."
  },
  "database": 2
}
EOF
```

Get database schema:

```bash
curl -H "X-API-KEY: $METABASE_API_KEY" \
  "$METABASE_URL/api/database/{DATABASE_ID}/metadata"
```

## Best Practices

1. **Cache Results**: Save query results to files when analyzing large datasets
2. **Use Native Queries**: For complex SQL, use `type: "native"` with direct SQL
3. **Check Rate Limits**: Metabase may throttle API requests
4. **Parse JSON**: Use `jq` or Node.js to parse JSON responses
5. **Error Handling**: Check HTTP status codes and response errors

## Example Workflow

```bash
# 1. Search for a question
QUESTIONS=$(curl -s -H "X-API-KEY: $METABASE_API_KEY" \
  "$METABASE_URL/api/search?q=revenue")

# 2. Extract question ID
QUESTION_ID=$(echo "$QUESTIONS" | jq -r '.data[0].id')

# 3. Fetch data
curl -H "X-API-KEY: $METABASE_API_KEY" \
  "$METABASE_URL/api/card/$QUESTION_ID/query/json" > data.json

# 4. Analyze with Node.js or jq
cat data.json | jq '[.[] | {revenue: .revenue, date: .date}]'
```

## Tips

- Use `/api/search` to find questions/dashboards by name
- Add `?parameters=[...]` to apply filters to questions
- Export results as CSV: `/api/card/{id}/query/csv`
- Check question metadata: `/api/card/{id}` (no query param)
- For large datasets, consider pagination or streaming

## Common Issues

1. **401 Unauthorized**: Check API key validity
2. **404 Not Found**: Verify question/dashboard ID exists
3. **Slow Queries**: Use EXPLAIN ANALYZE to optimize
4. **Empty Results**: Check database connection and query syntax

## Shell Quoting (Important!)

The `$METABASE_API_KEY` env var may contain special characters. **All examples in this file use these patterns consistently - follow them exactly!**

### Option 1: Simple Double Quotes (Recommended)

```bash
# Works for most cases - simplest approach
curl -s -H "X-API-KEY: $METABASE_API_KEY" \
    -H "Content-Type: application/json" \
    "https://metabase.vessel.co/api/endpoint"
```

### Option 2: Printf for Complex Special Characters

```bash
# Most robust - handles any special characters
curl -s -H "$(printf 'X-API-KEY: %s' "$METABASE_API_KEY")" \
    -H "Content-Type: application/json" \
    "https://metabase.vessel.co/api/endpoint"
```

### Option 3: Heredocs for JSON Payloads

```bash
# Cleanest for POST/PUT requests with JSON
curl -s -X POST \
    -H "X-API-KEY: $METABASE_API_KEY" \
    -H "Content-Type: application/json" \
    -d @- \
    "https://metabase.vessel.co/api/card" <<'EOF'
{
  "name": "Question Name",
  "dataset_query": {
    "type": "native",
    "native": {"query": "SELECT * FROM table"},
    "database": 2
  }
}
EOF
```

**Avoid**: `bash -c` wrappers add unnecessary complexity and quoting layers.

## Debugging Auth

Always test auth first with `/api/user/current`:

```bash
curl -s -H "X-API-KEY: $METABASE_API_KEY" \
    "https://metabase.vessel.co/api/user/current" | head -100
```

If this returns user JSON, auth works. If specific endpoints fail after, it's likely permissions.

## Adding Cards to Dashboards

**Important**: There's no POST endpoint for adding cards. Must use PUT with ALL cards:

```bash
# 1. Get existing dashboard cards
curl -s -H "X-API-KEY: $METABASE_API_KEY" \
    "https://metabase.vessel.co/api/dashboard/{ID}" | python3 -c "
import sys, json

d = json.load(sys.stdin)
dashcards = d.get('dashcards', [])

# Transform existing cards
existing = []
for dc in dashcards:
    existing.append({
        'id': dc['id'],
        'card_id': dc['card_id'],
        'row': dc['row'],
        'col': dc['col'],
        'size_x': dc['size_x'],
        'size_y': dc['size_y'],
        'parameter_mappings': dc.get('parameter_mappings', []),
        'visualization_settings': dc.get('visualization_settings', {})
    })

# Add new cards with NEGATIVE IDs
new_cards = [
    {'id': -1, 'card_id': NEW_CARD_ID, 'row': 0, 'col': 0, 'size_x': 6, 'size_y': 3,
     'parameter_mappings': [], 'visualization_settings': {}},
]

# Shift existing cards down if adding at top
for card in existing:
    card['row'] += 3

print(json.dumps({'cards': new_cards + existing}))
" > /tmp/dashboard_update.json

# 2. Apply update with PUT
curl -s -X PUT \
    -H "X-API-KEY: $METABASE_API_KEY" \
    -H "Content-Type: application/json" \
    -d @/tmp/dashboard_update.json \
    "https://metabase.vessel.co/api/dashboard/{ID}/cards"
```

## JSON Parsing

When `jq` fails on responses (control characters), use python3:

```bash
curl -s -H "X-API-KEY: $METABASE_API_KEY" \
    "$METABASE_URL/api/card/123" | \
    python3 -c "import sys,json; d=json.load(sys.stdin); print(d['id'])"
```

## Vessel-Specific

- Database ID: `2` (production)
- Dashboard 51: Automated Portfolio Reporting
- Always filter queries with `o.access_type = 'FULL'` for real org data
