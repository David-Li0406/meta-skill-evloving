---
name: commit
description: "Stage changes, create Conventional Commits, push branches, open GitHub pull requests with gh, and manage PR checks/auto-merge. Use when a user asks to commit, push, open a PR, enable auto-merge, or shepherd CI checks to green."
---

# Commit

## Overview

Automate the end-to-end git + GitHub CLI flow: branch creation, staging, Conventional Commit message, PR creation, and PR check monitoring/merge prompts.

## Workflow

1. Inspect repo state.
   - Run `git status -sb` and `git branch --show-current`.
   - If there are no changes, ask the user what to commit.

2. Ensure a non-main branch.
   - If current branch is `main`, create a new branch named `feat-<summary>`.
   - Prefer generating `<summary>` with `just scripts::commit-branch-name "<summary>"` (creates `feat-<summary>` automatically).
   - If the summary is unclear or the user has a preference, ask for a branch name instead of guessing.

3. Stage changes.
   - Stage tracked changes with `git add -A`.
   - If there are untracked files that are likely unintended, ask before staging.

4. Generate a Conventional Commit message.
   - Choose `type` based on change intent: `feat`, `fix`, `refactor`, `docs`, `chore`, etc.
   - Pick `scope` from the most affected top-level area (e.g., `services`, `cli`, `ui`).
   - Write: `<type>(<scope>): <imperative summary>`.
   - If unsure, ask the user to confirm the type/scope.

5. Commit and handle hook failures.
   - Run `git commit -m "<message>"`.
   - If hooks fail due to permissions or sandboxing (e.g., `/dev/ptmx`), re-run the same commit command with escalated permissions instead of bypassing hooks.
   - If hooks fail due to lint/test errors, fix issues, re-stage, and retry.
   - Do not disable or bypass hooks unless the user explicitly approves it.
   - If commit signing fails (GPG), ask the user whether to retry with signing fixed or proceed with `--no-gpg-sign`.

6. Push and create PR.
   - Push with `git push -u origin <branch>`.
   - Create PR with `just scripts::commit-pr-create "<title>" [body-path]`.
   - If `body-path` is omitted, the script auto-fills the PR body from recent changes.
   - Use `references/pr-body.md` when you want full manual control (update testing list based on what ran).
   - If PR creation fails due to missing remote branch, push then retry.

7. Ask about auto-merge.
   - After PR creation, ask: "Enable auto-merge?" and only proceed on explicit approval.
   - If approved, run `just scripts::commit-pr-auto-merge <pr-url>`.

8. Monitor checks.
   - Use `just scripts::commit-pr-checks <pr-url>` to monitor status.
   - If checks fail, inspect failures, apply fixes, commit/push, and re-check until green.
   - After checks pass, ask whether to merge if auto-merge is not enabled.

9. Sync with main before merge.
   - If the user requests it, fetch and rebase onto `origin/main` before merging.
   - Force-push with lease after rebase: `git push --force-with-lease`.
   - Re-check PR status after the rebase.

## Resources

### scripts/
- The repo-level `scripts/commit.ts` uses `bun` to call the `gh` CLI for branch naming and PR operations.
- Use the dedicated Just recipes: `scripts::commit-branch-name`, `scripts::commit-pr-create`, `scripts::commit-pr-auto-merge`, `scripts::commit-pr-checks`, `scripts::commit-pr-open`, `scripts::commit-pr-url`, `scripts::commit-pr-status`, `scripts::commit-pr-draft`, `scripts::commit-pr-ready`, `scripts::commit-pr-comment`, `scripts::commit-pr-close`.

### references/
- `references/pr-body.md` provides the PR body template.
