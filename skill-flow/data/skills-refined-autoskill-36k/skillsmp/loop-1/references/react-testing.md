# React Testing Library

React 19 testing with @testing-library/react 16.3+ and user-event v14.

## Query Priority

Always query the way users interact with the UI:

1. `byRole` - Accessible roles (button, textbox, heading)
2. `byLabelText` - Form labels
3. `byText` - Visible text
4. `byTestId` - Last resort only

## Custom Render Helper

```typescript
// apps/app/__tests__/helpers.tsx
import { render, RenderOptions } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ReactElement, ReactNode } from 'react'
import { ConvexProvider, ConvexReactClient } from 'convex/react'

// Create a mock Convex client for testing
const mockConvexClient = new ConvexReactClient(
  process.env.VITE_CONVEX_URL || 'https://test.convex.cloud'
)

interface WrapperProps {
  children: ReactNode
}

const AllProviders = ({ children }: WrapperProps) => {
  return (
    <ConvexProvider client={mockConvexClient}>
      {children}
    </ConvexProvider>
  )
}

type CustomRenderOptions = Omit<RenderOptions, 'wrapper'>

/**
 * Custom render with user-event setup and providers.
 * Use this for component tests that need Convex context.
 */
export function renderWithProviders(
  ui: ReactElement,
  options?: CustomRenderOptions
) {
  return {
    user: userEvent.setup(),
    ...render(ui, { wrapper: AllProviders, ...options }),
  }
}

/**
 * Simplified render with user-event setup (no providers).
 * Use this for presentational component tests.
 */
export function setup(ui: ReactElement, options?: CustomRenderOptions) {
  return {
    user: userEvent.setup(),
    ...render(ui, options),
  }
}

// Re-export everything from testing-library
export * from '@testing-library/react'
export { userEvent }
```

## Component Test Example

```typescript
import { describe, it, expect, vi } from 'vitest'
import { screen } from '@testing-library/react'
import { setup } from '../__tests__/helpers'
import { LoginForm } from './LoginForm'

describe('LoginForm', () => {
  it('submits with valid credentials', async () => {
    const onSubmit = vi.fn()
    const { user } = setup(<LoginForm onSubmit={onSubmit} />)

    // Use accessible queries (byRole, byLabelText)
    await user.type(screen.getByLabelText(/email/i), 'test@example.com')
    await user.type(screen.getByLabelText(/password/i), 'secret123')
    await user.click(screen.getByRole('button', { name: /sign in/i }))

    expect(onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'secret123',
    })
  })

  it('shows validation error for empty email', async () => {
    const { user } = setup(<LoginForm onSubmit={vi.fn()} />)

    await user.click(screen.getByRole('button', { name: /sign in/i }))

    // Prefer findBy for async assertions (better error messages)
    expect(await screen.findByRole('alert')).toHaveTextContent(/email is required/i)
  })
})
```

## Hook Test Example

```typescript
import { renderHook, act } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import { useCounter } from './useCounter'

describe('useCounter', () => {
  it('increments counter', () => {
    const { result } = renderHook(() => useCounter(0))

    act(() => result.current.increment())

    expect(result.current.count).toBe(1)
  })

  it('accepts initial value', () => {
    const { result } = renderHook(() => useCounter(10))

    expect(result.current.count).toBe(10)
  })
})
```

## Test Factories

```typescript
// apps/app/__tests__/factories.ts
import { faker } from '@faker-js/faker'

export interface User {
  id: string
  name: string
  email: string
  role: 'admin' | 'user' | 'guest'
  createdAt: number
}

export function createUser(overrides: Partial<User> = {}): User {
  return {
    id: faker.string.uuid(),
    name: faker.person.fullName(),
    email: faker.internet.email(),
    role: 'user',
    createdAt: Date.now(),
    ...overrides,
  }
}
```

## Async Patterns

### Use `findBy` for Async Elements
```typescript
// Waits for element to appear (useful for loading states)
const button = await screen.findByRole('button', { name: /submit/i })
```

### Use `waitFor` for State Changes
```typescript
await waitFor(() => {
  expect(screen.getByText(/success/i)).toBeInTheDocument()
})
```

### Use `waitForElementToBeRemoved` for Disappearing Elements
```typescript
await waitForElementToBeRemoved(() => screen.queryByText(/loading/i))
```

## User Event v14

All methods are async in v14:

```typescript
const { user } = setup(<Component />)

// Typing
await user.type(input, 'hello')
await user.clear(input)

// Clicking
await user.click(button)
await user.dblClick(button)

// Selecting
await user.selectOptions(select, 'option-value')

// Keyboard
await user.keyboard('{Enter}')
await user.tab()

// Clipboard
await user.copy()
await user.paste()
```

## Jest-DOM Matchers

```typescript
// In setup.ts (IMPORTANT for Vitest 4.x)
import * as matchers from '@testing-library/jest-dom/matchers'
expect.extend(matchers)

// Usage in tests
expect(element).toBeInTheDocument()
expect(element).toBeVisible()
expect(element).toHaveTextContent('text')
expect(element).toHaveAttribute('href', '/path')
expect(element).toBeDisabled()
expect(element).toHaveClass('active')
expect(element).toHaveFocus()
```

## Testing Patterns

### Testing Loading States
```typescript
it('shows loading state while fetching', async () => {
  setup(<UserProfile userId="123" />)

  expect(screen.getByText(/loading/i)).toBeInTheDocument()

  await waitForElementToBeRemoved(() => screen.queryByText(/loading/i))

  expect(screen.getByText('John Doe')).toBeInTheDocument()
})
```

### Testing Error States
```typescript
it('shows error message on fetch failure', async () => {
  server.use(
    http.get('/api/user', () => {
      return HttpResponse.json({ error: 'Not found' }, { status: 404 })
    })
  )

  setup(<UserProfile userId="123" />)

  expect(await screen.findByRole('alert')).toHaveTextContent(/not found/i)
})
```

### Testing Modals
```typescript
it('opens and closes modal', async () => {
  const { user } = setup(<ModalTrigger />)

  await user.click(screen.getByRole('button', { name: /open/i }))

  expect(screen.getByRole('dialog')).toBeInTheDocument()

  await user.click(screen.getByRole('button', { name: /close/i }))

  await waitForElementToBeRemoved(() => screen.queryByRole('dialog'))
})
```

## Anti-Patterns

- **Don't query by implementation details**: No `getByClassName`, no container queries
- **Don't use `getBy` for async**: Use `findBy` or `waitFor`
- **Don't test internal state**: Test what the user sees
- **Don't mock React**: Test real component behavior
