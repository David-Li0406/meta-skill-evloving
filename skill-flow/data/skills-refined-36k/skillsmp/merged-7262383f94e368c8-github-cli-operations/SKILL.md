---
name: github-cli-operations
description: Use this skill when interacting with GitHub repositories, managing pull requests, and checking CI status via the GitHub CLI.
---

# GitHub CLI Operations

Use GitHub CLI (`gh`) to interact with GitHub repositories, pull requests, issues, and workflows.

## Prerequisites

- GitHub CLI installed: `brew install gh` (macOS) or see [cli.github.com](https://cli.github.com)
- Authenticated: `gh auth login` (one-time setup)
- Repository context: Run commands from within a git repository or specify `--repo owner/repo`

## Quick Start

**Get PR details:**
```bash
gh pr view <pr-number> --json title,body,author,state
```

**Get PR diff:**
```bash
gh pr diff <pr-number>
```

**Check CI status:**
```bash
gh pr checks <pr-number>
```

**Create a PR:**
```bash
gh pr create --title "<title>" --body "<body>"
```

## Usage Patterns for PR Review

### Get PR Context

Get PR title, description, and metadata:
```bash
gh pr view <pr-number> --json title,body,author,state,baseRefName,headRefName
```

Get changed files:
```bash
gh pr view <pr-number> --json files --jq '.files[].path'
```

Get diff for specific file:
```bash
gh pr diff <pr-number> -- path/to/file
```

### Check PR Status

Check CI status:
```bash
gh pr checks <pr-number>
```

Check if PR is mergeable:
```bash
gh pr view <pr-number> --json mergeable,mergeStateStatus
```

### Link to Issues

Extract issue references from PR body:
```bash
gh pr view <pr-number> --json body --jq '.body' | grep -oE 'LIN-[0-9]+'
```

## Creating and Updating PRs

### Create a PR

```bash
gh pr create --title "<title>" --body "<body>"
```

### Update a PR

Edit title/body:
```bash
gh pr edit <pr-number> --title "<new-title>" --body "<new-body>"
```

Add/remove labels:
```bash
gh pr edit <pr-number> --add-label "<label>" --remove-label "<label>"
```

Add/remove reviewers:
```bash
gh pr edit <pr-number> --add-reviewer "<reviewer>" --remove-reviewer "<reviewer>"
```

## Viewing Failed Test Logs

```bash
gh run view <run-id> --log-failed
```

## Other Useful Commands

```bash
# List open PRs
gh pr list

# Checkout PR locally
gh pr checkout <pr-number>
```

## Reference Documentation

- **Command Reference**: See [commands.md](references/commands.md) for complete GitHub CLI command reference
- **GitHub CLI Manual**: [cli.github.com/manual](https://cli.github.com/manual)