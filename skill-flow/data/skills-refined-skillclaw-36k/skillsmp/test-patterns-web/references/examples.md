# Test Patterns - Production Examples

Real-world examples of Jest 30.2.0 and @testing-library/react v13.4.0 testing patterns from the web codebase.

## Example 1: Basic Component Test with data-testid

**File**: `app/unified-spaces/plans-sections/single-question-flow/components/steps/rte-number-of-people-step/NumberOfPeopleStep.spec.tsx:68`

```typescript
import React from 'react';
import { render, screen } from '@testing-library/react';

describe('<NumberOfPeopleStep />', () => {
  it('renders options with correct test ids', async () => {
    render(<NumberOfPeopleStep />);

    // Use data-testid for selection
    const option = await screen.findByTestId('goalsPlanNumberOfPeople-justMe');
    expect(option).toBeInTheDocument();

    // Verify attribute
    expect(option).toHaveAttribute(
      'data-testid',
      'goalsPlanNumberOfPeople-justMe'
    );
  });
});
```

**Component code:**
```typescript
<button data-testid="goalsPlanNumberOfPeople-justMe">
  Just Me
</button>
```

**Key patterns:**
- Use `data-testid` attribute (NOT `testID`)
- Query with `screen.findByTestId()` for async elements
- Verify with `toBeInTheDocument()` matcher
- Check attributes with `toHaveAttribute()`

## Example 2: Component with Providers

**File**: `app/unified-spaces/plans-sections/single-question-flow/components/steps/rte-number-of-people-step/NumberOfPeopleStep.spec.tsx:26`

```typescript
import React from 'react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { render, screen } from '@testing-library/react';

import { LocalStorageProvider } from '@/libs/local-storage';
import { SystemCountryProvider, SystemCountry } from '@/libs/system-country';
import { ServerEnvProvider } from '@/libs/server-env';

describe('<NumberOfPeopleStep />', () => {
  const onSelectionChange = jest.fn();

  const renderComponent = () =>
    render(
      <QueryClientProvider client={new QueryClient()}>
        <ServerEnvProvider>
          <SystemCountryProvider systemCountry={SystemCountry.FJ}>
            <LocalStorageProvider>
              <NumberOfPeopleStep
                onGoalsPlanRecommendationSelectionChange={onSelectionChange}
              />
            </LocalStorageProvider>
          </SystemCountryProvider>
        </ServerEnvProvider>
      </QueryClientProvider>
    );

  beforeEach(() => {
    onSelectionChange.mockReset();
  });

  it('renders correctly with providers', () => {
    renderComponent();

    // Component now has access to all context
    expect(screen.getByText('Number of People')).toBeInTheDocument();
  });
});
```

**Key patterns:**
- Create `renderComponent` helper with all providers
- Wrap with QueryClientProvider for React Query hooks
- Include SystemCountryProvider, ServerEnvProvider, etc.
- Reset mocks in `beforeEach`

## Example 3: Query by Role and Accessible Attributes

**File**: `app/unified-spaces/plans-sections/single-question-flow/components/steps/rte-number-of-people-step/NumberOfPeopleStep.spec.tsx:61`

```typescript
import { render, screen } from '@testing-library/react';

it('finds elements by role', async () => {
  render(<NumberOfPeopleStep />);

  // Query all checkboxes
  let options = await screen.findAllByRole('checkbox');
  expect(options.length).toBe(3);

  // Check ARIA attributes
  options.forEach((option) => {
    expect(option).toHaveAttribute('aria-checked', 'false');
  });

  // Query by text
  const heading = screen.getByText('Number of People');
  expect(heading).toBeInTheDocument();

  // Query by test id
  const specificOption = await screen.findByTestId('goalsPlanNumberOfPeople-justMe');
  expect(specificOption).toHaveAttribute('aria-checked', 'false');
});
```

**Key patterns:**
- Use `findAllByRole('checkbox')` for multiple elements
- Check ARIA attributes: `aria-checked`, `aria-pressed`, etc.
- Use `getByText()` for text content
- Use `findByTestId()` for specific elements

## Example 4: User Interaction with userEvent

**File**: Production pattern for user interactions

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('<NumberOfPeopleStep />', () => {
  it('handles user clicks', async () => {
    render(<NumberOfPeopleStep />);

    const button = await screen.findByTestId('goalsPlanNumberOfPeople-justMe');

    // Check initial state
    expect(button).toHaveAttribute('aria-checked', 'false');

    // Simulate user click
    await userEvent.click(button);

    // Check updated state
    expect(button).toHaveAttribute('aria-checked', 'true');
  });

  it('handles keyboard navigation', async () => {
    render(<NumberOfPeopleStep />);

    const button = await screen.findByTestId('goalsPlanNumberOfPeople-justMe');

    // Tab to element
    await userEvent.tab();

    // Press Enter
    await userEvent.keyboard('{Enter}');

    expect(button).toHaveAttribute('aria-checked', 'true');
  });

  it('handles text input', async () => {
    render(<Form />);

    const input = screen.getByLabelText('Email');

    // Type into input
    await userEvent.type(input, 'user@example.com');

    expect(input).toHaveValue('user@example.com');
  });
});
```

**Key patterns:**
- Use `userEvent.click()` for clicks (NOT fireEvent.click)
- Use `userEvent.type()` for text input
- Use `userEvent.keyboard()` for keyboard events
- Use `userEvent.tab()` for keyboard navigation
- Always await userEvent calls

## Example 5: Async Queries and waitFor

**File**: `app/unified-spaces/registration-page/steps/hooks/useForm/index.spec.tsx:34`

```typescript
import { render, screen, waitFor } from '@testing-library/react';

it('waits for async content', async () => {
  render(<AsyncComponent />);

  // findBy* automatically waits (default 1000ms timeout)
  const element = await screen.findByTestId('async-element');
  expect(element).toBeInTheDocument();

  // Check loading state disappeared
  expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
});

it('waits for complex conditions', async () => {
  render(<Component />);

  // waitFor for custom conditions
  await waitFor(() =>
    expect(screen.getByTestId('error-message')).toBeInTheDocument()
  );

  // Check error text
  expect(screen.getByTestId('error-message')).toHaveTextContent(
    'Invalid email'
  );
});

it('waits with custom timeout', async () => {
  render(<SlowComponent />);

  // Custom timeout (5 seconds)
  const element = await screen.findByTestId(
    'slow-element',
    {},
    { timeout: 5000 }
  );

  expect(element).toBeInTheDocument();
});
```

**Key patterns:**
- Use `findBy*` for elements that appear asynchronously
- Use `queryBy*` with `not.toBeInTheDocument()` for absence checks
- Use `waitFor()` for complex async conditions
- Set custom timeout if needed: `{ timeout: 5000 }`

## Example 6: Act Wrapper for State Updates

**File**: `app/unified-spaces/plans-sections/single-question-flow/components/steps/rte-number-of-people-step/NumberOfPeopleStep.spec.tsx:54`

```typescript
import { render, act } from '@testing-library/react';

describe('<Component />', () => {
  it('handles state updates', async () => {
    // Wrap render in act
    await act(() => {
      render(<Component />);
    });

    // Assertions after state has settled
    expect(screen.getByTestId('element')).toBeInTheDocument();
  });

  it('updates state programmatically', async () => {
    render(<Component />);

    const button = screen.getByTestId('increment-button');

    // act() is built into userEvent
    await userEvent.click(button);

    // No need for act() with userEvent
    expect(screen.getByTestId('counter')).toHaveTextContent('1');
  });
});
```

**Key patterns:**
- Wrap render in `act()` when component has immediate state updates
- `userEvent` methods automatically wrap in `act()`
- Use `act()` for manual state updates: `act(() => { /* update state */ })`

## Example 7: Mocking Dependencies

**File**: `app/unified-spaces/plans-sections/single-question-flow/components/steps/rte-number-of-people-step/NumberOfPeopleStep.spec.tsx:16`

```typescript
import { render, screen } from '@testing-library/react';

// Mock translation hook
jest.mock('@/libs/translation', () => ({
  useT9n: jest.fn(() => ({
    translateRaw: jest.fn((key: string) => key),
    translate: jest.fn((key: string) => <span>{key}</span>),
  })),
}));

// Mock router
jest.mock('@/libs/router', () => ({
  useRouter: jest.fn(() => ({
    pathname: '/test',
    query: {},
    push: jest.fn(),
  })),
}));

describe('<Component />', () => {
  const mockCallback = jest.fn();

  beforeEach(() => {
    // Reset mocks before each test
    mockCallback.mockReset();
  });

  afterEach(() => {
    // Clear all mocks after each test
    jest.clearAllMocks();
  });

  it('calls callback with correct arguments', async () => {
    render(<Component onSubmit={mockCallback} />);

    const button = screen.getByTestId('submit-button');
    await userEvent.click(button);

    // Verify callback was called
    expect(mockCallback).toHaveBeenCalledTimes(1);
    expect(mockCallback).toHaveBeenCalledWith({
      selection: 'justMe',
    });
  });

  it('mocks return values', () => {
    mockCallback.mockReturnValue('mocked value');

    const result = mockCallback();

    expect(result).toBe('mocked value');
  });
});
```

**Key patterns:**
- Mock modules with `jest.mock()`
- Mock hooks by returning mock implementation
- Create mock functions with `jest.fn()`
- Reset mocks in `beforeEach` with `.mockReset()`
- Clear all mocks in `afterEach` with `jest.clearAllMocks()`
- Check calls with `toHaveBeenCalledTimes()` and `toHaveBeenCalledWith()`

## Example 8: Form Submission with fireEvent

**File**: `app/unified-spaces/registration-page/steps/hooks/useForm/index.spec.tsx:70`

```typescript
import { render, fireEvent } from '@testing-library/react';

describe('Form submission', () => {
  it('submits form with fireEvent', () => {
    const handleSubmit = jest.fn();

    const { getByTestId } = render(
      <form onSubmit={handleSubmit} data-testid="test-form">
        <input type="text" name="email" data-testid="email-input" />
        <button type="submit" data-testid="submit-button">
          Submit
        </button>
      </form>
    );

    const form = getByTestId('test-form');
    const input = getByTestId('email-input');

    // Fill input
    fireEvent.change(input, { target: { value: 'user@example.com' } });

    // Submit form
    fireEvent.submit(form);

    expect(handleSubmit).toHaveBeenCalledTimes(1);
  });

  it('validates form before submission', async () => {
    render(<LoginForm />);

    const emailInput = screen.getByLabelText('Email');
    const submitButton = screen.getByTestId('submit-button');

    // Try to submit empty form
    await userEvent.click(submitButton);

    // Check validation error
    expect(await screen.findByText('Email is required')).toBeInTheDocument();

    // Fill in email
    await userEvent.type(emailInput, 'invalid-email');
    await userEvent.click(submitButton);

    // Check validation error
    expect(await screen.findByText('Invalid email format')).toBeInTheDocument();
  });
});
```

**Key patterns:**
- Use `fireEvent.change()` for input changes (or `userEvent.type()`)
- Use `fireEvent.submit()` for form submission
- Verify validation errors appear
- Check form handlers were called

## Example 9: Hook Testing with renderHook

**File**: Production pattern for testing custom hooks

```typescript
import { renderHook, act } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';

describe('useCustomHook', () => {
  const wrapper = ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={new QueryClient()}>
      {children}
    </QueryClientProvider>
  );

  it('returns initial value', () => {
    const { result } = renderHook(() => useCustomHook(), { wrapper });

    expect(result.current.value).toBe('initial');
    expect(result.current.isLoading).toBe(false);
  });

  it('updates value', () => {
    const { result } = renderHook(() => useCustomHook(), { wrapper });

    act(() => {
      result.current.setValue('updated');
    });

    expect(result.current.value).toBe('updated');
  });

  it('handles async operations', async () => {
    const { result } = renderHook(() => useAsyncHook(), { wrapper });

    expect(result.current.isLoading).toBe(true);

    // Wait for async operation
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.data).toEqual({ id: 1, name: 'Test' });
  });
});
```

**Key patterns:**
- Use `renderHook()` to test custom hooks
- Provide `wrapper` prop for providers
- Access hook return value via `result.current`
- Wrap updates in `act()`
- Use `waitFor()` for async operations

## Example 10: Snapshot Testing

```typescript
import { render } from '@testing-library/react';

describe('<Component /> snapshots', () => {
  it('matches snapshot', () => {
    const { container } = render(<Component />);

    expect(container.firstChild).toMatchSnapshot();
  });

  it('matches inline snapshot', () => {
    const { container } = render(<Button>Click Me</Button>);

    expect(container.firstChild).toMatchInlineSnapshot(`
      <button
        data-testid="button"
      >
        Click Me
      </button>
    `);
  });
});
```

**Key patterns:**
- Use `container.firstChild` for snapshot
- Use `toMatchSnapshot()` for external snapshot
- Use `toMatchInlineSnapshot()` for inline snapshot
- Update snapshots with `jest -u`

## Summary

**Common patterns:**
- Use `data-testid` (NOT `testID`)
- Wrap with providers in `renderComponent` helper
- Query with `screen.findByTestId()`, `screen.getByRole()`, `screen.getByText()`
- Use `userEvent` for interactions
- Use `findBy*` for async elements
- Use `waitFor()` for complex async conditions
- Wrap state updates in `act()`
- Mock dependencies with `jest.mock()`
- Reset mocks in `beforeEach`
- Use `toHaveBeenCalledWith()` to verify calls
