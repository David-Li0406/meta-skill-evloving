<overview>
Testing strategies for Next.js 16 applications. Covers unit tests, integration tests, and E2E tests.
</overview>

<test_types>
| Type | Purpose | Tools | Scope |
|------|---------|-------|-------|
| Unit | Test isolated functions/components | Jest, RTL | Single unit |
| Integration | Test component interactions | Jest, RTL | Multiple units |
| E2E | Test full user flows | Playwright | Entire app |
</test_types>

<jest_setup>
**Install dependencies:**
```bash
npm install -D jest jest-environment-jsdom @testing-library/react @testing-library/jest-dom @types/jest
```

**jest.config.ts:**
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

**jest.setup.ts:**
```typescript
import '@testing-library/jest-dom'
```

**package.json scripts:**
```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  }
}
```
</jest_setup>

<testing_client_components>
**Test Client Components with RTL:**

```tsx
// components/__tests__/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from '../Button'

describe('Button', () => {
  it('renders children', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByRole('button')).toHaveTextContent('Click me')
  })

  it('calls onClick when clicked', () => {
    const onClick = jest.fn()
    render(<Button onClick={onClick}>Click</Button>)

    fireEvent.click(screen.getByRole('button'))

    expect(onClick).toHaveBeenCalledTimes(1)
  })

  it('shows loading state', () => {
    render(<Button loading>Submit</Button>)

    expect(screen.getByRole('button')).toBeDisabled()
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })
})
```

**Test forms:**
```tsx
// components/__tests__/LoginForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { LoginForm } from '../LoginForm'

describe('LoginForm', () => {
  it('submits form data', async () => {
    const user = userEvent.setup()
    const onSubmit = jest.fn()

    render(<LoginForm onSubmit={onSubmit} />)

    await user.type(screen.getByLabelText(/email/i), 'test@example.com')
    await user.type(screen.getByLabelText(/password/i), 'password123')
    await user.click(screen.getByRole('button', { name: /submit/i }))

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      })
    })
  })

  it('shows validation errors', async () => {
    const user = userEvent.setup()

    render(<LoginForm onSubmit={jest.fn()} />)

    await user.click(screen.getByRole('button', { name: /submit/i }))

    expect(screen.getByText(/email is required/i)).toBeInTheDocument()
  })
})
```
</testing_client_components>

<testing_server_components>
**Server Components are async, test differently:**

```tsx
// components/__tests__/ProductList.test.tsx
import { render, screen } from '@testing-library/react'
import { ProductList } from '../ProductList'

// Mock data fetching
jest.mock('@/lib/data', () => ({
  getProducts: jest.fn().mockResolvedValue([
    { id: '1', name: 'Product 1', price: 10 },
    { id: '2', name: 'Product 2', price: 20 },
  ]),
}))

describe('ProductList', () => {
  it('renders products', async () => {
    // Server Component returns JSX
    const Component = await ProductList()
    render(Component)

    expect(screen.getByText('Product 1')).toBeInTheDocument()
    expect(screen.getByText('Product 2')).toBeInTheDocument()
  })
})
```

**Better: Test Server Components via E2E**
Server Components are better tested end-to-end since they integrate with routing, caching, etc.
</testing_server_components>

<testing_server_actions>
**Test Server Actions as functions:**

```typescript
// lib/__tests__/actions.test.ts
import { createProduct } from '../actions'
import { getUser } from '../dal'
import { db } from '@/db'

jest.mock('../dal')
jest.mock('@/db')

describe('createProduct', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('creates product for authenticated admin', async () => {
    (getUser as jest.Mock).mockResolvedValue({
      id: '1',
      role: 'admin',
    })
    ;(db.products.create as jest.Mock).mockResolvedValue({
      id: 'new-id',
    })

    const formData = new FormData()
    formData.append('name', 'New Product')
    formData.append('price', '29.99')

    const result = await createProduct(formData)

    expect(result).toEqual({ success: true })
    expect(db.products.create).toHaveBeenCalledWith({
      data: expect.objectContaining({
        name: 'New Product',
        price: 29.99,
      }),
    })
  })

  it('rejects unauthenticated users', async () => {
    (getUser as jest.Mock).mockResolvedValue(null)

    const formData = new FormData()
    formData.append('name', 'Product')
    formData.append('price', '10')

    await expect(createProduct(formData)).rejects.toThrow('Unauthorized')
  })

  it('validates input', async () => {
    (getUser as jest.Mock).mockResolvedValue({ id: '1', role: 'admin' })

    const formData = new FormData()
    formData.append('name', 'A')  // Too short
    formData.append('price', '10')

    const result = await createProduct(formData)

    expect(result).toEqual({
      error: expect.stringContaining('at least'),
    })
  })
})
```
</testing_server_actions>

<playwright_setup>
**Install Playwright:**
```bash
npm init playwright@latest
```

**playwright.config.ts:**
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
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'mobile',
      use: { ...devices['iPhone 13'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```
</playwright_setup>

<e2e_tests>
**E2E test examples:**

```typescript
// e2e/auth.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Authentication', () => {
  test('login flow', async ({ page }) => {
    await page.goto('/login')

    await page.fill('[name="email"]', 'test@example.com')
    await page.fill('[name="password"]', 'password123')
    await page.click('[type="submit"]')

    await expect(page).toHaveURL('/dashboard')
    await expect(page.getByText('Welcome')).toBeVisible()
  })

  test('redirect to login when not authenticated', async ({ page }) => {
    await page.goto('/dashboard')

    await expect(page).toHaveURL('/login')
  })
})

// e2e/products.spec.ts
test.describe('Products', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login')
    await page.fill('[name="email"]', 'admin@example.com')
    await page.fill('[name="password"]', 'adminpass')
    await page.click('[type="submit"]')
    await page.waitForURL('/dashboard')
  })

  test('create product', async ({ page }) => {
    await page.goto('/products/new')

    await page.fill('[name="name"]', 'Test Product')
    await page.fill('[name="price"]', '29.99')
    await page.click('[type="submit"]')

    await expect(page).toHaveURL('/products')
    await expect(page.getByText('Test Product')).toBeVisible()
  })

  test('delete product', async ({ page }) => {
    await page.goto('/products')

    // Find and delete first product
    await page.getByRole('button', { name: 'Delete' }).first().click()

    // Confirm dialog
    await page.getByRole('button', { name: 'Confirm' }).click()

    // Verify toast/message
    await expect(page.getByText('Product deleted')).toBeVisible()
  })
})
```

**Run E2E tests:**
```bash
npx playwright test
npx playwright test --ui  # Visual mode
npx playwright test --debug  # Debug mode
```
</e2e_tests>

<test_utilities>
**Custom render with providers:**

```tsx
// test-utils/render.tsx
import { render } from '@testing-library/react'
import { ThemeProvider } from '@/providers/ThemeProvider'

export function renderWithProviders(ui: React.ReactElement) {
  return render(
    <ThemeProvider>
      {ui}
    </ThemeProvider>
  )
}
```

**Mock Next.js functions:**
```typescript
// __mocks__/next/navigation.ts
export const useRouter = () => ({
  push: jest.fn(),
  replace: jest.fn(),
  refresh: jest.fn(),
})

export const usePathname = () => '/current-path'
export const useSearchParams = () => new URLSearchParams()
export const redirect = jest.fn()
```
</test_utilities>

<ci_integration>
**GitHub Actions:**

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm test -- --coverage

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npx playwright test

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```
</ci_integration>
