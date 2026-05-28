# Test Structure Reference

## Contents
- File Organization
- Test Anatomy
- Page Objects
- Fixtures for Reusable Setup
- Structure Anti-patterns

## File Organization

```
tests/
├── e2e/
│   ├── auth/
│   │   ├── login.spec.ts
│   │   └── signup.spec.ts
│   ├── dashboard/
│   │   └── dashboard.spec.ts
│   └── checkout/
│       └── checkout.spec.ts
├── fixtures/
│   └── index.ts
├── pages/
│   ├── login.page.ts
│   └── dashboard.page.ts
└── playwright.config.ts
```

## Test Anatomy

```typescript
import { test, expect } from '@playwright/test';

test.describe('Feature: User Login', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('/login');
    });

    test('logs in with valid credentials', async ({ page }) => {
        // Arrange - setup is in beforeEach

        // Act
        await page.getByLabel('Email').fill('user@example.com');
        await page.getByLabel('Password').fill('password123');
        await page.getByRole('button', { name: 'Sign in' }).click();

        // Assert
        await expect(page).toHaveURL('/dashboard');
        await expect(page.getByRole('heading', { name: 'Welcome' })).toBeVisible();
    });

    test('shows error for invalid credentials', async ({ page }) => {
        await page.getByLabel('Email').fill('user@example.com');
        await page.getByLabel('Password').fill('wrong');
        await page.getByRole('button', { name: 'Sign in' }).click();

        await expect(page.getByRole('alert')).toContainText('Invalid credentials');
    });
});
```

## Page Objects

Use page objects to encapsulate page interactions, not assertions:

```typescript
// pages/login.page.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
    readonly page: Page;
    readonly emailInput: Locator;
    readonly passwordInput: Locator;
    readonly submitButton: Locator;
    readonly errorAlert: Locator;

    constructor(page: Page) {
        this.page = page;
        this.emailInput = page.getByLabel('Email');
        this.passwordInput = page.getByLabel('Password');
        this.submitButton = page.getByRole('button', { name: 'Sign in' });
        this.errorAlert = page.getByRole('alert');
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

// In test file
test('logs in successfully', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('user@example.com', 'password123');

    await expect(page).toHaveURL('/dashboard');
});
```

## Fixtures for Reusable Setup

```typescript
// fixtures/index.ts
import { test as base, Page } from '@playwright/test';
import { LoginPage } from '../pages/login.page';
import { DashboardPage } from '../pages/dashboard.page';

type Fixtures = {
    loginPage: LoginPage;
    dashboardPage: DashboardPage;
    authenticatedPage: Page;
};

export const test = base.extend<Fixtures>({
    loginPage: async ({ page }, use) => {
        await use(new LoginPage(page));
    },

    dashboardPage: async ({ page }, use) => {
        await use(new DashboardPage(page));
    },

    // Fixture that provides an already-authenticated page
    authenticatedPage: async ({ page }, use) => {
        await page.goto('/login');
        await page.getByLabel('Email').fill('test@example.com');
        await page.getByLabel('Password').fill('password');
        await page.getByRole('button', { name: 'Sign in' }).click();
        await page.waitForURL('/dashboard');
        await use(page);
    },
});

export { expect } from '@playwright/test';

// Usage in tests
import { test, expect } from '../fixtures';

test('views dashboard data', async ({ authenticatedPage }) => {
    await expect(authenticatedPage.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
});
```

## Structure Anti-patterns

| Bad | Why | Good |
|-----|-----|------|
| Assertions inside page objects | Hides test intent | Page objects do actions, tests assert |
| Huge test files (500+ lines) | Hard to maintain | Split by feature/user flow |
| Copy-pasting setup code | DRY violation | Use fixtures or beforeEach |
| Testing multiple unrelated things | Hard to debug failures | One behavior per test |
| Vague test names | Unclear what's tested | Describe user action + expected outcome |
