# Test Patterns - Implementation Patterns

Implementation patterns and anti-patterns for Jest 30.2.0 and @testing-library/react v13.4.0.

## Pattern: Use data-testid (NOT testID)

Use the web standard data-testid attribute.

✅ **Good:**
```typescript
// Component
<button data-testid="submit-button">Submit</button>

// Test
const button = await screen.findByTestId('submit-button');
expect(button).toBeInTheDocument();
```

❌ **Bad:**
```typescript
// Don't use testID (React Native pattern)
<button testID="submit-button">Submit</button>

// Don't use className for test selection
const button = container.querySelector('.submit-button');
```

**Why:** `data-testid` is the web standard:
- Separate from styling
- Won't break when CSS changes
- Explicit test identifier
- Better than `testID` (React Native)

## Pattern: Use screen Instead of Destructuring

Always use screen for queries.

✅ **Good:**
```typescript
import { render, screen } from '@testing-library/react';

render(<Component />);

const element = screen.getByTestId('element');
const button = screen.getByRole('button');
const text = screen.getByText('Hello');
```

❌ **Bad:**
```typescript
// Don't destructure render
const { getByTestId, getByRole } = render(<Component />);

const element = getByTestId('element');
const button = getByRole('button');
```

**Why:** Using `screen`:
- Recommended by Testing Library
- Ensures queries use latest render
- More concise
- Consistent pattern

## Pattern: Query Priority

Follow the recommended query priority.

✅ **Good:**
```typescript
// 1. Accessible queries (best)
screen.getByRole('button', { name: 'Submit' });
screen.getByLabelText('Email');
screen.getByPlaceholderText('Enter email');

// 2. Semantic queries
screen.getByText('Welcome');
screen.getByDisplayValue('Current value');

// 3. Test IDs (last resort)
screen.getByTestId('complex-element');
```

❌ **Bad:**
```typescript
// Don't default to test IDs
screen.getByTestId('submit-button');
screen.getByTestId('email-input');
screen.getByTestId('welcome-text');
```

**Why:** Query priority:
- Accessible queries ensure proper ARIA
- Semantic queries reflect user experience
- Test IDs should be last resort
- Better accessibility testing

## Pattern: Wrap Components with Providers

Create render helper with all providers.

✅ **Good:**
```typescript
import { QueryClient, QueryClientProvider } from 'react-query';
import { SystemCountryProvider, SystemCountry } from '@/libs/system-country';

const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <QueryClientProvider client={new QueryClient()}>
      <SystemCountryProvider systemCountry={SystemCountry.US}>
        {component}
      </SystemCountryProvider>
    </QueryClientProvider>
  );
};

it('renders with providers', () => {
  renderWithProviders(<Component />);
  expect(screen.getByText('Content')).toBeInTheDocument();
});
```

❌ **Bad:**
```typescript
// Missing providers
it('renders', () => {
  render(<Component />);
  // Will fail if Component uses context
});
```

**Why:** Provider wrapper:
- Realistic testing environment
- Components work as in production
- Prevents missing context errors
- Reusable across tests

## Pattern: Use findBy for Async Elements

Use findBy queries for elements that appear asynchronously.

✅ **Good:**
```typescript
it('waits for async element', async () => {
  render(<AsyncComponent />);

  // findBy automatically waits
  const element = await screen.findByTestId('async-element');
  expect(element).toBeInTheDocument();
});
```

❌ **Bad:**
```typescript
it('fails with getBy', () => {
  render(<AsyncComponent />);

  // getBy doesn't wait - will throw error
  const element = screen.getByTestId('async-element');
  expect(element).toBeInTheDocument();
});
```

**Why:** `findBy*` queries:
- Automatically wait for elements
- Retry until found or timeout
- Handle async rendering naturally
- No manual waiting needed

## Pattern: Use queryBy for Absence Checks

Use queryBy to check element absence.

✅ **Good:**
```typescript
it('element is not present', () => {
  render(<Component />);

  // queryBy returns null if not found
  const element = screen.queryByTestId('missing-element');
  expect(element).not.toBeInTheDocument();
});
```

❌ **Bad:**
```typescript
it('element is not present', () => {
  render(<Component />);

  // getBy throws error if not found
  expect(() => screen.getByTestId('missing-element')).toThrow();
});
```

**Why:** `queryBy*` queries:
- Return null if not found (no error)
- Better for absence checks
- More readable with `not.toBeInTheDocument()`
- Explicit intent

## Pattern: Use userEvent for Interactions

Prefer userEvent over fireEvent for realistic interactions.

✅ **Good:**
```typescript
import userEvent from '@testing-library/user-event';

it('handles user interaction', async () => {
  render(<Component />);

  const button = screen.getByRole('button');

  // userEvent simulates real browser events
  await userEvent.click(button);

  expect(button).toHaveAttribute('aria-pressed', 'true');
});

it('types into input', async () => {
  render(<Form />);

  const input = screen.getByLabelText('Email');

  await userEvent.type(input, 'user@example.com');

  expect(input).toHaveValue('user@example.com');
});
```

❌ **Bad:**
```typescript
import { fireEvent } from '@testing-library/react';

it('handles click', () => {
  render(<Component />);

  const button = screen.getByRole('button');

  // fireEvent is lower-level, less realistic
  fireEvent.click(button);

  expect(button).toHaveAttribute('aria-pressed', 'true');
});
```

**Why:** `userEvent`:
- More realistic browser events
- Simulates user behavior accurately
- Triggers all related events (focus, blur, etc.)
- Better testing of real interactions

## Pattern: waitFor for Complex Async Conditions

Use waitFor for complex async conditions.

✅ **Good:**
```typescript
it('waits for complex condition', async () => {
  render(<Component />);

  // waitFor retries until condition passes
  await waitFor(() => {
    expect(screen.getByTestId('status')).toHaveTextContent('Success');
  });

  // Multiple conditions
  await waitFor(() => {
    expect(screen.getByTestId('count')).toHaveTextContent('5');
    expect(screen.getByTestId('status')).toHaveTextContent('Complete');
  });
});
```

❌ **Bad:**
```typescript
it('uses setTimeout', async () => {
  render(<Component />);

  // Don't use setTimeout
  await new Promise((resolve) => setTimeout(resolve, 1000));

  expect(screen.getByTestId('status')).toHaveTextContent('Success');
});
```

**Why:** `waitFor()`:
- Retries until condition passes
- Configurable timeout
- Fails fast if condition never passes
- No arbitrary waits

## Pattern: Mock Dependencies

Mock external dependencies and hooks.

✅ **Good:**
```typescript
// Mock router
jest.mock('@/libs/router', () => ({
  useRouter: jest.fn(() => ({
    pathname: '/test',
    query: {},
    push: jest.fn(),
  })),
}));

// Mock translation
jest.mock('@/libs/translation', () => ({
  useT9n: jest.fn(() => ({
    translate: (key: string) => key,
  })),
}));

describe('<Component />', () => {
  const mockCallback = jest.fn();

  beforeEach(() => {
    mockCallback.mockReset();
  });

  it('calls callback', async () => {
    render(<Component onSubmit={mockCallback} />);

    await userEvent.click(screen.getByRole('button'));

    expect(mockCallback).toHaveBeenCalledWith({ data: 'value' });
  });
});
```

❌ **Bad:**
```typescript
// Not mocking dependencies
it('uses real router', () => {
  // Will fail if router not available
  render(<Component />);
});

// Not resetting mocks
const mockFn = jest.fn();

it('test 1', () => {
  mockFn();
  expect(mockFn).toHaveBeenCalledTimes(1);
});

it('test 2', () => {
  // Still has 1 call from test 1
  expect(mockFn).toHaveBeenCalledTimes(1); // Wrong!
});
```

**Why:** Mocking:
- Isolates component under test
- Prevents external dependencies
- Makes tests predictable
- Resets state between tests

## Pattern: Reset Mocks in beforeEach

Always reset mocks between tests.

✅ **Good:**
```typescript
describe('<Component />', () => {
  const mockFn = jest.fn();

  beforeEach(() => {
    mockFn.mockReset();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('test 1', () => {
    mockFn();
    expect(mockFn).toHaveBeenCalledTimes(1);
  });

  it('test 2', () => {
    mockFn();
    // Correctly expects 1 call
    expect(mockFn).toHaveBeenCalledTimes(1);
  });
});
```

❌ **Bad:**
```typescript
// Not resetting mocks
const mockFn = jest.fn();

it('test 1', () => {
  mockFn();
  expect(mockFn).toHaveBeenCalledTimes(1);
});

it('test 2', () => {
  mockFn();
  // Wrong! Has 2 calls total
  expect(mockFn).toHaveBeenCalledTimes(1); // Fails
});
```

**Why:** Resetting mocks:
- Prevents test interdependence
- Each test starts clean
- Predictable test state
- Easier debugging

## Pattern: Use act() for State Updates

Wrap state updates in act() to avoid warnings.

✅ **Good:**
```typescript
import { renderHook, act } from '@testing-library/react';

it('updates state', () => {
  const { result } = renderHook(() => useCustomHook());

  act(() => {
    result.current.setValue('new value');
  });

  expect(result.current.value).toBe('new value');
});

it('renders with initial state update', async () => {
  await act(() => {
    render(<Component />);
  });

  expect(screen.getByTestId('element')).toBeInTheDocument();
});
```

❌ **Bad:**
```typescript
it('state update without act', () => {
  const { result } = renderHook(() => useCustomHook());

  // Warning: state update not wrapped in act()
  result.current.setValue('new value');

  expect(result.current.value).toBe('new value');
});
```

**Why:** `act()`:
- Prevents React warnings
- Ensures state updates are processed
- Makes tests more reliable
- Simulates React's batching

## Pattern: Test Hooks with renderHook

Use renderHook for testing custom hooks.

✅ **Good:**
```typescript
import { renderHook } from '@testing-library/react';

const wrapper = ({ children }: { children: React.ReactNode }) => (
  <QueryClientProvider client={new QueryClient()}>
    {children}
  </QueryClientProvider>
);

it('tests custom hook', () => {
  const { result } = renderHook(() => useCustomHook(), { wrapper });

  expect(result.current.value).toBe('initial');

  act(() => {
    result.current.setValue('updated');
  });

  expect(result.current.value).toBe('updated');
});
```

❌ **Bad:**
```typescript
// Testing hook by using it in a component
function TestComponent() {
  const { value, setValue } = useCustomHook();
  return (
    <div>
      <span data-testid="value">{value}</span>
      <button onClick={() => setValue('updated')}>Update</button>
    </div>
  );
}

it('tests hook through component', () => {
  render(<TestComponent />);
  // Indirect testing of hook
});
```

**Why:** `renderHook()`:
- Direct hook testing
- No need for wrapper component
- Clearer test intent
- Easier to test hook behavior

## Pattern: Verify Attributes with Matchers

Use jest-dom matchers for assertions.

✅ **Good:**
```typescript
it('checks element state', () => {
  render(<Component />);

  const button = screen.getByRole('button');

  // jest-dom matchers
  expect(button).toBeInTheDocument();
  expect(button).toBeVisible();
  expect(button).toHaveAttribute('data-testid', 'submit-button');
  expect(button).toHaveTextContent('Submit');
  expect(button).not.toBeDisabled();
});

it('checks form state', () => {
  render(<Form />);

  const input = screen.getByLabelText('Email');

  expect(input).toHaveValue('user@example.com');
  expect(input).toBeRequired();
  expect(input).toBeValid();
});
```

❌ **Bad:**
```typescript
it('checks with manual assertions', () => {
  render(<Component />);

  const button = screen.getByRole('button');

  // Manual attribute checks
  expect(button.getAttribute('data-testid')).toBe('submit-button');
  expect(button.textContent).toBe('Submit');
  expect(button.disabled).toBe(false);
});
```

**Why:** jest-dom matchers:
- More readable assertions
- Better error messages
- Standard testing library practice
- Covers common DOM checks

## Anti-Pattern: Using Container Queries

Don't query from container, use screen.

❌ **Bad:**
```typescript
it('queries from container', () => {
  const { container } = render(<Component />);

  // Don't query from container
  const element = container.querySelector('[data-testid="element"]');

  expect(element).toBeTruthy();
});
```

✅ **Good:**
```typescript
it('queries from screen', () => {
  render(<Component />);

  // Use screen
  const element = screen.getByTestId('element');

  expect(element).toBeInTheDocument();
});
```

**Why:** Using `screen`:
- Recommended pattern
- Better error messages
- More maintainable
- Consistent approach

## Anti-Pattern: Testing Implementation Details

Test behavior, not implementation.

❌ **Bad:**
```typescript
it('tests implementation', () => {
  const { rerender } = render(<Counter count={0} />);

  // Don't test component internal state
  expect(component.state.count).toBe(0);

  // Don't test prop changes directly
  rerender(<Counter count={1} />);
  expect(component.state.count).toBe(1);
});
```

✅ **Good:**
```typescript
it('tests behavior', async () => {
  render(<Counter />);

  // Test what user sees
  expect(screen.getByTestId('count')).toHaveTextContent('0');

  // Test user interactions
  await userEvent.click(screen.getByRole('button', { name: 'Increment' }));

  // Test resulting behavior
  expect(screen.getByTestId('count')).toHaveTextContent('1');
});
```

**Why:** Testing behavior:
- Tests what users experience
- More resilient to refactoring
- Catches real bugs
- Follows Testing Library philosophy

## Anti-Pattern: Not Awaiting Async Operations

Always await async operations.

❌ **Bad:**
```typescript
it('missing await', async () => {
  render(<Component />);

  // Missing await
  userEvent.click(button); // Should be: await userEvent.click(button)

  // Race condition - may pass or fail
  expect(screen.getByText('Clicked')).toBeInTheDocument();
});
```

✅ **Good:**
```typescript
it('awaits async operations', async () => {
  render(<Component />);

  const button = screen.getByRole('button');

  // Await userEvent
  await userEvent.click(button);

  // Await async queries
  const message = await screen.findByText('Clicked');
  expect(message).toBeInTheDocument();
});
```

**Why:** Awaiting async:
- Prevents race conditions
- Tests complete before assertions
- More reliable tests
- Catches timing issues

## Summary

**Key Patterns:**
- Use `data-testid` (NOT `testID`)
- Use `screen.*` (NOT destructured render)
- Query priority: role > label > text > testID
- Wrap components with providers
- Use `findBy*` for async elements
- Use `queryBy*` for absence checks
- Use `userEvent` over `fireEvent`
- Use `waitFor()` for complex async
- Mock dependencies and reset in `beforeEach`
- Use `act()` for state updates
- Use `renderHook()` for custom hooks
- Use jest-dom matchers

**Anti-Patterns to Avoid:**
- Using `testID` instead of `data-testid`
- Destructuring render instead of using screen
- Defaulting to test IDs instead of accessible queries
- Testing without providers
- Using `getBy*` for async elements
- Not mocking dependencies
- Not resetting mocks between tests
- Missing `await` on async operations
- Testing implementation details
- Querying from container
