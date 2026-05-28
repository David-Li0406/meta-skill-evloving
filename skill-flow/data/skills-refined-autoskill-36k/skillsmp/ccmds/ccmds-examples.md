# ccmds Examples & Workflows

Common patterns and workflows for efficient documentation search.

## Workflows

### Progressive Search (Most Efficient)

Start broad, narrow down, extract what you need:

```bash
# 1. Understand structure (minimal context)
ccmds outline -d 2

# 2. Find relevant docs
ccmds find "database migration" -o files

# 3. Extract just what you need
ccmds section ./docs/database/migrations.md "Schema Changes"
```

### Quick Answer

When you know the topic and likely file:

```bash
ccmds section ./docs/setup.md "Installation"
```

### Deep Research

When you need comprehensive information:

```bash
# Find all relevant docs
ccmds find "caching strategy" -l 10

# Then grep for specific patterns
ccmds grep "cache.*invalidat"
```

### Exploring Unknown Codebase

```bash
# See what documentation exists
ccmds list

# Get high-level structure
ccmds outline -d 2

# Search for specific topic
ccmds find "getting started"
```

---

## Common User Queries

| User Says | Command |
|-----------|---------|
| "What do the docs say about auth?" | `ccmds find "authentication"` |
| "How do I install this?" | `ccmds find "installation setup" -l 3` |
| "Find error E404" | `ccmds grep "E404"` |
| "Show me the API reference" | `ccmds outline -d 2` then `ccmds show` |
| "What's documented?" | `ccmds list` |
| "Check the troubleshooting guide" | `ccmds find "troubleshooting" -o files` |
| "Where is X configured?" | `ccmds grep "X.*config"` |
| "Find all TODOs in docs" | `ccmds grep "TODO\|FIXME" -o files` |

---

## Search Patterns

### AND Search (all terms must match)

```bash
ccmds find "authentication middleware"
ccmds find "database connection pool"
```

### OR Search (either term matches)

```bash
ccmds find "setup | installation"
ccmds find "error | exception | failure"
```

### Exact Match

```bash
ccmds find "'API Reference"
ccmds grep "specific phrase"
```

### Regex Patterns

```bash
ccmds grep "ERROR_[0-9]+"
ccmds grep "v[0-9]+\.[0-9]+"
ccmds grep "TODO|FIXME|HACK"
```

---

## Output Mode Selection

| Mode | When to Use |
|------|-------------|
| `json` | AI-optimized, compact (default) |
| `files` | Just need to know which files contain info |
| `compact` | Human-readable overview with snippets |
| `detailed` | Need full context around matches |

```bash
ccmds find "auth"               # Default: compact JSON for AI
ccmds find "auth" -o files      # Minimal: just paths
ccmds find "auth" -o compact    # Human-readable snippets
ccmds find "auth" -o detailed   # Full context
```

---

## Troubleshooting

### No results found

```bash
# Check config is correct
ccmds config

# Try fuzzy search instead of grep
ccmds find "term" instead of ccmds grep "term"

# Check files exist
ccmds list
```

### Too many results

```bash
# Limit results
ccmds find "query" -l 5

# Use more specific terms
ccmds find "authentication middleware" instead of "auth"

# Search specific directory
ccmds find "query" ./docs/api
```

### Results not relevant

```bash
# Use grep for exact matches
ccmds grep "exact term"

# Check structure first
ccmds outline -d 2

# Try different terms
```

---

## Best Practices

**DO:**
- Start with `outline` to understand structure
- Use `section` to extract only what you need
- Use `find` for conceptual queries
- Use `grep` for exact/pattern matches
- Use `-o files` when you just need paths

**DON'T:**
- Load entire files unless necessary
- Use `detailed` output for many results
- Specify directories if config has them
- Forget to escape regex special chars in grep
