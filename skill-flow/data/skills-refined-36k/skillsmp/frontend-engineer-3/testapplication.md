---
description: ANTIGRAVITY TESTING WORKFLOW
---

GLOBAL RULES
- Stack: FastAPI + Pytest | React + TypeScript + Vitest | Playwright (SMOKE ONLY)
- No full E2E in Playwright
- Playwright max 2–3 tests per feature
- Headless only, no trace/video/screenshots
- Stop execution on first failure
- folder structure should be singular modularity with each specific domain folder, should not add all the files in a single folder make loose coupling

FEATURE WORKFLOW

1. INPUT
- screen shot 
- Manual Test Suite with expected and actual result in table 

2. BACKEND (API → UNIT TEST)
- Write pytest unit tests:
  - success case
  - validation failure
  - auth/permission failure

3. FRONTEND (UI → UNIT TEST)
- Mock API response
- Write Vitest tests:
  - render check
  - success state
  - error state


4. E2E (PLAYWRIGHT → SMOKE ONLY)
- Add 1–2 smoke tests
- Validate:
  - page loads
  - route works
- No business logic assertions


EXECUTION ORDER
1. pytest tests/api
2. npm run test
3. npx playwright test --grep @smoke

DONE

step4 : For every feature: API unit tests → UI unit tests → minimal Playwright smoke tests only.

once done give the failed cases in bulled points