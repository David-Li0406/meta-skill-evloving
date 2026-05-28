<workflow name="write-tests">
<title>Write Tests for Next.js 16 App</title>

<required_reading>
**Read these reference files NOW:**
1. references/testing.md
2. references/server-client-components.md
</required_reading>

<process>

<step name="1-setup-testing">
<title>Set Up Testing Infrastructure</title>

**Install Jest and React Testing Library:**
```bash
npm install -D jest jest-environment-jsdom @testing-library/react @testing-library/jest-dom @types/jest
```

**Create jest.config.ts:**
```typescript
import type { Config } from 'jest'
import nextJest from 'next/jest'

const createJestConfig = nextJest({
  dir: './',
})

const config: Config = {
  coverageProvider: 'v8',
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
  testPathIgnorePatterns: ['<rootDir>/e2e/'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
}

export default createJestConfig(config)
```

**Create jest.setup.ts:**
```typescript
import '@testing-library/jest-dom'
```

**Add test script to package.json:**
```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  }
}
```
</step>

<step name="2-setup-e2e-testing">
<title>Set Up E2E Testing (Playwright)</title>

```bash
npm init playwright@latest
```

**Configure playwright.config.ts:**
```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```
</step>

<step name="3-test-client-components">
<title>Test Client Components</title>

```typescript
// components/__tests__/Counter.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { Counter } from '../Counter'

describe('Counter', () => {
  it('renders initial count', () => {
    render(<Counter initialCount={0} />)
    expect(screen.getByText('Count: 0')).toBeInTheDocument()
  })

  it('increments count on click', () => {
    render(<Counter initialCount={0} />)
    const button = screen.getByRole('button', { name: /increment/i })

    fireEvent.click(button)

    expect(screen.getByText('Count: 1')).toBeInTheDocument()
  })

  it('calls onChange when count changes', () => {
    const onChange = jest.fn()
    render(<Counter initialCount={0} onChange={onChange} />)
    const button = screen.getByRole('button', { name: /increment/i })

    fireEvent.click(button)

    expect(onChange).toHaveBeenCalledWith(1)
  })
})
```
</step>

<step name="4-test-server-components">
<title>Test Server Components</title>

**Testing Server Components requires async rendering:**

```typescript
// components/__tests__/ProductList.test.tsx
import { render, screen } from '@testing-library/react'
import { ProductList } from '../ProductList'

// Mock the data fetching
jest.mock('@/lib/data', () => ({
  getProducts: jest.fn().mockResolvedValue([
    { id: '1', name: 'Product 1', price: 10 },
    { id: '2', name: 'Product 2', price: 20 },
  ]),
}))

describe('ProductList', () => {
  it('renders products', async () => {
    // Server Components are async
    const Component = await ProductList()
    render(Component)

    expect(screen.getByText('Product 1')).toBeInTheDocument()
    expect(screen.getByText('Product 2')).toBeInTheDocument()
  })
})
```

**Alternative: Test at page level with E2E**
Server Components are often better tested with E2E tests.
</step>

<step name="5-test-server-actions">
<title>Test Server Actions</title>

```typescript
// lib/__tests__/actions.test.ts
import { createProduct } from '../actions'
import { getUser } from '../dal'

// Mock dependencies
jest.mock('../dal')
jest.mock('@/db', () => ({
  products: {
    create: jest.fn(),
  },
}))

describe('createProduct', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('creates product when user is admin', async () => {
    (getUser as jest.Mock).mockResolvedValue({ id: '1', role: 'admin' })

    const formData = new FormData()
    formData.append('name', 'New Product')
    formData.append('price', '29.99')

    const result = await createProduct(formData)

    expect(result).toEqual({ success: true })
  })

  it('returns error when user is not admin', async () => {
    (getUser as jest.Mock).mockResolvedValue({ id: '1', role: 'user' })

    const formData = new FormData()
    formData.append('name', 'New Product')
    formData.append('price', '29.99')

    await expect(createProduct(formData)).rejects.toThrow('Unauthorized')
  })

  it('returns error for invalid input', async () => {
    (getUser as jest.Mock).mockResolvedValue({ id: '1', role: 'admin' })

    const formData = new FormData()
    formData.append('name', 'A')  // Too short
    formData.append('price', '29.99')

    const result = await createProduct(formData)

    expect(result).toEqual({ error: 'Name must be at least 2 characters' })
  })
})
```
</step>

<step name="6-test-data-access-layer">
<title>Test Data Access Layer</title>

```typescript
// lib/__tests__/dal.test.ts
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'
import { getUser, getProtectedData } from '../dal'

jest.mock('next/headers')
jest.mock('next/navigation')

describe('Data Access Layer', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  describe('getUser', () => {
    it('returns user when session is valid', async () => {
      const mockCookies = {
        get: jest.fn().mockReturnValue({ value: 'valid-session' }),
      }
      ;(cookies as jest.Mock).mockResolvedValue(mockCookies)

      // Mock session verification
      jest.spyOn(global, 'verifySession' as any).mockResolvedValue({
        id: '1',
        name: 'Test User',
      })

      const user = await getUser()

      expect(user).toEqual({ id: '1', name: 'Test User' })
    })

    it('returns null when no session cookie', async () => {
      const mockCookies = {
        get: jest.fn().mockReturnValue(undefined),
      }
      ;(cookies as jest.Mock).mockResolvedValue(mockCookies)

      const user = await getUser()

      expect(user).toBeNull()
    })
  })

  describe('getProtectedData', () => {
    it('redirects when user not authenticated', async () => {
      const mockCookies = {
        get: jest.fn().mockReturnValue(undefined),
      }
      ;(cookies as jest.Mock).mockResolvedValue(mockCookies)

      await getProtectedData()

      expect(redirect).toHaveBeenCalledWith('/login')
    })
  })
})
```
</step>

<step name="7-write-e2e-tests">
<title>Write E2E Tests</title>

```typescript
// e2e/auth.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Authentication', () => {
  test('redirects to login when not authenticated', async ({ page }) => {
    await page.goto('/dashboard')

    await expect(page).toHaveURL('/login')
  })

  test('allows login with valid credentials', async ({ page }) => {
    await page.goto('/login')

    await page.fill('[name="email"]', 'test@example.com')
    await page.fill('[name="password"]', 'password123')
    await page.click('button[type="submit"]')

    await expect(page).toHaveURL('/dashboard')
    await expect(page.getByText('Welcome')).toBeVisible()
  })
})

// e2e/products.spec.ts
test.describe('Products', () => {
  test('displays product list', async ({ page }) => {
    await page.goto('/products')

    await expect(page.getByRole('heading', { name: 'Products' })).toBeVisible()
    await expect(page.getByRole('listitem')).toHaveCount.greaterThan(0)
  })

  test('adds product to cart', async ({ page }) => {
    // Login first
    await page.goto('/login')
    await page.fill('[name="email"]', 'test@example.com')
    await page.fill('[name="password"]', 'password123')
    await page.click('button[type="submit"]')

    // Add to cart
    await page.goto('/products')
    await page.click('button:has-text("Add to Cart")')

    // Verify cart updated
    await expect(page.getByText('Cart (1)')).toBeVisible()
  })
})
```
</step>

<step name="8-run-tests">
<title>Run Tests</title>

```bash
# Run unit tests
npm test

# Run with coverage
npm run test:coverage

# Run E2E tests
npx playwright test

# Run E2E tests with UI
npx playwright test --ui

# Run specific test file
npm test -- Counter.test.tsx
npx playwright test auth.spec.ts
```
</step>

</process>

<testing_strategy>
**What to test where:**

| Type | Test With | Example |
|------|-----------|---------|
| Client Components | Jest + RTL | Buttons, forms, interactive UI |
| Server Components | E2E or integration | Data display, layouts |
| Server Actions | Jest (unit) | Business logic, validation |
| Data Access Layer | Jest (unit) | Auth checks, data fetching |
| Full user flows | Playwright (E2E) | Login, checkout, CRUD |
| API Routes | Jest or Playwright | REST endpoints |
</testing_strategy>

<anti_patterns>
**Avoid:**
- Testing implementation details instead of behavior
- Mocking too much (test real behavior when possible)
- Skipping auth tests for Server Actions
- Only testing happy paths
- Not testing loading and error states
</anti_patterns>

<success_criteria>
Testing is complete when:
- [ ] Unit tests for Client Components
- [ ] Unit tests for Server Actions
- [ ] Unit tests for Data Access Layer
- [ ] E2E tests for critical user flows
- [ ] Coverage meets target (e.g., 80%)
- [ ] All tests pass
- [ ] Tests run in CI pipeline
</success_criteria>

</workflow>
