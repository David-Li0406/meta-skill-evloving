# Checkpoint Recovery

## Finding Checkpoints

Check `.context/checkpoints/INDEX.md` for available checkpoints:

```markdown
| Timestamp | Type | Position | Key Event |
|-----------|------|----------|-----------|
| 2026-01-10-1430 | milestone | auth-fix | Completed auth refactor |
| 2026-01-10-1500 | periodic | testing | Mid-test checkpoint |
```

## Loading a Specific Checkpoint

```
/session-start --checkpoint 2026-01-10-1430
```

## Recovery Steps

### Step 1: Read Checkpoint File

```
.context/checkpoints/checkpoint-[timestamp].md
```

### Step 2: Verify File States

Compare checkpoint's "Files Changed" against current git status:

```bash
git status
git diff [files listed in checkpoint]
```

### Step 3: Check for Conflicts

If files differ from checkpoint:
- Determine if changes are intentional (another session)
- Or if they need to be reverted

### Step 4: Restore Agent State

If checkpoint had active agents:
- Re-spawn agents as needed
- Provide them context from checkpoint

### Step 5: Resume Work

Continue from "Next step" in checkpoint's Current Position section.

## Troubleshooting

### Checkpoint File Missing

```
Most recent checkpoint not found.
Falling back to: [next most recent]
```

### Files Modified Since Checkpoint

```
Warning: Files have changed since checkpoint:
- path/to/file.ts: [modified/deleted/created]

Options:
1. Continue with current state (changes are intentional)
2. Investigate discrepancies before continuing
```

### Multiple Checkpoints Available

Present list and ask user:
```
Multiple checkpoints found:
1. 2026-01-10-1500 (periodic) - Most recent
2. 2026-01-10-1430 (milestone) - Auth refactor complete

Which checkpoint to load? [1/2]
```

## Checkpoint Types

| Type | Recovery Priority | Best For |
|------|-------------------|----------|
| milestone | High | After major work |
| pre-risk | High | Before risky operations |
| periodic | Medium | Regular saves |
| quick | Low | Brief pauses |
