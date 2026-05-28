---
name: github-issue-creator
description: Creates GitHub issues using gh CLI. Use when creating new issues.
---

# GitHub Issue Creator

Creates GitHub Issues using GitHub CLI.

## Procedure

### Confirm Issue Type

Understand the user's intent: bug report, feature request, or other type.
Check if labels, assignees, or milestones are specified.

### Detect Templates

Detect Issue templates. Filenames are case-insensitive.

Single file template locations (in priority order):

- `.github/issue_template.md`
- `issue_template.md` (repository root)
- `docs/issue_template.md`

Multiple templates directory locations:

- `.github/ISSUE_TEMPLATE/`
- `ISSUE_TEMPLATE/` (repository root)
- `docs/ISSUE_TEMPLATE/`

If a single file template is found, read and use it.
If a templates directory is found, list available templates and ask the user which one to use.
If no templates exist, use [templates/default.md](templates/default.md).

### Create Issue

Create the Issue with `gh issue create` and report the Issue URL to the user.

## Title Guidelines

The title should be a natural language sentence summarising the issue.
Do not use commit message format (e.g., "fix(auth): bug").

Good examples:
- ログイン時にセッションタイムアウトが発生する
- ダークモード切り替え機能を追加したい
- Login session timeout occurs unexpectedly

Bad examples:
- fix(auth): session timeout bug
- Bug

## Language

Write issue content in Japanese by default. If the user explicitly requests English, write in English.

## Creating Issues in Different Repositories

Use the `-R` flag to create an issue in a repository different from the current directory.

```bash
gh issue create -R OWNER/REPO --title "<title>" --body "<body>"
```
