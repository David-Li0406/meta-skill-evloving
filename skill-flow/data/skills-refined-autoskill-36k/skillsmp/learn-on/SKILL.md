---
name: learn-on
description: Enable learning mode as a reminder to extract insights
user_invokable: true
---

# Learn On

Enable learning mode. This sets a flag to remind you to run `/learn` before ending your session.

## What This Does

Activates learning mode where:
- A flag is set to indicate learning is active
- `/knowledge` will show a reminder to run `/learn` before ending
- Manual `/learn` is still required for extraction (v0.1.0)

This is useful for marking sessions where you want to capture insights, serving as a visual reminder to extract knowledge before ending.

## Instructions

1. Read `knowledge/state.json`
2. Update the state:
   ```json
   {
     "learning_mode": true,
     "learning_mode_since": "[current ISO timestamp]"
   }
   ```
3. Write updated state back to `knowledge/state.json`
4. Confirm to user

## Output Format

```
Learning Mode: ENABLED
------------------------
Learning mode is now active.

IMPORTANT: Remember to run /learn before ending your session!

Insights will be saved to:
  - knowledge/learnings/patterns.md
  - knowledge/learnings/quirks.md
  - knowledge/learnings/decisions.md

Use /learn-off to disable, or /learn for manual extraction.
```

## Notes

- Learning mode persists across the session but resets on new sessions
- You must still run `/learn` manually to extract insights (v0.1.0)
- Use `/knowledge` to see current learning status and the reminder
- Future versions may add automatic extraction triggers
