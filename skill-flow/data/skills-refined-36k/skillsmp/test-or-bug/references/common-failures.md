# Common E2E Test Failures

Categorized failure patterns with diagnosis and fixes based on `claude-patterns/playwright-best-practices.md`.

---

## Category 1: Selector/Element Failures

### Timeout waiting for selector

**Error**:

```
TimeoutError: locator.click: Timeout 30000ms exceeded.
waiting for locator('button:has-text("Save")')
```

**Diagnosis checklist**:

1. Does the element exist in the rendered page?
2. Was the button text changed in recent commits?
3. Is there a loading state blocking it?
4. Is the selector specific enough?

**If CODE BUG**: Button was removed or text changed unintentionally
**If TEST ISSUE**: Selector is wrong, or missing wait for loading state

**Fix (TEST ISSUE)**:

```typescript
// Bad: Generic selector
await page.click('button:has-text("Save")');

// Good: Wait for specific state first
await expect(page.getByRole("button", { name: "Save" })).toBeEnabled();
await page.getByRole("button", { name: "Save" }).click();
```

---

### Element not visible

**Error**:

```
Error: locator.click: Error: Element is not visible
```

**Diagnosis checklist**:

1. Is element behind a modal or overlay?
2. Is element conditionally rendered?
3. Is there a scroll needed?

**Fix**:

```typescript
// Ensure element is in viewport and visible
await expect(element).toBeVisible();
await element.scrollIntoViewIfNeeded();
await element.click();
```

---

## Category 2: Timing/Race Condition Failures

### Flaky test (passes sometimes)

**Diagnosis checklist**:

1. Does test use `waitForLoadState('networkidle')`? (Pattern 7)
2. Does test have race between navigation and assertion?
3. Is there a debounced input without timeout?

**Fix (Pattern 7)**:

```typescript
// Bad: Generic wait
await page.waitForLoadState("networkidle");

// Good: Wait for specific element
await expect(page.getByText("Dashboard")).toBeVisible();
```

### Search/filter not working

**Error**: Test types in search but results don't filter

**Cause**: Debounced input, test asserts before debounce completes

**Fix**:

```typescript
await searchInput.fill("test query");
// Add timeout for debounce
await expect(page.getByText("test query result")).toBeVisible({
  timeout: 3000,
});
```

---

## Category 3: Data/Database Failures

### Unique constraint violation

**Error**:

```
error: duplicate key value violates unique constraint "idx_sessions_account_date_unique"
```

**Diagnosis**: Two tests creating sessions with same account + date

**Fix (Pattern 12)**:

```typescript
// Bad: Hardcoded date
const sessionDate = "2025-01-15";

// Good: Worker-isolated date
import { getIsolatedDate } from "../fixtures/testIsolation";
const sessionDate = getIsolatedDate(1); // Unique per worker
```

### Foreign key violation

**Error**:

```
error: insert or update on table "sessions" violates foreign key constraint
```

**Diagnosis**: Referenced record (account, contact) doesn't exist

**Fix**: Ensure seeding creates all dependencies:

```typescript
const { account, contact } = await seedFullChain(supabase, orgId, userId);
await seedSession(supabase, { account_id: account.id, ... });
```

### Data not found after insert

**Error**: Test inserts data but can't find it

**Diagnosis**: Direct DB insert doesn't trigger automation events

**Fix (Pattern 4)**:

```typescript
// After direct insert, emit event if automation depends on it
await supabase.rpc("emit_automation_event", {
  p_event_type: "session_created",
  p_payload: { session_id: session.id },
});
```

---

## Category 4: Authentication Failures

### Login timeout in chromium project

**Error**:

```
TimeoutError: page.goto: Timeout 30000ms exceeded.
```

**Diagnosis (Pattern 1)**: Test in `chromium` project calls `loginAsUser()` but `chromium` uses pre-saved storage state.

**Fix**:

```typescript
// Tests in 'chromium' project should NOT call loginAsUser()
// They already have auth from setup project

// Tests in 'chromium-clean' project SHOULD call loginAsUser()
```

### Session expired mid-test

**Error**: Actions fail with 401 after test runs for a while

**Diagnosis**: Long-running test, auth token expired

**Fix**: Use shorter test timeout or refresh auth mid-test

---

## Category 5: Async/Worker Failures

### Email not sent

**Error**: Test waits for email_queue entry that never appears

**Diagnosis (Pattern 4)**:

1. Direct DB insert doesn't trigger automation
2. Worker isn't running locally
3. Missing `emit_automation_event` call

**Fix**:

```typescript
// Check worker health first
test.beforeAll(async () => {
  const response = await fetch('http://localhost:3001/health');
  expect(response.ok).toBe(true);
});

// After insert, emit event
await supabase.rpc('emit_automation_event', { ... });

// Use expect.poll for async wait
await expect.poll(async () => {
  const { data } = await supabase.from('email_queue').select().eq('session_id', id);
  return data?.length;
}, { timeout: 30000 }).toBeGreaterThan(0);
```

---

## Category 6: Cleanup/Isolation Failures

### Route handler errors

**Error**:

```
Error: Target page, context or browser has been closed
```

**Diagnosis (Pattern 5)**: Route handlers outlive the page

**Fix**:

```typescript
// If using performanceOptimizations fixture, cleanup is automatic

// If using base @playwright/test, add cleanup
test.afterEach(async ({ page }) => {
  await page.unrouteAll({ behavior: "ignoreErrors" });
});
```

### Test pollution (order matters)

**Error**: Test passes alone, fails when run with others

**Diagnosis (Pattern 2)**: Shared state between tests

**Fix**:

```typescript
// Use test.describe.serial ONLY for same-resource tests
// Otherwise ensure complete isolation

// Add pre-cleanup for interrupted test data
test.beforeEach(async ({ supabase }) => {
  await supabase.from("sessions").delete().eq("account_id", testAccountId);
});
```

---

## Category 7: Silent Pass Issues

### Test passes but feature is broken

**Diagnosis (Pattern 8)**: Test has silent pass anti-patterns

**Common culprits**:

```typescript
// BAD: .catch swallows error
const exists = await element.isVisible().catch(() => false);
// If element is broken, test passes!

// GOOD: Hard assertion
await expect(element).toBeVisible();
```

```typescript
// BAD: Early return skips test
if (!feature.enabled) return;
// Test does nothing, passes

// GOOD: Use test.skip with reason
test.skip(!feature.enabled, "Feature flag disabled");
```

```typescript
// BAD: Loop that runs zero times
for (const item of items) {
  await expect(item).toBeVisible();
}
// If items is empty, test passes!

// GOOD: Assert count first
expect(items.length).toBeGreaterThan(0);
```

---

## Quick Diagnosis Guide

| Error Pattern               | First Check                | Likely Cause                      |
| --------------------------- | -------------------------- | --------------------------------- |
| `TimeoutError: locator`     | Does element exist?        | Selector wrong or element removed |
| `duplicate key`             | Using hardcoded dates?     | Pattern 12 violation              |
| `foreign key`               | Is prerequisite seeded?    | Missing seed step                 |
| `401 Unauthorized`          | Which playwright project?  | Pattern 1 (chromium vs clean)     |
| `Target page closed`        | Using page.route()?        | Pattern 5 (route cleanup)         |
| Test passes but shouldn't   | Any `.catch(() => false)`? | Pattern 8 (silent pass)           |
| Works alone, fails together | Shared state?              | Pattern 2 (isolation)             |
