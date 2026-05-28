---
name: git-sync-workflow
description: Best practices for git sync, rebase, and hooks.
---

# Git Sync & Workflow

## When to use this skill
- Syncing with remote (`git pull`).
- Handling merge conflicts.
- Pushing code.

## 1. Sync Strategy
- **Pull Before Push**: ALways `git pull --rebase origin main` before starting work or pushing.
- **Rebase**: Prefer rebase over merge for local feature branches to keep history linear.

## 2. Pushing
- **Safety**: Use `--force-with-lease` instead of `--force` if rewriting history (only on your own branches).
- **Upstream**: Set upstream early (`git push -u origin feat/name`).

## 3. Hooks
- **Pre-commit**: Should run fast checks (lint-staged).
- **Pre-push**: Run heavier tests if the project considers it necessary, otherwise leave to CI.
