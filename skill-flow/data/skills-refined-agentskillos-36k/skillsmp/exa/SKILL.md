---
name: exa
description: Search the web and extract content using Exa AI. Use this skill when searching for current information, researching topics, fetching content from URLs, finding code examples, or when the user needs real-time web data. Also use for competitive research, finding similar pages, or extracting structured content from websites.
---

# Exa Web Search & Content Extraction

Real-time web search and content extraction powered by Exa AI.

**Prerequisite:** Set `EXA_API_KEY` environment variable.

## API Quick Reference

| Endpoint | Purpose |
| -------- | ------- |
| `POST /search` | Web search with optional content retrieval |
| `POST /contents` | Extract content from specific URLs |
| `POST /context` | Find code examples and programming context |

## Usage

### Web Search

```bash
# Basic search
curl -X POST 'https://api.exa.ai/search' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"query": "latest AI research", "text": true}'

# Deep search with more results
curl -X POST 'https://api.exa.ai/search' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"query": "React server components", "type": "deep", "numResults": 10, "text": true}'

# Fast search
curl -X POST 'https://api.exa.ai/search' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"query": "node.js version", "type": "fast"}'
```

### Extract URL Content

```bash
curl -X POST 'https://api.exa.ai/contents' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"urls": ["https://docs.example.com/api"], "text": true}'
```

### Code Context

```bash
curl -X POST 'https://api.exa.ai/context' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"query": "React useState hook examples", "tokensNum": 5000}'
```

## Workflow

Think step-by-step when using Exa:

1. **Choose the right endpoint** based on the task:
   - Web research, searching topics → `/search`
   - Extracting content from specific URLs → `/contents`
   - Programming examples, code context → `/context`

2. **Select search type** for `/search`:
   - `fast` - Quick results, lower latency
   - `auto` - Balanced (default)
   - `deep` - Comprehensive, higher quality

3. **Request content when needed** using `"text": true` or `"context": true`

## When to Use Each Endpoint

| Use `/search` | Use `/contents` | Use `/context` |
| ------------- | --------------- | -------------- |
| Finding relevant pages | You have a specific URL | Programming questions |
| General web research | Extracting known content | API/library usage |
| News and articles | Reading documentation | Code examples |
| Exploring options | Getting full article text | Implementation patterns |

## Search Types

| Type | Use Case | Speed |
| ---- | -------- | ----- |
| `fast` | Quick lookups, simple queries | Fastest |
| `auto` | General purpose, balanced results | Medium |
| `deep` | Complex research, comprehensive coverage | Slowest |

## Rules

- **Current year is 2026** - Use this for date-relative queries (e.g., "latest", "recent", "this year")
- Use `"type": "fast"` for simple factual queries
- Use `"type": "deep"` for research requiring comprehensive results
- Add `"text": true` to get full page content in search results
- Add `"context": true` for LLM-optimized context strings
- Use `/context` endpoint for programming questions instead of `/search`
- Prefer `/contents` when you have a specific URL to extract

## References

- [Search](references/search.md) - Web search parameters and options
- [Crawl](references/crawl.md) - URL content extraction
- [Code](references/code.md) - Programming context search
