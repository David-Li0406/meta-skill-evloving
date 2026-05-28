---
name: write-e2e-test
description: Write Playwright E2E tests following project patterns for components and user interactions. Use when adding tests for new features, testing accessibility, or validating responsive behavior.
---

# Write E2E Test

Create Playwright E2E tests for agentconfig.org following project patterns.

## Test File Location

All E2E tests live in `site/tests/e2e/`:

```
site/tests/e2e/
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

### 1. Role + Name (most resilient)
```typescript
page.getByRole('button', { name: 'Submit' })
page.getByRole('heading', { name: 'Welcome' })
page.getByRole('navigation')
```

### 2. Label/Placeholder (for form elements)
```typescript
page.getByLabel('Email address')
page.getByPlaceholder('Enter your email')
```

### 3. Text content (for static text)
```typescript
page.getByText('Learn more')
page.getByText(/welcome/i)  // regex for flexible matching
```

### 4. Test ID (when others don't work)
```typescript
page.getByTestId('file-tree-node')
```

### 5. CSS selectors (last resort)
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

### Expandable Content
```typescript
test('should expand tree node on click', async ({ page }) => {
  const treeNode = page.getByRole('button', { name: '.github/' })
  const childNode = page.getByRole('button', { name: 'copilot-instructions.md' })

  await expect(childNode).not.toBeVisible()

  await treeNode.click()

  await expect(childNode).toBeVisible()
})
```

### Copy to Clipboard
```typescript
test('should copy template to clipboard', async ({ page, context }) => {
  await context.grantPermissions(['clipboard-read', 'clipboard-write'])

  const copyButton = page.getByRole('button', { name: 'Copy template' })
  await copyButton.click()

  const clipboardText = await page.evaluate(() => navigator.clipboard.readText())
  expect(clipboardText).toContain('expected content')
})
```

## Responsive Testing

Test at multiple viewport sizes:

```typescript
test.describe('Mobile viewport', () => {
  test.use({ viewport: { width: 375, height: 667 } })

  test('should show mobile navigation', async ({ page }) => {
    await expect(page.getByRole('button', { name: 'Menu' })).toBeVisible()
  })
})

test.describe('Desktop viewport', () => {
  test.use({ viewport: { width: 1280, height: 720 } })

  test('should show full navigation', async ({ page }) => {
    await expect(page.getByRole('navigation')).toBeVisible()
  })
})
```

## Theme Testing

Test both light and dark modes:

```typescript
test.describe('Dark mode', () => {
  test.use({ colorScheme: 'dark' })

  test('should render with dark theme colors', async ({ page }) => {
    // Verify dark mode specific styling
  })
})

test.describe('Light mode', () => {
  test.use({ colorScheme: 'light' })

  test('should render with light theme colors', async ({ page }) => {
    // Verify light mode specific styling
  })
})
```

## Test Independence

Each test must be independent:
- Don't rely on state from previous tests
- Use `beforeEach` for common setup
- Clean up any side effects

## Assertions

Use Playwright's built-in assertions (auto-waiting):

```typescript
// Good - auto-waits for element
await expect(page.getByText('Hello')).toBeVisible()
await expect(page.getByRole('button')).toBeEnabled()
await expect(page.locator('.item')).toHaveCount(3)
await expect(page.getByRole('link')).toHaveAttribute('href', '/about')

// Bad - doesn't auto-wait
const text = await page.textContent('.item')
expect(text).toBe('Hello')
```

## Test Naming

Use descriptive names that explain the expected behavior:

```typescript
// Good
test('should expand tree node when clicked', ...)
test('should scroll to File Tree section when nav link is clicked', ...)
test('should display error message when copy fails', ...)

// Bad
test('click test', ...)
test('tree works', ...)
test('test 1', ...)
```

## Running Tests

```bash
cd site
bun run test              # Run all tests
bun run test:ui           # Interactive test UI
```

## Checklist

Before considering tests complete:

- [ ] Uses resilient locators (role > text > testid > css)
- [ ] Each test is independent
- [ ] Test name describes expected behavior
- [ ] Uses Playwright auto-waiting assertions
- [ ] Covers happy path and edge cases
- [ ] Tests responsive behavior if relevant
- [ ] Tests both themes if relevant
- [ ] No hardcoded waits (`page.waitForTimeout`)
