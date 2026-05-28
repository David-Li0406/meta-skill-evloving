---
name: playwright-e2e-testing
description: Use this skill when writing or running end-to-end tests with Playwright, focusing on best practices and the Page Object Model.
---

# Skill body

## MCP Workflow (MANDATORY If Available)

**⚠️ If you have Playwright MCP tools, ALWAYS use them BEFORE creating any test:**

1. **Navigate** to the target page.
2. **Take a snapshot** to see page structure and elements.
3. **Interact** with forms/elements to verify the exact user flow.
4. **Take screenshots** to document expected states.
5. **Verify page transitions** through the complete flow (loading, success, error).
6. **Document actual selectors** from snapshots (use real refs and labels).
7. **Only after exploring**, create test code with verified selectors.

**If MCP NOT available:** Proceed with test creation based on documentation and code analysis.

**Why This Matters:**
- ✅ Precise tests - exact steps needed, no assumptions.
- ✅ Accurate selectors - real DOM structure, not imagined.
- ✅ Real flow validation - verify the journey actually works.
- ✅ Avoid over-engineering - minimal tests for what exists.
- ✅ Prevent flaky tests - real exploration = stable tests.
- ❌ Never assume how UI "should" work.

## File Structure

```
e2e/
├── pages/
│   ├── {page-name}-page.ts   # Page Object Model
│   └── ...
├── fixtures/                  # Test data
└── {test-name}.spec.ts        # Test files
```

## Page Object Pattern

```typescript
// pages/login-page.ts
export class LoginPage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.fill('[name="email"]', email);
    await this.page.fill('[name="password"]', password);
    await this.page.click('button[type="submit"]');
    await this.page.waitForURL('/dashboard');
  }

  async getErrorMessage() {
    return await this.page.textContent('.alert-error');
  }
}
```

## Selectors

```typescript
// ✅ Prefer accessible selectors
page.getByRole('button', { name: 'Submit' });
page.getByText('Welcome');
page.getByLabel('Email');
page.getByPlaceholder('Enter email');

// ✅ Test ID (when no semantic option)
page.getByTestId('submit-button');

// ✅ CSS selector (as fallback)
page.locator('button[type="submit"]');
```

## Actions

```typescript
// ✅ Fill input
await page.fill('[name="email"]', 'test@example.com');

// ✅ Click
await page.click('button[type="submit"]');

// ✅ Select
await page.selectOption('[name="status"]', 'active');

// ✅ Check/uncheck
await page.check('[name="remember"]');
await page.uncheck('[name="remember"]');

// ✅ Type
await page.type('input', 'text', { delay: 100 });
```

## Assertions

```typescript
// ✅ Page URL
await expect(page).toHaveURL('/dashboard');

// ✅ Element visible
await expect(page.getByText('Welcome')).toBeVisible();

// ✅ Element hidden
await expect(page.getByTestId('modal')).toBeHidden();

// ✅ Text content
await expect(page.getByTestId('title')).toHaveText('Dashboard');

// ✅ Attribute
await expect(page.getByRole('button')).toHaveAttribute('disabled');

// ✅ Element count
await expect(page.locator('table tr')).toHaveCount(10);
```

## Waits

```typescript
// ✅ Wait for navigation
await page.waitForURL('/dashboard');

// ✅ Wait for element
await page.waitForSelector('[data-testid="loaded"]');

// ✅ Wait for load state
await page.waitForLoadState('networkidle');

// ✅ Wait for timeout (avoid!)
await page.waitForTimeout(1000); // Only when necessary
```

## Example Test

```typescript
// e2e/auth.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/login-page';

test.describe('Authentication', () => {
  test('should login successfully', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('admin@example.com', 'password123');
    await expect(page).toHaveURL('/dashboard');
  });

  test('should show error with invalid credentials', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('invalid@example.com', 'wrongpassword');
    const error = await loginPage.getErrorMessage();
    expect(error).toContain('Invalid credentials');
  });
});
```