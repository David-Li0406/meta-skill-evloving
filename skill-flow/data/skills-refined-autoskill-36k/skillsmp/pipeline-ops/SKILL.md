---
name: pipeline-ops
description: Run, monitor, and control the DSA-110 continuum imaging pipeline or its orchestration. Use for starting/stopping runs, backfills, scheduling, retries, runtime state inspection, Dagster/CLI entrypoints, and operational runbooks.
---

# Pipeline Ops

## Workflow

1) Clarify the operational goal
- Ask which pipeline stage(s) and scope (service control vs data processing).
- Identify the action: start, stop, resume, backfill, rerun, monitor, or audit.

2) Locate the authoritative entrypoint
- Prefer `scripts/ops/dsa110-ctl.sh` for service management.
- Prefer the unified CLI (`dsa110`) for data processing actions.
- Use Dagster UI for production orchestration when available.

3) Execute safely
- Prefer dry-run or smallest-scope execution first.
- Capture command, config, and timestamps for traceability.

4) Verify and record
- Check logs/state for expected transitions.
- Summarize outcome, status, and next steps for operators.

## Decision Shortcuts

- Service health, deploy, secrets, logs → `scripts/ops/dsa110-ctl.sh`
- Convert/calibrate/image/workflow/specs/diagnostics → `dsa110` CLI
- Asset lineage, sensor/schedule state, retries → Dagster UI

## Repo Pointers

- `scripts/ops/dsa110-ctl.sh`
- `scripts/dsa110-cli.py`
- `docs/reference/pipeline-execution.md`
- `docs/reference/cli-reference.md`
- `docs/operations/DSA110_CONTROL_GUIDE.md`
- `docs/tutorials/03_dagster_pipeline.md` (tutorial; verify before use)
- `logs/`
- `ops/`

## References

- Read `references/pipeline-ops.md` for trusted entrypoints, command patterns, and how to pick between Dagster/CLI/service control.

## Output Expectations

- Provide exact commands run (or proposed) and configs used.
- Provide run status summary and log locations.
- Note any deviations from documented runbooks and why.

## Guardrails

- Avoid destructive actions without explicit confirmation.
- If pipeline state is unknown, prefer read-only inspection first.
- Treat tutorials as advisory; validate against verified docs and code.
