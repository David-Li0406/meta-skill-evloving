---
name: testing
description: Policies for unit testing, E2E testing, and test-running constraints for DBConvert Streams UI.
---

# Testing (Agent & Copilot Rules)

## Scope
- Prefer **unit tests (Vitest)** by default.
- E2E tests (Playwright) are out of scope unless explicitly requested.
- Do not assume the dev server is running unless the user says it is.

## Commands (Preferred)
- Unit tests: `yarn test:unit`
- Lint/build checks (often faster signal): `yarn lint`, `yarn build`
- E2E tests: `yarn test` / `yarn test:headed` / `yarn test:ui` (only when asked)

## Critical Constraints
- **Never run `yarn dev` automatically.** The maintainer starts the dev server manually.
- Use **Yarn only** (no npm). Node >= 22 is required.

## Test Locations
- Unit tests: `src/__tests__/`
- Playwright E2E: `tests/` (auth state: `tests/.auth/user.json` is not committed)

## Adding/Changing Tests
- Add/update unit tests for new behavior where practical.
- Keep tests focused; avoid fragile timing-based assertions.
- Prefer testing public behavior over implementation details.

## Developer How-To
For developer-facing setup and step-by-step commands, see `TESTING.md`.
