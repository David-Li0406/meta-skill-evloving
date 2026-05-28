---
name: firecrawl-web-scraping
description: Use this skill when you need to scrape web pages, crawl websites, or extract structured data using Firecrawl, either through MCP or directly via API.
---

# Firecrawl Web Scraping

## Overview

This skill provides guidance for web scraping and content extraction using Firecrawl, either through the MCP or directly via the Firecrawl API. It enables scraping single pages, crawling entire websites, searching the web, and extracting structured data.

## When to Use This Skill

- Scraping content from single web pages
- Crawling multiple pages on a website
- Searching the web with automatic content extraction
- Discovering all URLs on a website
- Extracting structured data (prices, names, details)

## Tool Selection Guide

| Task | Tool | Notes |
|------|------|-------|
| Single page content | `firecrawl_scrape` (MCP) or API | Fast, reliable |
| Find URLs on site | `firecrawl_map` (MCP) or API | Discovery only |
| Web search | `firecrawl_search` (MCP) or API | With optional scraping |
| Multiple pages | `firecrawl_map` + `firecrawl_scrape` (MCP) or API | Better than crawl |
| Structured data | `firecrawl_extract` (MCP) or API | Uses LLM extraction |
| Full site crawl | `firecrawl_crawl` (MCP) or API | Use with caution |

## Core Tools

### Firecrawl MCP

#### firecrawl_scrape

Scrape content from a single URL.

**Tool:** `mcp__firecrawl__firecrawl_scrape`

```javascript
mcp__firecrawl__firecrawl_scrape({
  url: "https://docs.example.com/api",
  formats: ["markdown"],
  onlyMainContent: true,
  maxAge: 172800000
})
```

**Key Parameters:**
- `url`: Target URL
- `formats`: Output formats - "markdown", "html", "links"
- `onlyMainContent`: Extract only main content (recommended)
- `maxAge`: Cache TTL in ms (500% faster with cache)

#### firecrawl_search

Search the web and optionally scrape results.

**Tool:** `mcp__firecrawl__firecrawl_search`

**Without scraping (preferred):**
```javascript
mcp__firecrawl__firecrawl_search({
  query: "xterm.js terminal tutorial",
  limit: 5
})
```

**With scraping:**
```javascript
mcp__firecrawl__firecrawl_search({
  query: "VS Code extension API",
  limit: 3,
  scrapeOptions: {
    formats: ["markdown"],
    onlyMainContent: true
  }
})
```

### Firecrawl API (Direct)

#### Scrape Single Page

Extract content from a single URL.

**Endpoint**
```
POST https://api.firecrawl.dev/v1/scrape
```

**Usage**
```bash
curl -s -X POST "https://api.firecrawl.dev/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "formats": ["markdown"]
  }'
```

**Parameters**
- `url` (required): URL to scrape
- `formats` (optional): Output formats - `markdown`, `html`, `rawHtml`, `links`
- `onlyMainContent` (optional): Extract main content only (default: true)
- `waitFor` (optional): Wait time in ms for dynamic content

#### Map Website URLs

Discover all URLs on a website.

**Endpoint**
```
POST https://api.firecrawl.dev/v1/map
```

**Usage**
```bash
curl -s -X POST "https://api.firecrawl.dev/v1/map" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com"
  }' | jq '.links[]'
```

#### Search Web

Search the web and optionally scrape results.

**Endpoint**
```
POST https://api.firecrawl.dev/v1/search
```

**Usage**
```bash
curl -s -X POST "https://api.firecrawl.dev/v1/search" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "xterm.js WebGL performance",
    "limit": 5
  }'
```

#### Crawl Website

Crawl multiple pages from a website.

**Endpoint**
```
POST https://api.firecrawl.dev/v1/crawl
```

**Usage**
```bash
curl -s -X POST "https://api.firecrawl.dev/v1/crawl" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://docs.example.com",
    "limit": 10
  }'
```