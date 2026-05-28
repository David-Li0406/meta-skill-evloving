---
name: gh-pr-sync
description: "Sync GitHub PRs to local YAML files for code review analysis."
---

# gh-pr-sync

Syncs GitHub pull requests to local YAML files in `.prs/`.

## Commands

```
gh-pr-sync pull                  # Fetch open PRs from current repo
gh-pr-sync pull --repo owner/repo  # Fetch from specific repo
gh-pr-sync pull --limit 50       # Limit number of PRs (default 100)
gh-pr-sync pull --all            # Include closed/merged PRs
```

## File Format

`.prs/42-fix-login-bug.yaml`:
```yaml
number: 42
title: Fix login bug
state: open
author: alice
head: fix-login
base: main
labels: [bug]
created_at: 2024-01-15T10:00:00Z
updated_at: 2024-01-16T12:00:00Z
additions: 50
deletions: 10
is_draft: false
files:
  - path: src/auth.rs
    additions: 40
    deletions: 5
  - path: src/main.rs
    additions: 10
    deletions: 5
body: |
  PR description here...
```

## Usage

Use this to find recently changed files and optimization opportunities in open source projects:

```
gh-pr-sync pull --repo owner/repo --limit 20
cat .prs/*.yaml
```

## Reading Specific PRs

Files are named `<number>-<slug>.yaml`. To read specific PRs by number, use glob patterns:

```
cat .prs/42-*.yaml              # Read PR #42
cat .prs/100-*.yaml .prs/101-*.yaml  # Read multiple PRs
ls .prs/                        # List all PR files
```
