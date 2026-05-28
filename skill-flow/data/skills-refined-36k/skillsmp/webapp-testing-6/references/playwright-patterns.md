# Playwright Testing Patterns for LucidData

Comprehensive guide to end-to-end testing patterns using Playwright 1.57.0 in the LucidData project.

## Table of Contents

1. [Page Object Model](#page-object-model)
2. [Authentication Helper](#authentication-helper)
3. [Common Selectors](#common-selectors)
4. [Screenshot and Video Capture](#screenshot-and-video-capture)
5. [Network Interception](#network-interception)
6. [Multi-Browser Configuration](#multi-browser-configuration)
7. [Mobile Testing](#mobile-testing)
8. [Best Practices](#best-practices)

## Page Object Model

The Page Object Model (POM) encapsulates page-specific selectors and actions, making tests more maintainable.

### Example: Vault Page Object

```typescript
// __tests__/e2e/pages/vault.page.ts
import { Page, Locator } from '@playwright/test';

export class VaultPage {
  readonly page: Page;
  readonly createButton: Locator;
  readonly labelInput: Locator;
  readonly categorySelect: Locator;
  readonly metadataInput: Locator;
  readonly saveButton: Locator;
  readonly vaultList: Locator;

  constructor(page: Page) {
    this.page = page;
    this.createButton = page.getByRole('button', { name: 'Create Entry' });
    this.labelInput = page.getByLabel('Label');
    this.categorySelect = page.getByLabel('Category');
    this.metadataInput = page.getByLabel('Metadata (JSON)');
    this.saveButton = page.getByRole('button', { name: 'Save' });
    this.vaultList = page.locator('[data-testid="vault-list"]');
  }

  async goto() {
    await this.page.goto('/dashboard/vault');
  }

  async createEntry(label: string, category: string, metadata: object) {
    await this.createButton.click();
    await this.labelInput.fill(label);
    await this.categorySelect.selectOption(category);
    await this.metadataInput.fill(JSON.stringify(metadata));
    await this.saveButton.click();
  }

  async getEntryByLabel(label: string) {
    return this.vaultList.locator(`text=${label}`);
  }

  async deleteEntry(label: string) {
    const entry = await this.getEntryByLabel(label);
    await entry.locator('button[aria-label="Delete"]').click();
    await this.page.getByRole('button', { name: 'Confirm' }).click();
  }
}
```

### Using the Page Object

```typescript
// __tests__/e2e/vault/crud.spec.ts
import { test, expect } from '@playwright/test';
import { VaultPage } from '../pages/vault.page';
import { login } from '../helpers/auth';

test.describe('Vault CRUD Operations', () => {
  let vaultPage: VaultPage;

  test.beforeEach(async ({ page }) => {
    await login(page);
    vaultPage = new VaultPage(page);
    await vaultPage.goto();
  });

  test('should create vault entry', async () => {
    await vaultPage.createEntry('Test Entry', 'Identity', { key: 'value' });
    await expect(vaultPage.getEntryByLabel('Test Entry')).toBeVisible();
  });
});
```

## Authentication Helper

LucidData provides auth helpers in `__tests__/e2e/helpers/auth.ts`:

```typescript
import { Page } from '@playwright/test';

export const TEST_USER = {
  email: 'test@lucid.dev',
  password: 'TestPassword123!',
};

export async function login(page: Page, email?: string, password?: string) {
  await page.goto('/login');
  await page.fill('input[name="email"]', email || TEST_USER.email);
  await page.fill('input[name="password"]', password || TEST_USER.password);
  await page.click('button[type="submit"]');
  await page.waitForURL('/dashboard', { timeout: 10000 });
}

export async function signup(page: Page, email?: string, password?: string) {
  const userEmail = email || getUniqueEmail();
  await page.goto('/signup');
  await page.fill('input[name="email"]', userEmail);
  await page.fill('input[name="password"]', password || TEST_USER.password);
  await page.click('button[type="submit"]');
  await page.waitForURL('/dashboard', { timeout: 10000 });
  return userEmail;
}

export async function logout(page: Page) {
  await page.click('button[aria-label="Sign Out"]');
  await page.waitForURL('/', { timeout: 5000 });
}

export async function isAuthenticated(page: Page): Promise<boolean> {
  const url = page.url();
  return url.includes('/dashboard');
}

export function getUniqueEmail(): string {
  const timestamp = Date.now();
  const random = Math.floor(Math.random() * 1000);
  return `test-${timestamp}-${random}@lucid.dev`;
}

export async function clearSession(page: Page) {
  await page.context().clearCookies();
  await page.evaluate(() => localStorage.clear());
  await page.evaluate(() => sessionStorage.clear());
}
```

### Usage in Tests

```typescript
test.beforeEach(async ({ page }) => {
  await clearSession(page);
  await login(page);
});

test('protected route requires authentication', async ({ page }) => {
  await clearSession(page);
  await page.goto('/dashboard');
  await expect(page).toHaveURL('/login');
});
```

## Common Selectors

### Selector Strategies (in order of preference)

1. **By Role** (most semantic, accessible):
   ```typescript
   await page.getByRole('button', { name: 'Save' });
   await page.getByRole('textbox', { name: 'Email' });
   await page.getByRole('link', { name: 'Dashboard' });
   ```

2. **By Label** (good for form fields):
   ```typescript
   await page.getByLabel('Password');
   await page.getByLabel('Category');
   ```

3. **By Placeholder**:
   ```typescript
   await page.getByPlaceholder('Enter your email');
   ```

4. **By Text** (for unique text content):
   ```typescript
   await page.getByText('Welcome to Lucid');
   await page.getByText(/created successfully/i);
   ```

5. **By Test ID** (last resort):
   ```typescript
   await page.getByTestId('vault-list');
   ```

6. **CSS Selectors** (only when necessary):
   ```typescript
   await page.locator('input[name="email"]');
   await page.locator('.vault-card:first-child');
   ```

### LucidData-Specific Selectors

```typescript
// shadcn/ui Button variants
await page.getByRole('button', { name: 'Delete' }); // destructive variant
await page.getByRole('button', { name: 'Cancel' }); // outline variant

// shadcn/ui Dialog
await page.locator('[role="dialog"]');
await page.locator('[role="dialog"] >> text=Edit Vault Entry');

// shadcn/ui Select
await page.locator('[role="combobox"]').click();
await page.getByRole('option', { name: 'Identity' }).click();

// shadcn/ui Toast notifications
await expect(page.locator('[role="status"]')).toContainText('Success');

// Table rows
await page.locator('table tbody tr').count();
await page.locator('table >> text=John Doe');
```

## Screenshot and Video Capture

### Automatic Capture (configured in playwright.config.ts)

Screenshots and videos are automatically captured on test failures:
- Screenshots: `test-results/<test-name>/test-failed-1.png`
- Videos: `test-results/<test-name>/video.webm`
- Traces: `test-results/<test-name>/trace.zip`

### Manual Screenshots

```typescript
test('should capture screenshot', async ({ page }) => {
  await page.goto('/dashboard');

  // Full page screenshot
  await page.screenshot({ path: 'dashboard.png', fullPage: true });

  // Specific element screenshot
  const element = page.locator('.vault-card');
  await element.screenshot({ path: 'vault-card.png' });

  // Screenshot in test artifacts
  await page.screenshot({ path: test.info().outputPath('custom-screenshot.png') });
});
```

### Screenshots for Visual Regression (future)

```typescript
test('should match visual snapshot', async ({ page }) => {
  await page.goto('/dashboard');
  await expect(page).toHaveScreenshot('dashboard.png', {
    maxDiffPixels: 100,
  });
});
```

## Network Interception

### Wait for API Responses

```typescript
test('should wait for API call', async ({ page }) => {
  // Wait for specific API endpoint
  const responsePromise = page.waitForResponse(
    (response) => response.url().includes('/api/vault') && response.status() === 200
  );

  await page.click('button:has-text("Create Entry")');

  const response = await responsePromise;
  const data = await response.json();
  expect(data.success).toBe(true);
});
```

### Mock API Responses (future enhancement)

```typescript
test('should handle API error', async ({ page }) => {
  await page.route('/api/vault', (route) => {
    route.fulfill({
      status: 500,
      contentType: 'application/json',
      body: JSON.stringify({ error: 'Internal Server Error' }),
    });
  });

  await page.goto('/dashboard/vault');
  await expect(page.getByText('Error loading vault data')).toBeVisible();
});
```

## Multi-Browser Configuration

LucidData tests run across 5 browser projects (configured in `playwright.config.ts`):

1. **Chromium** (Chrome, Edge)
2. **Firefox**
3. **WebKit** (Safari)
4. **Mobile Chrome** (Pixel 5, 393×851)
5. **Mobile Safari** (iPhone 12, 390×844)

### Running Specific Browsers

```bash
# Run only Chromium tests
npx playwright test --project=chromium

# Run only mobile tests
npx playwright test --project="Mobile Chrome" --project="Mobile Safari"

# Run on all browsers (default)
npx playwright test
```

### Browser-Specific Tests

```typescript
test('should work on mobile', async ({ page, browserName }) => {
  test.skip(browserName !== 'webkit', 'Mobile Safari specific test');

  // Mobile-specific assertions
  await page.setViewportSize({ width: 390, height: 844 });
  await expect(page.locator('.mobile-menu')).toBeVisible();
});
```

## Mobile Testing

### Viewport Sizes

```typescript
test.describe('Mobile Responsive', () => {
  test.use({ viewport: { width: 375, height: 667 } }); // iPhone SE

  test('should display mobile navigation', async ({ page }) => {
    await page.goto('/dashboard');
    await expect(page.locator('[aria-label="Mobile menu"]')).toBeVisible();
  });
});
```

### Touch Interactions

```typescript
test('should handle touch gestures', async ({ page }) => {
  await page.goto('/dashboard');

  // Tap (equivalent to click on mobile)
  await page.tap('button:has-text("Menu")');

  // Swipe
  await page.locator('.swipeable-element').swipe({ x: -100, y: 0 });
});
```

### Device Emulation

```typescript
import { devices } from '@playwright/test';

test.use(devices['iPhone 12']);

test('should work on iPhone 12', async ({ page }) => {
  // Test runs with iPhone 12 user agent, viewport, and device pixel ratio
});
```

## Best Practices

### 1. Use Explicit Waits

```typescript
// Good: Wait for element to be visible
await expect(page.getByText('Success')).toBeVisible();

// Bad: Fixed timeout
await page.waitForTimeout(3000);
```

### 2. Avoid Flaky Selectors

```typescript
// Good: Semantic selector
await page.getByRole('button', { name: 'Save' });

// Bad: Position-dependent selector
await page.locator('button:nth-child(3)');
```

### 3. Test User Journeys, Not Implementation

```typescript
// Good: User perspective
test('should create and view vault entry', async ({ page }) => {
  await vaultPage.createEntry('My Data', 'Identity', {});
  await vaultPage.viewEntry('My Data');
  await expect(page.getByText('Identity')).toBeVisible();
});

// Bad: Testing implementation details
test('should call createVault API', async ({ page }) => {
  // Testing API internals instead of user outcomes
});
```

### 4. Clean Up Test Data

```typescript
test.afterEach(async ({ page }) => {
  // Delete test entries created during test
  await vaultPage.deleteAllTestEntries();
});
```

### 5. Parallelize Independent Tests

```typescript
test.describe.configure({ mode: 'parallel' });

test('test 1', async ({ page }) => { /* ... */ });
test('test 2', async ({ page }) => { /* ... */ });
test('test 3', async ({ page }) => { /* ... */ });
```

### 6. Use Test Fixtures for Common Setup

```typescript
// __tests__/e2e/fixtures/authenticated.ts
import { test as base } from '@playwright/test';
import { login } from '../helpers/auth';

export const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    await login(page);
    await use(page);
  },
});

// Usage
test('should access protected route', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('/dashboard/vault');
  // Already logged in
});
```

### 7. Handle Dialogs and Alerts

```typescript
test('should confirm deletion', async ({ page }) => {
  // Listen for dialog before triggering it
  page.once('dialog', async (dialog) => {
    expect(dialog.message()).toContain('Are you sure');
    await dialog.accept();
  });

  await page.click('button:has-text("Delete")');
});
```

### 8. Debug with Trace Viewer

When a test fails, view the trace:

```bash
npx playwright show-trace test-results/<test-name>/trace.zip
```

The trace viewer shows:
- Timeline of actions
- Screenshots at each step
- Network requests
- Console logs
- Source code

### 9. Use Soft Assertions for Multiple Checks

```typescript
test('should validate form fields', async ({ page }) => {
  await expect.soft(page.getByLabel('Email')).toBeVisible();
  await expect.soft(page.getByLabel('Password')).toBeVisible();
  await expect.soft(page.getByRole('button', { name: 'Submit' })).toBeEnabled();
  // All assertions run even if one fails
});
```

### 10. Test Error States

```typescript
test('should display validation error', async ({ page }) => {
  await page.goto('/signup');
  await page.fill('input[name="email"]', 'invalid-email');
  await page.click('button[type="submit"]');

  await expect(page.getByText('Invalid email address')).toBeVisible();
});
```

## LucidData E2E Test Checklist

- [ ] Test runs in multiple browsers (Chromium, Firefox, WebKit)
- [ ] Test works on mobile viewports (375px, 390px)
- [ ] Authentication state is properly managed (login/logout)
- [ ] Test data is cleaned up after test
- [ ] Waits for async operations (API calls, navigation)
- [ ] Uses semantic selectors (role, label, text)
- [ ] Tests user outcomes, not implementation
- [ ] Handles error states and edge cases
- [ ] Screenshots are captured on failure
- [ ] Test is deterministic (passes consistently)

---

**For more information:**
- [Playwright Documentation](https://playwright.dev)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [LucidData Test Data Reference](test-data.md)
