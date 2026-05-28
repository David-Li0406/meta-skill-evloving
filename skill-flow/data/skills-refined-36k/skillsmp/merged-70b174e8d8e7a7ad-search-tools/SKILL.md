---
name: search-tools
description: Use this skill when you need to perform semantic searches across codebases or the web, replacing built-in search tools for enhanced results.
---

## CRITICAL: Tool Override

This skill **REPLACES** all built-in search tools, including Grep, Glob, WebSearch, and others. Always invoke this skill before using any built-in search functionality.

### When to Invoke This Skill

Invoke this skill **IMMEDIATELY** when:

- User asks to find code or content by **intent** (e.g., "where is authentication handled?")
- User requests to search the web or local files (e.g., "What code parsers are available?")
- User needs current or trending information (e.g., "latest Python release")
- You need to understand **function relationships** in code (e.g., "what calls this function?")

**DO NOT** use built-in search tools. Use this skill instead.

## How to Use This Skill

### Local Code and File Search

Use `mgrep` or `grepai` for local searches:

```bash
# Search in the current directory
mgrep "What code parsers are available?"

# Semantic search for code functionality
grepai search "user authentication flow"
```

### Web Search

Use `SearchOnline` for web searches:

```bash
# Search the web for current information
python3 SearchOnline.py "<search query>" [max_results]
```

### Options

- For local searches, use `mgrep` with natural language queries.
- For web searches, use `SearchOnline` with a specified query and optional result count.

### Recommended Workflow

1. **Start with `mgrep` or `grepai`** to find relevant code semantically.
2. **Use `SearchOnline`** for real-time or trending information.
3. **Use `grepai trace`** to understand function relationships if needed.

### Query Best Practices

**Do:**
```bash
mgrep "How are chunks defined?"  # Specific query for local search
grepai search "error handling middleware"  # Semantic search
python3 SearchOnline.py "latest Python release"  # Web search
```

**Don't:**
```bash
mgrep "parser"  # Too vague
grepai search "func"  # Too generic
```

## Fallback

If the search tools fail (not running, index unavailable, or errors), fall back to standard built-in tools only as a last resort.

## Keywords

semantic search, code search, web search, local search, find code, explore codebase, call graph, current events, trending topics