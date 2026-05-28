---
name: web-scraping-firecrawl
description: Use this skill for intelligent web scraping, content extraction, and URL discovery using the Firecrawl API.
---

# Web Scraping with Firecrawl

This skill enables intelligent web scraping and data extraction using Firecrawl.

## When to Use

Use Firecrawl when you need to:
- Extract content from web pages and convert to markdown or other formats.
- Crawl multiple pages from a website.
- Search the web and retrieve scraped results.
- Discover all URLs on a website (sitemap generation).
- Extract structured data from web pages using AI.

## Available Tools

### Scrape a Single Page

Extract content from a single URL.

**Endpoint:**
```
POST https://api.firecrawl.dev/v1/scrape
```

**Usage:**
```bash
curl -s -X POST "https://api.firecrawl.dev/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "<url>",
    "formats": ["markdown"],
    "onlyMainContent": true
  }'
```

**Parameters:**
- `url` (required): URL to scrape.
- `formats` (optional): Output formats - `markdown`, `html`, `rawHtml`, `screenshot`, `links`, `summary`.
- `onlyMainContent` (optional): Extract main content only (default: true).

### Map Website URLs

Discover all URLs on a website.

**Endpoint:**
```
POST https://api.firecrawl.dev/v1/map
```

**Usage:**
```bash
curl -s -X POST "https://api.firecrawl.dev/v1/map" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "<url>"
  }' | jq '.links[]'
```

### Search the Web

Search the web and optionally scrape results.

**Endpoint:**
```
POST https://api.firecrawl.dev/v1/search
```

**Usage:**
```bash
curl -s -X POST "https://api.firecrawl.dev/v1/search" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "<search_query>",
    "limit": 5
  }'
```

### Crawl a Website

Crawl multiple pages from a website.

**Endpoint:**
```
POST https://api.firecrawl.dev/v1/crawl
```

**Usage:**
```bash
curl -s -X POST "https://api.firecrawl.dev/v1/crawl" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "<url>",
    "limit": 10,
    "maxDepth": 2
  }'
```

### Extract Structured Data

Extract structured data using AI.

**Endpoint:**
```
POST https://api.firecrawl.dev/v1/extract
```

**Usage:**
```bash
curl -s -X POST "https://api.firecrawl.dev/v1/extract" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["<url>"],
    "prompt": "<extraction_prompt>",
    "schema": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "price": {"type": "number"}
      }
    }
  }'
```

## Best Practices

1. **Start with mapping**: For large sites, use the mapping tool to understand the site structure.
2. **Use appropriate tools**: Choose the right tool based on your needs (e.g., `scrape` for single URLs, `crawl` for multiple pages).
3. **Handle crawls automatically**: Poll for crawl status until complete.
4. **Choose the right format**: Use `summary` for quick overviews, `markdown` for full content.
5. **Be mindful of rate limits**: Manage API credits and avoid excessive requests.

## Example Workflows

### Research Task
1. Use `search` to find relevant pages.
2. Use `scrape` on promising results for full content.

### Documentation Extraction
1. Use `map` to discover all documentation pages.
2. Use `crawl` or `batch_scrape` to extract content.
3. Poll for crawl status until complete.

### Quick Page Summary
1. Use `scrape` with `summary` format for a quick overview.
2. Follow up with a full `markdown` scrape if more detail is needed.

## Environment Setup

Requires `FIRECRAWL_API_KEY` environment variable. Get your API key from: https://firecrawl.dev