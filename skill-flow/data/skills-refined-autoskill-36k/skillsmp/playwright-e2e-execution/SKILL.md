---
name: playwright-e2e-execution
description: Run targeted Playwright E2E flows for auth, scheduling, and onboarding. Use when the user asks for E2E smoke tests or specific flow validation.
---
# Playwright E2E Execution

## Quick Start

1. Pick the specific flow to validate.
2. Run the matching Playwright script.
3. Report pass/fail with artifacts.

## Steps

- Use repo scripts:
  - `scripts/playwright-auth-smoke.ts`
  - `scripts/playwright-schedule-conflict.ts`
  - `scripts/playwright-therapist-authorization.ts`
  - `scripts/playwright-therapist-onboarding.ts`

## Output

- Pass/fail summary and any failing steps.
