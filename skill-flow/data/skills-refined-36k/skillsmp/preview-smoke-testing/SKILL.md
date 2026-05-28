---
name: preview-smoke-testing
description: Run preview build smoke tests and verify runtime config. Use when the user mentions preview smoke, runtime config validation, or pre‑deploy checks.
---
# Preview Smoke Testing

## Quick Start

1. Build preview artifacts.
2. Validate runtime config.
3. Run smoke checks.

## Steps

- Use repo scripts:
  - `scripts/preview-build.ts`
  - `scripts/run-preview-smoke.ts`
  - `scripts/smoke-preview.ts`
- Reference `docs/PREVIEW_SMOKE.md` for the required checks.

## Output

- Clear pass/fail summary.
- Any config mismatches or smoke failures listed with remediation.
