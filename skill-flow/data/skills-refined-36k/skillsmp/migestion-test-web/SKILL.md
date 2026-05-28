---
name: migestion-test-web
description: >
  Web E2E testing patterns for MiGestion - Playwright, page objects.
  Trigger: When writing or running E2E tests.
license: MIT
metadata:
  author: migestion
  version: '1.0'
  scope: [web]
  auto_invoke: 'Writing E2E tests'
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Test Structure

```
e2e/
├── pages/
│   ├── login-page.ts      # Page objects
│   ├── clients-page.ts
│   └── dashboard-page.ts
├── fixtures/              # Test data
└── *.spec.ts              # Test files
```

## Page Object Pattern

```typescript
// e2e/pages/login-page.ts
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
    await this.page.waitForURL('/dashboard');
  }

  async getErrorMessage() {
    return await this.page.textContent('.alert-error');
  }
}
```

## Test Example

```typescript
// e2e/auth.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/login-page';
import { DashboardPage } from './pages/dashboard-page';

test.describe('Authentication', () => {
  test('should login successfully', async ({ page }) => {
    const loginPage = new LoginPage(page);
    const dashboardPage = new DashboardPage(page);

    await loginPage.goto();
    await loginPage.login('admin@example.com', 'password123');

    await expect(page).toHaveURL('/dashboard');
    await expect(dashboardPage.page.getByText('Dashboard')).toBeVisible();
  });

  test('should show error with invalid credentials', async ({ page }) => {
    const loginPage = new LoginPage(page);

    await loginPage.goto();
    await loginPage.login('invalid@example.com', 'wrongpassword');

    const error = await loginPage.getErrorMessage();
    expect(error).toContain('Invalid credentials');
  });
});
```

## CRUD Operations Test

```typescript
// e2e/clients.spec.ts
import { test, expect } from '@playwright/test';
import { ClientsPage } from './pages/clients-page';

test.describe('Client Management', () => {
  test.beforeEach(async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.login('admin@example.com', 'password123');
  });

  test('should create new client', async ({ page }) => {
    const clientsPage = new ClientsPage(page);

    await clientsPage.goto();
    await clientsPage.clickNewClientButton();

    await page.fill('[name="companyName"]', 'Test Company');
    await page.fill('[name="contactName"]', 'John Doe');
    await page.fill('[name="email"]', 'john@test.com');
    await page.click('button[type="submit"]');

    await expect(page.getByText('Client created successfully')).toBeVisible();
    await expect(page.getByText('Test Company')).toBeVisible();
  });

  test('should filter clients by status', async ({ page }) => {
    const clientsPage = new ClientsPage(page);

    await clientsPage.goto();
    await clientsPage.filterByStatus('active');

    const rows = await clientsPage.getClientRows();
    for (const row of rows) {
      const status = await row.getByTestId('client-status').textContent();
      expect(status).toBe('Active');
    }
  });
});
```

## Form Testing

```typescript
test('should validate required fields', async ({ page }) => {
  await page.goto('/clients/new');
  await page.click('button[type="submit"]');

  await expect(page.getByText('Company name is required')).toBeVisible();
  await expect(page.getByText('Contact name is required')).toBeVisible();
});
```

## Pagination Test

```typescript
test('should paginate through results', async ({ page }) => {
  const clientsPage = new ClientsPage(page);
  await clientsPage.goto();

  const currentPage = await clientsPage.getCurrentPage();
  expect(currentPage).toBe(1);

  await clientsPage.clickNextPage();
  const nextPage = await clientsPage.getCurrentPage();
  expect(nextPage).toBe(2);
});
```

## API Interception

```typescript
test('should show loading state during API call', async ({ page }) => {
  await page.route('**/api/clients', async route => {
    await new Promise(resolve => setTimeout(resolve, 1000));
    await route.continue();
  });

  const clientsPage = new ClientsPage(page);
  await clientsPage.goto();

  await expect(page.getByTestId('spinner')).toBeVisible();
  await expect(page.getByTestId('spinner')).not.toBeVisible();
});
```

## Search Test

```typescript
test('should search clients', async ({ page }) => {
  const clientsPage = new ClientsPage(page);
  await clientsPage.goto();

  await clientsPage.search('Test Company');

  await expect(page.getByText('Test Company')).toBeVisible();
});
```

## Navigation Test

```typescript
test('should navigate between pages', async ({ page }) => {
  await page.goto('/dashboard');

  await page.click('text=Clients');
  await expect(page).toHaveURL('/clients');

  await page.click('text=Reports');
  await expect(page).toHaveURL('/reports');
});
```

## Mobile Responsive Test

```typescript
test.use({ viewport: { width: 375, height: 667 } }); // Mobile

test('should work on mobile', async ({ page }) => {
  const clientsPage = new ClientsPage(page);
  await clientsPage.goto();

  await expect(page.getByTestId('mobile-menu-button')).toBeVisible();
});
```

## Test Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
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
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],

  webServer: {
    command: 'npm run dev:web',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
});
```

## Commands

```bash
npm run test:e2e                  # Run all E2E tests
npm run test:e2e -- --ui          # Run with UI
npm run test:e2e -- --debug       # Debug mode
npm run test:e2e -- --headed      # Run with browser visible
npm run test:e2e -- auth.spec.ts  # Run specific test file
```

## Related Skills

- `playwright` - General Playwright patterns
- `migestion-web` - Web component patterns being tested
