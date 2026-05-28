---
name: dask
description: Send a task to Droid via the `dask` CLI and wait for the reply. Use only when the user explicitly delegates to Droid (ask/@droid/let droid/review); not for questions about Droid itself.
metadata:
  short-description: Ask Droid (wait for reply) via dask
  backend: droid
---

# dask (Ask Droid)

Use `dask` to forward the user's request to the Droid pane.

## Prereqs (Backend)

- `dping` should succeed.
- `dask` must run in the same environment as `ccb` (WSL vs native Windows).

## Execution (MANDATORY)

```bash
dask --sync -q <<'EOF'
$ARGUMENTS
EOF
```

## Workflow (Mandatory)

1. Ensure Droid backend is up (`dping`).
2. Run the command above with the user's request.
3. **IMPORTANT**: Use `timeout_ms: 3600000` (1 hour) to allow long-running tasks.
4. DO NOT send a second request until the current one exits.

## CRITICAL: Wait Silently (READ THIS)

After running `dask`, you MUST:
- **DO NOTHING** while waiting for the command to return
- **DO NOT** check status, monitor progress, or run any other commands
- **DO NOT** read files, search code, or do "useful" work while waiting
- **DO NOT** output any text like "waiting..." or "checking..."
- **JUST WAIT** silently until dask returns with the result

The command may take 10-60 minutes. This is NORMAL. Be patient.

If you find yourself wanting to do something while waiting, STOP. Just wait.

## Notes

- Always use `--sync` flag when calling from Codex.
- `dask` is synchronous; the `--sync` flag disables guardrail prompts intended for Claude.
- If the user requires a `CCB_DONE` sentinel, still include a brief execution summary in the reply (do not return only the sentinel).
