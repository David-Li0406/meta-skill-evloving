---
name: flow-next-sync
description: Use this skill to manually trigger plan-sync and update downstream task specs when code changes outpace specifications.
---

# Manual Plan-Sync

Manually trigger plan-sync to update downstream task specs.

**CRITICAL: flowctl is BUNDLED - NOT installed globally.** Always use:
```bash
FLOWCTL="${CLAUDE_PLUGIN_ROOT}/scripts/flowctl"
```

## Input

Arguments: $ARGUMENTS  
Format: `<id> [--dry-run]`

- `<id>` - task ID (fn-N.M) or epic ID (fn-N)
- `--dry-run` - show changes without writing

## Workflow

### Step 1: Parse Arguments

```bash
FLOWCTL="${CLAUDE_PLUGIN_ROOT}/scripts/flowctl"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
```

Parse $ARGUMENTS for:
- First positional arg = `ID`
- `--dry-run` flag = `DRY_RUN` (true/false)

**Validate ID format:**
- Must start with `fn-`
- If no ID provided: "Usage: /flow-next:sync <id> [--dry-run]"
- If doesn't match `fn-*` pattern: "Invalid ID format. Use fn-N (epic) or fn-N.M (task)."

Detect ID type:
- Contains `.` (e.g., fn-1.2) -> task ID
- No `.` (e.g., fn-1 or fn-1-abc) -> epic ID

### Step 2: Validate Environment

```bash
test -d .flow || { echo "No .flow/ found. Run flowctl init first."; exit 1; }
```

If `.flow/` is missing, output an error and stop.

### Step 3: Validate ID Exists

```bash
$FLOWCTL show <ID> --json
```

If the command fails:
- For task ID: "Task <id> not found. Run `flowctl list` to see available."
- For epic ID: "Epic <id> not found. Run `flowctl epics` to see available."

Stop on failure.

### Step 4: Find Downstream Tasks

**For task ID input:**
```bash
# Extract epic from task ID (remove .N suffix)
EPIC=$(echo "<task-id>" | sed 's/\.[0-9]*$//')

# Get all tasks in epic
$FLOWCTL tasks --epic "$EPIC" --json
```

Filter to `status: todo` or `status: blocked`. Exclude the source task itself.

**For epic ID input:**
```bash
$FLOWCTL tasks --epic "<epic-id>" --json
```

1. First, find a **source task** to anchor drift detection (agent requires `COMPLETED_TASK_ID`):
   - Prefer the most recently updated task with `status: done`
   - Else: most recently updated task with `status: in_progress`
   - Else: error "No completed or in-progress tasks to sync from. Complete a task first."

2. Then filter remaining tasks to `status: todo` or `status: blocked` (these are downstream).

**If no downstream tasks:**
```
No downstream tasks to sync (all done or none exist).
```
Stop here (success, nothing to do).

### Step 5: Spawn Plan-Sync Agent
```bash
# Command to spawn the plan-sync agent goes here
```