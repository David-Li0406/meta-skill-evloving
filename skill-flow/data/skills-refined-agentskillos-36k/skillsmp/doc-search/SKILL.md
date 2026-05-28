---
name: doc-search
description: Search across documentation content and metadata. Find docs by content, title, category, or tags. Use to locate relevant documentation or find where a topic is covered.
argument-hint: <query> [--tag tag] [--category cat]
allowed-tools: Read, Grep, Glob
---

# Search Documentation

Search across documentation files by content, metadata, or both.

## Instructions

1. **Parse the search query**:
   - `$ARGUMENTS` contains the search query and optional filters
   - Extract: query text, --tag filters, --category filter

2. **Search strategy**:

### Content Search
Use Grep to find matches in documentation content:
```
Search for: "$query"
In: docs/**/*.md, example/**/*.md
```

### Metadata Search
For tag/category filters, read frontmatter from matching files:
- If `--tag` specified: filter files where tags array contains the tag
- If `--category` specified: filter files where category matches

3. **Rank results by relevance**:
   - Title match: highest
   - H2/H3 header match: high
   - Content match: medium
   - Tag match: medium

4. **Present results**:

```markdown
## Search Results for "authentication"

### Exact Matches (3)

1. **Authentication Guide**
   `docs/guides/security/authentication.md`
   Category: Security | Tags: security, auth, api
   > "Learn how to implement authentication for the MCP server..."

2. **API Authentication**
   `example/api/authentication.md`
   Category: API | Tags: api, auth
   > "All API requests require authentication using..."

### Related (2)

3. **Getting Started**
   `docs/guides/getting-started.md`
   Category: Guides | Tags: beginner, setup
   > "...configure authentication in the setup process..."

---
Found 5 results in 0.2s
```

## Search Filters

| Filter | Usage | Example |
|--------|-------|---------|
| `--tag` | Filter by tag | `--tag security` |
| `--category` | Filter by category | `--category API` |
| `--title` | Search titles only | `--title` |

## Example Queries

```
/doc-search authentication              # Find docs about auth
/doc-search --tag security              # All security-tagged docs
/doc-search config --category Guides    # Config docs in Guides
/doc-search "error handling" --tag api  # API error handling docs
```

## Output Fields

For each result, show:
- **Title**: From frontmatter
- **Path**: Relative file path
- **Category**: From frontmatter
- **Tags**: From frontmatter
- **Snippet**: Matching content with context (50 chars each side)
