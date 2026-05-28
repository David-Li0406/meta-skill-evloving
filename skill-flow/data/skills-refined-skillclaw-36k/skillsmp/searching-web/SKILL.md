---
name: searching-web
description: Searches the web using Tavily API for real-time information. Use when the user needs current information, wants to search the internet, or asks questions requiring up-to-date web data.
---

# Web Search Tools

Tools for searching the web using the Tavily API.

## Requirements

Set environment variable:
- `TAVILY_API_KEY`: Your Tavily API key

## Basic Search

```python
result = await tavily_search(
    query="latest Python release",
    max_results=5
)
```

### Response format

```json
{
  "success": true,
  "data": {
    "results": [
      {
        "title": "Result Title",
        "url": "https://example.com",
        "content": "Snippet of the page content...",
        "score": 0.95
      }
    ],
    "query": "latest Python release"
  }
}
```

## Advanced Options

```python
result = await tavily_search(
    query="machine learning tutorials",
    max_results=10,
    search_depth="advanced",
    include_domains=["github.com", "arxiv.org"],
    exclude_domains=["pinterest.com"]
)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| query | str | Search query (required) |
| max_results | int | Number of results (default: 5) |
| search_depth | str | "basic" or "advanced" |
| include_domains | list | Only search these domains |
| exclude_domains | list | Exclude these domains |

## When to Use

- Finding current information not in training data
- Researching recent events or news
- Looking up documentation or tutorials
- Fact-checking with web sources
