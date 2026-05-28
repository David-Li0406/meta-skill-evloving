---
name: kickoff
description: Create and switch to a new git branch before starting a larger task, push the branch to the remote, proceed with work, and commit at the end. Use when the user asks to start work on a fresh branch and expects a remote push plus a final commit.
---

# Kickoff

## Overview
Announce the branch workflow up front, but delay branch creation and push until you are about to start work. If the work spans multiple repositories, repeat the workflow per repo with separate branches and commit in each repo at the end.

## Workflow

### 1) Preflight
- Confirm the repo root and the remote to use (default to `origin` if present).
- Check `git status --porcelain`; if dirty, ask whether to commit, stash, or continue as-is.
- Identify the base branch: prefer an explicit user choice; otherwise use the upstream or default branch.
- Follow any repo-specific branch naming rules if present (for example in `AGENTS.md`).
- If the work spans multiple repos, list them and run preflight per repo.

### 2) Declare intent and branch naming
- State you will create and push a branch when you are about to start work.
- Ask the user to provide a branch name based on the work; suggest a name if needed.
- If multiple repos are involved, ask for a branch name per repo and suggest names derived from each repo's scope.

### 3) Create branch (just before starting work)
- Create and switch right before the first change in that repo.
- Create and switch: `git checkout -b <branch> <base>` (or `git switch -c <branch> <base>`).
- Verify the branch: `git status -sb`.

### 4) Push branch
- Push and set upstream: `git push -u <remote> <branch>`.
- If the remote branch already exists, ask whether to track it or rename the local branch.
- If no remote is configured, ask whether to add one or skip the push.

### 5) Work phase
- Perform the requested work on the new branch.
- If multiple repos are involved, ensure you are on the correct branch in each repo before editing.

### 6) Finish with commit
- After completing the work, stage only the relevant files, review `git diff --staged`, and commit with a concise diff-based message.
- If multiple repos are involved, commit on each repo's branch.
- If the user provides a commit message, use it; otherwise propose one.
- If the user explicitly asks to skip the commit, stop after finishing changes and ask how they want to proceed.

## Notes
- Do not reset, discard, or rewrite existing user changes.
- Keep commands visible and confirm destructive or ambiguous actions.
