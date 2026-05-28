---
name: brave-search
description: Use this skill for headless web search and content extraction via the Brave Search API, ideal for retrieving documentation, facts, or any web content without a browser.
---

# Brave Search

Headless web search and content extraction using Brave Search. No browser required.

## Setup

Run once before first use:

```bash
cd {baseDir}
npm ci
```

Needs environment variable: `BRAVE_API_KEY`.

## Search

```bash
{baseDir}/search.js "query"                    # Basic search (5 results)
{baseDir}/search.js "query" -n 10              # More results
{baseDir}/search.js "query" --content          # Include page content as markdown
{baseDir}/search.js "query" -n 3 --content     # Combined
```

## Extract Page Content

```bash
{baseDir}/content.js https://example.com/article
```

Fetches a URL and extracts readable content as markdown.

## Output Format

```
--- Result 1 ---
Title: Page Title
Link: https://example.com/page
Snippet: Description from search results
Content: (if --content flag used)
  Markdown content extracted from the page...

--- Result 2 ---
...
```

## When to Use

- Searching for documentation or API references
- Looking up facts or current information
- Fetching content from specific URLs
- Any task requiring web search without interactive browsing