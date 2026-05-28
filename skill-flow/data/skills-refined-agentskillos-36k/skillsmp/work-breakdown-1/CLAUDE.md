# skills/work-breakdown/

## Overview

Work breakdown skill for decomposing implementation plans into bd (beads) issues. Converts plans into epics, tasks, dependencies, and estimates.

## Index

| File | Contents | Read When |
|------|----------|-----------|
| `SKILL.md` | Full workflow and bd command reference | Using this skill |
| `WORKBREAKDOWN_SKILL.md` | Extended examples and anti-patterns | Need detailed guidance |

## Key Points

1. **Read the plan first** - understand scope, phases, deliverables
2. **Break into epics** - 3-7 high-level work packages
3. **Decompose to tasks** - 30-480 minute chunks
4. **Map dependencies** - what blocks what
5. **Get approval** - present WBS before creating issues
6. **Execute sequentially** - epics first, then tasks, then dependencies

## Integration with bd

This skill produces output that maps directly to bd commands:

```bash
# Epics
bd create "Epic Name" -t epic -p 1 -e 480 -d "..." --json

# Tasks (children of epics)
bd create "Task Name" -t task -p 2 -e 120 --parent [epic_id] -d "..." --json

# Dependencies
bd dep add [child_id] [blocker_id]

# Verify
bd ready
bd dep tree [epic_id]
```

## Common Triggers

- "Break down this plan"
- "Create a work breakdown"
