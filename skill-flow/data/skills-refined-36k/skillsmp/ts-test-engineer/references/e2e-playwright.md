# Playwright E2E Testing Reference

End-to-end testing patterns for Next.js applications.

## Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [['html', { open: 'never' }]],
  use: {
    baseURL: 'http://localhost:3000',
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
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

## Basic Test Structure

```typescript
import { test, expect } from '@playwright/test';

test.describe('Home Page', () => {
  test('should display welcome message', async ({ page }) => {
    await page.goto('/');

    await expect(page.getByRole('heading', { name: /welcome/i })).toBeVisible();
  });

  test('should navigate to about page', async ({ page }) => {
    await page.goto('/');

    await page.click('a[href="/about"]');

    await expect(page).toHaveURL('/about');
    await expect(page.getByRole('heading', { name: /about/i })).toBeVisible();
  });
});
```

## Authentication Setup

```typescript
// e2e/auth.setup.ts
import { test as setup, expect } from '@playwright/test';

const authFile = 'playwright/.auth/user.json';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');

  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('button[type="submit"]');

  // Wait for successful login
  await expect(page).toHaveURL('/dashboard');

  // Save authentication state
  await page.context().storageState({ path: authFile });
});

// playwright.config.ts
export default defineConfig({
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },
  ],
});
```

## Using Authenticated State

```typescript
// e2e/dashboard.spec.ts
import { test, expect } from '@playwright/test';

// Uses pre-authenticated state from setup
test('should show dashboard for authenticated user', async ({ page }) => {
  await page.goto('/dashboard');

  await expect(page.getByText('Welcome back')).toBeVisible();
  await expect(page.getByRole('navigation')).toContainText('Logout');
});
```

## Page Object Model

```typescript
// e2e/pages/login.page.ts
import { Page, Locator, expect } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: /sign in/i });
    this.errorMessage = page.getByRole('alert');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toContainText(message);
  }
}

// e2e/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/login.page';

test('should show error for invalid credentials', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();

  await loginPage.login('invalid@example.com', 'wrongpassword');

  await loginPage.expectError('Invalid credentials');
});
```

## Form Testing

```typescript
test('should submit contact form', async ({ page }) => {
  await page.goto('/contact');

  await page.getByLabel('Name').fill('John Doe');
  await page.getByLabel('Email').fill('john@example.com');
  await page.getByLabel('Message').fill('Hello, this is a test message.');

  await page.getByRole('button', { name: /send/i }).click();

  // Wait for success message
  await expect(page.getByText('Message sent successfully')).toBeVisible();
});

test('should validate required fields', async ({ page }) => {
  await page.goto('/contact');

  await page.getByRole('button', { name: /send/i }).click();

  await expect(page.getByText('Name is required')).toBeVisible();
  await expect(page.getByText('Email is required')).toBeVisible();
});
```

## API Mocking

```typescript
import { test, expect } from '@playwright/test';

test('should display mocked data', async ({ page }) => {
  // Mock API response
  await page.route('/api/users', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { id: '1', name: 'Mock User 1' },
        { id: '2', name: 'Mock User 2' },
      ]),
    });
  });

  await page.goto('/users');

  await expect(page.getByText('Mock User 1')).toBeVisible();
  await expect(page.getByText('Mock User 2')).toBeVisible();
});

test('should handle API errors gracefully', async ({ page }) => {
  await page.route('/api/users', async (route) => {
    await route.fulfill({
      status: 500,
      body: JSON.stringify({ error: 'Server error' }),
    });
  });

  await page.goto('/users');

  await expect(page.getByRole('alert')).toContainText('Failed to load users');
});
```

## Visual Regression Testing

```typescript
test('should match homepage snapshot', async ({ page }) => {
  await page.goto('/');

  // Full page screenshot
  await expect(page).toHaveScreenshot('homepage.png');
});

test('should match component snapshot', async ({ page }) => {
  await page.goto('/components');

  const card = page.locator('.product-card').first();
  await expect(card).toHaveScreenshot('product-card.png');
});

// With threshold for minor differences
test('should match with threshold', async ({ page }) => {
  await page.goto('/');

  await expect(page).toHaveScreenshot('homepage.png', {
    maxDiffPixelRatio: 0.1,
  });
});
```

## Testing File Uploads

```typescript
test('should upload file', async ({ page }) => {
  await page.goto('/upload');

  const fileInput = page.locator('input[type="file"]');
  await fileInput.setInputFiles({
    name: 'test.txt',
    mimeType: 'text/plain',
    buffer: Buffer.from('Test file content'),
  });

  await page.getByRole('button', { name: /upload/i }).click();

  await expect(page.getByText('File uploaded successfully')).toBeVisible();
});
```

## Testing Modals and Dialogs

```typescript
test('should open and close modal', async ({ page }) => {
  await page.goto('/products');

  await page.click('[data-testid="open-modal"]');

  const modal = page.getByRole('dialog');
  await expect(modal).toBeVisible();
  await expect(modal.getByRole('heading')).toHaveText('Product Details');

  await modal.getByRole('button', { name: /close/i }).click();
  await expect(modal).not.toBeVisible();
});

// Confirm dialog
test('should confirm delete action', async ({ page }) => {
  await page.goto('/items/1');

  page.on('dialog', async (dialog) => {
    expect(dialog.message()).toContain('Are you sure');
    await dialog.accept();
  });

  await page.click('[data-testid="delete-button"]');

  await expect(page.getByText('Item deleted')).toBeVisible();
});
```

## Mobile Testing

```typescript
import { test, expect, devices } from '@playwright/test';

test.use({ ...devices['iPhone 13'] });

test('should show mobile menu', async ({ page }) => {
  await page.goto('/');

  // Desktop nav should be hidden
  await expect(page.locator('nav.desktop')).not.toBeVisible();

  // Mobile menu button should be visible
  const menuButton = page.getByRole('button', { name: /menu/i });
  await expect(menuButton).toBeVisible();

  await menuButton.click();

  await expect(page.getByRole('navigation')).toBeVisible();
});
```

## Accessibility Testing

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('should have no accessibility violations', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page }).analyze();

  expect(results.violations).toEqual([]);
});

test('should have no accessibility violations on form', async ({ page }) => {
  await page.goto('/contact');

  const results = await new AxeBuilder({ page })
    .include('form')
    .analyze();

  expect(results.violations).toEqual([]);
});
```

## Test Hooks

```typescript
import { test, expect } from '@playwright/test';

test.beforeAll(async () => {
  // Runs once before all tests
  console.log('Setting up test suite');
});

test.beforeEach(async ({ page }) => {
  // Runs before each test
  await page.goto('/');
});

test.afterEach(async ({ page }, testInfo) => {
  // Capture screenshot on failure
  if (testInfo.status !== 'passed') {
    await page.screenshot({
      path: `screenshots/${testInfo.title}.png`,
    });
  }
});

test.afterAll(async () => {
  // Cleanup after all tests
  console.log('Cleaning up test suite');
});
```

## Execution Commands

```bash
# Run all E2E tests
npx playwright test

# Run specific test file
npx playwright test e2e/login.spec.ts

# Run with UI mode (great for debugging)
npx playwright test --ui

# Run headed (see browser)
npx playwright test --headed

# Run specific project (browser)
npx playwright test --project=chromium

# Debug mode
npx playwright test --debug

# Generate report
npx playwright show-report

# Update snapshots
npx playwright test --update-snapshots
```
