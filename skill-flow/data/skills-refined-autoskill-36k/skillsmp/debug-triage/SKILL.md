---
name: debug-triage
description: "Systematically reproduce, diagnose, and fix bugs; use when debugging failures, crashes, or test errors (trigger keywords: debug, bug, failure, crash, flaky test)."
---

# Debug Triage

## What this skill does
- Reproduces issues, isolates root causes, and applies minimal fixes.
- Verifies fixes with targeted tests and documents findings.
- Produces a concise bug report when reproduction is possible.

## When to use it
- Trigger phrases: "debug", "bug", "failure", "crash", "flaky test".
- Use for runtime errors, test failures, or unexpected behavior.

## Step-by-step workflow
1) Gather context: expected vs actual behavior, error output, logs, environment details, and recent changes.
2) Reproduce with the smallest reliable steps; if not reproducible, ask for missing info or add targeted logging.
3) Trace the code path and form specific root-cause hypotheses (include config, data, and concurrency where relevant).
4) Validate hypotheses with evidence from code, logs, or targeted tests; rule out alternatives.
5) Apply a minimal fix aligned with project patterns; avoid unrelated refactors.
6) Verify: rerun reproduction steps and relevant tests; note any regression risks.
7) Document root cause, fix, tests, and remaining risks or follow-ups.

## Expected outputs / formatting
- Repro steps with expected vs actual behavior and observed output.
- Environment details (OS/version/config) when relevant.
- Root cause explanation with file references.
- Hypotheses tested (brief) and evidence used.
- Fix summary and tests run.
- Remaining risks or follow-ups.

## Example prompts
- "Debug this crash and propose a fix."
- "Investigate why this test is failing."
- "Triage this flaky test and suggest a minimal change."
