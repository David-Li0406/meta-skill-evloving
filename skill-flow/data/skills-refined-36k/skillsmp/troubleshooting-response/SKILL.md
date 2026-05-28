---
name: troubleshooting-response
description: Incident response and troubleshooting for pipeline failures. Use when investigating errors, log anomalies, failed runs, or degraded performance and when preparing recovery steps or mitigations.
---

# Troubleshooting + Response

## Workflow

1) Capture the symptom
- Record exact error messages, timestamps, and affected components.
- Identify the last known good state.

2) Gather evidence
- Collect relevant logs, configs, and recent changes.
- Prefer read-only inspection first.

3) Isolate the failure
- Reproduce in a minimal scope if possible.
- Identify whether this is data, config, code, or infrastructure.

4) Propose fixes and mitigations
- Offer low-risk rollback or workaround paths first.
- Document impact and follow-up actions.

## Repo Pointers

- `docs/troubleshooting/`
- `docs/ops/`
- `docs/operations/`
- `logs/`
- `scripts/diagnostics/`
- `scripts/ops/`

## Output Expectations

- Provide a timeline of findings and the suspected root cause.
- Provide step-by-step mitigation or fix with risk notes.

## Guardrails

- Avoid speculative fixes; prefer evidence-backed changes.
- If changes are required, propose a reversible path.
