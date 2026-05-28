# Search Reference

## Endpoint

```
POST https://api.exa.ai/search
```

## Authentication

```bash
-H "x-api-key: $EXA_API_KEY"
```

## Request Body

| Parameter | Required | Default | Description |
| --------- | -------- | ------- | ----------- |
| `query` | Yes | - | Search query |
| `type` | No | auto | Search type: `auto`, `fast`, `deep` |
| `numResults` | No | 10 | Number of results (max 100) |
| `text` | No | false | Include full text content |
| `context` | No | false | Include LLM-optimized context |
| `includeDomains` | No | - | Array of domains to include |
| `excludeDomains` | No | - | Array of domains to exclude |
| `startPublishedDate` | No | - | ISO 8601 date filter |
| `endPublishedDate` | No | - | ISO 8601 date filter |

## Search Types

| Type | Description | Latency | Use Case |
| ---- | ----------- | ------- | -------- |
| `fast` | Quick cached results | ~200ms | Simple lookups, known topics |
| `auto` | Balanced search | ~500ms | General purpose queries |
| `deep` | Comprehensive search | ~2s | Research, complex queries |

## Response Fields

| Field | Description |
| ----- | ----------- |
| `title` | Page title |
| `url` | Page URL |
| `text` | Full text content (if requested) |
| `publishedDate` | Publication date if available |
| `author` | Author if available |
| `summary` | AI summary (if available) |

## Examples

### Basic Search

```bash
# Quick search
curl -X POST 'https://api.exa.ai/search' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"query": "TypeScript generics"}'

# Fast search for simple queries
curl -X POST 'https://api.exa.ai/search' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"query": "node.js version", "type": "fast"}'

# Deep search for research
curl -X POST 'https://api.exa.ai/search' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"query": "microservices architecture patterns", "type": "deep", "numResults": 10}'
```

### With Content

```bash
# Get full text content
curl -X POST 'https://api.exa.ai/search' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"query": "GraphQL best practices", "text": true}'

# Get context for LLM
curl -X POST 'https://api.exa.ai/search' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"query": "Kubernetes deployment strategies", "context": true}'
```

### With Filters

```bash
# Filter by domain
curl -X POST 'https://api.exa.ai/search' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"query": "LLM research", "includeDomains": ["arxiv.org", "paperswithcode.com"]}'

# Filter by date
curl -X POST 'https://api.exa.ai/search' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"query": "AI news", "startPublishedDate": "2025-01-01T00:00:00.000Z"}'
```

## Error Handling

- **HTTP 401**: Invalid or missing API key
- **HTTP 429**: Rate limit exceeded
- **Timeout**: Query took too long - try simpler query or `"type": "fast"`
