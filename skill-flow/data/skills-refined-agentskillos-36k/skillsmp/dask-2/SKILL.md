---
name: dask
description: Async via dask, end turn immediately; use only when user explicitly delegates to Droid (ask/@droid/let droid/review); NOT for questions about Droid itself.
metadata:
  short-description: Ask Droid asynchronously via dask
---

# Ask Droid (Async)

Send the user’s request to Droid asynchronously.

## Execution (MANDATORY)

```
Bash(dask <<'EOF'
$ARGUMENTS
EOF
, run_in_background=true)
```

## Rules

- After running `dask`, say “Droid processing...” and immediately end your turn.
- Do not wait for results or check status in the same turn.

## Notes

- If it fails, check backend health with `dping`.
