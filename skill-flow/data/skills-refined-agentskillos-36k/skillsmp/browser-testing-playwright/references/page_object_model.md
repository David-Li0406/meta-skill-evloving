# Page Object Model (POM)

The Page Object Model is a design pattern that makes test code more readable, reusable, and easier to maintain. Instead of writing locator strings and interaction logic directly in your test files, you encapsulate them within a class that represents a page (or a component) of your application.

## Why use POM?

-   **Readability**: Tests become cleaner and focus on user actions, not implementation details.
-   **Maintainability**: If the UI changes, you only need to update the locators in one place (the Page Object class) instead of in every test that uses it.
-   **Reusability**: You can reuse Page Object methods across multiple tests.

## Creating a Page Object

A Page Object class typically includes:
1.  A constructor that takes the Playwright `Page` object.
2.  Locators for the elements on the page.
3.  Methods that perform actions on those elements (e.g., `login`, `fillUsername`).

### Example: `LoginPage.ts`

Here is an example of a Page Object for a login page.

```typescript
// tests/poms/LoginPage.ts
import { type Page, type Locator } from '@playwright/test';

export class LoginPage {
  // Make properties readonly to avoid accidental modification
  readonly page: Page;
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.usernameInput = page.locator('input[name="username"]');
    this.passwordInput = page.locator('input[name="password"]');
    this.loginButton = page.locator('button[type="submit"]');
    this.errorMessage = page.locator('.error-message');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(username: string, password: string) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }
}
```

## Using the Page Object in a Test

You can then instantiate and use this class in your test files.

```typescript
// tests/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from './poms/LoginPage';

test('should show error message with invalid credentials', async ({ page }) => {
  const loginPage = new LoginPage(page);

  await loginPage.goto();
  await loginPage.login('invalid-user', 'invalid-password');

  await expect(loginPage.errorMessage).toBeVisible();
  await expect(loginPage.errorMessage).toHaveText('Invalid username or password.');
});
```
This approach makes the test's intent clear and separates the test logic from the page's implementation details.