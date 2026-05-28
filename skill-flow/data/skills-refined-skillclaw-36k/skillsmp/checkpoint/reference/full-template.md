# Full Checkpoint Template

```markdown
# Checkpoint: [timestamp]

**Type**: [milestone/periodic/pre-risk/quick]
**Trigger**: [what prompted this checkpoint]

## Session Objective
[Overall goal of this session]

## Current Position

### Task In Progress
- **What**: [current task]
- **Status**: [where in the task]
- **Next step**: [immediate next action]

### Workflow Position
```
[workflow name]
Step 1: ✓ Complete
Step 2: ✓ Complete
Step 3: ◄── CURRENT
Step 4: Pending
```

## Work Completed Since Last Checkpoint

### Tasks Finished
- [Task 1]: [outcome]
- [Task 2]: [outcome]

### Files Changed
| File | Change | Verified |
|------|--------|----------|
| [path] | [what] | [yes/no] |

### Decisions Made
- [Decision]: [choice] because [reason]

## Agent Status

### Active Agents
| Agent | Task | Status | ETA |
|-------|------|--------|-----|
| [type] | [doing] | [state] | [when] |

### Pending Results
- [Agent]: Waiting for [what]

## Context Snapshot

### Docs Loaded
- `docs/features/[name].md`
- `docs/workflows/[name].md`

### Key Facts Established
- [Fact 1]: [source]
- [Fact 2]: [source]

### Working Assumptions
- [Assumption 1]
- [Assumption 2]

## Recovery Instructions

### To Resume From This Checkpoint
1. Read this checkpoint file
2. Verify current file states match "Files Changed"
3. Continue from "Next step" in Current Position
4. Re-spawn any active agents if needed

### If Something Went Wrong
1. [Rollback instruction if applicable]
2. [Recovery step]
3. [Alternative approach]

## Notes
[Any other context that would help recovery]
```
