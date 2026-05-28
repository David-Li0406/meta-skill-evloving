---
name: linear-search
description: Search Linear issues and projects. Use when finding issues, looking up bugs, or searching the backlog.
allowed-tools: Bash(linear-cli:*)
---

# Linear Search

Search Linear.app issues and projects using `linear-cli`.

## Search Issues

```bash
# Search issues by text
linear-cli s issues "authentication bug"

# Limit results
linear-cli s issues "login" --limit 5

# Get JSON output
linear-cli s issues "error" --output json
```

## Search Projects

```bash
# Search projects
linear-cli s projects "backend"

# Limit results
linear-cli s projects "api" --limit 10
```

## Combine with Filters

After searching, you can get details on specific issues:

```bash
# Get issue details
linear-cli i get LIN-123

# Get as JSON for parsing
linear-cli i get LIN-123 --output json

# List comments on issue
linear-cli cm list LIN-123 --output json
```

## Tips

- Search is case-insensitive
- Searches issue titles and descriptions
- Use `--output json` for programmatic access
