---
name: playwright-e2e-testing
description: Use this skill when writing Playwright E2E tests, implementing fixtures, or creating reusable test utilities for components and user interactions.
---

# Playwright E2E Testing Skill

This skill provides guidelines for writing Playwright E2E tests, implementing fixtures, and creating reusable test utilities.

## Test File Location

All E2E tests should be organized in the following directory structure:

```
playwright/tests/app-tests/{feature}/
├── feature.spec.ts
└── PLAN.md
```

## Test File Structure

```typescript
import { expect, test } from '~/helpers/fixtures';

test.describe.serial('Feature Name', () => {
  test('01. Test case description', async ({ page }) => {
    // Arrange
    await page.goto('http://localhost:3000/feature');

    // Act
    await page.getByTestId('some-button').click();

    // Assert
    await expect(page.getByText('Expected text')).toBeVisible();
  });
});
```

## Writing E2E Tests

### Common Patterns

- **Navigation**: Ensure that navigation links work as expected.
- **Form Interactions**: Test form submissions and validations.
- **Assertions**: Use Playwright's built-in assertions for auto-waiting.

### Locator Strategy

Use the following order of preference for selecting elements:

1. **Role + Name** (most resilient)
   ```typescript
   page.getByRole('button', { name: 'Submit' });
   ```
2. **Label/Placeholder** (for form elements)
   ```typescript
   page.getByLabel('Email address');
   ```
3. **Text content** (for static text)
   ```typescript
   page.getByText('Learn more');
   ```
4. **Test ID** (when others don't work)
   ```typescript
   page.getByTestId('file-tree-node');
   ```
5. **CSS selectors** (last resort)
   ```typescript
   page.locator('.custom-component');
   ```

## Implementing Fixtures

### Creating Fixtures

Use Playwright's `test.extend()` API to create reusable fixtures:

```typescript
import { test as base } from '@playwright/test';

export const test = base.extend({
  myPage: async ({ page }, use) => {
    await page.goto('http://localhost:3000/my-page');
    await use(page);
  },
});
```

### Page Object Model Fixture

Implement Page Object Models as fixtures:

```typescript
class MyPage {
  constructor(public readonly page: Page) {}

  async clickButton() {
    await this.page.getByTestId('my-button').click();
  }
}

export const test = base.extend<{ myPage: MyPage }>({
  myPage: async ({ page }, use) => {
    const myPage = new MyPage(page);
    await myPage.goto();
    await use(myPage);
  },
});
```

## Running Tests

To run tests, use the following commands:

```bash
cd playwright
npx playwright test tests/app-tests/{feature}/feature.spec.ts --project=chromium
```

## Checklist for New Tests

- [ ] Test file is in the correct `app-tests/<feature>/` directory.
- [ ] Uses `data-testid` selectors where possible.
- [ ] Includes meaningful assertions.
- [ ] Works on both Chromium and Firefox.
- [ ] Tests have been run and pass successfully.

## Debugging Tests

For debugging, use the following commands:

```bash
npx playwright test --ui      # UI mode for development
npx playwright test --debug   # Debug mode with breakpoints
```

## Related Documentation

- [Testing Strategy Research](../../../research/testing-strategy/2026-01-16-modern-testing-strategy.md) - When to write E2E vs unit tests.