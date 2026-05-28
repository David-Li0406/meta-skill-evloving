---
name: test-patterns-web
description: "WHAT: Jest and @testing-library/react patterns for web component testing. WHEN: testing components with providers, user interactions, async content, form validation. KEYWORDS: testing-library, Jest, screen, userEvent, render, findBy, waitFor, act, providers, web."
---

# Test Patterns - Web

Testing patterns for React web applications using Jest 30.2.0 and @testing-library/react v13.4.0.

## Documentation

This skill has comprehensive documentation:

- **[Production Examples](./references/examples.md)** - Real-world code examples from the codebase
- **[API Reference](./references/api-docs.md)** - Complete API documentation with official links
- **[Implementation Patterns](./references/patterns.md)** - Best practices and anti-patterns

## When to Use

Use these patterns for:
- Component unit tests
- Integration tests with providers
- User interaction testing
- Hook testing
- Form validation testing

**Note:** Use @testing-library/react (web version), NOT @testing-library/react-native!

## Core Principles

### 1. Use data-testid for Element Selection

**Use data-testid attribute (NOT testID) for test element selection.**

✅ **Good:**
```typescript
// Component
<button data-testid="goalsPlanNumberOfPeople-justMe">
  Just Me
</button>

// Test - app/unified-spaces/plans-sections/single-question-flow/components/steps/rte-number-of-people-step/NumberOfPeopleStep.spec.tsx:68
import { render, screen } from '@testing-library/react';

it('renders options with correct test ids', async () => {
  render(<NumberOfPeopleStep />);

  const option = await screen.findByTestId('goalsPlanNumberOfPeople-justMe');
  expect(option).toBeInTheDocument();

  // Check attribute
  expect(option).toHaveAttribute(
    'data-testid',
    'goalsPlanNumberOfPeople-justMe'
  );
});
```

❌ **Bad:**
```typescript
// Don't use testID (React Native pattern)
<button testID="my-button">Click Me</button>

// Don't use className for test selection
const button = container.querySelector('.my-button-class');
```

**Why:** data-testid is the web standard for test identifiers. It's separate from styling and provides stable selectors.

### 2. Render with Providers

**Wrap components with all required providers for realistic testing.**

✅ **Good:**
```typescript
// app/unified-spaces/plans-sections/single-question-flow/components/steps/rte-number-of-people-step/NumberOfPeopleStep.spec.tsx:26
import React from 'react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { render, screen } from '@testing-library/react';

import { LocalStorageProvider } from '@/libs/local-storage';
import { SystemCountryProvider, SystemCountry } from '@/libs/system-country';
import { ServerEnvProvider } from '@/libs/server-env';

describe('<NumberOfPeopleStep />', () => {
  const renderComponent = () =>
    render(
      <QueryClientProvider client={new QueryClient()}>
        <ServerEnvProvider>
          <SystemCountryProvider systemCountry={SystemCountry.FJ}>
            <LocalStorageProvider>
              <NumberOfPeopleStep onGoalsPlanRecommendationSelectionChange={onSelectionChange} />
            </LocalStorageProvider>
          </SystemCountryProvider>
        </ServerEnvProvider>
      </QueryClientProvider>
    );

  it('renders correctly', () => {
    renderComponent();
    // assertions...
  });
});
```

**Why:** Components often depend on context providers. Testing without them leads to false failures.

### 3. Query with screen and Roles

**Use screen queries with accessible roles and queries.**

✅ **Good:**
```typescript
// app/unified-spaces/plans-sections/single-question-flow/components/steps/rte-number-of-people-step/NumberOfPeopleStep.spec.tsx:61
import { render, screen } from '@testing-library/react';

it('finds elements by role', async () => {
  render(<NumberOfPeopleStep />);

  // Query by role
  let options = await screen.findAllByRole('checkbox');
  expect(options.length).toBe(3);

  options.forEach((option) => {
    expect(option).toHaveAttribute('aria-checked', 'false');
  });
});

// Query by test id
const element = await screen.findByTestId('goalsPlanNumberOfPeople-justMe');

// Query by text
const heading = screen.getByText('Number of People');
```

❌ **Bad:**
```typescript
// Don't destructure render
const { getByTestId } = render(<Component />);
const element = getByTestId('my-element'); // Use screen instead
```

**Why:** Using screen is the recommended pattern. It's more concise and ensures queries always use the most recent render.

### 4. User Interactions with userEvent

**Use @testing-library/user-event for realistic user interactions.**

✅ **Good:**
```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

it('handles user clicks', async () => {
  render(<NumberOfPeopleStep />);

  const button = await screen.findByTestId('goalsPlanNumberOfPeople-justMe');

  // Use userEvent for more realistic interactions
  await userEvent.click(button);

  expect(button).toHaveAttribute('aria-checked', 'true');
});
```

**Alternative (fireEvent):**
```typescript
// app/unified-spaces/registration-page/steps/hooks/useForm/index.spec.tsx:70
import { render, fireEvent } from '@testing-library/react';

it('submits form', () => {
  const { getByTestId } = render(<TestForm />);

  fireEvent.submit(getByTestId('form'));

  // assertions...
});
```

**Why:** userEvent simulates real browser events more accurately. fireEvent is lower-level but faster for simple cases.

### 5. Async Queries and Waits

**Use findBy queries and waitFor for async operations.**

✅ **Good:**
```typescript
// app/unified-spaces/registration-page/steps/hooks/useForm/index.spec.tsx:34
import { render, screen, waitFor } from '@testing-library/react';

it('waits for async content', async () => {
  render(<Component />);

  // findBy* automatically waits
  const element = await screen.findByTestId('async-element');
  expect(element).toBeInTheDocument();

  // Or use waitFor for complex conditions
  await waitFor(() =>
    expect(screen.getByTestId('error-message')).toBeInTheDocument()
  );
});
```

❌ **Bad:**
```typescript
// Don't use getBy* for async content
const element = screen.getByTestId('async-element'); // Will fail if not immediately present
```

**Why:** findBy* queries automatically wait and retry, handling async rendering naturally.

### 6. Act Wrapper for State Updates

**Wrap state updates with act() to avoid warnings.**

✅ **Good:**
```typescript
// app/unified-spaces/plans-sections/single-question-flow/components/steps/rte-number-of-people-step/NumberOfPeopleStep.spec.tsx:54
import { render, act } from '@testing-library/react';

it('handles state updates', async () => {
  await act(() => {
    render(<Component />);
  });

  // Continue with assertions
});
```

**Why:** act() ensures state updates are processed before assertions run, preventing test warnings.

### 7. Mock Dependencies

**Mock external dependencies and hooks.**

✅ **Good:**
```typescript
// app/unified-spaces/plans-sections/single-question-flow/components/steps/rte-number-of-people-step/NumberOfPeopleStep.spec.tsx:16
jest.mock('@/libs/translation', () => ({
  useT9n: jest.fn(() => ({
    translateRaw: jest.fn((key: string) => key),
    translate: jest.fn((key: string) => <span>{key}</span>),
  })),
}));

describe('<Component />', () => {
  const mockCallback = jest.fn();

  beforeEach(() => {
    mockCallback.mockReset();
  });

  it('calls callback', () => {
    render(<Component onSubmit={mockCallback} />);
    // trigger callback...
    expect(mockCallback).toHaveBeenCalledWith(expectedValue);
  });
});
```

**Why:** Mocking isolates the component under test and makes tests predictable.

## Testing Hooks

### Use renderHook (if available)

```typescript
import { renderHook } from '@testing-library/react';

it('tests custom hook', () => {
  const { result } = renderHook(() => useCustomHook());

  expect(result.current.value).toBe('initial');

  act(() => {
    result.current.setValue('updated');
  });

  expect(result.current.value).toBe('updated');
});
```

## Common Query Methods

### When to Use Each Query

```typescript
// getBy* - Element must be present immediately
const element = screen.getByTestId('element');

// queryBy* - Element might not exist (returns null)
const element = screen.queryByTestId('element');
expect(element).not.toBeInTheDocument();

// findBy* - Element will appear asynchronously
const element = await screen.findByTestId('element');

// getAllBy*, queryAllBy*, findAllBy* - Multiple elements
const elements = screen.getAllByRole('checkbox');
```

## File Organization

```
components/
├── MyComponent/
│   ├── MyComponent.tsx
│   ├── MyComponent.spec.tsx    # Component tests
│   └── MyComponent.test.tsx    # Alternative naming
└── hooks/
    ├── useMyHook.ts
    └── useMyHook.spec.tsx       # Hook tests
```

## Common Mistakes

1. **Using testID instead of data-testid** - testID is React Native, not web
2. **Not wrapping with providers** - Missing context causes test failures
3. **Using getBy for async content** - Use findBy instead
4. **Destructuring render** - Use screen.* instead of { getByTestId }
5. **Forgetting to mock dependencies** - Tests become flaky without mocks
6. **Not using act()** - Causes warnings about state updates

## Quick Reference

### Basic Test Structure

```typescript
import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('<MyComponent />', () => {
  it('renders and handles interaction', async () => {
    render(<MyComponent />);

    // Find element
    const button = await screen.findByTestId('my-button');

    // Check initial state
    expect(button).toBeInTheDocument();

    // Simulate interaction
    await userEvent.click(button);

    // Check updated state
    expect(button).toHaveAttribute('aria-pressed', 'true');
  });
});
```

### With Providers

```typescript
const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <QueryClientProvider client={new QueryClient()}>
      <SystemCountryProvider systemCountry={SystemCountry.US}>
        {component}
      </SystemCountryProvider>
    </QueryClientProvider>
  );
};
```

### Mocking

```typescript
// Mock module
jest.mock('@/libs/translation', () => ({
  useT9n: jest.fn(() => ({ translate: (key) => key })),
}));

// Mock function
const mockFn = jest.fn();
mockFn.mockReset();
mockFn.mockReturnValue('value');
expect(mockFn).toHaveBeenCalledWith(expectedArg);
```

### Async Testing

```typescript
// findBy (auto-waits)
const element = await screen.findByTestId('async-element');

// waitFor (custom condition)
await waitFor(() => {
  expect(screen.getByText('Loaded')).toBeInTheDocument();
});
```
