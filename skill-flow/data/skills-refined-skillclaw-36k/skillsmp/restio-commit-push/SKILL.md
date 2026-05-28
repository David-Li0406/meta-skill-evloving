---
name: restio-commit-push
description: "Create conventional commits with scope and push only to the current ticket branch (e.g., XX-###). Use when the user asks to commit changes or says 'commit', 'commit & push', or similar."
---

# Restio Commit + Push

## Overview
Create a conventional commit with scope, and push only to the current ticket branch. Never push to main/master/develop/development.

## Workflow

### 1) Verify branch safety
- Read `git status`.
- Determine current branch name.
- If HEAD is detached, stop and ask the user to checkout the ticket branch.
- If current branch is `main`, `master`, `develop`, or `development`, refuse and ask the user to switch to the ticket branch.
- If current branch does not match a ticket pattern `^[A-Z]{2,5}-\d+`, ask the user to confirm or switch.
- If there are merge conflicts, stop and ask the user to resolve them first.

### 2) Build commit message
- Use conventional format: `type(scope): message`.
- Choose `type` based on changes (e.g., `fix`, `feat`, `chore`, `docs`, `refactor`, `test`, `perf`).
- Use a short, imperative message.
- Scope should be a concise area: module, package, or feature name.
- If uncertain, ask the user for scope/message confirmation.

### 3) Commit
- If there are no changes to commit, stop and tell the user.
- If nothing is staged but changes exist, ask whether to stage all or specify files.
- Stage only intended files (ask if ambiguous).
- Run `git commit -m "type(scope): message"`.

### 4) Push
- Push only to the current ticket branch.
- Never push to `main`, `master`, `develop`, or `development`.
- If upstream isn’t set, use `git push -u origin <branch>`.

## Constraints
- Never force push unless user explicitly requests.
- Never commit or push if there are unresolved merge conflicts.
