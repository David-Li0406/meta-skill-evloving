---
name: test-to-playwright
description: Convert test-browser.sh output into deterministic Playwright e2e tests in TypeScript. Use when user wants to generate Playwright tests from agent-browser test scripts or output.
allowed-tools: Read, Write, Bash, Glob
---

# Convert Browser Tests to Playwright

This skill converts `test-browser.sh` (agent-browser CLI tests) into deterministic Playwright e2e tests.

## Workflow

1. **Read the source test script** at `test-browser.sh`
2. **Read any provided test output** if the user specifies a file
3. **Parse test sections** (marked with `# TEST N:` comments)
4. **Generate Playwright tests** using the mapping below
5. **Set up Playwright** if not already configured

## Command Mapping: agent-browser → Playwright

```typescript
// Navigation
agent-browser open "$URL"              → await page.goto(url)
agent-browser wait --load networkidle  → await page.waitForLoadState('networkidle')
agent-browser wait 500                 → await page.waitForTimeout(500)

// Clicks by role
find role button click --name "X"      → await page.getByRole('button', { name: 'X' }).click()
find role combobox click --name "X"    → await page.getByRole('combobox', { name: 'X' }).click()
find role option click --name "X"      → await page.getByRole('option', { name: 'X' }).click()
find role radio click --name "X"       → await page.getByRole('radio', { name: 'X' }).click()
find role switch click --name "X"      → await page.getByRole('switch', { name: 'X' }).click()
find role region click --name "X"      → await page.getByRole('region', { name: 'X' }).click()

// Regex name matching (e.g., --name "/Stars/")
find role button click --name "/X/"    → await page.getByRole('button', { name: /X/ }).click()

// Form filling
find label "X" fill "Y"                → await page.getByLabel('X').fill('Y')

// Screenshots
screenshot "path.png"                  → await page.screenshot({ path: 'path.png' })
```

## Test Structure Template

Generate tests with this structure:

```typescript
import { test, expect } from '@playwright/test';

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5173');
    await page.waitForLoadState('networkidle');
  });

  test('should do specific thing', async ({ page }) => {
    // Arrange: Set up preconditions

    // Act: Perform the action being tested

    // Assert: Verify expected outcomes
  });
});
```

## Feature Grouping

Map test sections from test-browser.sh to test files:

| Script Section | Test File | Description |
|----------------|-----------|-------------|
| TEST 1: Create Pin via Map Click | pin-create.spec.ts | Click map to create new pin |
| TEST 2: Fill Pin Form | pin-form.spec.ts | Fill all form field types |
| TEST 3: Save Pin | pin-save.spec.ts | Save and verify persistence |
| TEST 4: Create Second Pin | pin-crud.spec.ts | Multiple pin handling |
| TEST 5: Search Pins | pin-search.spec.ts | Search functionality |
| TEST 6: Filter by Category | pin-filter.spec.ts | Category filtering |
| TEST 7: Edit Pin | pin-crud.spec.ts | Edit existing pin |
| TEST 8: Delete Pin | pin-crud.spec.ts | Delete pin |

## Playwright Config Template

If `playwright.config.ts` doesn't exist, create it:

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
});
```

## Assertions to Include

For each test, add appropriate assertions:

```typescript
// Verify element exists
await expect(page.getByRole('button', { name: 'Save' })).toBeVisible();

// Verify text content
await expect(page.getByText('Golden Gate Bridge')).toBeVisible();

// Verify element count
await expect(page.getByRole('listitem')).toHaveCount(2);

// Verify form state
await expect(page.getByLabel('Title')).toHaveValue('Golden Gate Bridge');
```

## Setup Commands

If Playwright is not installed:

```bash
npm install -D @playwright/test
npx playwright install chromium
mkdir -p e2e
```

## Execution Steps

1. Read `test-browser.sh` to understand all test scenarios
2. Check if Playwright is in package.json; if not, install it
3. Create `playwright.config.ts` if it doesn't exist
4. Create `e2e/` directory if it doesn't exist
5. Generate one `.spec.ts` file per feature grouping
6. Each test should be self-contained with proper setup/teardown
7. Include helper function for clearing pins at test start

## Helper: Clear Pins Function

Include this helper in tests that need clean state:

```typescript
async function clearAllPins(page: Page) {
  // Repeatedly find and delete pins until none remain
  while (true) {
    const pinButton = page.getByRole('button', { name: /Stars/ });
    if (await pinButton.count() === 0) break;
    await pinButton.first().click();
    await page.waitForTimeout(300);
    await page.getByRole('button', { name: 'Delete' }).click();
    await page.waitForTimeout(500);
  }
}
```
