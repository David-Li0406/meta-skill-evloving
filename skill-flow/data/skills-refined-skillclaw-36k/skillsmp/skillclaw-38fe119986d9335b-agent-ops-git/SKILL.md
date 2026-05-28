---
name: agent-ops-git
description: Use this skill when you need to manage git operations safely, ensuring that actions like pushing and deleting branches require explicit user confirmation.
---

# Git Workflow (active-safe)

**Works with or without `aoc` CLI installed.** Issue tracking can be done via direct file editing.

## Git Commands

| Operation | Command | Notes |
|-----------|---------|-------|
| Check current branch | `git branch --show-current` | |
| Check current commit | `git rev-parse --short HEAD` | |
| Check uncommitted changes | `git status --porcelain` | |
| Create branch | `git checkout -b <branch>` | From constitution branch policy |
| Stage changes | `git add <files>` | |
| Commit | `git commit -m "..."` | Use structured message format |
| Stash work | `git stash push -m "..."` | |
| Unstash work | `git stash pop` | |
| View stash | `git stash list` | |
| Revert commit | `git revert <commit>` | Requires confirmation |

## Issue Integration (File-Based — Default)

| Operation | How to Do It |
|-----------|--------------|
| Start work | Edit issue in `.agent/issues/{priority}.md`: set `status: in_progress` |
| Close issue | Set `status: done`, add log entry with commit hash |

## CLI Integration (when aoc is available)

When `aoc` CLI is detected in `.agent/tools.json`:

```bash
# Update issue when starting work
aoc issues update <ID> --status in-progress --log "Started work"

# Close issue when committing
aoc issues close <ID> --log "Fixed in commit abc123"
```

## Never Auto-Execute

```bash
# These require explicit user confirmation:
git push           # Never auto-push
git push --force   # Never force push
git branch -D      # Never delete branches
```

## Scope

- ✅ Detect stale state (authoritative source)
- ✅ Create feature branches
- ✅ Commit checkpoints with structured messages
- ✅ Detect uncommitted changes
- ✅ Stash/unstash work in progress
- ✅ Revert agent's own commits (with confirmation)
- ❌ Never push without explicit user request
- ❌ Never force push
- ❌ Never delete remote branches

## Stale State Detection (authoritative)

Called by `agent-ops-state` at session start. This is the single source of truth for staleness.

### Procedure

1. Read `.agent/focus.md` session info:
   - `branch`: expected branch name
   - `last_commit`: expected HEAD commit (short hash)