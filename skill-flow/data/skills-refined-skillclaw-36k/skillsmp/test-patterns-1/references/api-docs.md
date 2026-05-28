# Jest + Testing Library API Reference

**Versions**: Jest 29.7.0, @testing-library/react-native 12.9.0

## Official Documentation

- **Jest**: https://jestjs.io/docs/api
- **Testing Library**: https://callstack.github.io/react-native-testing-library/
- **React Native Testing**: https://reactnative.dev/docs/testing-overview

## Testing Library API

### render

Render component for testing.

```typescript
import { render, screen } from '@testing-library/react-native';

const { getByText, queryByText, findByText, rerender, unmount } = render(
  <Component prop="value" />
);
```

**Returns**:
- `getByText`, `getByTestId`, `getByRole` - Throw if not found
- `queryByText`, `queryByTestId` - Return null if not found
- `findByText`, `findByTestId` - Async, wait for element
- `getAllBy*`, `queryAllBy*`, `findAllBy*` - Return arrays
- `rerender(element)` - Re-render with new props
- `unmount()` - Unmount component
- `debug()` - Print component tree

### screen

Global queries on rendered tree.

```typescript
screen.getByText('Submit');
screen.queryByTestId('loading-spinner');
await screen.findByText('Success');
```

### fireEvent

Simulate user interactions.

```typescript
fireEvent.press(button);
fireEvent.changeText(input, 'new text');
fireEvent(element, 'customEvent', eventData);
```

**Common Events**:
- `press(element)` - Press/tap
- `changeText(element, text)` - Change text input
- `scroll(element, eventData)` - Scroll event

### waitFor

Wait for async updates.

```typescript
await waitFor(() => {
  expect(screen.getByText('Loaded')).toBeTruthy();
});

await waitFor(
  () => expect(screen.getByText('Loaded')).toBeTruthy(),
  { timeout: 5000, interval: 100 }
);
```

### userEvent

More realistic user interactions (optional).

```typescript
import { userEvent } from '@testing-library/react-native';

const user = userEvent.setup();
await user.press(button);
await user.type(input, 'text');
```

## Jest API

### Matchers

```typescript
// Equality
expect(value).toBe(5);
expect(value).toEqual({ key: 'value' });
expect(value).toStrictEqual({ key: 'value' });

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toBeUndefined();
expect(value).toBeDefined();

// Numbers
expect(value).toBeGreaterThan(3);
expect(value).toBeGreaterThanOrEqual(3.5);
expect(value).toBeLessThan(5);
expect(value).toBeCloseTo(0.3, 5); // Floating point

// Strings
expect(text).toMatch(/pattern/);
expect(text).toContain('substring');

// Arrays
expect(array).toContain(item);
expect(array).toHaveLength(3);
expect(array).toEqual(expect.arrayContaining([1, 2]));

// Objects
expect(object).toHaveProperty('key');
expect(object).toHaveProperty('key', 'value');
expect(object).toMatchObject({ key: 'value' });

// Exceptions
expect(() => fn()).toThrow();
expect(() => fn()).toThrow(Error);
expect(() => fn()).toThrow('error message');

// Promises
await expect(promise).resolves.toBe(value);
await expect(promise).rejects.toThrow();

// Functions
expect(fn).toHaveBeenCalled();
expect(fn).toHaveBeenCalledTimes(2);
expect(fn).toHaveBeenCalledWith(arg1, arg2);
expect(fn).toHaveBeenLastCalledWith(arg1);
expect(fn).toHaveReturnedWith(value);
```

### Mock Functions

```typescript
// Create mock
const mockFn = jest.fn();
const mockFn = jest.fn(x => x * 2);
const mockFn = jest.fn().mockName('myMock');

// Mock return values
mockFn.mockReturnValue(42);
mockFn.mockReturnValueOnce(1).mockReturnValueOnce(2);
mockFn.mockResolvedValue(42); // Promise
mockFn.mockRejectedValue(new Error('fail'));

// Mock implementation
mockFn.mockImplementation((x) => x * 2);
mockFn.mockImplementationOnce((x) => x * 3);

// Reset
mockFn.mockClear(); // Clear calls/results
mockFn.mockReset(); // Clear + remove implementation
mockFn.mockRestore(); // Reset + restore original

// Inspect calls
mockFn.mock.calls; // [[arg1, arg2], [arg1, arg2]]
mockFn.mock.results; // [{ type: 'return', value: 42 }]
mockFn.mock.instances; // [this1, this2]
```

### Mocking Modules

```typescript
// Mock entire module
jest.mock('@libs/api');

// Mock with implementation
jest.mock('@libs/api', () => ({
  fetchData: jest.fn().mockResolvedValue({ id: 1 }),
}));

// Mock specific exports
jest.mock('@libs/api', () => ({
  ...jest.requireActual('@libs/api'),
  fetchData: jest.fn(),
}));

// Unmock
jest.unmock('@libs/api');

// Clear all mocks
jest.clearAllMocks();
jest.resetAllMocks();
jest.restoreAllMocks();
```

### Spying

```typescript
const spy = jest.spyOn(object, 'method');
spy.mockImplementation(() => 'mocked');
spy.mockRestore(); // Restore original

const spy = jest.spyOn(console, 'log').mockImplementation();
// Test code
spy.mockRestore();
```

### Timers

```typescript
jest.useFakeTimers();

// Advance timers
jest.advanceTimersByTime(1000);
jest.runAllTimers();
jest.runOnlyPendingTimers();

// Clear timers
jest.clearAllTimers();

jest.useRealTimers();
```

### Lifecycle Hooks

```typescript
beforeAll(() => {
  // Runs once before all tests
});

beforeEach(() => {
  // Runs before each test
});

afterEach(() => {
  // Runs after each test
});

afterAll(() => {
  // Runs once after all tests
});
```

### Test Structure

```typescript
describe('Component', () => {
  it('renders correctly', () => {
    expect(true).toBe(true);
  });

  test('handles click', () => {
    expect(fn).toHaveBeenCalled();
  });

  it.only('runs only this test', () => {});
  it.skip('skips this test', () => {});
  it.todo('write this test later');
});

describe.only('only this suite', () => {});
describe.skip('skip this suite', () => {});
```

## React Native Testing Patterns

### Testing Hooks

```typescript
import { renderHook } from '@testing-library/react-native';

const { result, rerender } = renderHook(() => useCustomHook(props));

expect(result.current.value).toBe(expected);

rerender(newProps);
```

### Testing with Providers

```typescript
const wrapper = ({ children }) => (
  <QueryClientProvider client={queryClient}>
    <ZestProvider>{children}</ZestProvider>
  </QueryClientProvider>
);

render(<Component />, { wrapper });
```

### Testing Async

```typescript
it('loads data', async () => {
  render(<Component />);

  expect(screen.queryByText('Loading')).toBeTruthy();

  await waitFor(() => {
    expect(screen.getByText('Loaded')).toBeTruthy();
  });
});
```

### Testing Navigation

```typescript
const navigation = {
  navigate: jest.fn(),
  goBack: jest.fn(),
  setOptions: jest.fn(),
};

render(<Screen navigation={navigation} />);

fireEvent.press(screen.getByText('Next'));
expect(navigation.navigate).toHaveBeenCalledWith('Details');
```

## Common Testing Patterns

### Snapshot Testing

```typescript
it('matches snapshot', () => {
  const tree = render(<Component />).toJSON();
  expect(tree).toMatchSnapshot();
});
```

### Testing Error Boundaries

```typescript
// Suppress console.error in tests
const spy = jest.spyOn(console, 'error').mockImplementation();

it('catches errors', () => {
  render(
    <ErrorBoundary>
      <ComponentThatThrows />
    </ErrorBoundary>
  );

  expect(screen.getByText('Error occurred')).toBeTruthy();
});

spy.mockRestore();
```

### Testing Custom Queries

```typescript
const utils = render(<Component />);
const getByDataQa = (qa) => utils.getByTestId(`qa-${qa}`);

expect(getByDataQa('submit-button')).toBeTruthy();
```

## Key Considerations

- Use `getBy*` when element must exist
- Use `queryBy*` when checking absence
- Use `findBy*` for async elements
- Always cleanup with `jest.clearAllMocks()` in `afterEach`
- Mock external dependencies
- Test user behavior, not implementation
- Use `screen` queries for better error messages
- Wait for async updates with `waitFor`
- Suppress console errors in tests that expect errors
