# Step Definition Examples

Behavior-focused step definitions with assertions.

## Login Steps

```typescript
// steps/login.steps.ts
import { Given, When, Then, TEST_USERS } from './fixtures';
import { expect } from '@playwright/test';

// Navigation
Given('I am on the login page', async ({ loginPage }) => {
  await loginPage.goto();
  await loginPage.waitForLoad();
});

// Behavior-focused actions
When('I login with valid credentials', async ({ loginPage }) => {
  const { email, password } = TEST_USERS.valid;
  await loginPage.login(email, password);
});

When('I login with invalid credentials', async ({ loginPage }) => {
  const { email, password } = TEST_USERS.invalid;
  await loginPage.login(email, password);
});

When('I login as admin', async ({ loginPage }) => {
  const { email, password } = TEST_USERS.admin;
  await loginPage.login(email, password);
});

When('I submit the login form without credentials', async ({ loginPage }) => {
  await loginPage.submitButton.click();
});

// Assertions - using POM locators
Then('I should be logged in', async ({ page }) => {
  await expect(page).toHaveURL(/.*dashboard/);
});

Then('I should see a login error', async ({ loginPage }) => {
  await expect(loginPage.errorAlert).toBeVisible();
});

Then('the email field should show a validation error', async ({ loginPage }) => {
  await expect(loginPage.emailInput).toHaveAttribute('aria-invalid', 'true');
});

// Parameterized - only when value IS the requirement
Then('the error message should be {string}', async ({ loginPage }, expected: string) => {
  await expect(loginPage.errorAlert).toHaveText(expected);
});

Then('I should see welcome message for {string}', async ({ page }, name: string) => {
  await expect(page.getByTestId('welcome-message')).toContainText(name);
});
```

## Role-Based Steps

```typescript
// steps/auth.steps.ts
import { Given, When, Then, TEST_USERS } from './fixtures';
import { expect } from '@playwright/test';

Given('I am logged in as {word}', async ({ loginPage, page }, role: string) => {
  const user = TEST_USERS[role as keyof typeof TEST_USERS];
  if (!user) throw new Error(`Unknown role: ${role}`);
  
  await loginPage.goto();
  await loginPage.login(user.email, user.password);
  await expect(page).toHaveURL(/.*dashboard/);
});

When('I visit the admin page', async ({ page }) => {
  await page.goto('/admin');
});

Then('I should see the admin panel', async ({ page }) => {
  await expect(page.getByRole('heading', { name: 'Admin Panel' })).toBeVisible();
});

Then('I should see access denied', async ({ page }) => {
  await expect(page.getByText('Access Denied')).toBeVisible();
});
```
