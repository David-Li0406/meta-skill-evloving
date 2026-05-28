---
name: testing-patterns
description: Testing patterns for unit, integration, and E2E tests. Mock patterns for Supabase, Redis, OpenAI. Use when writing tests or setting up test infrastructure.
---

# Testing Patterns

Comprehensive testing patterns including unit tests, integration tests, E2E tests, and mocking strategies for common services.

## When to Use

- Writing new features (TDD)
- Testing API endpoints
- Testing React components
- Mocking external services
- Setting up E2E tests
- Verifying user flows

## Test Types Overview

| Test Type | Scope | Speed | Examples |
|-----------|-------|-------|----------|
| Unit | Individual functions/components | Fast (< 50ms) | Pure functions, utilities, hooks |
| Integration | Multiple components/modules | Medium (< 1s) | API endpoints, database operations |
| E2E | Complete user flows | Slow (2-10s) | Login flow, checkout, search |

## Unit Testing Patterns

### Testing Pure Functions

```typescript
// src/lib/utils.ts
export function calculateProbability(yesVotes: number, noVotes: number): number {
  const total = yesVotes + noVotes
  if (total === 0) return 0.5
  return yesVotes / total
}

// src/lib/utils.test.ts
import { calculateProbability } from './utils'

describe('calculateProbability', () => {
  it('returns 0.5 for equal votes', () => {
    expect(calculateProbability(10, 10)).toBe(0.5)
  })

  it('returns 0.5 for zero votes', () => {
    expect(calculateProbability(0, 0)).toBe(0.5)
  })

  it('calculates correct probability for yes bias', () => {
    expect(calculateProbability(75, 25)).toBe(0.75)
  })

  it('calculates correct probability for no bias', () => {
    expect(calculateProbability(25, 75)).toBe(0.25)
  })

  it('handles edge case of one vote', () => {
    expect(calculateProbability(1, 0)).toBe(1)
    expect(calculateProbability(0, 1)).toBe(0)
  })
})
```

### Testing React Components

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MarketCard } from './MarketCard'

describe('MarketCard', () => {
  const mockMarket = {
    id: '1',
    name: 'Test Market',
    description: 'Test description',
    endDate: new Date('2025-12-31')
  }

  it('renders market information', () => {
    render(<MarketCard {...mockMarket} />)

    expect(screen.getByText('Test Market')).toBeInTheDocument()
    expect(screen.getByText('Test description')).toBeInTheDocument()
  })

  it('calls onBet when yes button clicked', async () => {
    const onBet = jest.fn()
    render(<MarketCard {...mockMarket} onBet={onBet} />)

    const yesButton = screen.getByRole('button', { name: /bet yes/i })
    await userEvent.click(yesButton)

    expect(onBet).toHaveBeenCalledWith('1', 'yes')
    expect(onBet).toHaveBeenCalledTimes(1)
  })

  it('disables buttons while loading', async () => {
    const onBet = jest.fn(() => new Promise(resolve => setTimeout(resolve, 100)))
    render(<MarketCard {...mockMarket} onBet={onBet} />)

    const yesButton = screen.getByRole('button', { name: /bet yes/i })
    await userEvent.click(yesButton)

    expect(yesButton).toBeDisabled()
    expect(screen.getByRole('button', { name: /bet no/i })).toBeDisabled()

    await waitFor(() => {
      expect(yesButton).not.toBeDisabled()
    })
  })

  it('shows loading spinner during bet', async () => {
    const onBet = jest.fn(() => new Promise(resolve => setTimeout(resolve, 100)))
    render(<MarketCard {...mockMarket} onBet={onBet} />)

    await userEvent.click(screen.getByRole('button', { name: /bet yes/i }))

    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument()

    await waitFor(() => {
      expect(screen.queryByTestId('loading-spinner')).not.toBeInTheDocument()
    })
  })
})
```

### Testing Custom Hooks

```typescript
import { renderHook, waitFor } from '@testing-library/react'
import { useDebounce } from './useDebounce'

describe('useDebounce', () => {
  beforeEach(() => {
    jest.useFakeTimers()
  })

  afterEach(() => {
    jest.useRealTimers()
  })

  it('returns initial value immediately', () => {
    const { result } = renderHook(() => useDebounce('test', 500))
    expect(result.current).toBe('test')
  })

  it('debounces value changes', () => {
    const { result, rerender } = renderHook(
      ({ value, delay }) => useDebounce(value, delay),
      { initialProps: { value: 'initial', delay: 500 } }
    )

    expect(result.current).toBe('initial')

    // Update value
    rerender({ value: 'updated', delay: 500 })

    // Value should not change immediately
    expect(result.current).toBe('initial')

    // Fast-forward time
    jest.advanceTimersByTime(500)

    // Value should now be updated
    waitFor(() => {
      expect(result.current).toBe('updated')
    })
  })

  it('cancels pending debounce on unmount', () => {
    const { unmount } = renderHook(() => useDebounce('test', 500))

    unmount()

    // Verify no errors and cleanup happened
    jest.advanceTimersByTime(500)
  })
})
```

## Integration Testing Patterns

### Testing API Routes

```typescript
// app/api/markets/route.test.ts
import { NextRequest } from 'next/server'
import { GET, POST } from './route'

// Mock database
jest.mock('@/lib/db', () => ({
  markets: {
    findMany: jest.fn(),
    create: jest.fn()
  }
}))

import { db } from '@/lib/db'

describe('GET /api/markets', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('returns markets successfully', async () => {
    const mockMarkets = [
      { id: '1', name: 'Market 1' },
      { id: '2', name: 'Market 2' }
    ]

    ;(db.markets.findMany as jest.Mock).mockResolvedValue(mockMarkets)

    const request = new NextRequest('http://localhost/api/markets')
    const response = await GET(request)
    const data = await response.json()

    expect(response.status).toBe(200)
    expect(data.success).toBe(true)
    expect(data.data).toEqual(mockMarkets)
  })

  it('validates pagination parameters', async () => {
    const request = new NextRequest('http://localhost/api/markets?page=0')
    const response = await GET(request)

    expect(response.status).toBe(400)
  })

  it('handles database errors', async () => {
    ;(db.markets.findMany as jest.Mock).mockRejectedValue(
      new Error('Database error')
    )

    const request = new NextRequest('http://localhost/api/markets')
    const response = await GET(request)

    expect(response.status).toBe(500)
  })
})

describe('POST /api/markets', () => {
  it('creates market with valid data', async () => {
    const newMarket = {
      name: 'New Market',
      description: 'Test description',
      category: 'politics',
      endDate: '2025-12-31T00:00:00Z'
    }

    ;(db.markets.create as jest.Mock).mockResolvedValue({
      id: '1',
      ...newMarket
    })

    const request = new NextRequest('http://localhost/api/markets', {
      method: 'POST',
      body: JSON.stringify(newMarket)
    })

    const response = await POST(request)
    const data = await response.json()

    expect(response.status).toBe(201)
    expect(data.success).toBe(true)
    expect(db.markets.create).toHaveBeenCalledWith({
      data: newMarket
    })
  })

  it('rejects invalid data', async () => {
    const invalidMarket = {
      name: 'ab', // Too short
      description: 'short'
    }

    const request = new NextRequest('http://localhost/api/markets', {
      method: 'POST',
      body: JSON.stringify(invalidMarket)
    })

    const response = await POST(request)

    expect(response.status).toBe(400)
    expect(db.markets.create).not.toHaveBeenCalled()
  })
})
```

## Mocking External Services

### Supabase Mock

```typescript
// __mocks__/@supabase/supabase-js.ts
export const createClient = jest.fn(() => ({
  from: jest.fn((table: string) => ({
    select: jest.fn(() => ({
      eq: jest.fn(() => Promise.resolve({
        data: [{ id: '1', name: 'Test' }],
        error: null
      })),
      single: jest.fn(() => Promise.resolve({
        data: { id: '1', name: 'Test' },
        error: null
      }))
    })),
    insert: jest.fn(() => Promise.resolve({
      data: { id: '1', name: 'New Item' },
      error: null
    })),
    update: jest.fn(() => ({
      eq: jest.fn(() => Promise.resolve({
        data: { id: '1', name: 'Updated' },
        error: null
      }))
    })),
    delete: jest.fn(() => ({
      eq: jest.fn(() => Promise.resolve({
        data: null,
        error: null
      }))
    }))
  })),
  auth: {
    getSession: jest.fn(() => Promise.resolve({
      data: { session: { user: { id: '1' } } },
      error: null
    })),
    signInWithPassword: jest.fn(() => Promise.resolve({
      data: { user: { id: '1', email: 'test@example.com' } },
      error: null
    })),
    signOut: jest.fn(() => Promise.resolve({ error: null }))
  }
}))
```

### Redis Mock

```typescript
// __mocks__/ioredis.ts
export default class Redis {
  private store = new Map<string, string>()

  async get(key: string): Promise<string | null> {
    return this.store.get(key) || null
  }

  async set(key: string, value: string): Promise<'OK'> {
    this.store.set(key, value)
    return 'OK'
  }

  async setex(key: string, seconds: number, value: string): Promise<'OK'> {
    this.store.set(key, value)
    // In real app, would expire after seconds
    return 'OK'
  }

  async del(key: string): Promise<number> {
    const existed = this.store.has(key)
    this.store.delete(key)
    return existed ? 1 : 0
  }

  async exists(key: string): Promise<number> {
    return this.store.has(key) ? 1 : 0
  }

  async hset(key: string, field: string, value: string): Promise<number> {
    const hash = JSON.parse(this.store.get(key) || '{}')
    hash[field] = value
    this.store.set(key, JSON.stringify(hash))
    return 1
  }

  async hget(key: string, field: string): Promise<string | null> {
    const hash = JSON.parse(this.store.get(key) || '{}')
    return hash[field] || null
  }

  async quit(): Promise<'OK'> {
    this.store.clear()
    return 'OK'
  }
}
```

### OpenAI Mock

```typescript
// __mocks__/openai.ts
export class OpenAI {
  embeddings = {
    create: jest.fn(async ({ input }: { input: string }) => ({
      data: [
        {
          embedding: new Array(1536).fill(0).map(() => Math.random()),
          index: 0
        }
      ],
      model: 'text-embedding-ada-002',
      usage: {
        prompt_tokens: 10,
        total_tokens: 10
      }
    }))
  }

  chat = {
    completions: {
      create: jest.fn(async ({ messages }: { messages: any[] }) => ({
        id: 'chatcmpl-123',
        object: 'chat.completion',
        created: Date.now(),
        model: 'gpt-4',
        choices: [
          {
            index: 0,
            message: {
              role: 'assistant',
              content: 'Mock AI response'
            },
            finish_reason: 'stop'
          }
        ],
        usage: {
          prompt_tokens: 50,
          completion_tokens: 10,
          total_tokens: 60
        }
      }))
    }
  }
}

export default OpenAI
```

### Testing with Mocked Services

```typescript
// lib/search.test.ts
import { searchMarkets } from './search'

jest.mock('ioredis')
jest.mock('@supabase/supabase-js')
jest.mock('openai')

import Redis from 'ioredis'
import { createClient } from '@supabase/supabase-js'
import OpenAI from 'openai'

describe('searchMarkets', () => {
  let redis: Redis
  let supabase: ReturnType<typeof createClient>
  let openai: OpenAI

  beforeEach(() => {
    redis = new Redis()
    supabase = createClient('url', 'key')
    openai = new OpenAI({ apiKey: 'test' })
  })

  it('uses vector search when Redis available', async () => {
    const results = await searchMarkets('election')

    expect(openai.embeddings.create).toHaveBeenCalledWith({
      input: 'election',
      model: 'text-embedding-ada-002'
    })

    expect(results.method).toBe('semantic')
  })

  it('falls back to full-text search when Redis fails', async () => {
    // Mock Redis failure
    jest.spyOn(redis, 'get').mockRejectedValue(new Error('Redis down'))

    const results = await searchMarkets('election')

    expect(results.method).toBe('fulltext')
  })

  it('uses substring search as last resort', async () => {
    // Mock both Redis and Supabase failures
    jest.spyOn(redis, 'get').mockRejectedValue(new Error('Redis down'))
    const mockSupabase = supabase as any
    mockSupabase.from().select().textSearch = jest.fn(() =>
      Promise.reject(new Error('Supabase error'))
    )

    const results = await searchMarkets('election')

    expect(results.method).toBe('substring')
  })
})
```

## E2E Testing with Playwright

### Setup

```typescript
// playwright.config.ts
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
    screenshot: 'only-on-failure'
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] }
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] }
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] }
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] }
    }
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI
  }
})
```

### E2E Test Patterns

```typescript
// e2e/markets.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Markets Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('displays list of markets', async ({ page }) => {
    await expect(page.locator('h1')).toContainText('Markets')

    const markets = page.locator('[data-testid="market-card"]')
    await expect(markets).toHaveCount(10, { timeout: 5000 })
  })

  test('search filters markets', async ({ page }) => {
    // Navigate to markets
    await page.click('a[href="/markets"]')

    // Search for specific term
    await page.fill('input[placeholder="Search markets"]', 'election')

    // Wait for debounce and results
    await page.waitForTimeout(600)

    // Verify filtered results
    const results = page.locator('[data-testid="market-card"]')
    await expect(results).toHaveCount(5)

    // Verify all results contain search term
    const firstResult = results.first()
    await expect(firstResult).toContainText('election', { ignoreCase: true })
  })

  test('pagination works correctly', async ({ page }) => {
    await page.click('a[href="/markets"]')

    // Check first page
    let markets = page.locator('[data-testid="market-card"]')
    await expect(markets).toHaveCount(20)

    // Go to next page
    await page.click('button[aria-label="Next page"]')

    // Wait for new results
    await page.waitForURL(/page=2/)

    // Verify different results
    markets = page.locator('[data-testid="market-card"]')
    await expect(markets).toHaveCount(20)
  })
})

test.describe('Market Creation', () => {
  test('creates new market', async ({ page }) => {
    // Login first (assuming auth flow)
    await page.goto('/login')
    await page.fill('input[name="email"]', 'test@example.com')
    await page.fill('input[name="password"]', 'password123')
    await page.click('button[type="submit"]')

    // Navigate to creator dashboard
    await page.goto('/creator-dashboard')

    // Fill market form
    await page.fill('input[name="name"]', 'Test Market ' + Date.now())
    await page.fill('textarea[name="description"]', 'This is a test market for E2E testing')
    await page.selectOption('select[name="category"]', 'politics')
    await page.fill('input[name="endDate"]', '2025-12-31T23:59')

    // Submit form
    await page.click('button[type="submit"]')

    // Verify success
    await expect(page.locator('text=Market created successfully')).toBeVisible()

    // Verify redirect
    await expect(page).toHaveURL(/\/markets\/test-market-/)
  })

  test('validates required fields', async ({ page }) => {
    await page.goto('/creator-dashboard')

    // Try to submit without filling fields
    await page.click('button[type="submit"]')

    // Verify error messages
    await expect(page.locator('text=Name is required')).toBeVisible()
    await expect(page.locator('text=Description is required')).toBeVisible()
  })
})

test.describe('Betting Flow', () => {
  test('places bet on market', async ({ page }) => {
    await page.goto('/markets/test-market')

    // Select outcome
    await page.click('button:has-text("Yes")')

    // Enter amount
    await page.fill('input[name="amount"]', '10')

    // Confirm bet
    await page.click('button:has-text("Place Bet")')

    // Verify confirmation
    await expect(page.locator('text=Bet placed successfully')).toBeVisible()

    // Verify updated balance
    await expect(page.locator('[data-testid="balance"]')).toContainText('90')
  })
})
```

### Visual Regression Testing

```typescript
// e2e/visual.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Visual Regression', () => {
  test('markets page matches snapshot', async ({ page }) => {
    await page.goto('/markets')
    await expect(page).toHaveScreenshot('markets-page.png')
  })

  test('dark mode matches snapshot', async ({ page }) => {
    await page.goto('/')
    await page.click('button[aria-label="Toggle dark mode"]')
    await expect(page).toHaveScreenshot('dark-mode.png')
  })
})
```

## Test Utilities

### Custom Matchers

```typescript
// test/matchers.ts
expect.extend({
  toBeWithinRange(received: number, floor: number, ceiling: number) {
    const pass = received >= floor && received <= ceiling
    return {
      pass,
      message: () =>
        pass
          ? `Expected ${received} not to be within range ${floor} - ${ceiling}`
          : `Expected ${received} to be within range ${floor} - ${ceiling}`
    }
  }
})

// Usage
test('probability is within valid range', () => {
  const prob = calculateProbability(75, 25)
  expect(prob).toBeWithinRange(0, 1)
})
```

### Test Factories

```typescript
// test/factories.ts
export function createMockMarket(overrides?: Partial<Market>): Market {
  return {
    id: '1',
    name: 'Test Market',
    description: 'Test description',
    category: 'politics',
    createdAt: new Date(),
    endDate: new Date('2025-12-31'),
    ...overrides
  }
}

export function createMockUser(overrides?: Partial<User>): User {
  return {
    id: '1',
    email: 'test@example.com',
    name: 'Test User',
    role: 'user',
    ...overrides
  }
}

// Usage
test('renders market card', () => {
  const market = createMockMarket({ name: 'Custom Market' })
  render(<MarketCard {...market} />)
  expect(screen.getByText('Custom Market')).toBeInTheDocument()
})
```

## Best Practices

- **Test Isolation**: Each test should be independent
- **Mock External Services**: Mock Supabase, Redis, OpenAI, etc.
- **Descriptive Names**: Test names should describe behavior
- **Arrange-Act-Assert**: Clear test structure
- **Test Edge Cases**: Null, undefined, empty, boundary values
- **E2E for Critical Flows**: Login, payment, key user journeys
- **Fast Unit Tests**: Keep unit tests < 50ms each
- **CI/CD Integration**: Run tests on every commit
- **Coverage Thresholds**: Aim for 80%+ coverage
- **Visual Regression**: Snapshot critical pages
