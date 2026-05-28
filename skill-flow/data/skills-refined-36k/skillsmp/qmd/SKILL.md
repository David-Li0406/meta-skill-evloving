---
name: qmd
description: |
  Local semantic search for docs, notes, knowledge bases. INVOKE THIS SKILL when user:
  - Asks to "search my notes/docs/vault/obsidian"
  - Wants to "find" something in their knowledge base
  - Says "what did I write about X"
  - Asks "do I have notes on X"
  - Needs context from their local markdown files
  - Mentions "qmd" directly
  - Asks about journal entries, meeting notes, or personal documentation
  Trigger phrases: "search notes", "find in docs", "search obsidian", "what do my notes say", "look in my vault"
allowed-tools: Bash, Read
---

# qmd - Local Document Search

Semantic + full-text search across local markdown docs using local LLMs.

## When to Use

Use qmd when the user wants to search their personal notes, documentation, or knowledge base. This includes Obsidian vaults, markdown notes directories, and any indexed collections.

## Search Commands

```sh
qmd search "query"    # BM25 full-text search
qmd vsearch "query"   # Semantic vector search
qmd query "query"     # Hybrid search with LLM reranking (best quality)
```

## Search Flags

| Flag | Purpose |
|------|---------|
| `-n <num>` | Limit results (default: 5) |
| `-c, --collection` | Restrict to specific collection |
| `--all` | Return all matches |
| `--min-score <num>` | Filter by relevance threshold |
| `--full` | Display complete document content |
| `--line-numbers` | Include line numbers |

## Output Formats

| Flag | Format |
|------|--------|
| `--files` | CSV: docid, score, filepath, context |
| `--json` | Structured JSON with snippets |
| `--csv` | Comma-separated values |
| `--md` | Markdown formatting |
| `--xml` | XML structure |

## Document Retrieval

```sh
qmd get "path/to/doc.md"      # Get specific document
qmd get "#abc123"             # Get by document ID
qmd multi-get "journals/*.md" # Get multiple docs by glob
```

## Collection Management

```sh
qmd collection list           # View all collections
qmd collection add ~/notes --name notes
qmd ls notes                  # List files in collection
qmd status                    # Index health
```

## Examples

```sh
# High-quality search with reranking
qmd query -n 10 "API design patterns"

# Full document content for LLM context
qmd search --md --full "error handling"

# Search specific collection
qmd search "meeting notes" -c work
```

## Workflow

1. Use `qmd collection list` to see available collections
2. Use `qmd query` for best search quality (uses LLM reranking)
3. Use `--full` when you need complete document content
4. Use `qmd get` to retrieve specific documents by path or ID

## Quick Start for Common Requests

| User says | Run this |
|-----------|----------|
| "search my notes for X" | `qmd query "X"` |
| "what did I write about X" | `qmd query --full "X"` |
| "find meeting notes about X" | `qmd search -c obsidian "meeting X"` |
| "show me my notes on X" | `qmd query -n 3 --full "X"` |
