# Playwright Patterns Reference

Advanced patterns for writing maintainable E2E tests with Playwright.

## Locator Strategies

### Role-Based (Preferred)

```typescript
// Buttons
page.getByRole('button', { name: 'Submit' })
page.getByRole('button', { name: /submit/i })  // Case insensitive

// Links
page.getByRole('link', { name: 'Home' })

// Form inputs
page.getByRole('textbox', { name: 'Email' })
page.getByRole('checkbox', { name: 'Remember me' })

// Navigation
page.getByRole('navigation')
page.getByRole('heading', { level: 1 })
```

### Label-Based (Forms)

```typescript
// Explicit labels
page.getByLabel('Email address')
page.getByLabel('Password')

// Placeholders (fallback)
page.getByPlaceholder('Enter email')
```

### Text-Based (Content)

```typescript
// Exact match
page.getByText('Welcome back')

// Partial match
page.getByText('Welcome', { exact: false })

// Regex
page.getByText(/welcome/i)
```

### Test ID (Last Resort)

```typescript
// Only when semantic locators aren't possible
page.getByTestId('complex-widget')
```

## Page Object Pattern

### Structure

```typescript
// pages/login.page.ts
import { Page, Locator } from '@playwright/test'

export class LoginPage {
  readonly page: Page
  readonly emailInput: Locator
  readonly passwordInput: Locator
  readonly submitButton: Locator
  readonly errorMessage: Locator

  constructor(page: Page) {
    this.page = page
    this.emailInput = page.getByLabel('Email')
    this.passwordInput = page.getByLabel('Password')
    this.submitButton = page.getByRole('button', { name: 'Sign in' })
    this.errorMessage = page.getByRole('alert')
  }

  async goto() {
    await this.page.goto('/login')
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email)
    await this.passwordInput.fill(password)
    await this.submitButton.click()
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toContainText(message)
  }
}
```

### Usage in Tests

```typescript
// tests/login.e2e.ts
import { test, expect } from '@playwright/test'
import { LoginPage } from './pages/login.page'

test('user can login with valid credentials', async ({ page }) => {
  const login = new LoginPage(page)
  await login.goto()
  await login.login('user@example.com', 'password123')
  await expect(page).toHaveURL('/dashboard')
})

test('shows error for invalid credentials', async ({ page }) => {
  const login = new LoginPage(page)
  await login.goto()
  await login.login('user@example.com', 'wrong')
  await login.expectError('Invalid credentials')
})
```

## Waiting Patterns

### Auto-Waiting (Default)

Playwright auto-waits for elements to be actionable:

```typescript
// These wait automatically
await page.getByRole('button').click()
await page.getByLabel('Email').fill('test@example.com')
```

### Explicit Assertions

```typescript
// Wait for visibility
await expect(page.getByText('Success')).toBeVisible()

// Wait for hidden
await expect(page.getByText('Loading')).toBeHidden()

// Wait for count
await expect(page.getByRole('listitem')).toHaveCount(5)
```

### Network Waiting

```typescript
// Wait for specific request
await page.waitForResponse('**/api/users')

// Wait for navigation
await Promise.all([
  page.waitForNavigation(),
  page.getByRole('button').click()
])
```

## Testing Patterns

### Setup and Teardown

```typescript
test.beforeEach(async ({ page }) => {
  await page.goto('/')
})

test.afterEach(async ({ page }) => {
  // Cleanup if needed
})
```

### Fixtures

```typescript
// fixtures.ts
import { test as base } from '@playwright/test'
import { LoginPage } from './pages/login.page'

export const test = base.extend<{ loginPage: LoginPage }>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page)
    await use(loginPage)
  }
})

// Usage
test('test with fixture', async ({ loginPage }) => {
  await loginPage.goto()
  // ...
})
```

### Authenticated Tests

```typescript
// Save auth state
test('login and save state', async ({ page }) => {
  await page.goto('/login')
  await page.getByLabel('Email').fill('user@example.com')
  await page.getByLabel('Password').fill('password')
  await page.getByRole('button', { name: 'Sign in' }).click()
  await page.context().storageState({ path: '.auth/user.json' })
})

// Reuse auth state
test.use({ storageState: '.auth/user.json' })
test('authenticated test', async ({ page }) => {
  await page.goto('/dashboard')  // Already logged in
})
```

## Debugging

### Screenshots

```typescript
await page.screenshot({ path: 'screenshot.png' })
await page.screenshot({ path: 'full.png', fullPage: true })
```

### Tracing

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    trace: 'on-first-retry'
  }
})

// View trace
// npx playwright show-trace trace.zip
```

### Debug Mode

```bash
# Run in headed mode with devtools
PWDEBUG=1 npx playwright test

# Run specific test
npx playwright test tests/login.e2e.ts --debug
```

## Anti-Patterns to Avoid

### Don't: Arbitrary Waits

```typescript
// Bad
await page.waitForTimeout(2000)

// Good
await expect(page.getByText('Loaded')).toBeVisible()
```

### Don't: Over-Specific Selectors

```typescript
// Bad
page.locator('#app > div.container > form > button.submit-btn')

// Good
page.getByRole('button', { name: 'Submit' })
```

### Don't: Shared State Between Tests

```typescript
// Bad - tests depend on each other
let userId: string

test('create user', async ({ page }) => {
  userId = await createUser()
})

test('update user', async ({ page }) => {
  await updateUser(userId)  // Depends on previous test
})

// Good - each test is independent
test('update user', async ({ page }) => {
  const userId = await createUser()  // Create fresh
  await updateUser(userId)
})
```
