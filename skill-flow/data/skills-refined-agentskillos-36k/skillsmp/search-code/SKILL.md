---
name: search-code
description: Search code and documentation using full-text and semantic search. Accepts a query string and returns matching files with relevance scores.
allowed-tools: Read,Grep,Glob
metadata:
  category: search
  version: 1.0.0
---

# Search Code Skill

This skill enables agents to search through indexed code and documentation using both full-text and semantic search capabilities.

## Usage

The search-code skill accepts a query string and returns matching documents with relevance scores. It supports various filters to narrow down results.

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| query | string | Yes | - | The search query string |
| limit | int | No | 20 | Maximum number of results to return |
| type | string | No | - | Filter by document type (source_code, markdown, config, etc.) |
| path_filter | string | No | - | Filter results to paths starting with this prefix |
| fuzzy_level | int | No | 0 | Fuzzy matching level (0-2) |
| include_highlights | bool | No | false | Include matched text highlights in results |

### Document Types

- `source_code` - Source code files (.go, .py, .js, etc.)
- `markdown` - Markdown documentation files
- `config` - Configuration files (YAML, JSON, TOML)
- `llm_prompt` - LLM prompts
- `llm_response` - LLM responses
- `web_fetch` - Fetched web content
- `note` - User notes
- `git_commit` - Git commit messages

### Example Usage

Search for function definitions:
```
Search for "func main" in Go files
```

Search with type filter:
```
Search for "authentication" in source_code documents only
```

Search with path filter:
```
Search for "TODO" in files under /src/
```

### Result Format

Each result includes:
- Document ID and path
- Document type and language (if applicable)
- Relevance score (0.0 - 1.0)
- Content snippet
- Matched fields and highlights (if requested)

### Best Practices

1. Use specific queries for better precision
2. Apply type filters when searching for specific content
3. Use path filters to scope searches to relevant directories
4. Enable highlights for context in search results
5. Increase fuzzy level for typo-tolerant searches
