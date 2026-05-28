---
name: git-commit-formatter
description: Use this when the user asks to commit changes, write a commit message, or prepare a PR. Enforces clean Conventional Commits with scopes for UI/perf/ux work.
---

# Git Commit Formatter

## Goal
Every commit message follows Conventional Commits so history stays readable during fast UI/animation iterations.

## Format
`<type>(<scope>): <description>`

### Allowed types
- feat: new feature
- fix: bug fix
- perf: performance improvement
- refactor: refactor without behavior change
- style: formatting / UI-only styling (no logic)
- docs: documentation
- test: tests
- chore: tooling / deps

### Scopes (use one)
Examples: `map`, `markers`, `ui`, `ux`, `anim`, `perf`, `filters`, `search`, `auth`

## Rules
- Description is imperative, short, no fluff.
- If there's a breaking change, add:
  `BREAKING CHANGE: ...`
- Prefer multiple small commits over one mega-commit during polish work.

## Examples
- `perf(map): reduce marker rerenders on pan`
- `style(ui): unify spacing + button states`
- `fix(filters): prevent double fetch on rapid toggle`
