---
name: learn-off
description: Disable learning mode
user_invokable: true
---

# Learn Off

Disable learning mode. The reminder flag will be cleared.

## What This Does

Deactivates learning mode:
- Clears the learning mode flag
- `/knowledge` will no longer show the session reminder
- Manual `/learn` commands still work

## Instructions

1. Read `knowledge/state.json`
2. Update the state:
   ```json
   {
     "learning_mode": false,
     "learning_mode_since": null
   }
   ```
3. Write updated state back to `knowledge/state.json`
4. Confirm to user with summary

## Output Format

```
Learning Mode: DISABLED
-------------------------
Learning mode is now inactive.

Session summary:
  - Extractions performed: X

Manual extraction is still available via /learn.
Use /knowledge to view accumulated insights.
```

## Notes

- Disabling learning mode does not delete any captured insights
- The knowledge base remains available for reference
- You can re-enable with `/learn-on` at any time
