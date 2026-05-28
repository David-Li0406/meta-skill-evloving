# Parallel Patterns

Dependency-aware batching strategies for efficient task execution.

## Parallelization Concepts

### Batch Structure

Tasks are organized into batches based on dependencies:

```yaml
parallelization:
  batch_1: ["TASK-1.1", "TASK-1.2", "TASK-1.3"]  # No dependencies
  batch_2: ["TASK-2.1", "TASK-2.2"]              # Depends on batch_1
  batch_3: ["TASK-3.1"]                          # Depends on batch_2
  critical_path: ["TASK-1.1", "TASK-2.1", "TASK-3.1"]
```

### Dependency Rules

- Tasks in same batch have NO dependencies on each other
- Tasks in batch N+1 depend on at least one task from batch N
- `critical_path` identifies the longest chain of dependencies

## Execution Patterns

### Pattern 1: Pure Parallel (Same Batch)

All tasks in a batch execute simultaneously:

```
# Batch 1 - All independent, execute in parallel
Task("ui-engineer-enhanced", "TASK-1.1: Button component")
Task("backend-typescript-architect", "TASK-1.2: API endpoint")
Task("ui-engineer-enhanced", "TASK-1.3: Form component")
```

### Pattern 2: Sequential Batches

Batches execute in order, but tasks within each batch are parallel:

```
# Execute Batch 1
[All batch_1 tasks in parallel]

# Wait for Batch 1 completion

# Execute Batch 2
[All batch_2 tasks in parallel]

# Wait for Batch 2 completion

# Continue...
```

### Pattern 3: Critical Path Optimization

Prioritize critical path tasks to minimize total time:

```
# If TASK-1.1 is on critical path and other batch_1 tasks are not:
# - Start TASK-1.1 first
# - Start other batch_1 tasks immediately after
# - This ensures critical path progresses ASAP
```

## Required Task Fields

Every task in progress files MUST have:

| Field | Description |
|-------|-------------|
| `assigned_to` | Array of agent names for delegation |
| `dependencies` | Array of task IDs that must complete first (empty `[]` if none) |
| `estimated_time` | Time estimate (e.g., "2h", "4h", "1d") |
| `status` | Current status (pending, in_progress, completed, blocked) |

### If Fields Missing

Delegate to lead-architect to annotate:

```
Task("lead-architect", "Annotate progress file ${progress_file} with missing orchestration fields (assigned_to, dependencies, estimated_time)")
```

## Identifying Ready Tasks

A task is ready to execute when:

1. `status` is `pending`
2. All tasks in `dependencies` array have `status: completed`

### YAML Check

```yaml
tasks:
  - id: TASK-2.1
    dependencies: [TASK-1.1, TASK-1.2]  # Both must be completed
    status: pending                      # Ready if deps complete
```

## Optimizing Execution Time

### Minimize Wait Time

- Start longest tasks first within each batch
- Use `estimated_time` to prioritize critical path

### Reduce Context Switches

- Group similar tasks on same agent
- Batch UI tasks together, backend tasks together

### Example Optimized Execution

```yaml
# Given:
batch_1:
  - TASK-1.1 (4h, critical_path)
  - TASK-1.2 (2h)
  - TASK-1.3 (1h)

# Optimized order (all parallel, but start longest first):
Task("backend-typescript-architect", "TASK-1.1: [4h critical]...")
Task("ui-engineer-enhanced", "TASK-1.2: [2h]...")
Task("codebase-explorer", "TASK-1.3: [1h]...")
```

## Handling Blocked Tasks

When a task blocks:

1. Mark as `status: blocked` in progress
2. Continue with other tasks in batch that don't depend on it
3. Document blocker and required resolution
4. Re-evaluate dependencies when blocker resolves

```yaml
tasks:
  - id: TASK-2.1
    status: blocked
    blocked_by: "External API not available"

  - id: TASK-2.2
    status: in_progress  # Can continue if no dependency on TASK-2.1
```

## Status Update Pattern

After each task completes:

```
Task("artifact-tracker", "Update ${PRD_NAME} phase ${phase_num}:
- Mark {task_id} as completed
- Add commit {commit_hash}
- Log: {brief_description}")
```

This updates:
- Task status in YAML
- Completion percentage
- Work log entry
- Files changed
- Parallelization batch status
