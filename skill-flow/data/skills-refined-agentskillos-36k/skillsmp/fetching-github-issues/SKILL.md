---
name: fetching-github-issues
description: Fetches GitHub issues for the current repository and formats them as markdown for LLM consumption. Use when the user asks to implement or read a GitHub issue.
---

# Fetching GitHub issues

Use the `repo-to-md` CLI tool to fetch GitHub issues and formats them as
LLM-friendly markdown.

## Primary usage

```bash
repo-to-md issue ISSUE_NUMBER
```

For example, to get issue #42 from the current repository, run

```bash
repo-to-md issue 42
```

## Prerequisites

- `gh` CLI must be installed and authenticated
- `repo-to-md` must be run from within a git repository with a configured remote

## Alternative usage

- `--repo <REPOSITORY>` to specify the repository as `owner/repo`

Examples:

```bash
# Fetch issue from a specific repository
repo-to-md issue 123 --repo anthropics/claude-code
```

## Output format

Generates markdown with issue metadata and description:

```markdown
# Issue #42: Title Here

- **State:** OPEN
- **Author:** @username
- **Created:** 2024-01-15T10:30:00Z
- **Labels:** bug, enhancement

## Description

Issue body content here...
```
