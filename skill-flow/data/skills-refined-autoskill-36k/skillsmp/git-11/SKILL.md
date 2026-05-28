---
name: git
description: Strict Git workflow enforcer. Handles Conventional Commits, standard branching, and advanced recovery (revert/reset) without executing write commands.
---

# Git Master (Safe Mode)

## Security Protocol

1. **NEVER EXECUTE** write commands (commit, push, rebase, branch).
2. **ONLY EXECUTE** read-only commands (`status`, `log`, `diff`).
3. **ALWAYS OUTPUT** commands in code blocks for user execution.

## 1. Standards

- **Commit Format:** `<type>(<scope>): <description>`
- **Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`.
- **Branch Format:** `<type>/<kebab-case-description>` (e.g., `feat/auth-login`).

## 2. Workflows

- **Commit:** Analyze `diff` -> Generate `git commit -m "type: desc"`.
- **Push:** Generate `git push -u origin <branch>`.
- **Sync:** Suggest `git fetch origin && git rebase origin/main`.
- **Squash:**
  1. Identify count $N$.
  2. Output `git rebase -i HEAD~N`.
  3. **Instruct:** "Change `pick` to `squash` (or `s`) for the bottom $N-1$ commits."

## 3. Recovery: "Wrong Push"

Identify if branch is **Public** (shared/main) or **Private** (feature).

### A. Public (Safe / No Force Push)

1. Undo on wrong: `git checkout wrong && git revert <hashes> && git push`.
2. Move to right: `git checkout right && git cherry-pick <hashes> && git push`.

### B. Private (Clean / Force Push OK)

1. Copy first: `git checkout right && git cherry-pick <hashes>`.
2. Reset wrong: `git checkout wrong && git reset --hard <good-hash> && git push -f`.

### C. Local/Recent ("Soft Reset")

For simple, recent moves:
`git reset --soft HEAD~N` -> `git checkout right` -> `git commit`.
