---
name: session-update
description: Update the active development session when work is completed. Use automatically after code changes, bug fixes, feature implementations, or file modifications when .claude/sessions/.current-session exists.
user-invocable: false
---

# Update the current development session

Read `.claude/sessions/.current-session` to find active session, then add timestamped update to the Progress section.

Include $ARGUMENTS as notes if provided, otherwise summarize recent work.

## When to update

- **Task start**: Change Goals `[ ]` → `[~]` (in progress)
- **Task complete**: Change `[~]` → `[x]` (completed), record in Progress section
- **Major milestone**: Add summary to Progress section
- **Problem/blocker found**: Record in Notes section

## Update format

```markdown
### YYYY-MM-DD HH:MM

- Completed work
- Issues found (if any)
```

## Guidelines

- Keep session updates concise to avoid disrupting workflow
- No need to notify user of every update (proceed naturally)
