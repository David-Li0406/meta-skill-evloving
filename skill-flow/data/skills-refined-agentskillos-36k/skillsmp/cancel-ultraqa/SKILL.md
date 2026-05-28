---
name: cancel-ultraqa
description: Cancel active UltraQA cycling workflow
---

# Cancel UltraQA

[ULTRAQA CANCELLED]

The UltraQA cycling workflow has been cancelled. Clearing state file.

## MANDATORY ACTION

Execute this command to cancel UltraQA:

```bash
mkdir -p .sisyphus && echo '{"active": false, "cancelled_at": "'$(date -Iseconds)'", "reason": "User cancelled via /cancel-ultraqa"}' > .omc/ultraqa-state.json
```

After running this command, the QA cycling will stop.

## To Start Fresh

- `/oh-my-claudecode:ultraqa --tests` - Run until all tests pass
- `/oh-my-claudecode:ultraqa --build` - Run until build succeeds
- `/oh-my-claudecode:ultraqa --lint` - Run until no lint errors
- `/oh-my-claudecode:ultraqa --typecheck` - Run until no type errors
- `/oh-my-claudecode:ultraqa --custom "pattern"` - Run until pattern matches
