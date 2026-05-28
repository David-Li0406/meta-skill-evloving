# Playwright Test Reference

Complete reference for running structured test suites with Playwright Test (`@playwright/test`).

## Overview

Playwright Test is a test runner built on top of Playwright. Unlike the MCP-based tools (Claude in Chrome, Browser MCP) which are for interactive browser operations, Playwright Test is for running structured, repeatable test suites with assertions.

## When to Use Playwright Test

| Use Case | Why Playwright Test |
|----------|---------------------|
| Regression testing | Repeatable, deterministic results |
| CI/CD pipelines | Reports, exit codes, parallelization |
| Pre-PR validation | Run full test suite before merge |
| Feature verification | Assertions ensure expected behavior |
| Cross-browser testing | Chromium, Firefox, WebKit |

## Prerequisites

1. Playwright installed: `@playwright/test` in package.json
2. Dev server running: `pnpm dev` or `npm run dev`
3. Test files in `tests/` or configured directory

## Basic Commands

```bash
# Run all tests
npx playwright test

# Run specific test file
npx playwright test tests/e2e/auth.spec.ts

# Run tests matching pattern
npx playwright test -g "login"

# Run in specific browser
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit

# Run with visible browser
npx playwright test --headed

# Run in debug mode
npx playwright test --debug

# Run with UI mode (interactive)
npx playwright test --ui

# Show HTML report
npx playwright show-report
```

## Test File Structure

```typescript
// tests/e2e/example.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    // Setup before each test
    await page.goto('http://localhost:3001');
  });

  test('should do something', async ({ page }) => {
    // Arrange
    await page.goto('/some-page');

    // Act
    await page.click('button.submit');

    // Assert
    await expect(page.locator('.success')).toBeVisible();
  });

  test('should handle error case', async ({ page }) => {
    await page.fill('[name="email"]', 'invalid');
    await page.click('button.submit');
    await expect(page.locator('.error')).toContainText('Invalid email');
  });
});
```

## Common Assertions

```typescript
// Element visibility
await expect(page.locator('.element')).toBeVisible();
await expect(page.locator('.element')).toBeHidden();

// Text content
await expect(page.locator('h1')).toContainText('Welcome');
await expect(page.locator('h1')).toHaveText('Welcome Back');

// URL
await expect(page).toHaveURL('/dashboard');
await expect(page).toHaveURL(/dashboard/);

// Input values
await expect(page.locator('input')).toHaveValue('test@example.com');

// Element count
await expect(page.locator('.item')).toHaveCount(5);

// Attribute
await expect(page.locator('button')).toHaveAttribute('disabled', '');
await expect(page.locator('button')).toBeEnabled();
await expect(page.locator('button')).toBeDisabled();

// Screenshot comparison
await expect(page).toHaveScreenshot('homepage.png');
```

## Common Actions

```typescript
// Navigation
await page.goto('http://localhost:3001/login');
await page.goBack();
await page.goForward();
await page.reload();

// Clicking
await page.click('button.submit');
await page.click('text=Sign In');
await page.dblclick('.item');
await page.click('button', { button: 'right' });

// Typing
await page.fill('[name="email"]', 'test@example.com');
await page.type('[name="search"]', 'query', { delay: 100 });
await page.press('[name="search"]', 'Enter');

// Selection
await page.selectOption('select#country', 'US');
await page.selectOption('select#country', { label: 'United States' });

// Checkboxes/Radio
await page.check('input[type="checkbox"]');
await page.uncheck('input[type="checkbox"]');

// File upload
await page.setInputFiles('input[type="file"]', 'path/to/file.pdf');

// Hover
await page.hover('.menu-item');

// Wait
await page.waitForSelector('.loaded');
await page.waitForURL('/dashboard');
await page.waitForTimeout(1000); // Use sparingly
```

## Selectors

```typescript
// CSS selectors
page.locator('.class-name')
page.locator('#id')
page.locator('[data-testid="submit"]')

// Text selectors
page.locator('text=Sign In')
page.locator('text=/Sign In/i')  // regex

// Role selectors (recommended)
page.getByRole('button', { name: 'Submit' })
page.getByRole('textbox', { name: 'Email' })
page.getByRole('link', { name: 'Home' })

// Label selectors
page.getByLabel('Email')
page.getByPlaceholder('Enter email')

// Test ID selectors (recommended for stability)
page.getByTestId('submit-button')
```

## Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',

  use: {
    baseURL: 'http://localhost:3001',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],

  webServer: {
    command: 'pnpm dev',
    url: 'http://localhost:3001',
    reuseExistingServer: !process.env.CI,
  },
});
```

## Test Patterns

### Authentication Test
```typescript
test('user can log in', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('test@example.com');
  await page.getByLabel('Password').fill('password123');
  await page.getByRole('button', { name: 'Sign In' }).click();

  await expect(page).toHaveURL('/dashboard');
  await expect(page.getByRole('heading')).toContainText('Welcome');
});
```

### Form Validation Test
```typescript
test('shows validation errors', async ({ page }) => {
  await page.goto('/signup');
  await page.getByRole('button', { name: 'Submit' }).click();

  await expect(page.getByText('Email is required')).toBeVisible();
  await expect(page.getByText('Password is required')).toBeVisible();
});
```

### API Response Test
```typescript
test('displays data from API', async ({ page }) => {
  await page.goto('/dashboard');

  // Wait for API data to load
  await page.waitForSelector('.data-loaded');

  // Verify data is displayed
  await expect(page.locator('.item')).toHaveCount(10);
});
```

### Mock API Test
```typescript
test('handles API error', async ({ page }) => {
  // Mock API to return error
  await page.route('**/api/data', route => {
    route.fulfill({ status: 500, body: 'Server Error' });
  });

  await page.goto('/dashboard');
  await expect(page.getByText('Error loading data')).toBeVisible();
});
```

## Running in CI/CD

```yaml
# GitHub Actions example
- name: Install Playwright
  run: npx playwright install --with-deps

- name: Run Playwright tests
  run: npx playwright test

- name: Upload test results
  uses: actions/upload-artifact@v3
  if: always()
  with:
    name: playwright-report
    path: playwright-report/
```

## Debugging

```bash
# Run with inspector
npx playwright test --debug

# Run with UI mode
npx playwright test --ui

# Run with trace viewer
npx playwright test --trace on
npx playwright show-trace trace.zip

# Run single test in headed mode
npx playwright test -g "test name" --headed
```

## Best Practices

1. **Use data-testid attributes** - Most stable selectors
2. **Use role selectors** - Better accessibility, more realistic
3. **Avoid timeouts** - Use `waitForSelector` instead
4. **Keep tests independent** - Each test should work in isolation
5. **Use beforeEach for setup** - Don't rely on test order
6. **Assert specific things** - Not just "page loaded"
7. **Mock external services** - Deterministic results

## Comparison with MCP Tools

| Aspect | Playwright Test | MCP Tools |
|--------|-----------------|-----------|
| Use case | Structured tests | Interactive exploration |
| Assertions | Built-in, rich | Manual verification |
| Repeatability | High | Varies |
| CI/CD | Designed for it | Not ideal |
| Reports | HTML, JSON, JUnit | Screenshots |
| Parallelization | Built-in | Manual |
| Authentication | Need to handle | Uses user's session (Chrome) |
