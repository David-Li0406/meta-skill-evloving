---
name: pr-auto
description: Create and merge pull requests via git and GitHub CLI while following repo templates and Conventional Commits. Use when a user asks to enable auto-merge, or merge a PR.
---

# PR-Auto

## Overview

Create a PR end-to-end: stage and commit changes, push the branch, fill the PR template, open the PR with gh, then merge it with gh safely.

## Workflow

1. Inspect git state: run `git status -sb`, identify uncommitted/untracked changes, and confirm which files to include. Avoid modifying unrelated files.
2. Stage changes: `git add <paths>` for the approved files only, then re-check status.
3. Commit: generate a Conventional Commit message when requested and run `git commit -m "<message>"`.
4. Push branch: `git push origin <branch>` or `git push -u origin <branch>` if needed. If push fails due to auth/remote issues, ask for next steps.
5. Build PR body: read `.github/pull_request_template.md` if present and fill required sections (Summary, Type of Change, Related Issues). Keep checkboxes accurate.
6. Ask for confirmation before creating the PR. Do not run `gh pr create` until the user says OK.
7. Create PR: `gh pr create --base <base> --head <branch> --title "<title>" --body "<body>"`, then return the PR URL.
8. If requested, ask for confirmation before merging. Then merge with `gh pr merge <pr> --squash` and return the final PR state/URL.

## Notes

- Follow repo conventions for templates and Conventional Commits.
- Require explicit confirmation before any network operations: `git push`, `gh pr create`, `gh pr merge`.
- Prefer not to merge if required reviews/checks are missing or failing; if blocked, report status and ask for next steps.
