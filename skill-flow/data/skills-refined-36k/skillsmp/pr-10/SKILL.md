---
name: pr
description: Create pull requests via git and GitHub CLI while following repo templates and Conventional Commits. Use when a user asks to make a PR, push a branch, open a GitHub PR.
---

# PR

## Overview

Create a PR end-to-end: stage and commit changes, push the branch, fill the PR template, ask for confirmation, then open the PR with `gh`.

## Workflow

1. Inspect git state: run `git status -sb`, identify uncommitted or untracked changes, and confirm which files to include. Avoid modifying unrelated files.
2. Stage changes: `git add <paths>` for the approved files only, then re-check status.
3. Commit: generate a Conventional Commit message when requested and run `git commit -m "<message>"`.
4. Push branch: `git push origin <branch>` or `git push -u origin <branch>` if needed. If push fails due to auth/remote issues, ask for next steps.
5. Build PR body: read `.github/pull_request_template.md` if present and fill required sections (Summary, Type of Change, Related Issues). Keep checkboxes accurate.
6. Ask for confirmation before creating the PR. Do not run `gh pr create` until the user says OK.
7. Create PR: `gh pr create --base <base> --head <branch> --title "<title>" --body "<body>"`, then return the PR URL.

## Notes

- Follow repo conventions for templates, required sections, and Conventional Commits.
- Require explicit confirmation before any network operations: `git push` or `gh pr create`
