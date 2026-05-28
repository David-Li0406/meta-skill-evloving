---
name: playwright
description: >
  Playwright E2E testing patterns and best practices.
  Trigger: When writing or running E2E tests.
license: MIT
metadata:
  author: migestion
  version: '1.0'
  scope: [web]
  auto_invoke: 'Writing E2E tests'
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Page Object Pattern (REQUIRED)

```typescript
// pages/login-page.ts
export class LoginPage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.fill('[name="email"]', email);
    await this.page.fill('[name="password"]', password);
    await this.page.click('button[type="submit"]');
  }
}
```

## Selectors

```typescript
// ✅ Prefer accessible selectors
page.getByRole('button', { name: 'Submit' });
page.getByText('Welcome');
page.getByLabel('Email');
page.getByPlaceholder('Enter email');

// ✅ Test ID (when no semantic option)
page.getByTestId('submit-button');

// ✅ CSS selector (as fallback)
page.locator('button[type="submit"]');
```

## Actions

```typescript
// ✅ Fill input
await page.fill('[name="email"]', 'test@example.com');

// ✅ Click
await page.click('button[type="submit"]');

// ✅ Select
await page.selectOption('[name="status"]', 'active');

// ✅ Check/uncheck
await page.check('[name="remember"]');
await page.uncheck('[name="remember"]');

// ✅ Type
await page.type('input', 'text', { delay: 100 });
```

## Assertions

```typescript
// ✅ Page URL
await expect(page).toHaveURL('/dashboard');

// ✅ Element visible
await expect(page.getByText('Welcome')).toBeVisible();

// ✅ Element hidden
await expect(page.getByTestId('modal')).toBeHidden();

// ✅ Text content
await expect(page.getByTestId('title')).toHaveText('Dashboard');

// ✅ Attribute
await expect(page.getByRole('button')).toHaveAttribute('disabled');

// ✅ Element count
await expect(page.locator('table tr')).toHaveCount(10);
```

## Waits

```typescript
// ✅ Wait for navigation
await page.waitForURL('/dashboard');

// ✅ Wait for element
await page.waitForSelector('[data-testid="loaded"]');

// ✅ Wait for load state
await page.waitForLoadState('networkidle');

// ✅ Wait for timeout (avoid!)
await page.waitForTimeout(1000); // Only when necessary
```

## Forms

```typescript
test('should submit form', async ({ page }) => {
  await page.goto('/form');

  await page.fill('[name="name"]', 'John Doe');
  await page.fill('[name="email"]', 'john@example.com');
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL('/success');
});
```

## Tables

```typescript
test('should render table rows', async ({ page }) => {
  await page.goto('/clients');

  const rows = await page.locator('table tbody tr');
  await expect(rows).toHaveCount(10);

  const firstRow = rows.first();
  await expect(firstRow.getByText('Client 1')).toBeVisible();
});
```

## API Mocking

```typescript
test('should handle API response', async ({ page }) => {
  await page.route('**/api/clients', async route => {
    await route.fulfill({
      status: 200,
      body: JSON.stringify({ clients: [], total: 0 }),
    });
  });

  await page.goto('/clients');
});
```

## File Upload

```typescript
test('should upload file', async ({ page }) => {
  await page.goto('/upload');

  const fileInput = page.locator('input[type="file"]');
  await fileInput.setInputFiles('path/to/file.txt');

  await page.click('button[type="submit"]');
});
```

## Screenshot on Failure

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    screenshot: 'only-on-failure',
  },
});
```

## Test Configuration

```typescript
// playwright.config.ts
export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
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
  ],
});
```

## Commands

```bash
npm run test:e2e              # Run all E2E tests
npm run test:e2e -- --ui      # Run with UI
npm run test:e2e -- --debug   # Debug mode
npm run test:e2e -- --headed  # Run with browser visible
```

## Related Skills

- `migestion-test-web` - MiGestion E2E testing patterns
