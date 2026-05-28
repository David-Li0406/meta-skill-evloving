---
name: bazinga-db-workflow
description: Use this skill when managing task groups, development plans, or success criteria tracking.
---

# Skill body

You are the bazinga-db-workflow skill. You manage task groups, development plans, and success criteria tracking.

## When to Invoke This Skill

**Invoke when:**
- Creating or updating task groups
- Saving or retrieving development plans
- Managing success criteria
- Tracking plan progress

**Do NOT invoke when:**
- Managing sessions or state → Use `bazinga-db-core`
- Logging interactions or reasoning → Use `bazinga-db-agents`
- Managing context packages → Use `bazinga-db-context`

## Script Location

**Path:** `.claude/skills/bazinga-db/scripts/bazinga_db.py`

All commands use this script with `--quiet` flag:
```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet <command> [args...]
```

## Commands

### create-task-group

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet create-task-group \
  "<group_id>" "<session_id>" "<description>" \
  [--specializations '<json_array>'] [--item_count N] [--initial_tier "<tier>"] \
  [--component-path "<path>"] [--complexity N] [--security_sensitive 0|1]
```

**Parameters:**
- `group_id`: Short identifier (e.g., `AUTH`, `CALC`)
- `session_id`: Parent session ID
- `description`: Human-readable description
- `--specializations`: JSON array of specialization paths
- `--initial_tier`: `"Developer"` or `"Senior Software Engineer"`
- `--complexity`: 1-10 scale

**Returns:** Created task group object.

### update-task-group

**CRITICAL: Argument order is `<group_id> <session_id>` (NOT session first)**

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet update-task-group \
  "<group_id>" "<session_id>" [--status "<status>"] [--assigned_to "<agent_id>"] \
  [--specializations '<json_array>'] [--item_count N] [--initial_tier "<tier>"] \
  [--component-path "<path>"] [--qa_attempts N] [--tl_review_attempts N] \
  [--security_sensitive 0|1] [--complexity N] \
  [--review_iteration N] [--no_progress_count N] [--blocking_issues_count N]
```

**Valid status values:** `pending`, `in_progress`, `completed`, `failed`, `approved_pending_merge`, `merging`