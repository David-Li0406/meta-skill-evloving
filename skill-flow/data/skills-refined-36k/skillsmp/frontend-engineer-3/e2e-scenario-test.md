---
description: End-to-end scenario testing - write test, run, fix issues, verify
---

// turbo-all

# E2E Scenario Testing Workflow

## Prerequisites
- Staging URL: http://localhost:8080/
- swagger API URL:http://localhost:8000/docs
- Test credentials from `/testapplication` workflow

## Step 1: Receive Scenario
**USER MUST PROVIDE:**
- Exact user role (player/coach/academy/admin)
- Specific credentials to use
- Step-by-step actions to perform
- Expected outcome

**DO NOT ASSUME OR HALLUCINATE ANY STEPS NOT SPECIFIED**

## Step 2: Analyze Existing Code
Before writing test:
1. Check relevant frontend pages/components for the flow
2. Check relevant API endpoints in backend
3. Understand current implementation

## Step 3: Write Playwright Test
Create test file in: `sportsmanagement_frontend/automation-testing/tests/scenarios/`

Test file naming: `{scenario-name}.spec.ts`

Test structure:
```typescript
import { test, expect } from '@playwright/test';

test.describe('Scenario: [EXACT SCENARIO NAME]', () => {
  test('[Step description]', async ({ page }) => {
    // Only implement steps specified by user
  });
});
```

## Step 4: Run Test
```bash
cd sportsmanagement_frontend/automation-testing
npx playwright test tests/scenarios/{test-file}.spec.ts --headed
```

## Step 5: Analyze Results
If test **PASSES**: 
- Report success to user
- Scenario verified ✅

If test **FAILS**:
- Capture exact error message
- Identify root cause (frontend/backend/data)
- Proceed to Step 6

## Step 6: Fix Issue
1. Locate exact file causing the issue in the ui or backend code or both
2. Make minimal fix to resolve the specific problem
3. Do NOT refactor or change unrelated code
4. Document what was changed and why

## Step 7: Re-run Test
```bash
npx playwright test tests/scenarios/{test-file}.spec.ts --headed
```

Repeat Steps 5-7 until test passes.

## Step 8: Report
Provide summary:
- Scenario tested
- Issues found (if any)
- Fixes applied (if any)
- Final status: PASS/FAIL

## Rules (CRITICAL)
1. **NO HALLUCINATION** - Only test what user specifies
2. **NO DEVIATION** - Stay on the exact scenario
3. **MINIMAL FIXES** - Only fix what breaks the test
4. **DOCUMENT EVERYTHING** - Show proof of each step
5. **ASK IF UNCLEAR** - Never assume user intent