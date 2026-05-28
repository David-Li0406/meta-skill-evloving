---
name: ship
description: Create a new branch from the current branch, push the branch, commit all local changes (including untracked files), push commits, and open a PR back to the original branch. Use when the user asks to move the current work to a new branch and open a PR to the branch they started from.
---

# Ship

## Overview

Move in-progress work to a new branch, push it, commit all changes, push commits, and open a PR back to the branch that was checked out when the request started.

## Workflow

1. Capture the base branch.
   - Run `git rev-parse --abbrev-ref HEAD` and store it as `base_branch`.
   - If HEAD is detached, ask the user for the base branch and set `base_branch` to that.
   - If a merge or rebase is in progress, stop and ask the user to resolve it first.

2. Decide the new branch name.
   - If the user specifies a name, use it.
   - Otherwise, generate it with these rules:
     - Choose a prefix from the request keywords:
       - `bugfix/` for bug/fix/crash/error
       - `refactor/` for refactor
       - `docs/` for docs
       - `test/` for test
       - Otherwise use `feature/`
     - Build a short topic slug from the request or a quick summary of the work.
       - Lowercase, ASCII, hyphenated, max ~50 chars.
     - If no topic is available, use `auto-YYYYMMDD-HHMM`.
     - Combine to `<prefix><topic>`.
   - Ensure the name is unique:
     - If `git show-ref --verify --quiet refs/heads/<name>` succeeds, append `-2`, `-3`, ...
     - Also check remote with `git ls-remote --heads origin <name>`.

3. Create the branch.
   - Run `git switch -c <new_branch>` (or `git checkout -b <new_branch>` if needed).

4. Push the new branch (before committing).
   - Use `origin` by default. If `origin` is missing, pick the first remote from `git remote` and note it.
   - Run `git push -u <remote> <new_branch>`.

5. Stage all changes (including untracked files).
   - Ensure editor buffers are saved; if unsure, ask the user to save before continuing.
   - Run `git add -A`.
   - If `git status --porcelain` is empty after staging, stop and report "no changes".

6. Commit everything.
   - If the user provides a commit message, use it.
   - Otherwise, map the prefix to a conventional type:
     - `feature/` -> `feat: <topic>`
     - `bugfix/` -> `fix: <topic>`
     - `docs/` -> `docs: <topic>`
     - `refactor/` -> `refactor: <topic>`
     - `test/` -> `test: <topic>`
     - Otherwise `chore: <topic>`
   - Convert the topic slug to words (replace `-` with spaces).
   - If the topic is `auto-...`, use `snapshot` instead.
   - Run `git commit -m "<message>"`.

7. Push commits to the remote.
   - Run `git push <remote> <new_branch>`.

8. Create the PR.
   - Title: use the commit subject line.
   - Body: use this template, with a brief summary if possible:
     - Summary:
       - `- Move current work to <new_branch>` (fallback if no better summary)
     - Testing:
       - `- Not run (not requested)` unless the user asked for tests
   - Run `gh pr create -B <base_branch> -H <new_branch> -t "<title>" -b "<body>"`.

9. Return to the base branch and report results.
   - Run `git switch <base_branch>`.
   - Report the new branch name and the PR URL.
