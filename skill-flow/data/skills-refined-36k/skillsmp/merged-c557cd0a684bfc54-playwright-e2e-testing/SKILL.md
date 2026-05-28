---
name: playwright-e2e-testing
description: Use this skill for setting up and executing end-to-end (E2E) browser tests with Playwright, including cross-browser testing, visual regression, and CI integration.
---

# End-to-End Testing with Playwright

This skill provides a comprehensive workflow for creating and managing end-to-end testing suites using Playwright.

## Core Workflow

1. **Setup and Configuration**: Initialize your Playwright project and configure the testing environment. Use the following commands:
   ```bash
   npm init playwright@latest
   npx playwright install
   ```
   Example configuration in `playwright.config.ts`:
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
       { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
       { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
       { name: 'webkit', use: { ...devices['Desktop Safari'] } },
     ],
     webServer: {
       command: 'npm run dev',
       url: 'http://localhost:3000',
       reuseExistingServer: !process.env.CI,
     },
   });
   ```

2. **Structure with Page Object Model (POM)**: Organize your test code by creating Page Object classes for each page or component to enhance readability and maintainability. Example:
   ```typescript
   // pages/login.page.ts
   import { Page, Locator } from '@playwright/test';

   export class LoginPage {
     readonly page: Page;
     readonly emailInput: Locator;
     readonly passwordInput: Locator;
     readonly submitButton: Locator;

     constructor(page: Page) {
       this.page = page;
       this.emailInput = page.locator('[data-testid="email"]');
       this.passwordInput = page.locator('[data-testid="password"]');
       this.submitButton = page.locator('[data-testid="submit"]');
     }

     async goto() {
       await this.page.goto('/login');
     }

     async login(email: string, password: string) {
       await this.emailInput.fill(email);
       await this.passwordInput.fill(password);
       await this.submitButton.click();
     }
   }
   ```

3. **Write User Flow Tests**: Create end-to-end tests that simulate user journeys. Example:
   ```typescript
   import { test, expect } from '@playwright/test';

   test('should login successfully', async ({ page }) => {
     const loginPage = new LoginPage(page);
     await loginPage.goto();
     await loginPage.login('user@example.com', 'password123');
     await expect(page).toHaveURL('/dashboard');
     await expect(page.locator('h1')).toContainText('Welcome');
   });
   ```

4. **Implement Visual Regression Testing**: Add screenshot assertions to catch unintended visual changes. Example:
   ```typescript
   test('visual comparison', async ({ page }) => {
     await page.goto('/');
     await expect(page).toHaveScreenshot('homepage.png', {
       maxDiffPixelRatio: 0.1,
     });
   });
   ```

5. **Configure Cross-Browser Testing**: Ensure your application works across different browsers by configuring projects in Playwright.

6. **Integrate with CI**: Automate your tests to run on every code change. Configure your CI pipeline to include Playwright tests.

7. **Manage Test Data**: Set up and tear down test data to ensure reliable and independent tests.

## Problem Playbooks

### Network Interception
Mock API responses to test various scenarios:
```typescript
test('mock API response', async ({ page }) => {
  await page.route('**/api/users', async (route) => {
    await route.fulfill({
      status: 200,
      body: JSON.stringify([{ id: 1, name: 'Mock User' }]),
    });
  });

  await page.goto('/users');
  await expect(page.locator('.user-name')).toContainText('Mock User');
});
```

### Handling Flaky Tests
Implement strategies to manage flaky tests, such as retries and proper wait strategies.

## Running Tests
Use the following commands to run your tests:
```bash
# Run all tests
npx playwright test

# Run specific file
npx playwright test <test_file_name>

# Run in headed mode
npx playwright test --headed

# Debug mode
npx playwright test --debug
```

## Code Review Checklist
- [ ] Use `data-testid` attributes for selectors.
- [ ] Implement Page Object Model for complex flows.
- [ ] Mock network requests where needed.
- [ ] Ensure proper wait strategies are in place.
- [ ] Configure screenshots on failure.
- [ ] Enable parallel execution.

## Anti-Patterns
1. Avoid hardcoded waits; use proper assertions.
2. Prevent fragile selectors; prefer `data-testid`.
3. Isolate tests to avoid shared state.
4. Implement retries for flaky tests.
5. Focus on testing user behavior rather than implementation details.