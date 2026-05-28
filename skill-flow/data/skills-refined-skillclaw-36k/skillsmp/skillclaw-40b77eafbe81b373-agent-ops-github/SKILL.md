---
name: agent-ops-github
description: Use this skill when you need to synchronize issues between agent-ops and GitHub, allowing for bidirectional updates and management of issues.
---

# Skill body

## Overview

This skill enables bidirectional synchronization between agent-ops issues and GitHub Issues. You can push local issues to GitHub, pull issues from GitHub to local, and manage the connection seamlessly.

**Tier:** 3 (Utility)  
**Works with or without `aoc` CLI installed**

## Use Cases

1. **Push issues to GitHub** — Share local issues with your team or track them in GitHub.
2. **Pull issues from GitHub** — Import GitHub issues as local agent-ops issues.
3. **Sync bidirectionally** — Keep local and GitHub issues in sync.
4. **Import PR feedback** — Get code review comments as local issues.
5. **Monitor external repos** — Track issues from dependencies.

## CRITICAL: No Assumptions

Before any GitHub API operation, you MUST:

1. **Confirm repository details** — Ask the user for `owner/repo` format.
2. **Verify authentication** — Check that `GITHUB_TOKEN` is set.
3. **Confirm the operation** — Summarize what will be done.
4. **Get explicit approval** — User must approve before API calls.

### Mandatory Confirmation

```
I will {push/pull/sync} issues {to/from} github.com/{owner}/{repo}:
- Operation: {describe what will happen}
- Issues affected: {count or list}

This will make API calls to GitHub. Continue? [Y/N]
```

## Requirements

### Environment
- `GITHUB_TOKEN` environment variable (required)
- Token needs `repo` scope (or `public_repo` for public repos)

### How to Create a Token
1. Go to GitHub → Settings → Developer settings → Personal access tokens.
2. Generate a new token (classic) with `repo` scope.
3. Add to `.env`: `GITHUB_TOKEN=ghp_xxxxxxxxxxxx`.

## Issue Sync Procedure (with aoc CLI)

### Check Sync Status
```bash
# See sync overview between local and GitHub
aoc github sync status --repo owner/repo
```

### Push Local Issues to GitHub
```bash
# Push a single issue
aoc github sync push FEAT-0042 --repo owner/repo

# Push all todo issues
aoc github sync push-all --repo owner/repo --status todo

# Push all issues (dry run first)
aoc github sync push-all --repo owner/repo --dry-run

# Use visible metadata block (instead of hidden comment)
aoc github sync push FEAT-0042 --repo owner/repo --visible
```

### Pull Issues from GitHub
```bash
# Pull a single GitHub issue (dry run by default)
aoc github sync pull 123 --repo owner/repo

# Actually import it
aoc github sync pull 123 --repo owner/repo --confirm
```