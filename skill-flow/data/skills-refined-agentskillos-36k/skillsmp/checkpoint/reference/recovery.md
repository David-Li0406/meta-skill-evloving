# Checkpoint Recovery

## Recovery Process

### Step 1: Find Available Checkpoints

Check `.context/checkpoints/INDEX.md` for list:

```markdown
| Timestamp | Type | Position | Key Event |
|-----------|------|----------|-----------|
| [time] | [type] | [task/step] | [what happened] |
```

### Step 2: Load Checkpoint

```
/session-start --checkpoint [timestamp]
```

This will:
1. Load the specified checkpoint
2. Verify file states
3. Report current position
4. Be ready to continue

### Step 3: Verify State

After loading checkpoint:
- Check files match checkpoint's "Files Changed"
- Verify database state if applicable
- Confirm no unexpected changes

### Step 4: Resume Work

Continue from "Next step" in checkpoint's Current Position.

## Manual Recovery

If `/session-start` not available:

1. Read checkpoint file directly
2. Note the "Current Position" → "Next step"
3. Re-establish context by reading listed docs
4. Re-spawn any active agents
5. Continue from next step

## Troubleshooting

### Files Don't Match Checkpoint

- Check git status for unexpected changes
- Use git to restore files if needed
- Note discrepancies before continuing

### Missing Checkpoint

- Check if compaction occurred (checkpoints may be pruned)
- Use most recent available checkpoint
- Fall back to handoff.md if no checkpoints

### Database State Changed

- For reversible changes: apply reverse
- For irreversible: note in session and proceed carefully
- Consider creating new baseline

## Checkpoint Retention

**Keep:**
- Last 3 checkpoints
- Any checkpoint marked "milestone"
- Today's checkpoints

**Delete (safe to remove):**
- Checkpoints older than 24 hours (unless milestone)
- Quick checkpoints after session ends
- Pre-risk checkpoints if operation succeeded

## Integration

### With /compact
Checkpoint first, then compact if needed. Checkpoint preserves state; compact clears context.

### With /handoff
Handoff is for session end. Checkpoint is for mid-session saves. Different purposes, complementary.

### With /session-start
Session-start can load from checkpoint, handoff, or compact-state. Checkpoints are preferred for recovery.
