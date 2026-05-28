# Artifact Tracking Integration

How dev-execution integrates with the artifact-tracking skill.

## When to Use Artifact Tracking

| Execution Mode | Use Artifact Tracking? |
|----------------|----------------------|
| Phase execution | **Always** |
| Quick feature | No (too lightweight) |
| Story execution | If multi-phase |
| Scaffolding | No |

## CLI-First Updates

**For status updates, use CLI scripts directly** (0 agent tokens):

```bash
# Mark task complete
python .claude/skills/artifact-tracking/scripts/update-status.py \
  -f .claude/progress/${PRD_NAME}/phase-${PHASE_NUM}-progress.md \
  -t TASK-1.1 -s completed

# Batch update after parallel execution
python .claude/skills/artifact-tracking/scripts/update-batch.py \
  -f .claude/progress/${PRD_NAME}/phase-${PHASE_NUM}-progress.md \
  --updates "TASK-1.1:completed,TASK-1.2:completed,TASK-1.3:completed"
```

**Use artifact-tracker agent only for**:
- Creating new progress files
- Updates requiring context/notes
- Recording blockers with resolution plans

## Workflow

### Before Execution

1. **Check for existing progress file**:
   ```bash
   ls .claude/progress/${PRD_NAME}/phase-${PHASE_NUM}-progress.md
   ```

2. **If missing, create via agent**:
   ```
   Task("artifact-tracker", "Create Phase ${PHASE_NUM} progress for ${PRD_NAME}")
   ```

### During Execution

1. **Read YAML frontmatter only** (~2KB, not full file):
   - Get `parallelization.batch_N` for current batch
   - Get `tasks[].assigned_to` for delegation

2. **Execute batch in parallel** (single message with multiple Task calls)

3. **Update via CLI after completion**:
   ```bash
   python .claude/skills/artifact-tracking/scripts/update-batch.py \
     -f FILE --updates "TASK-1.1:completed,TASK-1.2:completed"
   ```

### After Execution

1. **Validate phase completion**:
   ```
   Task("artifact-validator", "Validate Phase ${PHASE_NUM} for ${PRD_NAME}")
   ```

2. **Mark phase complete via CLI**:
   ```bash
   python .claude/skills/artifact-tracking/scripts/update-status.py \
     -f FILE -t PHASE -s completed
   ```

## Key Principles

| Principle | Implementation |
|-----------|---------------|
| CLI-first | Use scripts for simple status changes (~50 tokens) |
| YAML source of truth | Read frontmatter only, never parse markdown |
| Update immediately | Don't batch - update after each task completion |
| Validate before complete | Run artifact-validator before marking phase done |

## Reference

Full artifact-tracking skill: `.claude/skills/artifact-tracking/SKILL.md`

For format details, YAML schema, and agent operations: see artifact-tracking skill documentation.
