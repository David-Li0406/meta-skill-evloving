---
name: test-or-bug
description: Diagnoses failing E2E tests to determine if failure is a code bug or test issue. Use when user says "test or bug", "is this a test issue", "why is this test failing", "diagnose test failure", "debug e2e", or "analyze failing test".
allowed-tools: Bash, Read, Glob, Grep, Task, AskUserQuestion
version: 1.1.0
---

# Test or Bug

> Diagnose failing E2E tests to determine whether the failure indicates a code bug or a test issue.

<when_to_use>

## When to Use

Invoke when user says:

- "test or bug"
- "is this a test issue"
- "why is this test failing"
- "diagnose test failure"
- "debug e2e"
- "analyze failing test"
- "is this a bug or flaky test"

**Input**: Path to a failing E2E test spec file (e.g., `playwright/tests/session-creation.spec.ts`)

</when_to_use>

<workflow>

## Workflow Overview

| Phase | Action             | Details                                           | Duration |
| ----- | ------------------ | ------------------------------------------------- | -------- |
| 1     | Run Test           | Execute the failing test, capture full output     | 30-120s  |
| 2     | Error Analysis     | Parse error message, identify failure type        | ~10s     |
| 3     | Code Investigation | Check recent git changes, trace relevant code     | ~30s     |
| 4     | Pattern Check      | Compare test against playwright-best-practices.md | ~20s     |
| 5     | Verdict & Fix      | Deliver diagnosis + recommended fix               | ~10s     |

**Expected total duration**: 2-4 minutes depending on test complexity.

For detailed phase instructions: [references/diagnostic-phases.md](references/diagnostic-phases.md)

</workflow>

<diagnostic_flowchart>

## Diagnostic Decision Tree

Use this flowchart to classify failures:

```
E2E Test Failing?
│
├─ Test PASSES when skill runs it?
│  └─ FLAKY TEST - Likely test issue (race condition, timing)
│     → Check for missing waits, hardcoded timeouts
│
├─ In CI only, passes locally?
│  ├─ Worker/async related? → Pattern 4 (emit_automation_event)
│  ├─ Route cleanup issue? → Pattern 5 (fixture import)
│  └─ Parallel collision? → Pattern 12 (worker-isolated dates)
│
├─ Timeout error?
│  ├─ Selector not found? → Check if element exists in code
│  ├─ Network timeout? → Check API endpoint exists
│  └─ Generic timeout? → Pattern 7 (use specific waits)
│
├─ Assertion failure?
│  ├─ Expected value changed? → Likely CODE BUG
│  ├─ Wrong expected value in test? → TEST ISSUE
│  └─ Data-dependent? → Check seeding
│
├─ Database constraint error?
│  └─ Pattern 11 (missing required fields, unique violations)
│
├─ Auth timeout?
│  └─ Pattern 1 (chromium vs chromium-clean project)
│
└─ Test order matters?
   └─ Pattern 2 (test isolation, shared state)
```

Pattern references from: `claude-patterns/playwright-best-practices.md`

</diagnostic_flowchart>

<verdict_criteria>

## Verdict Classification

### CODE BUG Indicators

| Signal                                     | Confidence |
| ------------------------------------------ | ---------- |
| Test logic correct per patterns            | High       |
| Recent git changes touched code under test | High       |
| Assertion on real behavior fails           | High       |
| Multiple tests failing on same feature     | High       |
| Same test passed before recent commit      | Very High  |

### TEST ISSUE Indicators

| Signal                                       | Confidence |
| -------------------------------------------- | ---------- |
| Pattern violations found                     | High       |
| Hardcoded dates or non-isolated data         | High       |
| Uses UI creation when should seed            | Medium     |
| Missing `emit_automation_event`              | High       |
| Wrong project (chromium vs clean)            | Very High  |
| Silent pass patterns (`.catch(() => false)`) | Very High  |
| Test passes on re-run (flaky)                | High       |

### BOTH (Compound Verdict)

Sometimes a failing test reveals BOTH issues:

- Test has pattern violations AND code has a bug
- Report both with separate severity levels
- Recommend fixing test first if it masks the real failure

### UNCERTAIN

If signals are ambiguous:

- Report confidence level (Low/Medium/High)
- Present evidence for each hypothesis
- Recommend manual investigation

</verdict_criteria>

<execution>

## Phase Execution

### Phase 1: Run Test

```bash
npx playwright test <test-file> --reporter=list --timeout=60000 --retries=0
```

Flags explained:

- `--reporter=list`: Clear output format
- `--timeout=60000`: 60s timeout for faster diagnosis
- `--retries=0`: No retries to see actual failure

If test PASSES:

1. Note this as potential flaky test
2. Run again 2 more times to confirm
3. If inconsistent (some pass, some fail), classify as FLAKY

### Phase 2: Error Analysis

Read the playwright output and classify:

1. **Timeout**: `TimeoutError`, `waiting for selector`, `waiting for`
2. **Assertion**: `expect(received).toBe(expected)`, `toHaveText`, `toBeVisible`
3. **Network**: `net::ERR_`, `ECONNREFUSED`, `fetch failed`
4. **Database**: `duplicate key`, `violates foreign key`, `null value`
5. **Auth**: `unauthorized`, `401`, `login failed`

### Phase 3: Code Investigation

```bash
# Check recent changes to relevant files
git log --oneline -10 -- <relevant-paths>

# Diff against last known good state
git diff HEAD~5 -- <relevant-paths>
```

Identify:

- Files touched by the test (components, services, hooks)
- Recent commits that modified those files
- Changes that could cause the failure

### Phase 4: Pattern Check

Read `claude-patterns/playwright-best-practices.md` and check test against:

- Pattern 3: DB seeding vs UI creation
- Pattern 5: Route handler cleanup
- Pattern 7: Specific waits vs networkidle
- Pattern 8: Silent pass anti-patterns
- Pattern 12: Worker-isolated dates

### Phase 5: Verdict & Fix

Present findings using format from [references/verdict-template.md](references/verdict-template.md)

</execution>

<quick_reference>

## Quick Reference

**Commands**:

```bash
# Run specific test
npx playwright test playwright/tests/<name>.spec.ts

# Run with trace
npx playwright test <test> --trace on

# Show last report
npx playwright show-report
```

**Key Pattern Files**:

- `claude-patterns/playwright-best-practices.md` - Primary diagnostic source
- `playwright/fixtures/seedHelpers.account.ts` - Seeding helpers
- `playwright/fixtures/testIsolation.ts` - Worker-isolated dates
- `playwright/utils/timeouts.ts` - TIMEOUTS constants

**Common Fixes**:
| Issue | Fix |
|-------|-----|
| Hardcoded date | Use `getIsolatedDate()` from testIsolation.ts |
| UI creation for setup | Use `seedAccount()`, `seedSession()` from seedHelpers |
| Missing wait | Add `await expect(element).toBeVisible()` before interaction |
| Silent pass | Remove `.catch(() => false)`, add hard assertion |

</quick_reference>

<references>

## References

- [references/diagnostic-phases.md](references/diagnostic-phases.md) - Detailed phase execution
- [references/common-failures.md](references/common-failures.md) - Failure patterns and fixes
- [references/verdict-template.md](references/verdict-template.md) - Output format

</references>

<version_history>

## Version History

- **v1.1.0** (2025-01-18): AI optimization updates
  - Add blockquote summary after title

- **v1.0.0** (2025-01-15): Initial release
  - 5-phase diagnostic workflow
  - Decision tree from playwright-best-practices.md
  - Support for CODE BUG, TEST ISSUE, BOTH, and UNCERTAIN verdicts
  - Flaky test detection

</version_history>
