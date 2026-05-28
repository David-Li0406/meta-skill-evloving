# Page Object Model Examples

Complete examples of pure POMs (no decorators, no assertions).

## Login Page Object

```typescript
// page-objects/login.page.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  
  // Form elements - exposed for assertions in steps
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  
  // Feedback elements
  readonly errorAlert: Locator;
  readonly successMessage: Locator;
  readonly loadingSpinner: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: 'Sign in' });
    this.errorAlert = page.getByRole('alert');
    this.successMessage = page.getByTestId('welcome-message');
    this.loadingSpinner = page.getByTestId('loading');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async waitForLoad() {
    await this.emailInput.waitFor({ state: 'visible' });
  }

  // Actions only - NO assertions
  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async clearForm() {
    await this.emailInput.clear();
    await this.passwordInput.clear();
  }
}
```

## Dashboard Page Object

```typescript
// page-objects/dashboard.page.ts
import { Page, Locator } from '@playwright/test';

export class DashboardPage {
  readonly page: Page;
  
  readonly welcomeHeading: Locator;
  readonly userMenu: Locator;
  readonly logoutButton: Locator;
  readonly navItems: Locator;

  constructor(page: Page) {
    this.page = page;
    this.welcomeHeading = page.getByRole('heading', { name: /welcome/i });
    this.userMenu = page.getByTestId('user-menu');
    this.logoutButton = page.getByRole('button', { name: 'Logout' });
    this.navItems = page.getByRole('navigation').getByRole('link');
  }

  async goto() {
    await this.page.goto('/dashboard');
  }

  async openUserMenu() {
    await this.userMenu.click();
  }

  async logout() {
    await this.openUserMenu();
    await this.logoutButton.click();
  }

  async navigateTo(linkName: string) {
    await this.page.getByRole('navigation').getByRole('link', { name: linkName }).click();
  }
}
```
