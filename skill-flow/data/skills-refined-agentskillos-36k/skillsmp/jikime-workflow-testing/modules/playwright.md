# Playwright E2E Testing

Next.js 프로젝트를 위한 Playwright E2E 테스팅 패턴.

## Setup

### Installation

```bash
npm install -D @playwright/test
npx playwright install
```

### playwright.config.ts

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
    baseURL: 'http://localhost:3000',
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
      name: 'mobile',
      use: { ...devices['iPhone 14'] },
    },
  ],

  webServer: {
    command: 'npm run build && npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

---

## Test Patterns

### Basic Navigation

```typescript
// e2e/navigation.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Navigation', () => {
  test('should navigate to about page', async ({ page }) => {
    await page.goto('/');
    await page.click('text=About');
    await expect(page).toHaveURL('/about');
    await expect(page.locator('h1')).toContainText('About Us');
  });
});
```

### Form Submission

```typescript
// e2e/login.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Login', () => {
  test('successful login redirects to dashboard', async ({ page }) => {
    await page.goto('/login');

    // Fill form
    await page.fill('[name="email"]', 'user@example.com');
    await page.fill('[name="password"]', 'password123');

    // Submit
    await page.click('button[type="submit"]');

    // Verify redirect
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('[data-testid="welcome"]')).toContainText('Welcome');
  });

  test('shows error for invalid credentials', async ({ page }) => {
    await page.goto('/login');

    await page.fill('[name="email"]', 'wrong@example.com');
    await page.fill('[name="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');

    await expect(page.locator('[role="alert"]')).toContainText('Invalid credentials');
  });
});
```

### API Mocking

```typescript
// e2e/users.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Users Page', () => {
  test.beforeEach(async ({ page }) => {
    // Mock API response
    await page.route('**/api/users', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          { id: 1, name: 'John Doe' },
          { id: 2, name: 'Jane Smith' },
        ]),
      });
    });
  });

  test('displays user list', async ({ page }) => {
    await page.goto('/users');

    await expect(page.locator('text=John Doe')).toBeVisible();
    await expect(page.locator('text=Jane Smith')).toBeVisible();
  });
});
```

---

## Authentication

### Auth State Fixture

```typescript
// e2e/fixtures/auth.ts
import { test as base, expect } from '@playwright/test';

type AuthFixtures = {
  authenticatedPage: Page;
};

export const test = base.extend<AuthFixtures>({
  authenticatedPage: async ({ page }, use) => {
    // Login
    await page.goto('/login');
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    await page.waitForURL('/dashboard');

    await use(page);
  },
});

export { expect };
```

### Using Auth Fixture

```typescript
// e2e/dashboard.spec.ts
import { test, expect } from './fixtures/auth';

test('authenticated user sees dashboard', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('/dashboard');
  await expect(authenticatedPage.locator('h1')).toContainText('Dashboard');
});
```

### Storage State (Session Reuse)

```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    // Setup project - runs first
    { name: 'setup', testMatch: /.*\.setup\.ts/ },

    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        storageState: '.playwright/auth.json',
      },
      dependencies: ['setup'],
    },
  ],
});

// e2e/auth.setup.ts
import { test as setup } from '@playwright/test';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('button[type="submit"]');
  await page.waitForURL('/dashboard');

  // Save auth state
  await page.context().storageState({ path: '.playwright/auth.json' });
});
```

---

## Visual Testing

### Screenshot Comparison

```typescript
test('homepage visual', async ({ page }) => {
  await page.goto('/');

  // Full page screenshot
  await expect(page).toHaveScreenshot('homepage.png', {
    fullPage: true,
  });
});

test('component visual', async ({ page }) => {
  await page.goto('/components');

  // Element screenshot
  const card = page.locator('[data-testid="feature-card"]');
  await expect(card).toHaveScreenshot('feature-card.png');
});
```

### Update Snapshots

```bash
# Update all snapshots
npx playwright test --update-snapshots

# Update specific test
npx playwright test homepage.spec.ts --update-snapshots
```

---

## Best Practices

### Use Test IDs

```typescript
// Component
<button data-testid="submit-btn">Submit</button>

// Test
await page.click('[data-testid="submit-btn"]');
```

### Wait for Network

```typescript
// Wait for specific API
await Promise.all([
  page.waitForResponse('**/api/users'),
  page.click('button'),
]);

// Wait for all network idle
await page.waitForLoadState('networkidle');
```

### Retry Flaky Assertions

```typescript
// Auto-retry with expect
await expect(async () => {
  const response = await page.request.get('/api/status');
  expect(response.status()).toBe(200);
}).toPass({
  timeout: 10000,
});
```

### Parallel Test Isolation

```typescript
// Each test gets fresh context
test.describe.configure({ mode: 'parallel' });

test('test 1', async ({ page }) => {
  // Fresh browser context
});

test('test 2', async ({ page }) => {
  // Another fresh browser context
});
```

---

## Debugging

### UI Mode

```bash
npx playwright test --ui
```

### Debug Mode

```bash
npx playwright test --debug
```

### Trace Viewer

```bash
# Enable trace
npx playwright test --trace on

# View trace
npx playwright show-trace trace.zip
```

### Codegen (Record Tests)

```bash
npx playwright codegen localhost:3000
```
