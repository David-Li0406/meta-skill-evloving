---
name: edge-eval
description: Run eval snapshots, checks, or reports for Operator's Edge.
---

# Edge Eval

Run eval snapshots, invariant checks, and reports.

## Usage

- `$edge-eval snapshot`
- `$edge-eval check`
- `$edge-eval run-bank`
- `$edge-eval report`

## Instructions

1. Load `active_context.yaml` and read `evals` config.
2. If `evals.enabled` is false, explain and stop.
3. For `snapshot`:
   - Capture `state_before` in `.proof/evals/<date>/run-<n>/before.json`
4. For `check`:
   - Capture `state_after`, compute diff, run invariant checks
   - Log `eval_run` entry to `.proof/session_log.jsonl`
5. For `run-bank`:
   - Iterate `evals.task_bank` (default trials = `evals.trials.count`)
   - Run snapshot+check for each trial
   - Summarize pass/fail
6. For `report`:
   - Summarize last `eval_run` (pass/fail + failed invariants)

Warnings:
- Deterministic checks only.
- If snapshots are truncated, skip invariants and surface a warning.

