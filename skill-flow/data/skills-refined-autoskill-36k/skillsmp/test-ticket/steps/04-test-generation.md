# Step 4: Test Generation

**Duration**: ~3 minutes
**Purpose**: Create Playwright test files following project standards.

---

## Actions

### 1. Create/Verify Git Branch

```bash
# Ensure on correct branch
git checkout test/{ticket-id}-automated-tests 2>/dev/null || \
git checkout -b test/{ticket-id}-automated-tests
```

### 2. Spawn Test-Writer Agents

For complex features, spawn multiple agents in parallel:

```typescript
// Each scenario can be generated concurrently
const agents = scenarios.map(scenario =>
  Task({
    subagent_type: 'playwright-test-generator',
    prompt: generatePrompt(scenario)
  })
)
```

### 3. Generate Test Files

Each test file must include:

#### Imports
```typescript
import { test, expect } from '@playwright/test'
import { LoginPage } from '../../page-objects/LoginPage'
import { createAuthenticatedContextsParallel } from '../../utils/fast-setup'
import { getTimeout } from '../../utils/timeout-manager'
import { TEST_URLS, TEST_USERS, TEST_FEES } from '../../utils/constants'
```

#### Test Setup
```typescript
test.describe('{Feature} Tests', () => {
  let buyerContext: BrowserContext
  let sellerContext: BrowserContext

  test.beforeAll(async ({ browser }) => {
    const contexts = await createAuthenticatedContextsParallel(browser, {
      users: ['buyer', 'seller'],
      storageStateDir: '.auth'
    })
    buyerContext = contexts.buyer
    sellerContext = contexts.seller
  })

  test.afterAll(async () => {
    await buyerContext?.close()
    await sellerContext?.close()
  })
```

#### Test Structure
```typescript
  test('user can complete action', async () => {
    const page = await buyerContext.newPage()

    await test.step('Navigate to feature', async () => {
      await page.goto(TEST_URLS.feature, {
        waitUntil: 'domcontentloaded'
      })
    })

    await test.step('Perform action', async () => {
      await page
        .locator('button:visible')
        .filter({ hasText: 'Submit' })
        .first()
        .click()
    })

    await test.step('Verify result', async () => {
      await expect(page.locator('.success-message'))
        .toBeVisible({ timeout: getTimeout('element') })
    })
  })
})
```

### 4. Run TypeScript Type Checking

```bash
yarn check:types
```

Fix any type errors before proceeding.

---

## Code Standards

### Locator Patterns

```typescript
// Resilient locators (preferred)
page.locator('button:visible').filter({ hasText: 'Accept' }).first()
page.getByRole('button', { name: 'Submit' })
page.getByTestId('submit-button')

// Avoid fragile selectors
page.locator('#submit-btn')
page.locator('.btn-primary')
```

### Wait Strategies

```typescript
// Use timeout manager
await page.waitForURL('**/dashboard', {
  timeout: getTimeout('navigation'),
  waitUntil: 'domcontentloaded'
})

// Never hardcode timeouts
await page.waitFor({ timeout: 5000 }) // BAD
```

### Assertions

```typescript
// Use test.step for grouping
await test.step('Verify submission success', async () => {
  await expect(page.locator('.success')).toBeVisible()
  await expect(page.locator('.error')).not.toBeVisible()
})
```

---

## Output

Test files created in: `automation/playwright/tests/{feature}/`

**File Naming Convention**:
```
{feature-name}.spec.ts       # Main test file
{feature-name}-edge.spec.ts  # Edge cases (optional)
{feature-name}-api.spec.ts   # API tests (if applicable)
```

---

## Common Issues

### Import Resolution
```
Error: Cannot find module '../utils/fast-setup'
```
**Fix**: Verify path aliases in `tsconfig.json`

### Page Object Missing
```
Error: Cannot find module '../../page-objects/FeaturePage'
```
**Fix**: Create page object or use existing one

### Type Mismatch
```
Error: Property 'newMethod' does not exist on type 'Page'
```
**Fix**: Update Playwright types or use type assertion

