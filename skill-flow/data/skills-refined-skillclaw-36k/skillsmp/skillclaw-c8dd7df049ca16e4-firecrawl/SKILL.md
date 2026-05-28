---
name: firecrawl
description: Use this skill when you need to scrape web pages, discover URLs, search the web, or extract structured data using the Firecrawl API.
---

# Skill body

## Overview

Firecrawl is a powerful web scraping and search API that allows you to fetch web content, discover URLs on sites, and extract structured data from pages.

## When to Use This Skill

Use this skill when you need to:
- **Scrape a webpage** and convert it to markdown or HTML.
- **Crawl an entire website** and extract all pages.
- **Discover all URLs** on a website.
- **Search the web** and get full page content.
- **Extract structured data** using AI.

## Prerequisites

1. Sign up at [Firecrawl](https://www.firecrawl.dev/).
2. Get your API key from the dashboard.

```bash
export FIRECRAWL_API_KEY="fc-your-api-key"
```

## Important Note

When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'` to avoid issues with environment variables being cleared.

```bash
bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $FIRECRAWL_API_KEY"'
```

## How to Use

All examples below assume you have `FIRECRAWL_API_KEY` set. The base URL for the API is `https://api.firecrawl.dev/v1`.

### 1. Scrape - Single Page

Extract content from a single webpage.

#### Basic Scrape

Write to `/tmp/firecrawl_request.json`:

```json
{
  "url": "https://example.com",
  "formats": ["markdown"]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.firecrawl.dev/v1/scrape" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" -H "Content-Type: application/json" -d @/tmp/firecrawl_request.json'
```

#### Scrape with Options

Write to `/tmp/firecrawl_request.json`:

```json
{
  "url": "https://docs.example.com/api",
  "formats": ["markdown"],
  "onlyMainContent": true,
  "timeout": 30000
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.firecrawl.dev/v1/scrape" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" -H "Content-Type: application/json" -d @/tmp/firecrawl_request.json' | jq '.data.markdown'
```

### 2. Map - Discover URLs

Finds all URLs on a website.

```bash
bash -c 'curl -s -X POST "https://api.firecrawl.dev/v1/map" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" -H "Content-Type: application/json" -d "{\"url\": \"https://example.com\"}"'
```

### 3. Search - Web Search

Searches the web and returns results with optional content scraping.

```bash
bash -c 'curl -s -X POST "https://api.firecrawl.dev/v1/search" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" -H "Content-Type: application/json" -d "{\"query\": \"typescript tutorials\"}"'
```

### 4. Extract - Structured Data

Extracts specific data from pages using LLM prompts.

```bash
bash -c 'curl -s -X POST "https://api.firecrawl.dev/v1/extract" -H "Authorization: Bearer ${FIRECRAWL_API_KEY}" -H "Content-Type: application/json" -d "{\"url\": \"https://example.com\", \"prompt\": \"Extract the main heading and description\"}"'
```