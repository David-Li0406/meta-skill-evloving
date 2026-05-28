/**
 * Playwright-BDD Fixtures & Step Definitions Template
 * 
 * ARCHITECTURE:
 * - POMs are pure (no decorators, no assertions)
 * - Step definitions contain assertions and use POMs via fixtures
 * - Test data is managed here, NOT in Gherkin scenarios
 */

import { test as base, createBdd } from 'playwright-bdd';
import { expect } from '@playwright/test';
// Import page objects
// import { LoginPage } from '../page-objects/login.page';

// ============================================================
// Test Data - Manage credentials here, NOT in Gherkin
// ============================================================
export const TEST_USERS = {
  valid: { email: 'testuser@example.com', password: 'validPassword123' },
  invalid: { email: 'wrong@example.com', password: 'wrongPassword' },
  admin: { email: 'admin@example.com', password: 'adminPassword123' },
};

// ============================================================
// Custom Fixtures
// ============================================================
type Fixtures = {
  // loginPage: LoginPage;
  ctx: Record<string, unknown>;
};

export const test = base.extend<Fixtures>({
  // loginPage: async ({ page }, use) => {
  //   await use(new LoginPage(page));
  // },
  ctx: async ({}, use) => {
    await use({});
  },
});

export const { Given, When, Then, Before, After } = createBdd(test);

// ============================================================
// Hooks
// ============================================================

// After(async ({ page, $testInfo }) => {
//   if ($testInfo.status === 'failed') {
//     await page.screenshot({ path: `screenshots/${$testInfo.title}.png` });
//   }
// });

// ============================================================
// Step Definitions
// ============================================================

Given('I am on the home page', async ({ page }) => {
  await page.goto('/');
});

// ✅ Behavior-focused action steps
// When('I login with valid credentials', async ({ loginPage }) => {
//   const { email, password } = TEST_USERS.valid;
//   await loginPage.login(email, password);
// });

// ✅ Assertions belong in step definitions, NOT in POMs
// Then('I should see a login error', async ({ loginPage }) => {
//   await expect(loginPage.errorAlert).toBeVisible();
// });

// ✅ Parameterize only when value IS the requirement
Then('the error message should be {string}', async ({ page }, expected: string) => {
  await expect(page.getByRole('alert')).toHaveText(expected);
});
