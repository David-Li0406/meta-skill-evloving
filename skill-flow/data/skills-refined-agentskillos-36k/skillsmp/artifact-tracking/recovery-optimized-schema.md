# Recovery-Optimized Progress Schema

Schema additions that make session recovery trivial (from 15+ minutes to <2 minutes).

## Problem

When sessions crash during batch execution, recovery requires:
1. Finding agent logs by partial ID
2. Parsing JSONL with fragile commands
3. Cross-referencing with git status
4. Manual verification of each task

## Solution: Capture Recovery Metadata at Launch

### Enhanced Task Schema

```yaml
tasks:
  - id: "TASK-1.2"
    title: "Create FrontmatterDisplay component"
    status: "in_progress"
    assigned_to: ["ui-engineer-enhanced"]
    dependencies: ["TASK-1.1"]
    estimate: "3h"

    # === RECOVERY FIELDS (NEW) ===
    expected_files:                    # What this task should create/modify
      - path: "components/entity/frontmatter-display.tsx"
        action: "create"               # create | modify | delete
        min_lines: 100                 # Optional: minimum expected size
      - path: "lib/frontmatter.ts"
        action: "modify"

    agent_id: "a610b3c"               # Recorded when launched
    launched_at: "2025-12-31T21:02:39Z"
    completed_at: null                 # Set when verified complete
```

### Execution Log (Batch-Level)

```yaml
execution_log:
  - batch: 1
    launched_at: "2025-12-31T21:00:00Z"
    status: "completed"
    agents:
      - { task_id: "TASK-1.1", agent_id: "a73c8f7" }
      - { task_id: "TASK-1.5", agent_id: "ae21dbc" }
  - batch: 2
    launched_at: "2025-12-31T21:02:30Z"
    status: "in_progress"              # or "crashed" if detected
    agents:
      - { task_id: "TASK-1.2", agent_id: "a610b3c" }
      - { task_id: "TASK-1.6", agent_id: "af0ec2b" }
      - { task_id: "TASK-1.7", agent_id: "a39f2a9" }
      - { task_id: "TASK-1.8", agent_id: "a9935ea" }
```

## Recovery Workflow with New Schema

### Step 1: Read Execution Log (5 seconds)
```bash
# Extract last in_progress batch
head -50 phase-1-progress.md | grep -A20 'status: "in_progress"'
```

### Step 2: Verify Files Exist (10 seconds per task)
```bash
# For each task in batch, check expected_files
for file in "${expected_files[@]}"; do
  if [ -f "$file" ]; then
    echo "✓ $task_id: $file exists"
  fi
done
```

### Step 3: Mark Complete or Resume (instant)
```
# If all expected_files exist → mark complete
# If missing → resume agent by ID
```

## Orchestration Changes

### At Launch Time

When `/dev:execute-phase` launches a batch, immediately record:

```markdown
#### After Task() calls:

1. Parse agent_id from Task() return value
2. Update progress YAML with:
   - task.agent_id
   - task.launched_at
   - execution_log entry for batch
3. Commit this metadata update (fast, small)
```

### Template for Batch Launch

```
📋 Launching Batch 2 (4 tasks)

| Task ID  | Agent | Expected Files | Status |
|----------|-------|----------------|--------|
| TASK-1.2 | a610b3c | frontmatter-display.tsx (create) | 🚀 |
| TASK-1.6 | af0ec2b | page.tsx (modify) | 🚀 |
| TASK-1.7 | a39f2a9 | frontmatter.test.ts (create) | 🚀 |
| TASK-1.8 | a9935ea | catalog-tabs.test.tsx (create) | 🚀 |

Recording to progress file...
```

## Recovery with New Schema

### Instant Recovery Check
```bash
#!/bin/bash
# recover-batch.sh - Check batch completion status

PROGRESS_FILE="$1"
BATCH="$2"

# Extract expected files for batch
for task in $(yq ".execution_log[] | select(.batch == $BATCH) | .agents[].task_id" "$PROGRESS_FILE"); do
  expected=$(yq ".tasks[] | select(.id == \"$task\") | .expected_files[].path" "$PROGRESS_FILE")

  all_exist=true
  for file in $expected; do
    if [ ! -f "$file" ]; then
      all_exist=false
      break
    fi
  done

  if $all_exist; then
    echo "✅ $task: COMPLETE (all files exist)"
  else
    agent_id=$(yq ".tasks[] | select(.id == \"$task\") | .agent_id" "$PROGRESS_FILE")
    echo "❌ $task: INCOMPLETE (resume agent $agent_id)"
  fi
done
```

## Benefits

| Metric | Before | After |
|--------|--------|-------|
| Recovery time | 15+ minutes | <2 minutes |
| Log parsing needed | Always | Only for ambiguous cases |
| Agent ID lookup | Search logs | Direct from YAML |
| File verification | Manual | Automated |
| Resume capability | Manual Task() | Agent ID available |

## Integration Points

### 1. artifact-tracking skill
- Update schema to include `expected_files` and `execution_log`
- Add `record_launch` function for batch metadata

### 2. execute-phase command
- Add step after Task() to record agent_id
- Output launch table with agent IDs

### 3. recovering-sessions skill
- First check: Read `execution_log` from progress file
- Fast path: Verify `expected_files` exist
- Slow path: Parse logs only if ambiguous

## Migration

Existing progress files work unchanged. New fields are optional but recommended.

When creating new progress files via `artifact-tracker`, include `expected_files` for each task based on the implementation plan.
