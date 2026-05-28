---
name: browser-testing-playwright
description: Use this skill when you want to set up and run end-to-end (E2E) browser tests using Playwright, covering project setup, user flow testing, visual regression, and CI integration.
---

# End-to-End Browser Testing with Playwright

This skill provides a structured workflow for creating a robust end-to-end testing suite using Playwright.

## Core Workflow

1. **Setup and Configuration**: Start by initializing your Playwright project and installing the necessary browsers.
   ```bash
   npm init playwright@latest
   npx playwright install
   ```
   Create a `playwright.config.ts` file with the following configuration:
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

2. **Structure with Page Object Model (POM)**: Organize your test code by creating Page Object classes for each page or component. This pattern enhances readability and maintainability.

3. **Write User Flow Tests**: With POMs in place, write end-to-end tests that simulate user journeys. For example, a test for user authentication:
   ```typescript
   import { test, expect } from '@playwright/test';

   test.describe('Authentication', () => {
     test('should login successfully', async ({ page }) => {
       await page.goto('/login');
       await page.fill('[data-testid="email"]', 'user@example.com');
       await page.fill('[data-testid="password"]', 'password123');
       await page.click('[data-testid="submit"]');
       await expect(page).toHaveURL('/dashboard');
       await expect(page.locator('h1')).toContainText('Welcome');
     });
   });
   ```

4. **Implement Visual Regression Testing**: Add screenshot assertions to catch unintended visual changes.

5. **Configure Cross-Browser Testing**: Ensure your application works across different browsers by configuring projects in Playwright.

6. **Integrate with CI**: Automate your tests to run on every code change. Set up a CI pipeline to execute your tests.

7. **Manage Test Data**: Learn strategies for setting up and tearing down test data to ensure reliable and independent tests.

## Bundled Resources

This skill includes reference files to guide you through each step. When you need to implement a part of the workflow, refer to the relevant sections in this document.