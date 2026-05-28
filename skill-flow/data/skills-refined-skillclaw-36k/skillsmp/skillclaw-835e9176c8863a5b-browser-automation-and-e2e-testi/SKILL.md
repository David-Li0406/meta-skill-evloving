---
name: browser-automation-and-e2e-testing
description: Use this skill for writing browser-based tests using Playwright for end-to-end testing, visual regression, and validating user workflows.
---

# Skill body

## When to Use This Skill

Use when:
- Writing end-to-end tests
- Testing user workflows
- Validating cross-browser compatibility
- Implementing visual regression tests
- Debugging browser interactions

## Playwright Setup

### Installation

```bash
pnpm add -D @playwright/test
npx playwright install
```

### Configuration

Create a `playwright.config.ts` file with the following content:

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  timeout: 30000,
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
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'mobile', use: { ...devices['iPhone 13'] } },
  ],

  webServer: {
    command: 'pnpm dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
});
```

## Test Patterns

### Basic Page Test

```typescript
import { test, expect } from '@playwright/test';

test('homepage loads correctly', async ({ page }) => {
  await page.goto('/');

  await expect(page).toHaveTitle(/My App/);
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
});
```

### User Flow Test

```typescript
test('user can upload and process files', async ({ page }) => {
  await page.goto('/');

  // Upload file
  const fileInput = page.locator('input[type="file"]');
  await fileInput.setInputFiles('./test-files/sample.txt');

  // Wait for processing
  await expect(page.getByText('Processing...')).toBeVisible();
  await expect(page.getByText('Processing...')).not.toBeVisible();

  // Verify result
  await expect(page.getByTestId('file-tree')).toContainText('sample.txt');
});
```

### Form Interaction

```typescript
test('form submission works', async ({ page }) => {
  await page.goto('/settings');

  // Fill form
  await page.getByLabel('Max file size').fill('64');
  await page.getByLabel('Remove empty lines').check();

  // Submit
  await page.getByRole('button', { name: 'Save' }).click();
});
```

## Critical Guidelines

### E2E Testing Requirements

- **No Mocking in E2E Tests**: Always test against real backend services to avoid false confidence in tests.
- **Pre-Flight Health Check**: Ensure backend and frontend endpoints are responsive before running tests.

### Timeout Configuration

| Timeout Type      | Local (M3 Max) | CI   |
|-------------------|----------------|------|
| Test timeout      | 5s             | 30s  |
| Action timeout    | 2s             | 10s  |
| Navigation timeout | 3s             | 15s  |
| Expect timeout    | 2s             | 10s  |
| Global timeout    | 2 min          | 10 min |

Tests will fail fast if services are down, and global setup verifies services before tests run.