# Code Reference

## Endpoint

```
POST https://api.exa.ai/context
```

Also known as **Exa Code** - optimized for finding code examples and programming context.

## Authentication

```bash
-H "x-api-key: $EXA_API_KEY"
```

## Request Body

| Parameter | Required | Default | Description |
| --------- | -------- | ------- | ----------- |
| `query` | Yes | - | Programming query (max 2000 chars) |
| `tokensNum` | No | dynamic | Token limit: `"dynamic"` or `50-100000` |

## Response Fields

| Field | Description |
| ----- | ----------- |
| `response` | Formatted code snippets and context |
| `resultsCount` | Number of sources found |
| `outputTokens` | Tokens in response |

## Focused Domains

The code search focuses on programming-related sources:

- GitHub
- Stack Overflow
- Dev.to
- Medium
- freeCodeCamp
- MDN Web Docs
- Python Docs
- Rust Docs (docs.rs)
- Go Docs (pkg.go.dev)
- npm, PyPI

## Examples

### Basic Code Search

```bash
# Find React hook examples
curl -X POST 'https://api.exa.ai/context' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"query": "React useState hook examples", "tokensNum": 5000}'

# Find Express middleware patterns
curl -X POST 'https://api.exa.ai/context' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"query": "Express.js authentication middleware"}'

# Find TypeScript examples
curl -X POST 'https://api.exa.ai/context' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"query": "TypeScript generic constraints"}'
```

### With Token Control

```bash
# Quick lookup (fewer tokens)
curl -X POST 'https://api.exa.ai/context' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"query": "Python list comprehension", "tokensNum": 2000}'

# Detailed context (more tokens)
curl -X POST 'https://api.exa.ai/context' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"query": "GraphQL resolver patterns", "tokensNum": 15000}'

# Dynamic (let API decide)
curl -X POST 'https://api.exa.ai/context' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"query": "Next.js app router configuration", "tokensNum": "dynamic"}'
```

## Query Tips

| Good Query | Bad Query |
| ---------- | --------- |
| `React useEffect cleanup function examples` | `useEffect` |
| `Express.js JWT authentication middleware` | `auth` |
| `Python async await with aiohttp` | `async` |
| `TypeScript generic constraints with extends` | `generics` |

Be specific about:

- The library or framework
- The specific feature or API
- The programming language
- The use case (authentication, caching, etc.)

## Token Guidelines

| Token Range | Use Case |
| ----------- | -------- |
| 1000-3000 | Quick syntax lookup |
| 5000 (default) | Standard examples |
| 10000-20000 | Detailed patterns |
| 30000-50000 | Comprehensive research |

## Error Handling

- **HTTP 401**: Invalid or missing API key
- **HTTP 429**: Rate limit exceeded
- **Few results**: Try broader query or different keywords
