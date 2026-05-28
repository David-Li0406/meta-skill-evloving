---
name: debug-mode
description: Run an iterative, hypothesis-driven “debug mode” loop to diagnose and fix a bug using targeted instrumentation and log capture. Use when the user wants an interactive debug loop, when you need to quickly narrow a failure via added debug statements, or when you need a lightweight way to centralize logs from a repro run (via `agent-skills debug` server + SSE UI).
---

# Debug Mode

Run a tight debug loop: form a hypothesis, instrument the smallest surface area, capture evidence, update the hypothesis, and repeat until you can ship a fix with a regression test (or a clear root-cause explanation).

This skill assumes you can add temporary debug statements and that you can ask the user to run a repro while a local log capture server is running.

## Quick start

1. Start the log capture server:

```bash
agent-skills debug
```

2. Ask the user to reproduce while sending logs to the server (pick a method):
- `agent-skills debug send …`
- `curl -X POST … /v1/logs`

3. Use the captured evidence to pick the next instrumentation point and repeat.

Reference: `skills/debug-mode/references/debug-server.md`.

## Workflow (debug loop)

1. Establish the repro and success criteria.
   - Ask for exact commands/inputs and the expected vs actual outcome.
   - Freeze variables: versions, env, config, dataset, feature flags.
   - If the bug is flaky, ask for frequency and a “best repro” loop.

2. Form a falsifiable hypothesis.
   - Phrase it as: “If X is happening, we should observe Y at location Z.”
   - Prefer hypotheses that narrow the search space (not “something is wrong”).

3. Instrument minimally.
   - Add logs at decision boundaries, not every line.
   - Log identifiers and invariants (IDs, counts, state machine states), not entire blobs.
   - Include correlation keys (`requestId`, `userId`, `jobId`, etc.).

4. Capture and review evidence.
   - Use the debug server UI and/or the NDJSON file as the shared artifact.
   - Summarize the evidence in a small table: observation → supports/refutes → next step.

5. Iterate until root cause is isolated.
   - Move instrumentation “upstream” or “downstream” based on what you learned.
   - Delete/undo misleading logs; keep only the ones that pay rent.

6. Fix + lock it in.
   - Implement the smallest safe fix.
   - Add a regression test or a runnable repro script.
   - Remove or downgrade temporary debug statements.

## Notes for using `agent-skills debug`

- Default auth is a random token printed at startup.
- By default, events are appended as NDJSON to `.agent-skills/debug.ndjson` (disable with `--out=`).
- Use headers for ingestion where possible; use `?token=` mainly for the browser UI.
- Prefer structured JSON logs with stable keys over freeform text.
