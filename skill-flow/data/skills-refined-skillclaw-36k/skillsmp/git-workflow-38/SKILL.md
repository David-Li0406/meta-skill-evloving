---
name: git-workflow
description: Git workflow automation for creating feature branches, committing, pushing, merging to main, and pushing main. Use when asked to do git branch/commit/push/merge steps or "one command" release.
---

# Git Workflow Automation

## When to Use
- Requests to create a feature branch
- Commit and push changes
- Merge into `main`
- One-command or scripted git workflows

## Core Patterns
- Use a descriptive branch name (feature/..., fix/..., chore/...)
- Stage changes with `git add -A`
- Commit with a concise message
- Push feature branch to `origin`
- Merge into `main` with `--no-ff` when possible
- Push `main`

## Safety Checks
- Ensure the working tree is clean before merging
- Fail early on conflicts
- Do not force-push unless explicitly requested

## Example
```
cd /path/to/repo && \
  git checkout -b feature/your-branch && \
  git add -A && \
  git commit -m "Describe change" && \
  git push -u origin HEAD && \
  git checkout main && \
  git merge --no-ff feature/your-branch && \
  git push origin main
```
