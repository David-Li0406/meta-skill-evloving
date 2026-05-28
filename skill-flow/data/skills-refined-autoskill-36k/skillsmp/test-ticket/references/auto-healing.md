# Auto-Healing Reference

Detailed documentation for the test auto-healing system used in the execution loop.

## Overview

The execution loop (Step 5) automatically detects and fixes common test failures. When a test fails, the system analyzes the error, applies an appropriate fix, and retries. After 3 failed attempts, tests are marked `test.fixme()` for manual review.

---

## Error Detection and Fixes

| Error Type | Detection Pattern | Fix Applied | Example |
|------------|-------------------|-------------|---------|
| **Locator not found** | `locator resolved to ... elements` | Add `:visible` filter | `page.locator('button').locator(':visible')` |
| **Timeout exceeded** | `Timeout 30000ms exceeded` | Use `getTimeout()` helper | `await page.waitForSelector(sel, { timeout: getTimeout() })` |
| **Strict mode violation** | `strict mode violation` | Add `.first()` | `page.locator('button').first()` |
| **401 Unauthorized** | `401 Unauthorized`, `Authentication failed` | Delete `.auth/`, recreate session | Remove stale auth state and re-authenticate |
| **Network error** | `net::ERR_CONNECTION_REFUSED` | Retry with backoff | Wait 2s, then retry request |
| **Element not visible** | `element is not visible` | Add `waitForVisible` | `await el.waitFor({ state: 'visible' })` |
| **Element detached** | `element is detached from DOM` | Re-query element | Re-fetch locator before action |

---

## Healing Strategy Per Error Type

### Locator Not Found

**Detection:**
```
Error: locator.click: Error: locator resolved to 3 elements
```

**Analysis:**
- Multiple elements match the selector
- Need to narrow down to specific element

**Fixes (in order):**
1. Add `:visible` filter to exclude hidden elements
2. Add `.first()` if multiple visible elements exist
3. Add more specific selector (data-testid, aria-label)
4. Use `nth()` if order is predictable

**Code transformation:**
```typescript
// Before
await page.locator('button').click()

// After (attempt 1)
await page.locator('button').locator(':visible').click()

// After (attempt 2)
await page.locator('button').locator(':visible').first().click()

// After (attempt 3)
await page.locator('[data-testid="submit-button"]').click()
```

---

### Timeout Exceeded

**Detection:**
```
Error: Timeout 30000ms exceeded waiting for element
```

**Analysis:**
- Element takes longer to appear than default timeout
- May indicate slow page load or dynamic content

**Fixes (in order):**
1. Use project's `getTimeout()` helper for consistent timeouts
2. Add explicit wait for element state
3. Add network idle wait before action

**Code transformation:**
```typescript
// Before
await page.waitForSelector('.modal')

// After (attempt 1)
await page.waitForSelector('.modal', { timeout: getTimeout() })

// After (attempt 2)
await page.waitForSelector('.modal', { timeout: getTimeout(), state: 'visible' })

// After (attempt 3)
await page.waitForLoadState('networkidle')
await page.waitForSelector('.modal', { timeout: getTimeout() })
```

---

### Strict Mode Violation

**Detection:**
```
Error: strict mode violation: locator resolved to 2 elements
```

**Analysis:**
- Playwright's strict mode prevents ambiguous selections
- Multiple elements match when exactly one is expected

**Fixes (in order):**
1. Add `.first()` to select first matching element
2. Add more specific selector
3. Use `filter()` with additional criteria

**Code transformation:**
```typescript
// Before
await page.locator('.list-item').click()

// After (attempt 1)
await page.locator('.list-item').first().click()

// After (attempt 2)
await page.locator('.list-item').filter({ hasText: 'Expected Text' }).click()
```

---

### 401 Unauthorized

**Detection:**
```
Error: 401 Unauthorized
Error: Authentication failed
Error: Session expired
```

**Analysis:**
- Stored authentication state is stale or invalid
- Session may have expired between test runs

**Fixes (in order):**
1. Delete `.auth/` directory to clear stale state
2. Re-run authentication setup
3. Use fresh browser context

**Code transformation:**
```typescript
// Healing script
import { rm } from 'fs/promises'
import { authSetup } from './auth.setup'

// Clear stale auth
await rm('.auth', { recursive: true, force: true })

// Re-authenticate
await authSetup()
```

---

## Healing Loop Implementation

```typescript
interface HealingResult {
  success: boolean
  attempt: number
  fix?: string
  error?: string
}

async function executeWithHealing(
  testFn: () => Promise<void>,
  maxAttempts: number = 3
): Promise<HealingResult> {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      await testFn()
      return { success: true, attempt }
    } catch (error) {
      const fix = analyzErrorAndApplyFix(error)

      if (!fix || attempt === maxAttempts) {
        return {
          success: false,
          attempt,
          error: error.message
        }
      }

      // Fix applied, retry
      console.log(`Attempt ${attempt}: Applied fix - ${fix}`)
    }
  }
}
```

---

## When Auto-Healing Fails

After 3 failed attempts, tests are marked with `test.fixme()`:

```typescript
test.fixme('user can submit form', async ({ page }) => {
  // AUTO-HEALING FAILED after 3 attempts
  // Last error: Element not found after all fix attempts
  // Requires manual investigation

  await page.goto('/form')
  await page.locator('.submit').click()
})
```

**Manual review checklist:**
- [ ] Verify element exists in the DOM
- [ ] Check if element requires user interaction to appear
- [ ] Review page state at time of failure (screenshots/traces)
- [ ] Consider if test assumptions are still valid

---

## Exolar Integration

When Exolar MCP is available, failures are classified:

```typescript
const classification = await mcp.exolar.perform_exolar_action({
  action: 'classify',
  params: {
    execution_id: executionId,
    test_name: testName
  }
})

// Classification result: FLAKE | BUG | ENV_ISSUE
```

| Classification | Action |
|----------------|--------|
| **FLAKE** | Apply auto-healing, retry |
| **BUG** | Skip healing, report as failure |
| **ENV_ISSUE** | Fix environment, retry all tests |

---

## Best Practices

### DO:
- Trust auto-healing for transient issues
- Review healed tests periodically for patterns
- Update locators proactively when UI changes

### DON'T:
- Rely on auto-healing as permanent solution
- Ignore repeated healing on same test
- Skip manual review of `test.fixme()` tests
