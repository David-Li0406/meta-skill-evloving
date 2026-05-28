---
name: cancel-ralph-loop
description: Use this skill to cancel an active Ralph loop session when you need to stop the iterative process.
---

# Cancel Ralph Loop

This skill cancels an active Ralph loop session, allowing for a clean exit and preserving progress.

## When to Use

- The loop is stuck or making no progress.
- You want to manually intervene or take a different approach.
- You receive a max iterations warning and need to stop.

## What It Does

1. Checks for the current loop state.
2. Deactivates the loop and updates the status.
3. Reports the final state, including iterations completed and tasks finished.

## Usage

Simply invoke:
```
/cancel-ralph-loop
```

## Process

### Step 1: Check Loop State

Check for the existence of the loop state file:

```bash
if [ -f ".claude/ralph-loop.local.md" ]; then
    # Proceed to cancel the loop
else
    echo "No active Ralph Loop found."
    exit 1
fi
```

### Step 2: Deactivate Loop

If the loop is active, delete the state file and update the status:

```bash
rm .claude/ralph-loop.local.md
echo "Ralph Loop cancelled."
```

### Step 3: Report Status

After cancellation, report the following to the user:

```
Ralph loop cancelled.

Session: {session name}
Iterations completed: {n}/{max}
Tasks completed: {n}/{total}

Progress preserved in:
- prd.json (completed tasks still marked)
- progress.txt (session log)

To resume: /ralph
```

## Alternative: Manual Cancellation

You can also cancel the loop manually by deleting the state file directly:

```bash
rm ".claude/ralph-loop.local.md"
```

## Notes

- Cancellation is immediate, and work in progress is preserved.
- Use `/ralph-loop` to start a new loop if needed.