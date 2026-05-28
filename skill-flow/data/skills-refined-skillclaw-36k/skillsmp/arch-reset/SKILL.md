---
name: arch-reset
description: Reset session state for a fresh start
disable-model-invocation: true
---

# /arch-reset Skill

**Status: Active**

Reset the current architecture session to start fresh. Removes session state and optionally preserves the log.

## Usage

```
/arch-reset
/arch-reset --keep-log
```

## What Gets Reset

By default, removes:
- `.claude/arch/state.json` - session state
- `.claude/arch/session_log.json` - step completion log

With `--keep-log`, only removes `state.json` (preserves the log for reference).

**Note:** `TASK_GRAPH.json` and other architecture artifacts are NOT removed. Run `/arch [request]` to regenerate them.

---

## Step 1: Confirm Reset

Display the current session status and ask for confirmation:

```
Current session:
  Phase: [phase]
  Current step: [current_step or "none"]
  Log entries: [count]

This will remove state.json and session_log.json.
Continue? (y/n)
```

If user declines, stop without changes.

---

## Step 2: Execute Reset

Run the reset command:

```bash
python scripts/arch_session.py reset
```

Or to preserve the log:

```bash
python scripts/arch_session.py reset --keep-log
```

---

## Step 3: Report Result

Output the result:

```
Reset complete. Removed: state.json, session_log.json

Run /arch to start a new planning session.
```

---

## When to Use

Use `/arch-reset` when:

- **Starting over** - need to re-plan from scratch
- **Session is corrupted** - state is invalid or out of sync
- **Requirements changed** - original plan is no longer valid
- **Testing** - want to verify the full workflow again

Use `--keep-log` when:

- You want to preserve the history for reference
- Debugging issues with the workflow

---

## Constraints

- **Confirmation required**: Always confirm before resetting
- **Preserves TASK_GRAPH.json**: Architecture artifacts remain intact
- **Non-destructive**: Only removes session state, not source code
