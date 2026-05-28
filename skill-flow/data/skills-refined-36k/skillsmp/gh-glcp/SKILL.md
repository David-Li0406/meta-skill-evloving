---
name: gh-glcp
description: GitHub CLI best practices for GLCP organization. **REQUIRED** Use when accessing GitHub resources (workflows, PRs, issues, commits) in the glcp organization. Always prefer `gh` CLI over GitHub MCP server tools for glcp org to avoid 404 errors and access issues.
---

# GitHub CLI for GLCP Organization

Use GitHub CLI (`gh`) for all GitHub operations in the `glcp` organization instead of GitHub MCP server tools.

## When to Use This Skill

**ALWAYS use `gh` CLI for glcp organization when:**
- Viewing workflow runs and job logs
- Accessing pull requests
- Reading issues and comments
- Getting commit details
- Any other GitHub API operations

**Problem:** GitHub MCP server tools frequently return 404 errors for glcp organization resources, even when they exist.

**Solution:** Use `gh` CLI commands which have direct authentication and proper access.

## Common Operations

### Workflow Runs and Jobs

**View workflow run with failed job logs:**
```bash
gh run view <run-id> --repo glcp/<repo-name> --log-failed
```

**View specific job details:**
```bash
gh run view <run-id> --repo glcp/<repo-name> --job <job-id>
```

**List workflow runs:**
```bash
gh run list --repo glcp/<repo-name> --limit 10
```

### Pull Requests

**View PR details:**
```bash
gh pr view <pr-number> --repo glcp/<repo-name>
```

**Check PR status:**
```bash
gh pr view <pr-number> --repo glcp/<repo-name> --json state,mergedAt
```

**List PRs:**
```bash
gh pr list --repo glcp/<repo-name> --limit 10
```

### Issues

**View issue:**
```bash
gh issue view <issue-number> --repo glcp/<repo-name>
```

**List issues:**
```bash
gh issue list --repo glcp/<repo-name> --limit 10
```

### Commits

**View commit details:**
```bash
gh api repos/glcp/<repo-name>/commits/<sha>
```

## Best Practices

- Always specify `--repo glcp/<repo-name>` for clarity
- Use `--json` flag for structured output when parsing is needed
- Pipe large outputs through `grep`, `head`, or `tail` for manageable results
- Save large outputs to temp files for analysis

## Error Handling

If `gh` CLI returns authentication errors:
1. Check `gh auth status`
2. Re-authenticate with `gh auth login`
3. Ensure correct organization access

If resources truly don't exist, `gh` will provide clear error messages unlike the ambiguous 404s from MCP tools.
