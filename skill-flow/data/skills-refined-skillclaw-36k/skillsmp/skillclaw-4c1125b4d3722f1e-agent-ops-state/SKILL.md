---
name: agent-ops-state
description: Use this skill to maintain and manage .agent state files effectively throughout a session, ensuring that all relevant information is consistently updated and accessible.
---

# AgentOps State Discipline

**Works with or without `aoc` CLI installed.** State management uses direct file operations by default.

## State File Operations (Default)

All state files are managed via direct file operations:

| File | Operations |
|------|-----------|
| `.agent/constitution.md` | Read/write directly |
| `.agent/focus.md` | Read/write directly |
| `.agent/memory.md` | Read/write directly |
| `.agent/baseline.md` | Read/write directly |
| `.agent/issues/{priority}.md` | Read/append/edit directly |

### Issue Management (File-Based)

| Operation | How to Do It |
|-----------|--------------|
| List issues by priority | Read `.agent/issues/{priority}.md` directly |
| Show issue details | Search for issue ID in priority files |
| Create issue | Append to appropriate `.agent/issues/{priority}.md` file |
| Update issue status | Edit `status:` field directly in file |
| Close issue | Set `status: done` + move to `history.md` |
| Get summary | Count issues across priority files |

### Git Status

```bash
# Check current branch
git branch --show-current

# Check for uncommitted changes
git status --porcelain

# Get last commit hash
git rev-parse --short HEAD
```

## CLI Integration (when aoc is available)

When `aoc` CLI is detected in `.agent/tools.json`, these commands provide convenience shortcuts:

| Operation | CLI Command |
|-----------|-------------|
| List issues by priority | `aoc issues list --priority critical` |
| Show issue details | `aoc issues show <ID>` |
| Create issue | `aoc issues create --type BUG --title "..."` |
| Update issue status | `aoc issues update <ID> --status in-progress` |
| Close issue | `aoc issues close <ID>` |
| Get summary | `aoc issues summary` |

**Note:** CLI is optional — all operations can be performed via direct file editing.

## When to Use
- At the start of a session/response
- After any meaningful step (analysis/plan decision/implementation/test run)
- When adding/updating issues
- Before concluding a response

## Session Start

At session start:
1. **Check for staleness**: Delegate to `agent-ops-git` stale detection.
2. **Read state files** in order (see below).
3. **Validate** the integrity of the state files.