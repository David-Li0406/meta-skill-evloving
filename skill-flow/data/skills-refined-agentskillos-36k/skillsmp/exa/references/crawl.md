# Crawl Reference

## Endpoint

```
POST https://api.exa.ai/contents
```

## Authentication

```bash
-H "x-api-key: $EXA_API_KEY"
```

## Request Body

| Parameter | Required | Default | Description |
| --------- | -------- | ------- | ----------- |
| `urls` | Yes | - | Array of URLs to crawl |
| `text` | No | false | Include full text content |
| `livecrawl` | No | fallback | `never`, `fallback`, `preferred`, `always` |
| `livecrawlTimeout` | No | 10000 | Timeout in milliseconds |

## Response Fields

| Field | Description |
| ----- | ----------- |
| `url` | The crawled URL |
| `title` | Page title |
| `text` | Extracted text content |
| `author` | Author if available |
| `publishedDate` | Publication date if available |

## Examples

### Basic Crawl

```bash
# Extract content from a documentation page
curl -X POST 'https://api.exa.ai/contents' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"urls": ["https://docs.python.org/3/tutorial/classes.html"], "text": true}'

# Extract from a blog post
curl -X POST 'https://api.exa.ai/contents' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"urls": ["https://blog.example.com/article"], "text": true}'
```

### With Live Crawling

```bash
# Prefer live content for fresh results
curl -X POST 'https://api.exa.ai/contents' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"urls": ["https://example.com/page"], "text": true, "livecrawl": "preferred"}'
```

### Multiple URLs

```bash
curl -X POST 'https://api.exa.ai/contents' \
  -H "x-api-key: $EXA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"urls": ["https://example.com/page1", "https://example.com/page2"], "text": true}'
```

## Use Cases

| Scenario | Example |
| -------- | ------- |
| Read documentation | `{"urls": ["https://docs.lib.com/api"], "text": true}` |
| Extract article content | `{"urls": ["https://blog.com/post"], "text": true}` |
| Get README content | `{"urls": ["https://github.com/org/repo"], "text": true}` |

## Error Handling

- **HTTP 401**: Invalid or missing API key
- **HTTP 404**: URL not found or inaccessible
- **No content returned**: Page may be blocked or empty
- **Timeout**: Large page - try with shorter timeout
