# Jest Mocking API Reference

**Version**: Jest 29.7.0

## Official Documentation

- **Mock Functions**: https://jestjs.io/docs/mock-functions
- **Manual Mocks**: https://jestjs.io/docs/manual-mocks
- **ES6 Class Mocks**: https://jestjs.io/docs/es6-class-mocks

## Mock Functions

### jest.fn()

Create mock function.

```typescript
const mockFn = jest.fn();
const mockFn = jest.fn(x => x * 2); // With implementation
const mockFn = jest.fn().mockName('fetchData'); // Named mock

mockFn(1, 2);
expect(mockFn).toHaveBeenCalledWith(1, 2);
```

### Mock Return Values

```typescript
mockFn.mockReturnValue(42);
mockFn.mockReturnValueOnce(1).mockReturnValueOnce(2).mockReturnValue(3);

// Promises
mockFn.mockResolvedValue({ id: 1 });
mockFn.mockResolvedValueOnce({ id: 1 }).mockResolvedValue({ id: 2 });
mockFn.mockRejectedValue(new Error('fail'));
mockFn.mockRejectedValueOnce(new Error('fail'));
```

### Mock Implementation

```typescript
mockFn.mockImplementation((x) => x * 2);
mockFn.mockImplementationOnce((x) => x * 3);

// Async implementation
mockFn.mockImplementation(async (x) => {
  await delay(100);
  return x * 2;
});
```

### Mock Properties

```typescript
mockFn.mock.calls; // [[arg1, arg2], [arg3]]
mockFn.mock.results; // [{ type: 'return', value: 42 }]
mockFn.mock.instances; // [this1, this2]
mockFn.mock.contexts; // [context1, context2]
mockFn.mock.lastCall; // [lastArg1, lastArg2]
```

### Clearing/Resetting Mocks

```typescript
mockFn.mockClear(); // Clear calls and results only
mockFn.mockReset(); // Clear + remove implementation
mockFn.mockRestore(); // Reset + restore original (for spies)

jest.clearAllMocks(); // Clear all mock calls
jest.resetAllMocks(); // Reset all mocks
jest.restoreAllMocks(); // Restore all spies
```

## Module Mocking

### jest.mock()

Auto-mock entire module.

```typescript
// Auto-mock (all exports become jest.fn())
jest.mock('@libs/api');

// With factory
jest.mock('@libs/api', () => ({
  fetchData: jest.fn(),
  updateData: jest.fn(),
}));

// Partial mock (keep some real exports)
jest.mock('@libs/api', () => ({
  ...jest.requireActual('@libs/api'),
  fetchData: jest.fn(),
}));
```

### jest.doMock()

Runtime module mocking (not hoisted).

```typescript
beforeEach(() => {
  jest.doMock('@libs/api', () => ({
    fetchData: jest.fn().mockResolvedValue({ id: 1 }),
  }));
});
```

### jest.unmock()

Remove module mock.

```typescript
jest.unmock('@libs/api'); // Use real implementation
```

### jest.requireActual()

Require actual module (not mocked).

```typescript
const actualApi = jest.requireActual('@libs/api');
```

### jest.requireMock()

Require mocked module.

```typescript
const mockedApi = jest.requireMock('@libs/api');
```

## Spying

### jest.spyOn()

Spy on method without replacing it.

```typescript
const spy = jest.spyOn(object, 'method');

// Mock implementation
spy.mockImplementation(() => 'mocked');
spy.mockReturnValue('value');

// Restore original
spy.mockRestore();

// Verify calls
expect(spy).toHaveBeenCalled();
```

### Spy on Console

```typescript
const consoleSpy = jest.spyOn(console, 'error').mockImplementation();

// Test code that logs errors

expect(consoleSpy).toHaveBeenCalledWith('Error message');
consoleSpy.mockRestore();
```

### Spy on Object Properties

```typescript
const spy = jest.spyOn(object, 'property', 'get');
spy.mockReturnValue('mocked value');

const spy = jest.spyOn(object, 'property', 'set');
```

## Testing Library Specific Mocks

### Mock React Navigation

```typescript
const mockNavigate = jest.fn();
const mockGoBack = jest.fn();
const mockSetOptions = jest.fn();

jest.mock('@react-navigation/native', () => ({
  ...jest.requireActual('@react-navigation/native'),
  useNavigation: () => ({
    navigate: mockNavigate,
    goBack: mockGoBack,
    setOptions: mockSetOptions,
  }),
}));
```

### Mock Zustand Store

```typescript
const mockIncrement = jest.fn();
const mockStore = {
  count: 0,
  increment: mockIncrement,
};

jest.mock('@stores/useCountStore', () => ({
  useCountStore: (selector) => {
    if (selector) return selector(mockStore);
    return mockStore;
  },
}));
```

### Mock TanStack Query

```typescript
jest.mock('@tanstack/react-query', () => ({
  ...jest.requireActual('@tanstack/react-query'),
  useQuery: jest.fn(),
  useMutation: jest.fn(),
}));

// In test
(useQuery as jest.Mock).mockReturnValue({
  data: { id: 1, title: 'Test' },
  isLoading: false,
  error: null,
});
```

### Mock Apollo Client

```typescript
jest.mock('@apollo/client', () => ({
  ...jest.requireActual('@apollo/client'),
  useQuery: jest.fn(),
  useMutation: jest.fn(),
}));

// In test
(useQuery as jest.Mock).mockReturnValue({
  data: { recipe: { id: 1 } },
  loading: false,
  error: null,
});

(useMutation as jest.Mock).mockReturnValue([
  jest.fn().mockResolvedValue({ data: { updateRecipe: { id: 1 } } }),
  { loading: false, error: null },
]);
```

### Mock React Native Modules

```typescript
jest.mock('react-native/Libraries/Animated/NativeAnimatedHelper');

jest.mock('react-native', () => ({
  ...jest.requireActual('react-native'),
  Platform: {
    OS: 'ios',
    select: jest.fn((obj) => obj.ios),
  },
  Dimensions: {
    get: jest.fn(() => ({ width: 375, height: 812 })),
  },
}));
```

## Advanced Patterns

### Manual Mocks

Create `__mocks__` directory next to module.

```
src/
  libs/
    api.ts
    __mocks__/
      api.ts  <-- Mock implementation
```

```typescript
// __mocks__/api.ts
export const fetchData = jest.fn().mockResolvedValue({ id: 1 });
export const updateData = jest.fn();
```

### Factory Functions

```typescript
export const createMockUser = (overrides = {}) => ({
  id: '1',
  name: 'Test User',
  email: 'test@example.com',
  ...overrides,
});

const user = createMockUser({ name: 'John' });
```

### Mock Timers

```typescript
beforeEach(() => {
  jest.useFakeTimers();
});

afterEach(() => {
  jest.useRealTimers();
});

test('delays execution', () => {
  const fn = jest.fn();

  setTimeout(fn, 1000);

  jest.advanceTimersByTime(1000);

  expect(fn).toHaveBeenCalled();
});

// Modern timers (preferred)
jest.useFakeTimers({ doNotFake: ['nextTick'] });
```

### Mock Dates

```typescript
beforeEach(() => {
  jest.useFakeTimers();
  jest.setSystemTime(new Date('2024-01-01'));
});

afterEach(() => {
  jest.useRealTimers();
});

test('uses fixed date', () => {
  expect(new Date().toISOString()).toBe('2024-01-01T00:00:00.000Z');
});
```

### Conditional Mocks

```typescript
jest.mock('@libs/api', () => {
  if (process.env.TEST_ENV === 'integration') {
    return jest.requireActual('@libs/api');
  }
  return {
    fetchData: jest.fn().mockResolvedValue({ id: 1 }),
  };
});
```

## Assertion Helpers

### toHaveBeenCalled

```typescript
expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledTimes(2);
expect(mockFn).toHaveBeenCalledWith(arg1, arg2);
expect(mockFn).toHaveBeenLastCalledWith(arg1);
expect(mockFn).toHaveBeenNthCalledWith(1, arg1);
```

### toHaveReturned

```typescript
expect(mockFn).toHaveReturned();
expect(mockFn).toHaveReturnedTimes(2);
expect(mockFn).toHaveReturnedWith(value);
expect(mockFn).toHaveLastReturnedWith(value);
expect(mockFn).toHaveNthReturnedWith(1, value);
```

### Mock Matchers

```typescript
expect(mockFn).toHaveBeenCalledWith(
  expect.anything(),
  expect.any(Number),
  expect.arrayContaining([1, 2]),
  expect.objectContaining({ key: 'value' }),
  expect.stringContaining('substring'),
  expect.stringMatching(/pattern/)
);
```

## Common Patterns

### Reset Mocks Between Tests

```typescript
beforeEach(() => {
  jest.clearAllMocks(); // Clear call history
});

// Or in test
afterEach(() => {
  jest.restoreAllMocks(); // Restore spies
});
```

### Mock Implementation Per Test

```typescript
describe('Component', () => {
  beforeEach(() => {
    mockFn.mockClear();
  });

  it('test 1', () => {
    mockFn.mockReturnValue(1);
    // test
  });

  it('test 2', () => {
    mockFn.mockReturnValue(2);
    // test
  });
});
```

### Spy on Imported Function

```typescript
import * as api from '@libs/api';

it('calls fetchData', () => {
  const spy = jest.spyOn(api, 'fetchData').mockResolvedValue({ id: 1 });

  // test

  expect(spy).toHaveBeenCalled();
  spy.mockRestore();
});
```

## Key Considerations

- Clear mocks in `beforeEach` to avoid test pollution
- Use `mockRestore()` on spies to restore original implementation
- Prefer `jest.spyOn()` over `jest.fn()` when you need to restore
- Use `jest.requireActual()` for partial mocks
- Mock at module level, not inside tests (except `doMock`)
- Use factory functions for consistent mock data
- Mock external dependencies, not internal logic
- Test behavior, not implementation details
