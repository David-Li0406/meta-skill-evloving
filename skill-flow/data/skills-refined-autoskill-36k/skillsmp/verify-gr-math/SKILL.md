---
name: verify-gr-math
description: "GR/warp verification workflow for CasimirBot: enforce WARP_AGENTS constraints, math-stage reporting, adapter verification, certificate integrity, and training-trace export. Use when editing GR/warp modules, constraint policies, warp viability, math stage registry, or any change that requires the Casimir verification gate."
---
# Verify GR Math

## Overview
Run the repo guardrails for GR/warp changes (math-stage checks, required tests, adapter verification, and certificate integrity) before claiming viability or completion.

## Workflow Decision Tree
1) Scope the change
- Identify touched files.
- If any file is in the GR/warp pipelines or listed in `MATH_STATUS.md`, run the full workflow.
- If unsure, run `npm run math:trace -- <path-or-tag>` to resolve stage and dependencies.

2) Update math-stage evidence
- Run `npm run math:report` to refresh `reports/math-report.json` and `reports/math-report.md`.
- Run `npm run math:validate` to check stage rules and evidence coverage.

3) Run required tests (warp/GR features)
- When touching GR/warp features or Stage 3 modules, run the required tests from `WARP_AGENTS.md`:
  - tests/theory-checks.spec.ts
  - tests/stress-energy-brick.spec.ts
  - tests/york-time.spec.ts
  - tests/gr-agent-loop.spec.ts
  - tests/gr-agent-loop-baseline.spec.ts
  - tests/gr-constraint-gate.spec.ts
  - tests/gr-constraint-network.spec.ts
  - tests/stress-energy-matter.spec.ts
- Use `npx vitest run <file...>` or `npm run test -- <file...>`.

4) Run Casimir verification gate (required for any patch)
- Run `npm run casimir:verify -- --ci --trace-out artifacts/training-trace.jsonl`.
- If auth/tenancy is enabled, pass `--token` and `--tenant` (check `ENABLE_AGI_AUTH` and `AGI_TENANT_REQUIRED`).
- Override the adapter endpoint with `--url` or `CASIMIR_PUBLIC_BASE_URL` if needed.

5) Enforce results
- If verdict is FAIL, fix the first failing HARD constraint and re-run until PASS.
- Do not claim "physically viable" unless all HARD constraints pass and certificate status is ADMISSIBLE with integrity OK.
- Capture verdict, firstFail, deltas, and certificate hash in the response.
- If verification cannot run, state that and stop.

## Reference Files
- `WARP_AGENTS.md` for constraints, required tests, and certificate policy.
- `MATH_STATUS.md` for stage maturity and allowed claims.
- `MATH_GRAPH.json` for dependency stage edges.
- `reports/math-report.json` for evidence gaps and unit coverage.
- `docs/ADAPTER-CONTRACT.md` and `cli/casimir-verify.ts` for adapter details.
