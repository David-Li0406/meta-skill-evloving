---
name: testing
description: >
  Implement testing patterns for PhotoVault using Playwright and Vitest.
  Use when writing E2E tests, unit tests, API route tests, or debugging
  flaky tests. Includes PhotoVault test fixtures, page objects, and
  Stripe webhook testing patterns.
---

# ⚠️ MANDATORY WORKFLOW - DO NOT SKIP

**When this skill activates, you MUST follow the expert workflow before writing any code:**

1. **Spawn Domain Expert** using the Task tool with this prompt:
   ```
   Read the expert prompt at: C:\Users\natha\Stone-Fence-Brain\VENTURES\PhotoVault\claude\experts\testing-expert.md

   Then research the codebase and write an implementation plan to: docs/claude/plans/testing-[task-name]-plan.md

   Task: [describe the user's request]
   ```

2. **Spawn QA Critic** after expert returns, using Task tool:
   ```
   Read the QA critic prompt at: C:\Users\natha\Stone-Fence-Brain\VENTURES\PhotoVault\claude\experts\qa-critic-expert.md

   Review the plan at: docs/claude/plans/testing-[task-name]-plan.md
   Write critique to: docs/claude/plans/testing-[task-name]-critique.md
   ```

3. **Present BOTH plan and critique to user** - wait for approval before implementing

**DO NOT read files and start coding. DO NOT rationalize that "this is simple." Follow the workflow.**

---

# Testing Integration

## Core Principles

### Test the User Journey, Not the Code

Tests should verify what users experience, not internal implementation details.

```typescript
// ❌ BAD: Testing implementation
test('setGalleryPaid sets is_paid to true', () => {
  const gallery = { is_paid: false }
  setGalleryPaid(gallery)
  expect(gallery.is_paid).toBe(true)
})

// ✅ GOOD: Testing behavior
test('client gains access after payment completes', async ({ page }) => {
  await page.goto('/gallery/abc123')
  expect(page.locator('[data-testid="locked-message"]')).toBeVisible()

  await completePayment(page)

  await page.goto('/gallery/abc123')
  expect(page.locator('[data-testid="photo-grid"]')).toBeVisible()
})
```

### Each Test Must Be Independent

Tests should not depend on each other or on execution order.

```typescript
// ❌ BAD: Tests depend on each other
test('create gallery', async () => {
  galleryId = await createGallery()  // Sets global state!
})
test('add photos to gallery', async () => {
  await addPhotos(galleryId)  // Depends on previous test!
})

// ✅ GOOD: Each test sets up its own data
test('add photos to gallery', async () => {
  const gallery = await createTestGallery()  // Fresh setup
  await addPhotos(gallery.id)
})
```

### No Flaky Tests - Handle Async Properly

```typescript
// ❌ BAD: Arbitrary sleep
await page.click('#submit')
await page.waitForTimeout(2000)
expect(page.locator('.success')).toBeVisible()

// ✅ GOOD: Wait for specific condition
await page.click('#submit')
await expect(page.locator('.success')).toBeVisible({ timeout: 5000 })
```

## Anti-Patterns

**Testing implementation details**
```typescript
// WRONG: Testing internal state
const { result } = renderHook(() => useCounter())
expect(result.current.count).toBe(1)

// RIGHT: Testing what user sees
await expect(page.locator('[data-testid="count"]')).toHaveText('1')
```

**Sharing state between tests**
```typescript
// WRONG: Global state
let testUser: User
beforeAll(async () => { testUser = await createUser() })

// RIGHT: Fresh state per test
beforeEach(async () => { testUser = await createUser() })
afterEach(async () => { await deleteUser(testUser.id) })
```

**Not using data-testid for selectors**
```typescript
// WRONG: Fragile selectors
await page.click('.btn-primary')
await page.click('button:nth-child(2)')

// RIGHT: Stable test IDs
await page.click('[data-testid="checkout-button"]')
```

**Asserting too much in one test**
```typescript
// WRONG: Multiple behaviors in one test
test('checkout flow', async ({ page }) => {
  // Test gallery, checkout, payment, access... if it fails, which part broke?
})

// RIGHT: One behavior per test
test('gallery displays event name', async ({ page }) => {...})
test('checkout redirects to Stripe', async ({ page }) => {...})
```

## Playwright E2E Pattern

```typescript
// tests/e2e/gallery-access.spec.ts
import { test, expect } from '@playwright/test'
import { createTestGallery, cleanupTestData } from '../fixtures/data'

test.describe('Gallery Access', () => {
  let gallery: TestGallery

  test.beforeEach(async () => {
    gallery = await createTestGallery()
  })

  test.afterEach(async () => {
    await cleanupTestData(gallery.id)
  })

  test('unpaid gallery shows locked state', async ({ page }) => {
    await page.goto(`/gallery/${gallery.access_code}`)

    await expect(page.locator('[data-testid="locked-overlay"]')).toBeVisible()
    await expect(page.locator('[data-testid="photo-grid"]')).not.toBeVisible()
  })

  test('paid gallery shows photos', async ({ page }) => {
    await markGalleryPaid(gallery.id)
    await page.goto(`/gallery/${gallery.access_code}`)

    await expect(page.locator('[data-testid="photo-grid"]')).toBeVisible()
  })
})
```

## Vitest Unit Test Pattern

```typescript
// tests/unit/commission.test.ts
import { describe, it, expect } from 'vitest'
import { calculateCommission } from '@/lib/payments/commission'

describe('calculateCommission', () => {
  it('splits amount 50/50 between platform and photographer', () => {
    const result = calculateCommission(10000)

    expect(result).toEqual({
      photographerAmount: 5000,
      platformAmount: 5000,
      totalAmount: 10000,
    })
  })

  it('throws for negative amounts', () => {
    expect(() => calculateCommission(-100)).toThrow('Amount must be positive')
  })
})
```

## Page Object Pattern

```typescript
// tests/pages/GalleryPage.ts
import { Page, Locator, expect } from '@playwright/test'

export class GalleryPage {
  readonly page: Page
  readonly photoGrid: Locator
  readonly payButton: Locator
  readonly lockedOverlay: Locator

  constructor(page: Page) {
    this.page = page
    this.photoGrid = page.locator('[data-testid="photo-grid"]')
    this.payButton = page.locator('[data-testid="pay-button"]')
    this.lockedOverlay = page.locator('[data-testid="locked-overlay"]')
  }

  async goto(accessCode: string) {
    await this.page.goto(`/gallery/${accessCode}`)
  }

  async expectLocked() {
    await expect(this.lockedOverlay).toBeVisible()
    await expect(this.photoGrid).not.toBeVisible()
  }
}

// Usage:
test('unpaid gallery is locked', async ({ page }) => {
  const galleryPage = new GalleryPage(page)
  await galleryPage.goto('ABC123')
  await galleryPage.expectLocked()
})
```

## PhotoVault Configuration

### Test File Structure

```
tests/
├── e2e/                    # Playwright E2E tests
├── integration/            # API & webhook tests
├── unit/                   # Unit tests
├── fixtures/               # Test data factories
├── pages/                  # Page objects
└── utils/                  # Test helpers
```

### Stripe Test Cards

| Card | Number | Use Case |
|------|--------|----------|
| Success | `4242 4242 4242 4242` | Happy path |
| Decline | `4000 0000 0000 0002` | Payment failure |
| 3D Secure | `4000 0025 0000 3155` | Auth required |

### Critical Test Scenarios

| Priority | Scenario | Type |
|----------|----------|------|
| P0 | Payment completes and access granted | E2E |
| P0 | Commission recorded correctly | Integration |
| P0 | Webhook idempotency (no duplicates) | Integration |
| P1 | Failed payment handled gracefully | E2E |

### Test Environment

```bash
cd photovault-hub
npm run dev -- -p 3002

# Stripe CLI for webhook testing
stripe listen --forward-to localhost:3002/api/webhooks/stripe
```

## Debugging Checklist

1. Is each test independent? No shared state?
2. Are you using data-testid selectors?
3. Are you waiting for conditions, not arbitrary timeouts?
4. Is the test testing behavior, not implementation?
5. Are test fixtures cleaned up after each test?
