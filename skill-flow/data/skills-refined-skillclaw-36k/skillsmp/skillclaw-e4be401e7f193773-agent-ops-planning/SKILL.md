---
name: agent-ops-planning
description: Use this skill when you need to produce a thorough plan before implementation, clarifying unknowns and validating iterations based on confidence levels.
---

# Planning workflow

**Works with or without `aoc` CLI installed.** Issue tracking can be done via direct file editing.

## Issue Tracking (File-Based — Default)

| Operation | How to Do It |
|-----------|--------------|
| Create planning issue | Append to `.agent/issues/medium.md` with type `PLAN` |
| Update status | Edit `status:` field directly in priority file |
| Add log entry | Append to issue's `### Log` section |
| Show issue | Search for issue ID in priority files |

### Build Commands (from constitution)

```bash
# Read actual commands from .agent/constitution.md to understand project structure
build: uv run python -m build
test: uv run pytest
```

### Reference Documents

Implementation details are stored as markdown:
```
.agent/issues/references/{ISSUE-ID}-impl-plan.md
```

## CLI Integration (when `aoc` is available)

When `aoc` CLI is detected in `.agent/tools.json`, these commands provide convenience shortcuts:

| Operation | Command |
|-----------|---------|
| Create planning issue | `aoc issues create --type PLAN --title "..."` |
| Update status | `aoc issues update <ID> --status in-progress` |
| Add log entry | `aoc issues update <ID> --log "Plan iteration 2 complete"` |
| Show issue | `aoc issues show <ID>` |

## Preconditions
- Work should be tracked as an issue before planning begins.
- Constitution exists and is baseline-ready (or stop and run constitution workflow).
- Baseline exists if any code change is expected (or stop and run baseline workflow first).

## Issue-First Principle

Before starting detailed planning:

1. **Check for existing issue**: Is there already an issue for this work?
   - Yes → proceed with planning, reference the issue ID.
   - No → suggest creating one first.

2. **Create issue if needed**:
   ```
   This work isn't tracked yet. Create an issue first?
   
   Suggested: FEAT-{next}@{hash} — "{title from request}"
   Priority: {inferred priority}
   
   [Y]es, create and continue / [N]o, plan without issue
   ```

3. **Reference issue throughout**:
   - Plan title: "Plan for {ISSUE-ID}: {title}"
   - Update issue status to `in-progress` as planning progresses.