---
name: github-search
description: Use this skill to search GitHub for code, repositories, issues, and pull requests via MCP.
---

# GitHub Search Skill

## When to Use

- Search code across repositories
- Find issues or pull requests
- Look up repository information

## Instructions

```bash
uv run python -m runtime.harness scripts/github_search.py \
    --type "<search_type>" \
    --query "<your_search_query>"
```

### Parameters

- `--type`: Search type - `code`, `repos`, `issues`, `prs`
- `--query`: Search query (supports GitHub search syntax)
- `--owner`: (optional) Filter by repository owner
- `--repo`: (optional) Filter by repository name

### Examples

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

## MCP Server Required

Requires `github` server in mcp_config.json with GITHUB_PERSONAL_ACCESS_TOKEN.