# Diagnostic Phases - Detailed Execution

## Phase 1: Run Test

### Goal

Execute the failing test and capture complete output for analysis.

### Commands

```bash
# Standard diagnostic run (recommended)
npx playwright test <test-file> --reporter=list --timeout=60000 --retries=0

# With trace capture for visual debugging
npx playwright test <test-file> --trace on --timeout=60000 --retries=0

# Run specific test by name
npx playwright test <test-file> -g "test name pattern"
```

### Flag Rationale

| Flag              | Purpose                                         |
| ----------------- | ----------------------------------------------- |
| `--reporter=list` | Clean line-by-line output for parsing           |
| `--timeout=60000` | 60s cap prevents indefinite hangs               |
| `--retries=0`     | See actual failure, not masked by retry success |
| `--trace on`      | Capture screenshots/DOM for visual inspection   |

### Handling Test Pass

If the test PASSES when you run it:

1. **Run 3 times total** to detect intermittent failures
2. **Check pass rate**:
   - 3/3 pass = Not reproducible locally, may be CI-specific
   - 2/3 pass = FLAKY - likely timing/race condition
   - 1/3 pass = Mostly failing, continue diagnosis
3. **Report flakiness** in verdict if inconsistent

### Capturing Output

Save full output for analysis:

- Error message and stack trace
- Which test step failed
- Timeout duration if applicable
- Any console errors logged

---

## Phase 2: Error Analysis

### Goal

Classify the error type to guide investigation direction.

### Error Categories

#### Timeout Errors

```
TimeoutError: locator.click: Timeout 30000ms exceeded.
=========================== logs ===========================
waiting for locator('button:has-text("Submit")')
```

**Investigation path**: Check if element exists, selector is correct, page loaded

#### Assertion Errors

```
Error: expect(received).toBe(expected)
Expected: "Active"
Received: "Pending"
```

**Investigation path**: Check if expected value changed in code, or test expectation is wrong

#### Network Errors

```
net::ERR_CONNECTION_REFUSED at http://localhost:8080/api/sessions
```

**Investigation path**: Is dev server running? Is API endpoint correct?

#### Database Errors

```
error: duplicate key value violates unique constraint "idx_sessions_account_date_unique"
```

**Investigation path**: Check seeding, date isolation, cleanup

#### Auth Errors

```
TimeoutError: page.goto: Timeout 30000ms exceeded.
waiting for navigation to "http://localhost:8080/dashboard"
```

**Investigation path**: Check auth storage state, correct project (chromium vs chromium-clean)

### Extracting Key Information

From error output, identify:

1. **Failed step**: Which `test.step()` or assertion
2. **Selector**: What element was being targeted
3. **Expected vs Actual**: For assertions
4. **Duration**: How long before timeout

---

## Phase 3: Code Investigation

### Goal

Determine if recent code changes could have caused the failure.

### Git Commands

```bash
# Find files the test interacts with
# (extract from test file: page.goto URLs, selectors, API calls)

# Recent commits to those files
git log --oneline -10 -- src/components/SessionForm.tsx src/services/sessionService.ts

# What changed recently
git diff HEAD~5 -- src/components/SessionForm.tsx

# Find when a specific line was last changed
git log -p -S "buttonText" -- src/components/SessionForm.tsx
```

### Identifying Relevant Files

From the test file, trace:

1. **Routes visited**: `page.goto('/sessions')` → `src/pages/Sessions.tsx`
2. **Selectors used**: `getByRole('button', { name: 'Save' })` → component with that button
3. **API calls**: `waitForResponse('/api/sessions')` → `src/services/sessionService.ts`
4. **Data dependencies**: What's being seeded, what's being asserted

### Correlation Analysis

| If Recent Changes Include... | Likely Cause                                        |
| ---------------------------- | --------------------------------------------------- |
| Selector text changed        | Test selector outdated (TEST ISSUE)                 |
| API response shape changed   | Test expectation wrong OR frontend broken           |
| Business logic changed       | Could be intentional (TEST ISSUE) or bug (CODE BUG) |
| No relevant changes          | Look at external factors (data, environment)        |

---

## Phase 4: Pattern Check

### Goal

Compare the test against documented best practices to identify test issues.

### Read Pattern File

```bash
Read claude-patterns/playwright-best-practices.md
```

### Critical Pattern Checks

#### Pattern 3: DB Seeding vs UI Creation

- **Check**: Does test use UI to create prerequisite data?
- **Issue**: Slow and flaky
- **Fix**: Use `seedAccount()`, `seedSession()` from fixtures

#### Pattern 5: Route Handler Cleanup

- **Check**: Does test use `page.route()` without cleanup?
- **Issue**: "Target page closed" errors
- **Fix**: Use `performanceOptimizations` fixture or add `afterEach` with `page.unrouteAll()`

#### Pattern 7: Specific Waits

- **Check**: Does test use `waitForLoadState('networkidle')`?
- **Issue**: Flaky, slow
- **Fix**: Wait for specific element: `await expect(element).toBeVisible()`

#### Pattern 8: Silent Pass Anti-patterns

- **Check**: Does test have `.catch(() => false)` without follow-up assertion?
- **Issue**: Test passes even when feature is broken
- **Fix**: Add hard assertion after conditional

#### Pattern 12: Worker-Isolated Dates

- **Check**: Does test use hardcoded dates like `new Date('2025-01-15')`?
- **Issue**: Parallel collisions in CI
- **Fix**: Use `getIsolatedDate()` from `testIsolation.ts`

### Recording Violations

For each pattern violation found:

1. Note the pattern number
2. Quote the offending code
3. Provide the fix from the pattern file

---

## Phase 5: Verdict & Fix

### Goal

Synthesize findings into clear verdict with actionable fix.

### Decision Matrix

| Code Changes? | Pattern Violations? | Test Passes on Re-run? | Verdict            |
| ------------- | ------------------- | ---------------------- | ------------------ |
| Yes           | No                  | No                     | CODE BUG           |
| No            | Yes                 | Maybe                  | TEST ISSUE         |
| Yes           | Yes                 | Maybe                  | BOTH               |
| No            | No                  | Yes                    | FLAKY (TEST ISSUE) |
| No            | No                  | No                     | UNCERTAIN          |

### Presenting Verdict

Use the format from [verdict-template.md](verdict-template.md):

1. Lead with verdict (CODE BUG / TEST ISSUE / BOTH / UNCERTAIN)
2. Show confidence level
3. Present evidence
4. Provide fix recommendation
5. Offer to implement fix

### If UNCERTAIN

When signals are mixed:

1. Present both hypotheses
2. Rank by likelihood
3. Suggest manual investigation steps
4. Offer to gather more information
