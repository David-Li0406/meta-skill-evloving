---
name: small-bugfix
description: Lightweight triage→repro→patch→quick tests flow for small fixes; optimized for mini-executor/executor
---

# Small Bugfix

Use for small, well-scoped fixes. Keeps scope tight and favors fast validation.

## Steps
1) Triage
- Clarify symptom, scope, and owner code path
- Capture minimal repro steps (or note if not reproducible)

2) Reproduce (or approximate)
- Repro locally if possible; if not, craft a minimal hypothetical repro based on logs/description
- Note any blockers to repro

3) Patch minimally
- Change the smallest surface; avoid refactors
- Keep logging unobtrusive; prefer structured logs if already used

4) Quick tests
- Run the smallest effective checks: targeted unit/integration or a fast smoke path
- If no tests exist, describe a minimal test that would catch this

5) Verify and summarize
- Confirm symptom resolved (or reason if not fully testable)
- Record files touched, risk, and follow-ups (e.g., add test later)

## Outputs
- Repro note (actual or hypothetical)
- Patch summary and risk
- Tests run (or suggested) and results
- Follow-ups (tech debt, missing test)

## When to stop and ask
- No plausible repro path
- Fix touches high-risk areas (auth, payments, migrations) → escalate to full plan
- Requires schema/API changes → use migration-safe-change skill instead
