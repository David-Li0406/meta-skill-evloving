---
name: Webapp Testing
description: Test web applications with Playwright for UI verification and debugging
version: 1.0.0
source: Adapted from anthropics/skills
---

# Webapp Testing with Playwright

## Purpose

Test local web applications using Playwright for:
- UI verification and visual regression
- User flow testing
- Accessibility compliance
- Cross-browser compatibility
- Debug UI behavior with screenshots/traces

## FrankX Project Setup

The project already has Playwright configured:

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
});
```

## Test Structure

```
tests/
├── e2e/
│   ├── homepage.spec.ts      # Landing page tests
│   ├── navigation.spec.ts    # Nav/routing tests
│   ├── blog.spec.ts          # Blog functionality
│   ├── products.spec.ts      # Product pages
│   └── forms.spec.ts         # Form submissions
```

## Core Patterns

### Page Object Model
```typescript
// tests/pages/HomePage.ts
export class HomePage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/');
  }

  async getHeroTitle() {
    return this.page.locator('h1').first().textContent();
  }

  async clickCTA() {
    await this.page.getByRole('button', { name: /get started/i }).click();
  }

  async subscribeToNewsletter(email: string) {
    await this.page.getByPlaceholder(/email/i).fill(email);
    await this.page.getByRole('button', { name: /subscribe/i }).click();
  }
}
```

### Basic Test Structure
```typescript
import { test, expect } from '@playwright/test';
import { HomePage } from './pages/HomePage';

test.describe('Homepage', () => {
  let homePage: HomePage;

  test.beforeEach(async ({ page }) => {
    homePage = new HomePage(page);
    await homePage.goto();
  });

  test('should display hero section', async ({ page }) => {
    const title = await homePage.getHeroTitle();
    expect(title).toContain('FrankX');
  });

  test('should navigate to products on CTA click', async ({ page }) => {
    await homePage.clickCTA();
    await expect(page).toHaveURL(/products/);
  });
});
```

### Form Testing
```typescript
test('should submit contact form', async ({ page }) => {
  await page.goto('/contact');

  // Fill form
  await page.getByLabel('Name').fill('Test User');
  await page.getByLabel('Email').fill('test@example.com');
  await page.getByLabel('Message').fill('Test message');

  // Submit
  await page.getByRole('button', { name: /send/i }).click();

  // Verify success
  await expect(page.getByText(/thank you/i)).toBeVisible();
});
```

### API Mocking
```typescript
test('should display products from API', async ({ page }) => {
  // Mock API response
  await page.route('/api/products', async route => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { id: 1, name: 'Product 1', price: 99 },
        { id: 2, name: 'Product 2', price: 149 },
      ]),
    });
  });

  await page.goto('/products');

  await expect(page.getByText('Product 1')).toBeVisible();
  await expect(page.getByText('Product 2')).toBeVisible();
});
```

### Visual Regression Testing
```typescript
test('hero section visual regression', async ({ page }) => {
  await page.goto('/');

  // Screenshot comparison
  await expect(page.locator('.hero-section')).toHaveScreenshot('hero.png', {
    maxDiffPixels: 100,
  });
});
```

### Accessibility Testing
```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('should pass accessibility checks', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .analyze();

  expect(results.violations).toEqual([]);
});
```

## Debugging Techniques

### Screenshots on Failure
```typescript
test.afterEach(async ({ page }, testInfo) => {
  if (testInfo.status !== 'passed') {
    await page.screenshot({
      path: `screenshots/${testInfo.title}-failure.png`,
      fullPage: true,
    });
  }
});
```

### Trace Viewer
```bash
# Run with trace
npx playwright test --trace on

# View trace
npx playwright show-trace trace.zip
```

### Debug Mode
```bash
# Headed mode with slowMo
npx playwright test --headed --slowmo=500

# Debug specific test
npx playwright test homepage.spec.ts --debug

# UI mode
npx playwright test --ui
```

### Console Logging
```typescript
test('debug console logs', async ({ page }) => {
  page.on('console', msg => {
    console.log(`Browser: ${msg.type()}: ${msg.text()}`);
  });

  await page.goto('/');
});
```

## Commands

```bash
# Run all e2e tests
npm run test:e2e

# Run specific test file
npx playwright test homepage.spec.ts

# Run with specific browser
npx playwright test --project=chromium

# Update snapshots
npx playwright test --update-snapshots

# Generate test from recording
npx playwright codegen localhost:3000

# Show last HTML report
npx playwright show-report
```

## Best Practices

1. **Use semantic locators**
   ```typescript
   // Good - semantic
   page.getByRole('button', { name: 'Submit' })
   page.getByLabel('Email')
   page.getByText('Welcome')

   // Avoid - fragile
   page.locator('.btn-primary')
   page.locator('#email-input')
   ```

2. **Wait for network idle**
   ```typescript
   await page.goto('/', { waitUntil: 'networkidle' });
   ```

3. **Use test isolation**
   ```typescript
   test.describe.configure({ mode: 'parallel' });
   ```

4. **Clean state between tests**
   ```typescript
   test.beforeEach(async ({ context }) => {
     await context.clearCookies();
   });
   ```

## FrankX-Specific Tests

### PDF Download Flow
```typescript
test('should download PDF guide', async ({ page }) => {
  await page.goto('/guides');

  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.click('text=Download PDF'),
  ]);

  expect(download.suggestedFilename()).toMatch(/\.pdf$/);
});
```

### Newsletter Signup
```typescript
test('newsletter signup flow', async ({ page }) => {
  await page.goto('/');

  await page.fill('[data-testid="email-input"]', 'test@example.com');
  await page.click('[data-testid="subscribe-btn"]');

  await expect(page.getByText(/check your inbox/i)).toBeVisible();
});
```

## When to Use This Skill

- Writing new e2e tests
- Debugging UI issues
- Verifying user flows
- Testing responsive design
- Accessibility auditing

## Related Skills

- `test-driven-development` - TDD principles apply to e2e
- `systematic-debugging` - Debug failing tests
- `shadcn-ui-patterns` - Component patterns to test
