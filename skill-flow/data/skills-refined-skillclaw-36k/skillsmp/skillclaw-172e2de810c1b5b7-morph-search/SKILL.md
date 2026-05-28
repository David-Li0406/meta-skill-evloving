---
name: morph-search
description: Use this skill when you need to perform fast codebase searches and edits using WarpGrep, significantly faster than traditional grep.
---

# Morph Codebase Search

Fast, AI-powered codebase search using WarpGrep. 20x faster than traditional grep.

## When to Use

- Search codebase for patterns, function names, and variables.
- Quickly find code across large codebases.
- Programmatically edit files.

## Usage

### Search for Code Patterns
```bash
uv run python -m runtime.harness scripts/morph_search.py \
    --search "authentication" --path "."
```

### Search with Regex
```bash
uv run python -m runtime.harness scripts/morph_search.py \
    --search "def.*login" --path "./src"
```

### Edit a File
```bash
uv run python -m runtime.harness scripts/morph_search.py \
    --edit "/path/to/file.py" --content "new content"
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--search` | Search query/pattern |
| `--path` | Directory to search (default: `.`) |
| `--edit` | File path to edit |
| `--content` | New content for file (use with `--edit`) |

## Examples

```bash
# Find all async functions
uv run python -m runtime.harness scripts/morph_search.py \
    --search "async def" --path "./src"

# Search for imports
uv run python -m runtime.harness scripts/morph_search.py \
    --search "from fastapi import" --path "."
```

## Comparison with ast-grep

| Tool | Best For |
|------|----------|
| **morph/warpgrep** | Fast text/regex search (20x faster) |
| **ast-grep** | Structural code search (understands syntax) |

## MCP Server Required

Requires `morph` server in `mcp_config.json` with `MORPH_API_KEY`.