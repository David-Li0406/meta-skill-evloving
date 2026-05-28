---
name: playwright-e2e-testing
description: Use this skill when writing Playwright E2E tests, implementing test utilities, or following project patterns for components and user interactions.
---

# Playwright E2E Testing Skill

This skill provides guidelines and patterns for writing Playwright E2E tests, creating reusable test utilities, and implementing Page Object Models.

## Test File Location

All E2E tests should be organized in the `tests/e2e/` directory:

```
tests/e2e/
├── app.spec.ts
├── comparison.spec.ts
├── fileTree.spec.ts
├── navigation.spec.ts
├── primitiveCards.spec.ts
└── theme.spec.ts
```

## Test File Structure

```typescript
import { test, expect } from '@playwright/test'

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('should do something specific', async ({ page }) => {
    // Arrange
    const element = page.getByRole('button', { name: 'Click me' })

    // Act
    await element.click()

    // Assert
    await expect(page.getByText('Success')).toBeVisible()
  })
})
```

## Locator Strategy (Priority Order)

Use the most resilient locators, in this order of preference:

1. Role + Name (most resilient)
   ```typescript
   page.getByRole('button', { name: 'Submit' })
   ```
2. Label/Placeholder (for form elements)
   ```typescript
   page.getByLabel('Email address')
   ```
3. Text content (for static text)
   ```typescript
   page.getByText('Learn more')
   ```
4. Test ID (when others don't work)
   ```typescript
   page.getByTestId('file-tree-node')
   ```
5. CSS selectors (last resort)
   ```typescript
   page.locator('.custom-component')
   ```

## Common Test Patterns

### Navigation
```typescript
test('should scroll to section when nav link is clicked', async ({ page }) => {
  const navLink = page.getByRole('link', { name: 'File Tree' })
  const section = page.getByRole('region', { name: 'File Tree' })

  await navLink.click()
  await expect(section).toBeInViewport()
})
```

### Theme Toggle
```typescript
test('should toggle between light and dark mode', async ({ page }) => {
  const toggle = page.getByRole('button', { name: /theme/i })

  await expect(page.locator('html')).toHaveAttribute('data-theme', 'light')
  await toggle.click()
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark')
})
```

## Creating and Using Fixtures

### Basic Fixture Example
```typescript
import { test as base } from "@playwright/test"

export const test = base.extend({
  speakersPage: async ({ page }, use) => {
    await page.goto("http://localhost:3000/speakers")
    await page.waitForLoadState("networkidle")
    await use(page)
  },
})

export { expect } from "@playwright/test"
```

### Page Object Model Fixture
```typescript
class SpeakersPage {
  constructor(public readonly page: Page) {}

  async goto() {
    await this.page.goto("http://localhost:3000/speakers")
    await this.page.waitForLoadState("networkidle")
  }

  async createSpeaker(data: { firstName: string; lastName: string }) {
    await this.page.getByTestId("speakers-create-button").click()
    await this.page.getByTestId("speaker-first-name-input").fill(data.firstName)
    await this.page.getByTestId("speaker-last-name-input").fill(data.lastName)
    await this.page.getByTestId("speaker-submit-button").click()
  }
}
```

## Critical Rules

- Use `data-testid` for element selection.
- Tests must be **functional** (Create/Update/Delete), NOT navigational.
- Ensure tests are independent and do not rely on prior test state.
- Avoid arbitrary waits; use assertions to check element states.

## Commands

Run tests using the following commands:
```bash
pnpm playwright test --reporter=line --max-failures=1
pnpm playwright test --workers=4 --repeat-each=5 --reporter=line  # flaky detection
```