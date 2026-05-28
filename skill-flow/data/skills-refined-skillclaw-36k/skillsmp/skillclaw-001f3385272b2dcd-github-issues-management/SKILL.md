---
name: github-issues-management
description: Use this skill when you need to manage GitHub issues and pull requests using the `gh` CLI tool.
---

# Skill body

You are a GitHub workflow assistant specialized in using the `gh` CLI tool for managing issues and pull requests on GitHub.

## When to use this skill

Use this skill when you want to:

- View or fetch GitHub issues
- Create, edit, or manage issues
- View or analyze pull requests
- Get file content from GitHub repositories
- Search issues or PRs
- View PR diffs or comments
- Check PR status or CI checks
- Any other GitHub-related operation

## Important Rules

**CRITICAL:**

- **ALWAYS use `gh` CLI via Bash** for GitHub operations
- **NEVER use GitHub MCP tools** - use `gh` CLI instead
- Prefer `gh` commands over `gh api` when available
- Always work within the current repository context

## Common GitHub Operations

### View Issues

```bash
# List issues
gh issue list

# View specific issue
gh issue view <issue-number>

# View issue with comments
gh issue view <issue-number> --comments

# Search issues
gh issue list --search "search terms"

# Filter by state
gh issue list --state open
gh issue list --state closed
```

### Create and Manage Issues

```bash
# Create a new issue interactively
gh issue create

# Create an issue with title and body
gh issue create --title "Issue Title" --body "Issue Body"

# Add a comment to an issue
gh issue comment <issue-number> --body "Your comment here"

# Close an issue
gh issue close <issue-number>

# Reopen an issue
gh issue reopen <issue-number>

# Edit an issue to add labels or assignees
gh issue edit <issue-number> --add-label "bug" --add-assignee "@me"
```

### View Pull Requests

```bash
# List PRs
gh pr list

# View specific PR
gh pr view <pr-number>

# View PR with diff
gh pr view <pr-number> --diff

# View PR comments
gh pr view <pr-number> --comments

# Check PR status
gh pr status

# List PR files
gh pr diff <pr-number> --name-only
```

### Get File Content

```bash
# View file from current repo
gh api repos/{owner}/{repo}/contents/{path}

# View file from specific branch
gh api repos/{owner}/{repo}/contents/{path}?ref=branch-name
```

### CI/CD Status

```bash
# Check workflow runs
gh run list

# View specific run
gh run view <run-id>

# View run logs
gh run view <run-id> --log

# List checks for PR
gh pr checks <pr-number>
```

### Best Practices

- Always check the current status of the repository with `gh issue list` before creating new issues to avoid duplicates.
- Use descriptive titles and detailed bodies for new issues.
- When working on an issue, assign it to yourself to avoid overlapping work.
- Use `gh issue status` to see a summary of issues relevant to you.