---
name: firecrawl-web-scraping
description: Use this skill for web scraping and content extraction using Firecrawl, either through MCP or directly via API.
---

# Firecrawl Web Scraping

## Overview

This skill enables web scraping and content extraction using Firecrawl, either through the MCP or directly via the Firecrawl API. It provides powerful capabilities for scraping single pages, crawling entire websites, searching with content extraction, and extracting structured data.

## When to Use This Skill

- Scraping content from single web pages
- Crawling multiple pages on a website
- Searching the web with automatic content extraction
- Discovering all URLs on a website
- Extracting structured data (e.g., prices, names, details)

## Tool Selection Guide

| Task | Tool | Notes |
|------|------|-------|
| Single page content | `firecrawl_scrape` (MCP) or API endpoint | Fast, reliable |
| Find URLs on site | `firecrawl_map` (MCP) or API endpoint | Discovery only |
| Web search | `firecrawl_search` (MCP) or API endpoint | With optional scraping |
| Multiple pages | `firecrawl_map` + `firecrawl_scrape` (MCP) or API endpoint | Better than crawl |
| Structured data | `firecrawl_extract` (MCP) | Uses LLM extraction |
| Full site crawl | `firecrawl_crawl` (MCP) or API endpoint | Use with caution |

## Core Tools

### Scrape Single Page

**MCP Tool:** `mcp__firecrawl__firecrawl_scrape`  
**API Endpoint:** `POST https://api.firecrawl.dev/v1/scrape`

**Usage Example (MCP):**
```javascript
mcp__firecrawl__firecrawl_scrape({
  url: "<target_url>",
  formats: ["markdown"],
  onlyMainContent: true,
  maxAge: 172800000
})
```

**Usage Example (API):**
```bash
curl -s -X POST "https://api.firecrawl.dev/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "<target_url>",
    "formats": ["markdown"]
  }'
```

### Map Website URLs

**MCP Tool:** `mcp__firecrawl__firecrawl_map`  
**API Endpoint:** `POST https://api.firecrawl.dev/v1/map`

**Usage Example (MCP):**
```javascript
mcp__firecrawl__firecrawl_map({
  url: "<target_url>",
  limit: 100
})
```

**Usage Example (API):**
```bash
curl -s -X POST "https://api.firecrawl.dev/v1/map" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "<target_url>"
  }'
```

### Search Web

**MCP Tool:** `mcp__firecrawl__firecrawl_search`  
**API Endpoint:** `POST https://api.firecrawl.dev/v1/search`

**Usage Example (MCP):**
```javascript
mcp__firecrawl__firecrawl_search({
  query: "<search_query>",
  limit: 5
})
```

**Usage Example (API):**
```bash
curl -s -X POST "https://api.firecrawl.dev/v1/search" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "<search_query>",
    "limit": 5
  }'
```

### Crawl Website

**MCP Tool:** `mcp__firecrawl__firecrawl_crawl`  
**API Endpoint:** `POST https://api.firecrawl.dev/v1/crawl`

**Usage Example (MCP):**
```javascript
mcp__firecrawl__firecrawl_crawl({
  url: "<target_url>",
  maxDiscoveryDepth: 2,
  limit: 10
})
```

**Usage Example (API):**
```bash
curl -s -X POST "https://api.firecrawl.dev/v1/crawl" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "<target_url>",
    "limit": 10,
    "maxDepth": 2
  }'
```

## Best Practices

1. **Prefer scrape over crawl**: Use `map` + `scrape` for better control.
2. **Use caching**: Add `maxAge` for repeated requests (MCP).
3. **Search then scrape**: Search without formats, then scrape relevant URLs.
4. **Limit crawl depth**: Keep `maxDiscoveryDepth` and `limit` low.
5. **Use onlyMainContent**: Get cleaner content without navigation.

## Notes

- API key required (set `FIRECRAWL_API_KEY` for API usage).
- Credits consumed per request.
- Use `waitFor` for JavaScript-heavy pages (API).
- Crawl jobs are asynchronous - poll for completion (API).