---
name: gh-cli
description: GitHub CLI (gh) for debugging GitHub Actions and viewing releases. Use when working with: (1) GitHub Actions - view runs, check failures, download logs, re-run workflows, watch builds, (2) Releases - view, list, and download release assets. Supports JSON output for scripting and automation.
---

# GitHub CLI (gh) Skill

Focused guide to using GitHub CLI for debugging GitHub Actions and accessing release information.

## Authentication

```bash
# Login with browser
gh auth login

# Check authentication status
gh auth status

# Switch between accounts
gh auth switch
```

## GitHub Actions

### Viewing Runs

```bash
# List recent workflow runs
gh run list

# List runs with limit
gh run list --limit 50

# List runs by status
gh run list --status failure
gh run list --status success
gh run list --status in_progress

# List runs for specific workflow
gh run list --workflow "CI"

# List runs on specific branch
gh run list --branch main

# Get JSON output for scripting
gh run list --json conclusion,name,databaseId,headBranch,createdAt,status,displayTitle
```

### Viewing Run Details

```bash
# View run summary
gh run view <run-id>

# View run in browser
gh run view <run-id> --web

# View failed logs only
gh run view <run-id> --log-failed

# View full logs
gh run view <run-id> --log

# View job details
gh run view <run-id> --job <job-id>
```

### Managing Runs

```bash
# Cancel a running workflow
gh run cancel <run-id>

# Re-run a workflow
gh run rerun <run-id>

# Re-run only failed jobs
gh run rerun <run-id> --failed

# Watch a run in real-time
gh run watch <run-id>

# Download run artifacts
gh run download <run-id>

# Download specific artifact
gh run download <run-id> --name artifact-name
```

### Working with Workflows

```bash
# List workflows
gh workflow list

# View workflow details
gh workflow view <workflow-name>

# Enable/disable workflow
gh workflow enable <workflow-name>
gh workflow disable <workflow-name>

# Trigger a workflow
gh workflow run <workflow-name>

# Trigger with inputs
gh workflow run <workflow-name> --field key=value
```

### Finding Failed Runs

```bash
# Get last 3 failed runs with details
gh run list --status failure --limit 3 --json conclusion,name,databaseId,headBranch,createdAt,displayTitle

# Filter by workflow name
gh run list --status failure --workflow "CI" --limit 10

# Get failure details and logs
gh run list --status failure --limit 1 | \
  jq -r '.[0].databaseId' | \
  xargs -I {} gh run view {} --log-failed
```

## Pull Requests (Viewing Only)

```bash
# List open PRs
gh pr list

# List PRs by author
gh pr list --author @me

# View PR in terminal
gh pr view <pr-number>

# View PR in browser
gh pr view <pr-number> --web

# View PR checks/status
gh pr checks <pr-number>

# Checkout a PR locally
gh pr checkout <pr-number>
```

## Releases

```bash
# List releases
gh release list

# View specific release
gh release view <tag>

# View latest release
gh release view --latest

# Download release assets
gh release download <tag>

# Download specific asset
gh release download <tag> --pattern "*.tar.gz"

# Get JSON output
gh release list --json tagName,name,createdAt,isLatest
```

## Repository Operations

```bash
# View repository details
gh repo view

# View in browser
gh repo view --web

# View specific repo
gh repo view owner/repo

# Clone repository
gh repo clone owner/repo
```

## JSON Output and Scripting

```bash
# Get specific fields from runs
gh run list --json databaseId,conclusion,name,createdAt | \
  jq '.[] | select(.conclusion == "failure")'

# Count failures by workflow
gh run list --limit 100 --json name,conclusion | \
  jq 'group_by(.name) | map({name: .[0].name, failures: map(select(.conclusion == "failure")) | length})'

# Custom table format
gh run list --json conclusion,name,createdAt | \
  jq -r '.[] | "\(.createdAt)\t\(.conclusion)\t\(.name)"'
```

## Investigating CI Failures Workflow

```bash
# 1. List recent failures
gh run list --status failure --limit 10

# 2. View specific failure details
gh run view <run-id>

# 3. Check failed logs
gh run view <run-id> --log-failed

# 4. Re-run failed jobs
gh run rerun <run-id> --failed

# 5. Watch re-run
gh run watch <run-id>
```

## Configuration

```bash
# View current config
gh config list

# Set default repository for session
export GH_REPO="owner/repo"
```

## Environment Variables

- `GH_TOKEN` - Authentication token
- `GH_REPO` - Default repository (owner/repo)
- `GH_HOST` - GitHub Enterprise host
- `GITHUB_TOKEN` - Alternative to GH_TOKEN

## Tips & Best Practices

1. **Use JSON output for automation**: Add `--json field1,field2` for structured data
2. **Leverage jq for filtering**: Pipe JSON output to jq for complex filtering
3. **Set defaults**: Use `GH_REPO` environment variable for frequently used repos
4. **Watch runs in real-time**: Use `gh run watch` to monitor CI/CD
5. **Filter early**: Use built-in filters (`--status`, `--workflow`, `--branch`) before piping to jq
6. **Download artifacts**: Use `gh run download` to get build artifacts for debugging

## Getting Help

```bash
gh help                    # General help
gh <command> --help        # Command-specific help
```
