---
name: firecrawl
description: Web scraping, search, and data extraction using Firecrawl API. Use when users need to fetch web content, discover URLs on sites, search the web, or extract structured data from pages.
---

# Firecrawl

## Overview

Firecrawl is a powerful web scraping and search API. This plugin provides a token-efficient interface for Claude Code through slash commands.

## When to Use This Skill

- **Scraping**: Fetch content from a single URL as markdown
- **Mapping**: Discover all URLs on a website
- **Searching**: Search the web and optionally scrape results
- **Extracting**: Pull structured data from pages using LLM

## Quick Reference

| Task | Command |
|------|---------|
| Scrape a page | `/firecrawl:scrape <url>` |
| Map a site | `/firecrawl:map <url>` |
| Search the web | `/firecrawl:search <query>` |
| Extract data | `/firecrawl:extract <url> --prompt "..."` |

## Commands

### Scrape - Get Page Content

Fetches and converts a web page to clean markdown.

```
/firecrawl:scrape https://example.com
/firecrawl:scrape https://example.com --format summary
```

**Options:**
- `--format markdown|summary` - Output format (default: markdown)

**Best for:**
- Reading documentation
- Fetching article content
- Getting page text for analysis

### Map - Discover URLs

Finds all URLs on a website. Useful for understanding site structure.

```
/firecrawl:map https://example.com
/firecrawl:map https://example.com --limit 50
```

**Options:**
- `--limit N` - Maximum URLs to return (default: 100)

**Best for:**
- Understanding site structure
- Finding specific pages before scraping
- Discovering documentation sections

### Search - Web Search

Searches the web and returns results with optional content scraping.

```
/firecrawl:search typescript tutorials
/firecrawl:search "react hooks guide" --limit 10
```

**Options:**
- `--limit N` - Maximum results (default: 5)

**Supports search operators:**
- `"exact phrase"` - Exact match
- `-term` - Exclude term
- `site:example.com` - Limit to domain
- `intitle:word` - Word in title

**Best for:**
- Finding information across the web
- Researching topics
- Finding documentation

### Extract - Structured Data

Extracts specific data from pages using LLM prompts.

```
/firecrawl:extract https://example.com --prompt "Extract the main heading and description"
/firecrawl:extract https://example.com/product --prompt "Extract price and features" --schema '{"price": {"type": "number"}, "features": {"type": "array"}}'
```

**Options:**
- `--prompt "text"` - What to extract (required)
- `--schema '{...}'` - JSON Schema for structured output

**Best for:**
- Extracting specific data points
- Getting structured information
- Pulling prices, names, dates, etc.

## Environment Setup

Requires `FIRECRAWL_API_KEY` environment variable.

Get your API key from: https://firecrawl.dev

## Examples

### Research a Topic
```
/firecrawl:search "best practices for TypeScript error handling" --limit 5
```

### Read Documentation
```
/firecrawl:scrape https://docs.example.com/api/authentication
```

### Map a Documentation Site
```
/firecrawl:map https://docs.example.com --limit 200
```

### Extract Product Info
```
/firecrawl:extract https://store.example.com/product/123 --prompt "Extract product name, price, and availability"
```

## Token Efficiency

This plugin is designed for minimal token consumption:

- **Scrape**: Returns clean markdown, truncated at 8000 chars
- **Map**: Shows up to 50 URLs with titles
- **Search**: Limits to 10 results with summaries
- **Extract**: Returns only requested data

Compare to the full MCP server which loads ~14k tokens just from tool definitions.

## Error Handling

Common errors:
- `API key required` - Set FIRECRAWL_API_KEY
- `Invalid URL` - Check URL format
- `Rate limited` - Wait and retry (auto-handled)
- `Site blocked` - Some sites block scraping

## Pricing Note

Firecrawl charges per operation:
- Scrape: 1 credit per page
- Map: 1 credit per call
- Search: 1 credit per result
- Extract: Varies by complexity

Check https://firecrawl.dev/pricing for current rates.
