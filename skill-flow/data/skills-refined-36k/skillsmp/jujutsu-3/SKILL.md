---
name: jujutsu
description: |
  MANDATORY skill for ALL version control operations. Load this skill BEFORE any VCS action.

  This project uses Jujutsu (jj) exclusively. Git commands are PROHIBITED. Always use jj commands
  for: commits, branching, rebasing, pushing, pulling, and all other VCS operations.

  MUST load when: (1) Creating or modifying commits, (2) Pushing to remote, (3) Creating branches
  or bookmarks, (4) Managing stacked diffs/PRs, (5) Resolving conflicts, (6) Any version control.

  Triggers: Any VCS operation, commits, branches, push, pull, rebase, stacked PRs, Change IDs.
---

# Jujutsu for Agents

## Core Concepts

**Working copy is a commit.** Every file edit auto-snapshots into `@`. No staging area.

**Change IDs persist.** Always reference Change IDs (e.g., `zsowkzkt`), not commit hashes. IDs survive rebases.

**Conflicts don't halt.** jj records conflicts in commits; fix them later.

## Quick Reference

| Task | Command |
|------|---------|
| Check state | `jj status --no-pager` |
| Name current work | `jj describe -m "message"` |
| Seal and start new | `jj new` |
| Jump to commit | `jj edit <change_id>` |
| Move file to parent | `jj squash --into @- <file>` |
| Create bookmark | `jj bookmark create <name> -r @` |
| Push bookmark | `jj git push --bookmark <name>` |
| List conflicts | `jj resolve --list` |
| Undo last operation | `jj undo` |
| Find by description | `jj log -r 'description("text")' --no-graph -T 'change_id "\n"'` |
| **Format code** | `jj fix` |
| **Quick lint check** | `jj quality` |
| **Full verify + push** | `jj secure-push` |
| **Post-merge sync** | `jj git fetch && jj rebase -s <next> -d main` |

## Workflow Patterns

### Basic Loop
```bash
# 1. Edit files (auto-snapshots)
# 2. Name the work
jj describe -m "feat: add feature"
# 3. Seal and continue
jj new
```

### Edit Mid-Stack
```bash
# Find and jump to target
jj edit <change_id>
# Make edits (auto-snapshots)
# Return to tip
jj edit <tip_id>
# Verify no conflicts
jj log -r '::@' --template 'change_id " " conflict "\n"'
```

### Post-Merge Sync (after GitHub merges)

**jj has no `git pull --rebase` equivalent.** After a PR is merged on GitHub:

```bash
# 1. Fetch the merged commit
jj git fetch

# 2. Rebase remaining work onto new main
jj rebase -s <oldest-unmerged-change-id> -d main
```

**Important:** Always use `gh pr merge --rebase` (not `--squash`). With rebase-merge, jj recognizes the commit is on main. Squash-merge creates a new hash, leaving orphaned "zombie" commits.

### Forbidden Commands

- `jj split` — requires TUI, use [construction method](references/workflows.md#hunk-level-split-construction-method)
- `jj resolve` — requires TUI, parse and rewrite conflict markers manually

## Quality Gates

This project uses `jj fix` for auto-formatting and custom aliases for verification.

### Philosophy

- **Category A (formatters):** Run `jj fix` anytime — auto-applies ruff, prettier, buf format
- **Category B (verifiers):** Run `jj secure-push` before pushing — runs all linters, type checkers, tests

### Commands

| Command | Purpose | Speed |
|---------|---------|-------|
| `jj fix` | Format modified files (ruff, prettier, buf) | ~5s |
| `jj fix-all` | Format entire repo | ~30s |
| `jj quality` | Quick check: format + lint + type-check | ~30s |
| `jj secure-push` | Full pipeline: format → lint → build → test → push | ~5min |

### Workflow Integration

```bash
# While coding: format often
jj fix

# Before pushing: verify everything
jj secure-push --bookmark my-feature

# Quick sanity check (no tests)
jj quality
```

### What Runs

**`jj fix`:** ruff-format, ruff-fix (isort/pyupgrade), prettier, buf format

**`jj secure-push`:** buf lint → pyright → eslint → prettier check → angular build → pytest → vitest → playwright → e2e → generated code check → push

## Detailed Protocols

See [references/workflows.md](references/workflows.md) for:
- State verification protocols
- Non-interactive splitting techniques
- Post-merge sync workflow
- Conflict resolution steps
- Safety and recovery operations

See [references/divergent-changes.md](references/divergent-changes.md) for:
- Identifying divergent changes (multiple commits with same change ID)
- Resolution strategies: abandon, give new ID, squash, or ignore
- Common causes and prevention
