---
name: github-search
description: Use this skill to search GitHub for code, repositories, issues, and pull requests via MCP or GitHub CLI.
---

# GitHub Search Skill

## When to Use

- Search code across repositories
- Find issues or pull requests
- Look up repository information

## Instructions

### Using MCP

```bash
uv run python -m runtime.harness scripts/github_search.py \
    --type "<type>" \
    --query "<your search query>"
```

### Using GitHub CLI

```bash
gh search <type> <query> [flags]
```

### Parameters

- `<type>`: Search type - `code`, `repos`, `issues`, `prs`
- `<query>`: Search query (supports GitHub search syntax)
- `--owner`: (optional) Filter by repo owner
- `--repo`: (optional) Filter by repo name
- `--limit`: (optional) Max results to fetch
- `--`: (optional) Use before the query when it contains a `-` qualifier

### Examples

#### MCP Examples

```bash
# Search code
uv run python -m runtime.harness scripts/github_search.py \
    --type "code" \
    --query "authentication language:python"

# Search issues
uv run python -m runtime.harness scripts/github_search.py \
    --type "issues" \
    --query "bug label:critical" \
    --owner "anthropics"
```

#### GitHub CLI Examples

```bash
# Search code
gh search code "authentication language:python"

# Search issues
gh search issues "bug label:critical" --owner "anthropics"

# Search pull requests in a repo
gh search prs "is:open review:required" --repo "cli/cli"
```

## Requirements

- For MCP: Requires `github` server in `mcp_config.json` with `GITHUB_PERSONAL_ACCESS_TOKEN`.
- For GitHub CLI: Requires GitHub CLI (`gh`) to be installed and authenticated (`gh auth status` or `gh auth login`).