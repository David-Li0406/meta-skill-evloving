# Verdict Template

Use this format when presenting diagnostic results.

---

## Standard Verdict Format

````markdown
## Diagnosis: [VERDICT]

**Confidence**: [High/Medium/Low]

### Summary

[1-2 sentence summary of finding]

### Evidence

**Error observed**:
[Quote the key error message]

**Investigation findings**:

- [Finding 1]
- [Finding 2]
- [Finding 3]

### Root Cause

[Explain why this is happening]

### Recommended Fix

[Describe the fix]

```[language]
// Code showing the fix
```
````

### Next Steps

1. [Step 1]
2. [Step 2]

---

Would you like me to implement this fix?

````

---

## Verdict Types

### CODE BUG

```markdown
## Diagnosis: CODE BUG

**Confidence**: High

### Summary
Recent code changes broke the session creation flow. The `handleSubmit` function now returns before saving.

### Evidence

**Error observed**:
````

Error: expect(received).toHaveText(expected)
Expected: "Session created"
Received: ""

````

**Investigation findings**:
- Test logic follows best practices (Pattern 3: uses seeding)
- Commit `abc123` (2 days ago) modified `SessionForm.tsx`
- The commit added early return on line 45 that skips the save

### Root Cause
PR #123 added validation but introduced early return that prevents form submission.

### Recommended Fix

Remove the erroneous early return in `src/components/SessionForm.tsx:45`:

```typescript
// Current (broken)
if (!isValid) return;
onSubmit(data); // Never reached if valid!

// Fixed
if (!isValid) return;
await onSubmit(data);
````

### Next Steps

1. Fix the early return logic in SessionForm.tsx
2. Re-run the test to confirm fix
3. Check if other tests are affected

---

Would you like me to implement this fix?

````

---

### TEST ISSUE

```markdown
## Diagnosis: TEST ISSUE

**Confidence**: High

### Summary
Test violates Pattern 12 (worker-isolated dates), causing parallel test collisions in CI.

### Evidence

**Error observed**:
````

error: duplicate key value violates unique constraint "idx_sessions_account_date_unique"

````

**Investigation findings**:
- Test uses hardcoded date: `new Date('2025-01-15')`
- No recent code changes to session logic
- Error only occurs in CI with parallel workers
- Pattern 12 requires `getIsolatedDate()` for session dates

### Root Cause
Multiple parallel workers create sessions with identical date, violating unique constraint.

### Recommended Fix

Use worker-isolated dates in `playwright/tests/session-creation.spec.ts`:

```typescript
// Current (broken)
const sessionDate = '2025-01-15';

// Fixed
import { getIsolatedDate } from '../fixtures/testIsolation';
const sessionDate = getIsolatedDate(1);
````

### Next Steps

1. Update test to use isolated dates
2. Run test 3x locally to confirm no collision
3. Push and verify CI passes

---

Would you like me to implement this fix?

````

---

### BOTH

```markdown
## Diagnosis: BOTH CODE BUG AND TEST ISSUE

**Confidence**: Medium

### Summary
Test has a pattern violation that masked a real code bug. Both need fixing.

### Evidence

**Test Issue (P2)**:
- Test uses `.catch(() => false)` without follow-up assertion (Pattern 8)
- This caused test to pass silently when the bug was introduced

**Code Bug (P1)**:
- `formatCurrency` function throws on null input since commit `def456`
- Bug was hidden by the silent pass pattern

### Root Cause
1. Test was written with anti-pattern that swallows errors
2. Code change introduced null handling bug
3. Bug went undetected because test passed silently

### Recommended Fix

**Fix test first** (to properly detect the bug):
```typescript
// Current (silent pass)
const formatted = await getCurrency().catch(() => false);
if (!formatted) return; // Silently exits

// Fixed (fail loudly)
const formatted = await getCurrency();
expect(formatted).toBeTruthy();
````

**Then fix code**:

```typescript
// Current (throws on null)
export function formatCurrency(value: number) {
  return value.toFixed(2);
}

// Fixed (handles null)
export function formatCurrency(value: number | null) {
  if (value === null) return "$0.00";
  return `$${value.toFixed(2)}`;
}
```

### Next Steps

1. Fix test to remove silent pass pattern
2. Verify test now fails (correctly detecting the bug)
3. Fix the formatCurrency function
4. Verify test passes

---

Would you like me to implement these fixes in order?

````

---

### UNCERTAIN

```markdown
## Diagnosis: UNCERTAIN

**Confidence**: Low

### Summary
Unable to definitively determine if this is a code bug or test issue. Signals are mixed.

### Evidence

**For CODE BUG**:
- API response shape appears different than expected
- Some related tests are also failing

**For TEST ISSUE**:
- Test passed 2/3 runs (flaky behavior)
- No obvious pattern violations found

**Inconclusive**:
- No recent git changes to relevant files
- Error message is ambiguous

### Hypotheses

1. **Flaky test (60% likely)**: Timing issue with async state update
2. **External dependency (30% likely)**: API behavior changed
3. **Environment issue (10% likely)**: Local state differs from CI

### Recommended Investigation

1. Run test 5 more times to establish pass rate
2. Check API logs for the failing request
3. Compare local vs CI environment variables
4. Add `--trace on` to capture visual state at failure

---

Would you like me to gather more information with any of these approaches?
````

---

### FLAKY

````markdown
## Diagnosis: FLAKY TEST (TEST ISSUE)

**Confidence**: High

### Summary

Test passes inconsistently (2/3 runs). Race condition or timing issue.

### Evidence

**Run results**:

- Run 1: FAIL (timeout waiting for element)
- Run 2: PASS
- Run 3: PASS

**Investigation findings**:

- Uses `waitForLoadState('networkidle')` (Pattern 7 violation)
- No explicit wait before clicking button
- Element appears after async data load

### Root Cause

Test doesn't wait for specific element before interacting. Race between navigation completing and element rendering.

### Recommended Fix

Replace generic wait with specific element wait:

```typescript
// Current (flaky)
await page.goto("/dashboard");
await page.waitForLoadState("networkidle");
await page.click('button:has-text("Create")');

// Fixed (stable)
await page.goto("/dashboard");
await expect(page.getByRole("button", { name: "Create" })).toBeVisible();
await page.getByRole("button", { name: "Create" }).click();
```
````

### Next Steps

1. Update test with explicit waits
2. Run 5x to confirm stability
3. Remove any `waitForLoadState('networkidle')` calls

---

Would you like me to implement this fix?

```

---

## Confidence Levels

| Level | When to Use |
|-------|-------------|
| **High** | Clear evidence pointing to single cause |
| **Medium** | Strong indicators but some ambiguity |
| **Low** | Mixed signals, multiple possible causes |

## Verdict Selection Guide

| Evidence Pattern | Verdict |
|------------------|---------|
| Code changed, test follows patterns, assertion fails on real behavior | CODE BUG |
| Pattern violations found, no code changes, flaky behavior | TEST ISSUE |
| Both code issues and test issues found | BOTH |
| Passes sometimes, no clear pattern violation | FLAKY (TEST ISSUE) |
| Mixed signals, can't determine | UNCERTAIN |
```
