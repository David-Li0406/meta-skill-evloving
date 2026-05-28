---
name: git-commits-branches
description: Conventional commits, naming prefixes, and branch strategies.
---

# Git Commits & Branches

## When to use this skill
- Committing code.
- Creating new branches.
- Merging PRs.

## 1. Commit Messages
- **Conventional Commits**: Use `type(scope): description`.
  - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.
- **Scope**: Lowercase, concise (e.g., `auth`, `header`).
- **Body**: Optional short description of *why* (not just what) if the change is complex.

## 2. Branch Naming
- **Format**: `type/short-description` (e.g., `feat/add-login`, `fix/nav-bug`).
- **Separators**: Use hyphens (`-`).

## 3. Atomic Commits
- **Granularity**: One logical change per commit. Do not squash unrelated fixes.
- **Verification**: Ensure tests/lint pass *before* committing.
