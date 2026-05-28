---
name: systematic-debugging
description: Use for bugs/test failures. Reproduce, isolate root cause, fix, and validate with evidence.
---

## Workflow

1. Reproduce the issue reliably (capture exact commands, inputs, and environment).
2. Collect evidence (logs, stack traces, failing tests, minimal repro).
3. Narrow scope (bisect or localize to the smallest function/module).
4. Form a hypothesis (one likely root cause) and a test to falsify it.
5. Apply the smallest fix that addresses the root cause.
6. Validate (re-run the repro; run the tightest relevant tests; watch for regressions).
7. Add a guardrail if appropriate (assertion, validation, or targeted test).

## Output expectations

- State: repro steps, hypothesis, and the verification you ran.
- Prefer minimal diffs over broad refactors.
