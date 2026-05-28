---
name: agent-ops-implementation
description: Use this skill when you need to implement a project based on a validated and approved plan, ensuring small diffs, frequent tests, and stopping on ambiguity.
---

# Implementation workflow

**Works with or without `aoc` CLI installed.** Issue tracking can be done via direct file editing.

## Build/Test Commands (from constitution)

Implementation uses project-specific commands from **constitution.md**:

```bash
# Read actual commands from .agent/constitution.md
build: uv run python -m build     # or: npm run build
lint: uv run ruff check .         # or: npm run lint  
test: uv run pytest               # or: npm run test
format: uv run ruff format .      # or: npm run format
```

## Issue Tracking (File-Based — Default)

| Operation | How to Do It |
|-----------|--------------|
| Start work | Edit issue in `.agent/issues/{priority}.md`: set `status: in_progress` |
| Add log entry | Append to issue's `### Log` section: `- YYYY-MM-DD: Completed step 1` |
| Create follow-up | Append new issue to appropriate priority file |
| Complete issue | Set `status: done`, add log entry, move to `history.md` |

### Example Implementation Flow (File-Based)

1. Edit issue in `.agent/issues/{priority}.md` — set `status: in_progress`
2. Update `.agent/focus.md` — "Implementing {ISSUE-ID}"
3. Run tests after each change (from constitution)
4. Edit issue — add log entry for progress
5. When done, set `status: done`, add final log entry, move to `history.md`

## CLI Integration (when aoc is available)

When `aoc` CLI is detected in `.agent/tools.json`, these commands provide convenience shortcuts:

| Operation | Command |
|-----------|---------|
| Start work | `aoc issues update <ID> --status in-progress` |
| Add log entry | `aoc issues update <ID> --log "Completed step 1"` |
| Create follow-up | `aoc issues create --type CHORE --title "..."` |
| Complete issue | `aoc issues close <ID> --log "Done"` |

## Preconditions
- Constitution is confirmed.
- Baseline exists.
- Final plan exists and is approved (or stop and ask for approval).
- Work is tracked as an issue (or create one before starting).
- **Implementation details file exists** (from planning phase) — check `.agent/issues/references/{ISSUE-ID}-impl-plan.md`