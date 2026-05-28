---
name: github-workflow
description: Use for GitHub operations - creating PRs, checking CI status, reviewing PR comments, managing issues.
---

# GitHub Workflow

## Overview

This skill triggers the **github** MCP server for repository operations using Personal Access Token authentication.

## When to Use

- "Create a pull request"
- "Check CI status"
- "List open issues"
- "Get PR review comments"
- "Merge this PR"
- "What's the build status?"

## Available Operations

### Pull Requests
```
- Create new PR with title and body
- List open/closed PRs
- Get PR details and comments
- Merge PR (with approval)
- Close PR
```

### Issues
```
- List open issues
- Create new issue
- Add comments to issues
- Close/reopen issues
- Add labels
```

### CI/CD
```
- Check workflow run status
- Get build logs
- Re-run failed workflows
- View action results
```

### Repository
```
- List branches
- Compare branches
- Get commit history
- Check file contents
```

## MCP Server

**Server**: github
**Package**: @github/mcp-server
**Requires**: GITHUB_TOKEN environment variable set

## VeilBreakers Repo

**Repository**: Sharks820/VeilBreakers3D
**Main Branch**: master
**Current Branch**: feature/godot-documentation-transfer

## PR Template

```markdown
## Summary
[1-3 bullet points]

## Changes
- [List of changes]

## Testing
- [ ] Tested in Unity Editor
- [ ] No compile errors
- [ ] No console warnings
```

## Workflow Integration

### Before Merge
1. Create PR with clear description
2. Run unity-code-reviewer agent on changes
3. Check CI status via this skill
4. Address any review comments
5. Merge when approved

### Issue Tracking
1. Check open issues before starting work
2. Reference issue numbers in commits
3. Close issues via commit message or PR
