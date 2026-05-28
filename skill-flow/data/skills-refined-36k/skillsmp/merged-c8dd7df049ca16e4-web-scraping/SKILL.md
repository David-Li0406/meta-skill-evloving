---
name: web-scraping
description: Use this skill for intelligent web scraping, data extraction, and URL discovery using the Firecrawl API.
---

# Web Scraping with Firecrawl

This skill enables intelligent web scraping and data extraction using the Firecrawl API.

## When to Use

Use this skill when you need to:
- Extract content from web pages and convert it to markdown or other formats.
- Crawl multiple pages from a website.
- Search the web and retrieve scraped results.
- Discover all URLs on a website (sitemap generation).
- Get summaries, screenshots, or links from web pages.

## Available Tools

### Scrape - Get Page Content

Fetches and converts a web page to clean markdown or other formats.

**Command:**
```bash
/firecrawl:scrape <url> --format <markdown|html|screenshot|summary>
```

**Best for:**
- Reading documentation
- Fetching article content
- Getting page text for analysis

### Map - Discover URLs

Finds all URLs on a website. Useful for understanding site structure.

**Command:**
```bash
/firecrawl:map <url> --limit <N>
```

**Best for:**
- Understanding site structure
- Finding specific pages before scraping

### Search - Web Search

Searches the web and returns results with optional content scraping.

**Command:**
```bash
/firecrawl:search <query> --limit <N>
```

**Supports search operators:**
- `"exact phrase"` - Exact match
- `-term` - Exclude term
- `site:example.com` - Limit to domain
- `intitle:word` - Word in title

**Best for:**
- Finding information across the web
- Researching topics

### Extract - Structured Data

Extracts specific data from pages using LLM prompts.

**Command:**
```bash
/firecrawl:extract <url> --prompt "<description>" --schema '{"key": {"type": "type"}}'
```

**Best for:**
- Extracting specific data points
- Getting structured information

## Environment Setup

Requires `FIRECRAWL_API_KEY` environment variable. Get your API key from: https://firecrawl.dev

## Example Workflows

### Research Task
1. Use `search` to find relevant pages.
2. Use `scrape` on promising results for full content.

### Documentation Extraction
1. Use `map` to discover all documentation pages.
2. Use `crawl` or `batch_scrape` to extract content.
3. Poll `check_crawl_status` until complete.

### Quick Page Summary
1. Use `scrape` with `summary` format for a quick overview.
2. Follow up with full `markdown` scrape if more detail is needed.

## Best Practices

1. **Start with map**: For large sites, use `firecrawl_map` first to understand the site structure.
2. **Use appropriate tool**: Choose the right tool based on your needs (single URL, multiple URLs, unknown pages).
3. **Handle crawls automatically**: Always poll for crawl status until complete.
4. **Choose the right format**: Use `summary` for quick overviews, `markdown` for full content.
5. **Handle rate limits**: Be mindful of API credits and rate limits on large operations.
6. **JavaScript-rendered content**: Firecrawl automatically handles dynamic content.

## Response Format

### Scrape Response
```json
{
  "success": true,
  "data": {
    "markdown": "# Page Title\n\nContent...",
    "metadata": {
      "title": "Page Title",
      "description": "...",
      "url": "https://..."
    }
  }
}
```

### Crawl Status Response
```json
{
  "success": true,
  "status": "completed",
  "completed": 50,
  "total": 50,
  "data": [...]
}
```

## Guidelines

1. **Rate limits**: Add delays between requests to avoid 429 errors.
2. **Crawl limits**: Set reasonable `limit` values to control API usage.
3. **Main content**: Use `onlyMainContent: true` for cleaner output.
4. **Async crawls**: Large crawls are async; poll for status.
5. **Extract prompts**: Be specific for better AI extraction results.
6. **Check success**: Always check the `success` field in responses.