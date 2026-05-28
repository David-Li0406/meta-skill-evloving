---
name: vault-search
description: >
  Use when user wants to find past records or notes on a topic.
  Triggered when intention involves remembering, locating, or querying knowledge.
  Searches vault by content, tags, and frontmatter.
---

# Vault Search

## Behavior

1. Parse user query to extract:
   - Keywords (main search terms)
   - Time range (if mentioned: "last week", "January", etc.)
   - Type filter (project, resource, daily, etc.)
   - Tag filter (if specified)
   - Folder scope (if specified)

2. Execute search using Grep/Glob tools
3. Rank and present results with context snippets
4. Offer to open, summarize, or explore specific results

## Search Strategies

| Query Type | Method |
|------------|--------|
| By content | Grep for keywords across all .md files |
| By tag | Search `tags:` in frontmatter |
| By type | Filter by `type:` field in frontmatter |
| By project | Filter by `project:` field |
| By date | Filter by `created:` or `date:` range |
| By folder | Scope search to specific folder |

## Search Syntax Hints

- `"exact phrase"` → exact match
- `tag:ai/agents` → search by tag
- `type:project` → filter by note type
- `in:Resources` → search in specific folder
- `after:2024-01` → date filtering

## Output Format

```
## Search Results for "{query}"

Found {n} notes:

1. **{title}** (`{path}`)
   > {context snippet with match highlighted}
   Tags: {tags} | Created: {date}

2. ...
```

## Follow-up Actions

After showing results, offer:
- "Open {note name}?"
- "Summarize these results?"
- "Search for something related?"
- "Show more context from {note}?"
