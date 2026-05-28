---
name: github-search
description: Search GitHub code, repositories, issues, and PRs via gh CLI
allowed-tools: [Bash, Read]
---

# GitHub Search Skill

## When to Use

- Search code across repositories
- Find issues or PRs
- Look up repository information

## Instructions

```bash
gh search <type> <query> [flags]
```

### Parameters

- `<type>`: Search type - `code`, `repos`, `issues`, `prs`
- `<query>`: Search query (supports GitHub search syntax)
- `--owner`: (optional) Filter by repo owner (all search types)
- `--repo`: (optional) Filter by repo name (code/issues/prs only)
- `--limit`: (optional) Max results to fetch
- `--`: (optional) Use before the query when it contains a `-` qualifier, e.g. `-- "bug -label:critical"`

### Examples

```bash
# Search code
gh search code "authentication language:python"

# Search issues
gh search issues "bug label:critical" --owner "anthropics"

# Search pull requests in a repo
gh search prs "is:open review:required" --repo "cli/cli"
```

## Requirements

Requires GitHub CLI (`gh`) to be installed and authenticated (`gh auth status` or `gh auth login`).
