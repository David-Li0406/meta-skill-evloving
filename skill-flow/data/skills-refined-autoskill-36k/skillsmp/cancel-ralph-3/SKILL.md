---
name: cancel-ralph
description: Cancel active Ralph Loop
detection_patterns:
  - "cancel ralph"
  - "stop ralph loop"
  - "end ralph loop"
  - "abort ralph"
  - "exit ralph loop"
auto_invoke: false
---

# Cancel Ralph Skill

Cancel an active Ralph Loop session.

## Detection Patterns

This skill activates when the user says things like:
- "cancel ralph"
- "stop ralph loop"
- "end the ralph loop"
- "abort ralph loop"

## Behavior

When activated:

1. **Check for active loop**:
   - Look for `.claude/ralph-loop.local.md`

2. **If active**:
   - Read current state (mode, iteration count)
   - Delete the state file
   - Confirm cancellation

3. **If not active**:
   - Inform user no loop is running

## Implementation

```bash
if [ -f ".claude/ralph-loop.local.md" ]; then
    rm .claude/ralph-loop.local.md
    echo "Ralph Loop cancelled."
else
    echo "No active Ralph Loop found."
fi
```

## Notes

- Cancellation is immediate
- Work in progress is preserved
- Use `/ralph-loop` to start a new loop
