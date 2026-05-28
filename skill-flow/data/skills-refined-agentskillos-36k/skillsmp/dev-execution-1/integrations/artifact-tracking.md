# Artifact Tracking Integration

How dev-execution integrates with the artifact-tracking skill.

## When to Use Artifact Tracking

| Execution Mode | Use Artifact Tracking? |
|----------------|----------------------|
| Phase execution | **Always** |
| Quick feature | No (too lightweight) |
| Story execution | If multi-phase |
| Scaffolding | No |

## Core Integration Points

### Progress File Location

```
.claude/progress/{PRD_NAME}/phase-{PHASE_NUM}-progress.md
```

### YAML Frontmatter Structure

```yaml
---
prd_name: feature-name
phase: 1
status: in_progress
completion: 45%
tasks:
  - id: TASK-1.1
    title: Task title
    status: completed
    assigned_to: [ui-engineer-enhanced]
    dependencies: []
  - id: TASK-1.2
    title: Another task
    status: in_progress
    assigned_to: [backend-typescript-architect]
    dependencies: [TASK-1.1]
parallelization:
  batch_1: [TASK-1.1, TASK-1.2]
  batch_2: [TASK-2.1]
---
```

## Workflow

### Before Execution

1. **Check for existing progress file**:
   ```bash
   progress_file=".claude/progress/${PRD_NAME}/phase-${PHASE_NUM}-progress.md"
   ```

2. **If missing, create via artifact-tracker**:
   ```
   Task("artifact-tracker", "Create Phase ${PHASE_NUM} progress for ${PRD_NAME}")
   ```

### During Execution

1. **Read YAML frontmatter only** (token-efficient):
   ```bash
   head -100 ${progress_file} | sed -n '/^---$/,/^---$/p'
   ```

2. **Identify batch from `parallelization` field**

3. **After task completion, update via artifact-tracker**:
   ```
   Task("artifact-tracker", "Update ${PRD_NAME} phase ${PHASE_NUM}: Mark TASK-X.Y complete")
   ```

### After Execution

1. **Validate phase completion**:
   ```
   Task("artifact-validator", "Validate Phase ${PHASE_NUM} for ${PRD_NAME}")
   ```

2. **Mark phase complete**:
   ```
   Task("artifact-tracker", "Update ${PRD_NAME} phase ${PHASE_NUM}: Set status to complete")
   ```

## Key Principles

### Token Efficiency

- **Read YAML only** (~2KB) instead of full file (~25KB)
- Let subagents read detailed task sections when implementing
- Use artifact-tracker for updates (not manual Edit)

### Update Immediately

- Update task status right after completion
- Don't batch multiple status updates
- Include commit hash in completion notes

### Always Validate

- Use artifact-validator before marking phase complete
- Verify all success criteria met
- Check no blockers remain

## Status Updates

### Task Completed

```
Task("artifact-tracker", "Update ${PRD_NAME} phase ${PHASE_NUM}:
- Mark TASK-1.1 as completed
- Add commit abc1234
- Log: Implemented Button component with tests")
```

### Task Blocked

```
Task("artifact-tracker", "Update ${PRD_NAME} phase ${PHASE_NUM}:
- Mark TASK-1.2 as blocked
- Log blocker: External API dependency unavailable
- Add to blockers section")
```

### Phase Complete

```
Task("artifact-tracker", "Finalize ${PRD_NAME} phase ${PHASE_NUM}:
- Mark phase as completed
- Update completion to 100%
- Generate phase completion summary")
```

## Artifact-Tracker Commands

The artifact-tracker agent understands these operations:

| Operation | Description |
|-----------|-------------|
| Create | Create new progress file |
| Update | Update task status, add logs |
| Query | Get pending/blocked tasks |
| Validate | Check completion criteria |
| Finalize | Mark phase complete |

## Reference

Full artifact-tracking skill: `.claude/skills/artifact-tracking/SKILL.md`
