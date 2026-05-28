# Fixtures Examples

Setting up fixtures with createBdd and TEST_USERS.

## Extended Fixtures with Multiple POMs

```typescript
// steps/fixtures.ts
import { test as base, createBdd } from 'playwright-bdd';
import { expect } from '@playwright/test';
import { LoginPage } from '../page-objects/login.page';
import { DashboardPage } from '../page-objects/dashboard.page';

export const TEST_USERS = {
  valid: { email: 'user@example.com', password: 'password123', name: 'Test User' },
  invalid: { email: 'wrong@example.com', password: 'badpass' },
  admin: { email: 'admin@example.com', password: 'admin123', name: 'Admin User' },
};

type Fixtures = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
  ctx: Record<string, unknown>;
};

export const test = base.extend<Fixtures>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },
  dashboardPage: async ({ page }, use) => {
    await use(new DashboardPage(page));
  },
  ctx: async ({}, use) => {
    await use({});
  },
});

export const { Given, When, Then, Before, After, BeforeAll, AfterAll } = createBdd(test);
export { TEST_USERS };
```

## Hooks

```typescript
import { Before, After, BeforeAll, AfterAll } from './fixtures';

// Runs once per worker (browser instance)
BeforeAll(async ({ browser }) => {
  console.log(`Worker started: ${browser.browserType().name()}`);
});

// Runs before each scenario
Before(async ({ page }) => {
  // Clear cookies/storage if needed
  await page.context().clearCookies();
});

// Conditional hook - only for @auth tagged scenarios
Before({ tags: '@auth' }, async ({ page }) => {
  // Pre-authenticate or setup auth state
});

// Runs after each scenario
After(async ({ page, $testInfo }) => {
  if ($testInfo.status === 'failed') {
    const screenshotPath = `screenshots/${$testInfo.title.replace(/\s+/g, '-')}.png`;
    await page.screenshot({ path: screenshotPath });
  }
});

// Cleanup after worker finishes
AfterAll(async () => {
  console.log('Worker cleanup complete');
});
```
