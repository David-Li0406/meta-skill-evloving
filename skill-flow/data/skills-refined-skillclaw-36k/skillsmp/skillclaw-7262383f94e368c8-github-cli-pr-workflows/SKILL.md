---
name: github-cli-pr-workflows
description: Use this skill when managing pull requests on GitHub, including checking CI status, viewing logs, and creating or updating PRs via the command line.
---

# GitHub CLI for PR Workflows

Quick reference for `gh` commands focused on pull request workflows.

## Prerequisites

- GitHub CLI installed: `brew install gh` (macOS) or see [cli.github.com](https://cli.github.com)
- Authenticated: `gh auth login` (one-time setup)
- Repository context: Run commands from within a git repository or specify `--repo owner/repo`

## Checking PR Status

```bash
# Check CI status for current branch's PR
gh pr checks

# Check specific PR
gh pr checks <pr-number>

# Watch until checks finish
gh pr checks --watch

# Only show required checks
gh pr checks --required

# JSON output for scripting
gh pr checks --json name,state,conclusion
```

Exit codes: `0` = passed, `1` = failed, `8` = pending

## Viewing Failed Test Logs

```bash
# View run summary (interactive picker if no ID)
gh run view

# View specific run with job details
gh run view <run-id> -v

# View logs for failed steps only (most useful)
gh run view <run-id> --log-failed

# View full log for a specific job
gh run view --job <job-id> --log

# Open in browser
gh run view <run-id> --web
```

To get job ID from a URL like `.../runs/123/job/456`, job ID is `456`.

## Creating PRs

```bash
# Interactive (prompts for title/body)
gh pr create

# With title and body
gh pr create --title "Fix bug" --body "Details here"

# Auto-fill from commit messages
gh pr create --fill

# Draft PR
gh pr create --draft

# With reviewers and labels
gh pr create -r reviewer1,reviewer2 -l bug,urgent

# Specify base branch
gh pr create --base develop
```

## Updating PRs

```bash
# Edit title/body
gh pr edit <pr-number> --title "New title" --body "New body"

# Add/remove labels
gh pr edit <pr-number> --add-label "bug" --remove-label "wip"

# Add/remove reviewers
gh pr edit <pr-number> --add-reviewer alice --remove-reviewer bob

# Self-assign
gh pr edit <pr-number> --add-assignee "@me"

# Change base branch
gh pr edit <pr-number> --base main
```

## Other Useful Commands

```bash
# View PR details
gh pr view <pr-number>

# View PR in browser
gh pr view <pr-number> --web

# List open PRs
gh pr list

# Checkout PR locally
gh pr checkout <pr-number>

# View PR comments
gh api repos/{owner}/{repo}/issues/<pr-number>/comments

# Re-run failed jobs
gh run rerun <run-id> --failed
```