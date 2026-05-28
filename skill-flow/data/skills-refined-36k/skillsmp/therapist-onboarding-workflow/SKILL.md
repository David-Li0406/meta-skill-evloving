---
name: therapist-onboarding-workflow
description: Validate therapist onboarding end-to-end flow. Use when the user mentions onboarding tests, therapist onboarding, or onboarding smoke checks.
---
# Therapist Onboarding Workflow

## Quick Start

1. Validate runtime config for onboarding.
2. Run onboarding flow tests.
3. Summarize failures and remediation.

## Steps

- Follow `docs/onboarding-runbook.md`.
- Use repo script:
  - `scripts/playwright-therapist-onboarding.ts`
- Capture any config or UI failures in the summary.

## Output

- Pass/fail summary with steps that failed.
- Any missing config or data requirements called out.
