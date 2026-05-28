---
name: kagi-search
description: Use this skill when you need to search the web for current information, documentation, facts, or references using the Kagi Search API.
---

# Kagi Search

Web search using the Kagi Search API, returning results with titles, URLs, snippets, and optional Quick Answers.

## Quick Start

```bash
export KAGI_API_KEY="your_api_key"
kagi-search "your search query"
# or run directly:
python3 scripts/kagi-search.py "your search query"
```

## Features

- **Clean output** - Title, URL, snippet, and metadata for each result
- **Quick Answers** - Returns a summary with references when available
- **Pagination support** - Control result count and offset
- **JSON mode** - Raw JSON output for scripting
- **API balance** - Displays remaining API quota
- **Fast & lightweight** - Pure Python, no dependencies

## Options

| Flag | Description |
|------|-------------|
| `query` | Search terms (required) |
| `-n, --limit` | Number of results (default: 10) |
| `-s, --offset` | Offset for pagination (default: 0) |
| `--json` | Output raw JSON |
| `--no-related` | Hide related searches |
| `-d, --debug` | Enable debug mode (logs to stderr) |
| `-h, --help` | Show help |

## Examples

```bash
# Basic search
kagi-search "python async await tutorial"

# Limit results
kagi-search "AI news" --limit 5

# Pagination
kagi-search "recipes" --offset 10 --limit 5

# JSON for scripting
kagi-search "github stars" --json | jq '.results[].url'

# Hide related searches
kagi-search "rust programming" --no-related
```

## JSON Output Format

```json
{
  "results": [
    {
      "title": "Page Title",
      "url": "https://example.com",
      "snippet": "Description text..."
    }
  ],
  "quick_answer": {
    "markdown": "Formatted answer...",
    "raw_text": "Plain text answer...",
    "references": [
      { "title": "Source", "url": "https://..." }
    ]
  }
}
```

## Setup

**Environment:**
```bash
export KAGI_API_KEY="your_api_key"
# Add to ~/.bashrc or ~/.zshrc for persistence
```

**PATH access:**
```bash
# Make executable and add to PATH
chmod +x scripts/kagi-search.py
cp scripts/kagi-search.py ~/.local/bin/kagi-search
```

## Requirements

- Python 3.7+
- `KAGI_API_KEY` environment variable
- Internet connection

## Workflow

1. Run `kagi-search --json "query"`
2. Parse JSON response
3. Check `quick_answer` first - often has the direct answer with citations
4. Use `results` array for detailed sources and additional context