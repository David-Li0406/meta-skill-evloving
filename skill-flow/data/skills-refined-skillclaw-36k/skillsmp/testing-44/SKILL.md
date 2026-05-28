---
name: testing
description: This skill provides Testing Library best practices for the fitness app. Use when writing component tests, API tests, or database tests. Covers user-centric testing patterns, query strategies, and async state handling.
---

# Testing Best Practices

This skill provides guidance for writing user-centric tests using Vitest, Testing Library, and Nuxt Test Utils.

## Core Principles

**User-Centric Philosophy**: Test what users see and do, not implementation details.

**Never Test Implementation**:
- ❌ Don't access `wrapper.vm` or internal component state
- ❌ Don't test props directly
- ❌ Don't query by CSS selectors or test IDs
- ❌ Don't shallow mount components
- ❌ Never include skipped tests with it.skip

**Always Test Behavior**:
- ✅ Query by accessibility (roles, labels, text)
- ✅ Interact like a user (click, type, keyboard)
- ✅ Assert on what users see
- ✅ Full component rendering with dependencies
- ✅ Ensure it works on Mobile and Desktop

## Test Stack

### Component Tests

Use `@nuxt/test-utils/runtime` for Nuxt components:

```typescript
import { renderSuspended } from '@nuxt/test-utils/runtime'
import { screen } from '@testing-library/vue'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, beforeEach } from 'vitest'
import MyComponent from './MyComponent.vue'

describe('MyComponent', () => {
  let user: ReturnType<typeof userEvent.setup>

  beforeEach(() => {
    user = userEvent.setup()
  })

  describe('form rendering', () => {
    it('should display all form fields', async () => {
      await renderSuspended(MyComponent)

      expect(screen.getByLabelText(/email/i)).toBeDefined()
      expect(screen.getByLabelText(/password/i)).toBeDefined()
      expect(screen.getByRole('button', { name: /submit/i })).toBeDefined()
    })
  })

  describe('form input', () => {
    it('should allow user to type in fields', async () => {
      await renderSuspended(MyComponent)

      const emailInput = screen.getByLabelText(/email/i) as HTMLInputElement
      await user.type(emailInput, 'test@example.com')

      expect(emailInput.value).toBe('test@example.com')
    })
  })
})
```

**Key imports:**
- `renderSuspended` - Render component in full Nuxt environment
- `screen` - Query rendered output
- `userEvent` - Simulate realistic user interactions
- Test file naming: `*.nuxt.test.ts` for Nuxt components

**File Naming Convention:**
- Component tests: `*.nuxt.test.ts` (e.g., `Login.nuxt.test.ts`)
- Page tests: `*.nuxt.test.ts` (e.g., `login.nuxt.test.ts`)
- Server/API tests: `*.test.ts` (e.g., `index.get.test.ts`)
- Utility tests: `*.test.ts` (e.g., `format.test.ts`)
- E2E tests: `*.spec.ts` (e.g., `login.spec.ts`)

### API Tests

Test server routes using `$fetch`:

```typescript
import { describe, it, expect, beforeAll } from 'vitest'

describe('/api/workouts', () => {
  let authCookie: string

  beforeAll(async () => {
    // Setup test user session
    const response = await $fetch('/api/auth/login', {
      method: 'POST',
      body: { email: 'test@example.com', password: 'password' }
    })
    authCookie = response.headers.get('set-cookie') || ''
  })

  it('should return user workouts', async () => {
    const workouts = await $fetch('/api/workouts', {
      headers: { cookie: authCookie }
    })

    expect(Array.isArray(workouts)).toBe(true)
    expect(workouts[0]).toHaveProperty('id')
    expect(workouts[0]).toHaveProperty('name')
  })

  it('should return 401 without auth', async () => {
    await expect($fetch('/api/workouts')).rejects.toThrow('401')
  })
})
```

**Key points:**
- Use `$fetch` within tests to call API routes
- Test authentication, validation, errors, and success cases
- Test file naming: `*.test.ts` for API tests

### Database Tests

Test query functions directly:

```typescript
import { describe, it, expect, beforeEach } from 'vitest'
import { db } from '~~/server/database'
import { queryUserWorkouts } from '~~/server/database/queries/workouts'
import { users } from '~~/server/database/schema'

describe('queryUserWorkouts', () => {
  let userId: string

  beforeEach(async () => {
    // Create test user
    const [user] = await db.insert(users).values({
      email: 'test@example.com',
      name: 'Test User'
    }).returning()
    userId = user.id
  })

  it('should return empty array when user has no workouts', async () => {
    const workouts = await queryUserWorkouts(userId)
    expect(workouts).toEqual([])
  })

  it('should enforce RLS - only return user\'s workouts', async () => {
    // Create workout for another user
    const [otherUser] = await db.insert(users).values({
      email: 'other@example.com',
      name: 'Other'
    }).returning()

    // Create workout for other user
    await db.insert(workouts).values({
      userId: otherUser.id,
      name: 'Other\'s Workout'
    })

    // Query should return empty for original user
    const userWorkouts = await queryUserWorkouts(userId)
    expect(userWorkouts).toEqual([])
  })
})
```

**Key points:**
- Test query functions in isolation
- Use transactions for test data
- Verify RLS policies work correctly
- Test file naming: `*.test.ts` for database tests

## Query Priority

Use queries in this order (from Testing Library docs):

1. **getByRole** - Preferred for interactive elements
```typescript
screen.getByRole('button', { name: /sign in/i })
screen.getByRole('link', { name: /forgot password/i })
screen.getByRole('heading', { name: /welcome/i })
screen.getByRole('textbox', { name: /email/i })
```

2. **getByLabelText** - Best for form inputs
```typescript
screen.getByLabelText(/email/i)
screen.getByLabelText(/password/i)
```

3. **getByPlaceholderText** - When label isn't available
```typescript
screen.getByPlaceholderText(/enter your email/i)
```

4. **getByText** - For non-interactive text
```typescript
screen.getByText(/welcome back/i)
screen.getByText(/successfully logged in/i)
```

5. **getByTestId** - Last resort only (avoid if possible)
```typescript
screen.getByTestId('submit-button') // Use getByRole instead
```

**Query variants:**
- `getBy*` - Throws if not found, throws if multiple
- `queryBy*` - Returns null if not found
- `findBy*` - Async, waits for element to appear

**Regex matching:**
Always use case-insensitive regex for text matching:
```typescript
// ✅ Good
screen.getByText(/sign in/i)
screen.getByRole('button', { name: /submit/i })

// ❌ Bad
screen.getByText('Sign In') // Breaks if text changes
```

## Common Test Patterns

### Pattern 1: Form Submission

Test user filling out and submitting a form:

```typescript
describe('login form', () => {
  let user: ReturnType<typeof userEvent.setup>

  beforeEach(() => {
    user = userEvent.setup()
  })

  it('should submit form with valid credentials', async () => {
    const navigateTo = vi.fn()
    vi.stubGlobal('navigateTo', navigateTo)

    await renderSuspended(LoginForm)

    // Fill form
    await user.type(screen.getByLabelText(/email/i), 'test@example.com')
    await user.type(screen.getByLabelText(/password/i), 'password123')

    // Submit
    await user.click(screen.getByRole('button', { name: /sign in/i }))

    // Assert navigation
    await waitFor(() => {
      expect(navigateTo).toHaveBeenCalledWith('/dashboard')
    })
  })
})
```

### Pattern 2: Interactive Elements

Test buttons, toggles, and other interactive elements:

```typescript
describe('password visibility toggle', () => {
  it('should toggle password visibility', async () => {
    await renderSuspended(LoginForm)

    const passwordInput = screen.getByLabelText(/password/i) as HTMLInputElement
    const toggleButton = screen.getByRole('button', { name: /show password/i })

    expect(passwordInput.type).toBe('password')

    await user.click(toggleButton)
    expect(passwordInput.type).toBe('text')

    await user.click(toggleButton)
    expect(passwordInput.type).toBe('password')
  })
})
```

### Pattern 3: Conditional Rendering

Test components that show/hide based on state:

```typescript
it('should show success message after submission', async () => {
  await renderSuspended(ForgotPasswordForm)

  // Initially no success message
  expect(screen.queryByText(/check your email/i)).toBeNull()

  // Submit form
  await user.type(screen.getByLabelText(/email/i), 'test@example.com')
  await user.click(screen.getByRole('button', { name: /send/i }))

  // Success message appears
  await waitFor(() => {
    expect(screen.getByText(/check your email/i)).toBeDefined()
  })

  // Form is hidden
  expect(screen.queryByLabelText(/email/i)).toBeNull()
})
```

### Pattern 4: Navigation

Test links and navigation behavior:

```typescript
it('should navigate to signup page', async () => {
  await renderSuspended(LoginPage)

  const signupLink = screen.getByRole('link', { name: /create account/i })
  expect(signupLink.getAttribute('href')).toBe('/signup')
})

it('should redirect if already logged in', async () => {
  const navigateTo = vi.fn()
  vi.stubGlobal('navigateTo', navigateTo)

  // Mock logged in state
  mockNuxtImport('useUserSession', () => ({
    loggedIn: ref(true)
  }))

  await renderSuspended(LoginPage)

  await waitFor(() => {
    expect(navigateTo).toHaveBeenCalledWith('/')
  })
})
```

### Pattern 5: Multi-Step Flows

Test wizards and multi-step forms:

```typescript
it('should progress through email and OTP steps', async () => {
  await renderSuspended(EmailOtpPage)

  // Step 1: Email form visible
  expect(screen.getByLabelText(/email/i)).toBeDefined()
  expect(screen.queryByLabelText(/verification code/i)).toBeNull()

  // Submit email
  await user.type(screen.getByLabelText(/email/i), 'test@example.com')
  await user.click(screen.getByRole('button', { name: /send code/i }))

  // Step 2: OTP form visible
  await waitFor(() => {
    expect(screen.queryByLabelText(/email/i)).toBeNull()
    expect(screen.getByLabelText(/verification code/i)).toBeDefined()
  })
})
```

## Async State Handling

**Always test all four states**: loading, error, empty, and success.

### Loading State

```typescript
it('should show loading state during submission', async () => {
  await renderSuspended(LoginForm)

  const submitButton = screen.getByRole('button', { name: /sign in/i })

  // Initially not disabled
  expect(submitButton.disabled).toBe(false)

  // Fill and submit
  await user.type(screen.getByLabelText(/email/i), 'test@example.com')
  await user.type(screen.getByLabelText(/password/i), 'password')
  await user.click(submitButton)

  // Button disabled during loading
  expect(submitButton.disabled).toBe(true)
  expect(screen.getByText(/signing in/i)).toBeDefined()
})
```

### Error State

```typescript
it('should show error message on API failure', async () => {
  // Mock API error
  vi.mocked($fetch).mockRejectedValueOnce(new Error('Invalid credentials'))

  await renderSuspended(LoginForm)

  await user.type(screen.getByLabelText(/email/i), 'test@example.com')
  await user.type(screen.getByLabelText(/password/i), 'wrong')
  await user.click(screen.getByRole('button', { name: /sign in/i }))

  await waitFor(() => {
    expect(screen.getByText(/invalid credentials/i)).toBeDefined()
  })
})
```

### Empty State

```typescript
it('should show empty state when no data', async () => {
  // Mock empty response
  vi.mocked($fetch).mockResolvedValueOnce([])

  await renderSuspended(WorkoutList)

  await waitFor(() => {
    expect(screen.getByText(/no workouts yet/i)).toBeDefined()
    expect(screen.getByRole('button', { name: /create workout/i })).toBeDefined()
  })
})
```

### Success State

```typescript
it('should display data when loaded', async () => {
  // Mock successful response
  vi.mocked($fetch).mockResolvedValueOnce([
    { id: '1', name: 'Morning Workout' },
    { id: '2', name: 'Evening Workout' }
  ])

  await renderSuspended(WorkoutList)

  await waitFor(() => {
    expect(screen.getByText(/morning workout/i)).toBeDefined()
    expect(screen.getByText(/evening workout/i)).toBeDefined()
  })
})
```

## Mocking Strategies

### Mock Nuxt Composables

```typescript
import { mockNuxtImport } from '@nuxt/test-utils/runtime'

mockNuxtImport('useUserSession', () => ({
  user: ref({ id: '1', email: 'test@example.com' }),
  loggedIn: ref(true),
  clear: vi.fn()
}))

mockNuxtImport('useToast', () => ({
  message: vi.fn()
}))
```

### Mock $fetch

```typescript
import { vi } from 'vitest'

vi.mock('#app', () => ({
  $fetch: vi.fn()
}))

// In test
vi.mocked($fetch).mockResolvedValueOnce({ success: true, data: {} })
```

### Mock navigateTo

```typescript
const navigateTo = vi.fn()
vi.stubGlobal('navigateTo', navigateTo)

// Assert
expect(navigateTo).toHaveBeenCalledWith('/dashboard')
```

## Test Organization

Group tests with `describe` blocks using **lowercase** naming:

```typescript
describe('component name', () => {
  let user: ReturnType<typeof userEvent.setup>

  beforeEach(() => {
    user = userEvent.setup()
  })

  describe('form rendering', () => {
    it('should display heading', async () => { /* ... */ })
    it('should display all form fields', async () => { /* ... */ })
    it('should display submit button', async () => { /* ... */ })
  })

  describe('form input', () => {
    it('should allow user to type email', async () => { /* ... */ })
    it('should allow user to type password', async () => { /* ... */ })
  })

  describe('form validation', () => {
    it('should show error for invalid email', async () => { /* ... */ })
    it('should show error for short password', async () => { /* ... */ })
  })

  describe('form submission', () => {
    it('should submit with valid data', async () => { /* ... */ })
    it('should show error on API failure', async () => { /* ... */ })
    it('should redirect on success', async () => { /* ... */ })
  })
})
```

**IMPORTANT: Naming Convention**
- Main `describe()` block: Use **lowercase with spaces** (e.g., `describe('component name', ...)` or `describe('page name', ...)`)
- Nested `describe()` blocks: Use **lowercase with spaces** (e.g., `describe('form rendering', ...)`)
- Test descriptions: Always start with "should" and describe behavior

**Common group names (lowercase):**
- form rendering
- form input
- form validation
- form submission
- interactive elements
- navigation
- loading states
- error handling
- conditional rendering
- password visibility toggle
- alternative login/signup methods
- initial values

## Common Pitfalls

### ❌ Pitfall 1: Testing Props

```typescript
// Wrong
it('accepts email prop', () => {
  const wrapper = mount(Component, { props: { email: 'test@example.com' } })
  expect(wrapper.props('email')).toBe('test@example.com')
})

// Right
it('should display email in message', async () => {
  await renderSuspended(Component, { props: { email: 'test@example.com' } })
  expect(screen.getByText(/test@example\.com/i)).toBeDefined()
})
```

### ❌ Pitfall 2: Accessing Internal State

```typescript
// Wrong
it('has loading state', () => {
  const wrapper = mount(Component)
  expect(wrapper.vm.isLoading).toBe(false)
})

// Right
it('should show loading spinner', async () => {
  await renderSuspended(Component)
  // Trigger loading state
  await user.click(screen.getByRole('button', { name: /submit/i }))
  expect(screen.getByRole('status', { name: /loading/i })).toBeDefined()
})
```

### ❌ Pitfall 3: Empty Smoke Tests

```typescript
// Wrong
it('renders', () => {
  const wrapper = mount(Component)
  expect(wrapper.exists()).toBe(true)
})

// Right
it('should display form heading and inputs', async () => {
  await renderSuspended(Component)
  expect(screen.getByRole('heading', { name: /sign in/i })).toBeDefined()
  expect(screen.getByLabelText(/email/i)).toBeDefined()
  expect(screen.getByLabelText(/password/i)).toBeDefined()
})
```

### ❌ Pitfall 4: Using CSS Selectors

```typescript
// Wrong
const button = wrapper.find('.submit-btn')
const input = wrapper.find('#email-input')

// Right
const button = screen.getByRole('button', { name: /submit/i })
const input = screen.getByLabelText(/email/i)
```

### ❌ Pitfall 5: Not Handling Async

```typescript
// Wrong
it('should show success message', async () => {
  await renderSuspended(Component)
  await user.click(screen.getByRole('button'))
  expect(screen.getByText(/success/i)).toBeDefined() // May fail
})

// Right
it('should show success message', async () => {
  await renderSuspended(Component)
  await user.click(screen.getByRole('button'))
  await waitFor(() => {
    expect(screen.getByText(/success/i)).toBeDefined()
  })
})
```

## Running Tests

### Vitest (Unit & Component Tests)

```bash
# Run all tests
pnpm test

# Run tests in watch mode
pnpm test:watch

# Run tests with UI
pnpm test:ui

# Run tests with coverage
pnpm test:coverage

# Run specific test file
pnpm test path/to/file.test.ts

# Run specific project (unit or nuxt)
pnpm test --project=unit
pnpm test --project=nuxt

# Run tests matching pattern
pnpm test --grep "should submit form"
```

### Playwright (E2E Tests)

```bash
# Run all E2E tests
pnpm test:e2e

# Run E2E tests in headed mode (browser visible)
HEADED=true pnpm test:e2e

# Run specific E2E test file
pnpm test:e2e tests/e2e/auth/login.spec.ts

# View E2E test report
pnpm exec playwright show-report
```

## Test Configuration

### Vitest Setup

- **Config file:** `vitest.config.ts`
- **Setup file:** `vitest.setup.ts`
- **Two test projects:**
  - `unit`: Node environment for server/shared utils
  - `nuxt`: Nuxt environment for components/pages
- **Coverage:** V8 provider with multiple reporters (text, json, html, clover)

### Playwright Setup

- **Config file:** `playwright.config.ts`
- **Test directory:** `./tests/e2e`
- **Base URL:** `http://localhost:3000`
- **Browser:** Chromium (Desktop Chrome)
- **Workers:** 6 locally, 1 in CI
- **Retries:** 0 locally, 2 in CI

## Coverage Thresholds

Current thresholds (as of latest config):
- Statements: 56.08%
- Branches: 37.5%
- Functions: 53.7%
- Lines: 56.18%

Check coverage:
```bash
pnpm test:coverage
```

## E2E Testing Patterns

### Test Helpers

Use shared helper functions for common operations:

**Auth Helpers** (`tests/helpers/auth.ts`):
```typescript
import { loginAsTestUser, logout, registerNewUser } from './helpers/auth'

test('should login successfully', async ({ page }) => {
  await loginAsTestUser(page, 'josephanson@hotmail.co.uk', 'Testtest1')
  await expect(page).toHaveURL(/\/feed/)
})

test('should logout successfully', async ({ page }) => {
  await loginAsTestUser(page)
  await logout(page)
  await expect(page).toHaveURL('/')
})
```

**Test Fixtures** (`tests/fixtures/users.ts`):
```typescript
import { testUser, adminUser, newUser } from '../../fixtures/users'

test('should login with test user', async ({ page }) => {
  await loginAsTestUser(page, testUser.email, testUser.password)
})
```

### E2E Test Structure

```typescript
import { expect, test } from '@playwright/test'
import { testUser } from '../../fixtures/users'
import { loginAsTestUser } from '../../helpers/auth'

test.describe('Feature Name', () => {
  test('should perform user action', async ({ page }) => {
    // Setup
    await loginAsTestUser(page, testUser.email, testUser.password)

    // Action
    await page.getByRole('button', { name: /click me/i }).click()

    // Assert
    await expect(page).toHaveURL(/\/expected-url/)
  })
})
```

### E2E Best Practices

1. **Use Test Helpers:** Reuse `loginAsTestUser`, `logout`, and other helpers
2. **Use Fixtures:** Import user data from `tests/fixtures/users.ts`
3. **Wait for States:** Use `waitForLoadState('networkidle')` and `waitForURL()`
4. **Accessible Queries:** Use `getByRole`, `getByPlaceholder`, `getByText` when possible
5. **Timeouts:** Set appropriate timeouts for async operations
6. **Clean State:** E2E tests should handle authentication state properly

## Mocking in Component Tests

### Mock `$fetchResult`

For components that use `$fetchResult` (custom fetch wrapper):

```typescript
const mockFetchResult = vi.fn()
vi.stubGlobal('$fetchResult', mockFetchResult)

beforeEach(() => {
  vi.clearAllMocks()
  mockFetchResult.mockResolvedValue({ success: true })
})

// In test
await waitFor(() => {
  expect($fetchResult).toHaveBeenCalledWith(
    '/api/endpoint',
    expect.objectContaining({
      method: 'PUT',
      body: expect.objectContaining({
        field: 'value',
      }),
    }),
  )
})
```

### Working with Portals and UISelect

When testing Shadcn UISelect components that render options in portals:

```typescript
it('should show options when clicked', async () => {
  await renderSuspended(Component)

  const selects = screen.getAllByRole('combobox')
  await user.click(selects[0])

  // Wait for portal rendering - options render in body
  await waitFor(() => {
    const options = screen.queryAllByRole('option')
    expect(options.length).toBeGreaterThan(0)
  }, { timeout: 1000 })

  expect(screen.getByRole('option', { name: /option text/i })).toBeDefined()
})
```

## Additional Resources

For detailed migration examples, see:
- `.claude/specs/05-test-coverage-improvement/MIGRATION-PATTERNS.md` - Before/after examples
- `.claude/specs/05-test-coverage-improvement/design.md` - Test patterns and architecture
- [Testing Library Docs](https://testing-library.com/docs/vue-testing-library/intro)
- [Nuxt Test Utils](https://nuxt.com/docs/getting-started/testing)
- [Playwright Docs](https://playwright.dev/docs/intro)
