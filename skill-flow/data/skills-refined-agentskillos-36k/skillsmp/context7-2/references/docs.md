# Docs Reference

## Endpoint

```
GET https://context7.com/api/v2/context
```

## Parameters

| Parameter | Required | Default | Description |
| --------- | -------- | ------- | ----------- |
| `libraryId` | Yes | - | Library ID from search (e.g., `/facebook/react`) |
| `query` | Yes | - | Documentation topic or question |
| `type` | No | json | Response format: `json` or `txt` |

## Authentication

```bash
-H "Authorization: Bearer $CONTEXT7_API_KEY"
```

## Response Formats

### JSON (default)

Returns an array of documentation snippets:

```json
[
  {
    "title": "Using the Effect Hook",
    "content": "The Effect Hook lets you perform side effects...",
    "source": "react.dev/reference/react/useEffect"
  }
]
```

### Text (`type=txt`)

Returns plain text optimized for LLM prompts.

## Examples

### Basic Queries

```bash
# Get code examples (JSON)
curl "https://context7.com/api/v2/context?libraryId=/facebook/react&query=useState%20hook" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"

# Get text format for LLM
curl "https://context7.com/api/v2/context?libraryId=/vercel/next.js&query=app%20router%20middleware&type=txt" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"
```

### With Specific Version

```bash
# Pin to a specific version
curl "https://context7.com/api/v2/context?libraryId=/vercel/next.js/v15.1.8&query=app%20router" \
  -H "Authorization: Bearer $CONTEXT7_API_KEY"
```

## Query Tips

| Good Query | Bad Query |
| ---------- | --------- |
| `useState with TypeScript` | `hooks` |
| `JWT authentication middleware` | `auth` |
| `database connection pooling` | `database` |
| `form validation with zod` | `forms` |

Be specific about:

- The feature or API you need
- The programming language (TypeScript, JavaScript)
- The use case (authentication, caching, etc.)

## Error Handling

| Code | Description | Action |
| ---- | ----------- | ------ |
| 200 | Success | Process the response normally |
| 301 | Library redirected | Use the new library ID from `redirectUrl` |
| 401 | Invalid API key | Check API key format (starts with `ctx7sk`) |
| 404 | Library not found | Verify the library ID |
| 429 | Rate limit exceeded | Wait and retry |
