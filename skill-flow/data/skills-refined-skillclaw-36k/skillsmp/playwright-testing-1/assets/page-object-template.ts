import { type Page, type Locator } from '@playwright/test';

/**
 * Page Object Model Template
 * 
 * POMs are PURE abstractions of page structure and interactions.
 * They should NOT contain:
 * - BDD decorators or step definitions
 * - Assertions (expose locators instead, assert in steps)
 * - Business logic or test data
 * 
 * POMs SHOULD contain:
 * - Locators as readonly properties
 * - Action methods (click, fill, navigate)
 * - Guard waits for navigation completion
 */

export class TemplatePage {
  readonly page: Page;
  
  // Expose locators as readonly properties for assertions in steps
  readonly heading: Locator;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorAlert: Locator;

  constructor(page: Page) {
    this.page = page;
    
    // Prefer locator strategies (in order):
    // 1. getByTestId('id') - Most reliable
    // 2. getByRole('role', { name: 'text' }) - Semantic
    // 3. getByLabel('label') - Form fields
    // 4. getByText('text') - Static content
    // 5. locator('css') - Last resort
    
    this.heading = page.getByRole('heading', { level: 1 });
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: 'Sign in' });
    this.errorAlert = page.getByRole('alert');
  }

  async goto() {
    await this.page.goto('/page-url');
  }

  async waitForLoad() {
    await this.heading.waitFor({ state: 'visible' });
  }

  // Action methods - NO assertions here
  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}
