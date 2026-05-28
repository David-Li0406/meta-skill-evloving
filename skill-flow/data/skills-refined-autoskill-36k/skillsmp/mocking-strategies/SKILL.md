---
name: mocking-strategies
description: "WHAT: Mock external dependencies in React Native tests with jest.mock and factory patterns. WHEN: testing TanStack Query, Apollo GraphQL, React Navigation, Zustand stores, native modules. KEYWORDS: mock, jest.mock, TanStack Query, Apollo, navigation, Zustand, native modules, clearAllMocks, builder, factory."
---

# Mocking Strategies for React Native Testing

## Documentation

This skill has comprehensive documentation:

- **[Production Examples](./references/examples.md)** - Real-world code examples from the codebase
- **[API Reference](./references/api-docs.md)** - Complete API documentation with official links
- **[Implementation Patterns](./references/patterns.md)** - Best practices and anti-patterns


## Core Principles

**Mock external dependencies only, test internal logic.** Replace network calls, navigation, native modules, and third-party libraries with controlled test doubles. Never mock internal utilities or helpers.

**Why**: Proper mocking enables fast, isolated, reliable tests that focus on component logic without external dependencies. Test behavior, not implementation.

## When to Use This Skill

Use these mocking strategies when testing:

- Components using TanStack Query or Apollo Client
- Navigation behavior with React Navigation
- Components reading from Zustand stores
- Native module integrations (device info, analytics)
- Platform-specific code (iOS vs Android)
- Responsive layouts with window dimensions
- Components with complex external dependencies

## Mocking TanStack Query

### Mock useQuery Return Values

Test different data states without real API calls:

```typescript
import { useQuery } from '@tanstack/react-query';

jest.mock('@tanstack/react-query', () => ({
  useQuery: jest.fn(),
  useQueryClient: jest.fn(),
}));

describe('Component using useQuery', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should handle loading state', () => {
    (useQuery as jest.Mock).mockReturnValue({
      data: undefined,
      isLoading: true,
      error: null,
    });

    const { result } = renderHook(() => useMyHook());

    expect(result.current.isLoading).toBe(true);
  });

  it('should handle success state with data', () => {
    const mockData = { id: '123', name: 'Test' };

    (useQuery as jest.Mock).mockReturnValue({
      data: mockData,
      isLoading: false,
      error: null,
    });

    const { result } = renderHook(() => useMyHook());

    expect(result.current.data).toEqual(mockData);
  });

  it('should handle error state', () => {
    const mockError = new Error('Network error');

    (useQuery as jest.Mock).mockReturnValue({
      data: undefined,
      isLoading: false,
      error: mockError,
    });

    const { result } = renderHook(() => useMyHook());

    expect(result.current.error).toBe(mockError);
  });
});
```

**Why**: Configure different states per test to verify loading, success, and error handling.

### Mock useMutation

Test mutations without triggering real API calls:

```typescript
import { useMutation } from '@tanstack/react-query';

jest.mock('@tanstack/react-query', () => ({
  useMutation: jest.fn(),
}));

describe('Component using useMutation', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should call mutation with correct data', async () => {
    const mockMutate = jest.fn();

    (useMutation as jest.Mock).mockReturnValue({
      mutate: mockMutate,
      isLoading: false,
      isSuccess: false,
      isError: false,
    });

    const { result } = renderHook(() => useSaveRecipe());

    act(() => {
      result.current.mutate({ url: 'https://example.com/recipe' });
    });

    expect(mockMutate).toHaveBeenCalledWith({
      url: 'https://example.com/recipe',
    });
  });

  it('should handle mutation success', () => {
    (useMutation as jest.Mock).mockReturnValue({
      mutate: jest.fn(),
      isLoading: false,
      isSuccess: true,
      data: { id: '123', title: 'Recipe' },
    });

    const { result } = renderHook(() => useSaveRecipe());

    expect(result.current.isSuccess).toBe(true);
    expect(result.current.data).toEqual({ id: '123', title: 'Recipe' });
  });
});
```

**Why**: Test optimistic updates, error handling, and success states in isolation.

## Mocking Apollo Client (GraphQL)

### Mock useQuery Hook

Test GraphQL operations without a server:

```typescript
import { useQuery } from '@apollo/client';

jest.mock('@apollo/client', () => ({
  useQuery: jest.fn(),
  gql: jest.fn((query) => query),
}));

describe('GraphQL Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should handle loading state', () => {
    (useQuery as jest.Mock).mockReturnValue({
      data: undefined,
      loading: true,
      error: undefined,
    });

    const { getByTestId } = render(<MyComponent />);

    expect(getByTestId('loading-spinner')).toBeDefined();
  });

  it('should render data from query', () => {
    const mockData = {
      recipes: [
        { id: '1', title: 'Pasta' },
        { id: '2', title: 'Salad' },
      ],
    };

    (useQuery as jest.Mock).mockReturnValue({
      data: mockData,
      loading: false,
      error: undefined,
    });

    const { getByText } = render(<RecipeList />);

    expect(getByText('Pasta')).toBeDefined();
    expect(getByText('Salad')).toBeDefined();
  });

  it('should handle query errors', () => {
    const mockError = new Error('GraphQL Error');

    (useQuery as jest.Mock).mockReturnValue({
      data: undefined,
      loading: false,
      error: mockError,
    });

    const { getByText } = render(<MyComponent />);

    expect(getByText(/error/i)).toBeDefined();
  });
});
```

**Why**: Mock GraphQL responses to test data fetching without network dependencies.

## Mocking React Navigation

### Mock useNavigation Hook

Test navigation behavior without navigation stack:

```typescript
import { useNavigation } from '@react-navigation/native';

jest.mock('@react-navigation/native', () => ({
  useNavigation: jest.fn(),
  useRoute: jest.fn(),
  useFocusEffect: jest.fn(),
}));

describe('Component using navigation', () => {
  const mockNavigate = jest.fn();
  const mockGoBack = jest.fn();

  beforeEach(() => {
    (useNavigation as jest.Mock).mockReturnValue({
      navigate: mockNavigate,
      goBack: mockGoBack,
      setOptions: jest.fn(),
    });

    jest.clearAllMocks();
  });

  it('should navigate to detail screen with params', () => {
    const { getByTestId } = render(<RecipeCard recipe={mockRecipe} />);

    fireEvent.press(getByTestId('recipe-card'));

    expect(mockNavigate).toHaveBeenCalledWith('RecipeDetail', {
      recipeId: mockRecipe.id,
    });
  });

  it('should go back when close button pressed', () => {
    const { getByTestId } = render(<DetailScreen />);

    fireEvent.press(getByTestId('close-button'));

    expect(mockGoBack).toHaveBeenCalled();
  });
});
```

**Why**: Test navigation actions without actual stack manipulation.

### Mock useRoute for Route Params

Test screens with different parameter combinations:

```typescript
import { useRoute } from '@react-navigation/native';

jest.mock('@react-navigation/native', () => ({
  useRoute: jest.fn(),
  useNavigation: jest.fn(),
}));

describe('Screen with route params', () => {
  it('should use route params', () => {
    const mockParams = {
      recipeId: '123',
      source: 'favorites',
    };

    (useRoute as jest.Mock).mockReturnValue({
      params: mockParams,
      name: 'RecipeDetail',
    });

    const { getByText } = render(<RecipeDetailScreen />);

    expect(getByText(/Recipe 123/)).toBeDefined();
  });
});
```

**Why**: Test screens with various param combinations without navigation.

## Mocking Zustand Stores

### Mock Store Return Values

Test components in isolation from global state:

```typescript
import { useProductStore } from '@modules/store/zustand-store';

jest.mock('zustand/react/shallow', () => ({
  shallow: jest.fn((fn) => fn),
}));

jest.mock('@modules/store/zustand-store', () => ({
  useProductStore: jest.fn(),
}));

describe('Component with Zustand store', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should render with store data', () => {
    (useProductStore as jest.Mock).mockReturnValue({
      selectedProducts: ['product-1', 'product-2'],
      addProduct: jest.fn(),
      removeProduct: jest.fn(),
    });

    const { getByText } = render(<ProductList />);

    expect(getByText('2 products selected')).toBeDefined();
  });

  it('should call store action on button press', () => {
    const mockAddProduct = jest.fn();

    (useProductStore as jest.Mock).mockReturnValue({
      selectedProducts: [],
      addProduct: mockAddProduct,
      removeProduct: jest.fn(),
    });

    const { getByTestId } = render(<ProductCard productId="123" />);

    fireEvent.press(getByTestId('add-button'));

    expect(mockAddProduct).toHaveBeenCalledWith('123');
  });
});
```

**Why**: Isolate components from global state, test with various store states.

## Mocking Native Modules

### Mock react-native-device-info

Provide consistent device data:

```typescript
jest.mock('react-native-device-info', () => ({
  getBundleId: () => 'com.yourcompany.app',
  getSystemName: () => 'iOS',
  getSystemVersion: () => '17.0',
  getVersion: () => '5.2.1',
  getBrand: () => 'Apple',
  getApplicationName: () => 'YourCompany',
  getBuildNumber: () => '123',
  getDeviceId: () => 'iPhone14,2',
}));

describe('Device Info Component', () => {
  it('should display device information', () => {
    const { getByText } = render(<DeviceInfo />);

    expect(getByText(/iOS 17.0/)).toBeDefined();
    expect(getByText(/YourCompany 5.2.1/)).toBeDefined();
  });
});
```

**Why**: Consistent device data across test environments.

### Mock Custom Native Modules

Prevent errors when native code unavailable:

```typescript
jest.mock('@data-access/native', () => ({
  AppConfigDataAccess: {
    queries: {
      useBrandState: jest.fn().mockReturnValue({ data: 'yourcompany' }),
      useSystemCountry: jest.fn().mockReturnValue({ data: 'US' }),
    },
  },
}));

jest.mock('@libs/native-modules/analytics-tracker', () => ({
  SharedModulesAnalyticsTracker: {
    trackAnalyticsEvent: jest.fn(),
    trackOpenScreenEvent: jest.fn(),
  },
  AnalyticsEvent: jest.fn().mockImplementation((params) => params),
}));

describe('Component with native modules', () => {
  const mockTrackEvent = SharedModulesAnalyticsTracker.trackAnalyticsEvent as jest.Mock;

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should track event using native module', () => {
    const { getByTestId } = render(<TrackedButton />);

    fireEvent.press(getByTestId('button'));

    expect(mockTrackEvent).toHaveBeenCalledWith({
      eventName: 'button_clicked',
      parameters: expect.any(Object),
    });
  });
});
```

**Why**: Native modules throw errors in test environment without mocks.

## Mocking React Native Core

### Mock useWindowDimensions

Test responsive layouts:

```typescript
import { useWindowDimensions } from 'react-native';

jest.mock('react-native', () => ({
  ...jest.requireActual('react-native'),
  useWindowDimensions: jest.fn(),
}));

describe('Responsive component', () => {
  it('should render mobile layout on small screen', () => {
    (useWindowDimensions as jest.Mock).mockReturnValue({
      width: 375,
      height: 667,
      scale: 2,
      fontScale: 1,
    });

    const { getByTestId } = render(<ResponsiveLayout />);

    expect(getByTestId('mobile-layout')).toBeDefined();
  });

  it('should render tablet layout on large screen', () => {
    (useWindowDimensions as jest.Mock).mockReturnValue({
      width: 1024,
      height: 768,
      scale: 2,
      fontScale: 1,
    });

    const { getByTestId } = render(<ResponsiveLayout />);

    expect(getByTestId('tablet-layout')).toBeDefined();
  });
});
```

**Why**: Test responsive behavior without changing device settings.

### Mock Platform

Test platform-specific code:

```typescript
import { Platform } from 'react-native';

describe('Platform-specific component', () => {
  const originalOS = Platform.OS;

  afterEach(() => {
    Platform.OS = originalOS; // Restore original
  });

  it('should render iOS-specific component', () => {
    Platform.OS = 'ios';

    const { getByTestId } = render(<PlatformComponent />);

    expect(getByTestId('ios-feature')).toBeDefined();
  });

  it('should render Android-specific component', () => {
    Platform.OS = 'android';

    const { getByTestId } = render(<PlatformComponent />);

    expect(getByTestId('android-feature')).toBeDefined();
  });
});
```

**Why**: Test both platforms without multiple test environments. Always restore in `afterEach`.

## Test Helper Patterns

### Builder Pattern for Complex Setup

Reduce boilerplate in complex tests:

```typescript
class AnalyticsTestBuilder {
  private contextProps: Record<string, unknown> = {};
  private brandData = 'yourcompany';

  withContextData(data: Record<string, unknown>) {
    this.contextProps = data;
    return this;
  }

  withBrand(brand: string) {
    this.brandData = brand;
    return this;
  }

  build() {
    mockUseBrandState.mockReturnValue({ data: this.brandData });

    if (Object.keys(this.contextProps).length > 0) {
      const Wrapper = ({ children }: React.PropsWithChildren) => (
        <AnalyticsProvider {...this.contextProps}>{children}</AnalyticsProvider>
      );

      return renderHook(() => useAnalyticsTracker(), { wrapper: Wrapper });
    }

    return renderHook(() => useAnalyticsTracker());
  }
}

// Usage
const { result } = new AnalyticsTestBuilder()
  .withContextData({ screenName: 'Store' })
  .withBrand('greenchef')
  .build();
```

**Why**: Builder pattern makes complex setup readable and maintainable.

### Mock Factory Functions

Create consistent mocks with defaults:

```typescript
const createMockNavigation = (overrides = {}) => ({
  navigate: jest.fn(),
  goBack: jest.fn(),
  setOptions: jest.fn(),
  ...overrides,
});

const createMockRoute = (params = {}) => ({
  params,
  name: 'TestScreen',
  key: 'test-key',
});

// Usage
const mockNavigation = createMockNavigation({
  navigate: jest.fn((screen) => console.log('Navigating to', screen)),
});

const mockRoute = createMockRoute({
  recipeId: '123',
  source: 'favorites',
});
```

**Why**: Factories provide consistent mocks with sensible defaults and easy overrides.

## Common Mistakes to Avoid

❌ **Don't forget to clear mocks between tests**:

```typescript
describe('Tests with mocks', () => {
  const mockFn = jest.fn();

  it('first test', () => {
    mockFn();
    expect(mockFn).toHaveBeenCalledTimes(1);
  });

  it('second test', () => {
    // ❌ mockFn.mock.calls still has calls from first test
    expect(mockFn).toHaveBeenCalledTimes(0); // Fails!
  });
});
```

✅ **Do clear mocks in beforeEach**:

```typescript
describe('Tests with mocks', () => {
  const mockFn = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks(); // Clear all mocks
  });

  it('first test', () => {
    mockFn();
    expect(mockFn).toHaveBeenCalledTimes(1);
  });

  it('second test', () => {
    expect(mockFn).toHaveBeenCalledTimes(0); // Passes!
  });
});
```

❌ **Don't mock too much**:

```typescript
// ❌ Overmocking makes tests brittle
jest.mock('../../utils');
jest.mock('../../hooks');
jest.mock('../../components');
jest.mock('../../services');
```

✅ **Do mock only external dependencies**:

```typescript
// ✅ Mock external APIs and modules, test internal logic
jest.mock('@tanstack/react-query');
jest.mock('@libs/networking-client');

// Don't mock: local utils, helpers, or components
```

❌ **Don't use hardcoded mock return values everywhere**:

```typescript
// ❌ Same mock data in every test
jest.mock('@data-access/query', () => ({
  useRecipes: () => ({ data: mockRecipes, isLoading: false }),
}));
```

✅ **Do configure mocks per test**:

```typescript
// ✅ Configure mock differently per test
jest.mock('@data-access/query');

describe('Recipe list', () => {
  it('shows loading state', () => {
    (useRecipes as jest.Mock).mockReturnValue({
      data: undefined,
      isLoading: true,
    });
    // Test loading state
  });

  it('shows recipes', () => {
    (useRecipes as jest.Mock).mockReturnValue({
      data: mockRecipes,
      isLoading: false,
    });
    // Test data display
  });
});
```

## Quick Reference

**TanStack Query**: Mock `useQuery`/`useMutation` return values per test

**Apollo Client**: Mock `useQuery` with loading/data/error states

**Navigation**: Mock `useNavigation` and `useRoute` hooks

**Zustand**: Mock store hooks with different state combinations

**Native Modules**: Mock in jest.setup.ts or per-test file

**Platform**: Set `Platform.OS`, restore in `afterEach`

**Best Practices**:
- ✅ Clear mocks in `beforeEach(() => jest.clearAllMocks())`
- ✅ Mock external dependencies only
- ✅ Configure mocks per test for different states
- ✅ Use builder pattern for complex setups
- ✅ Create factory functions for consistent mocks
- ✅ Test behavior, not implementation

**Key Libraries**:
- Jest 29.7.0
- @testing-library/react-native 12.9.0
- TanStack Query 5.59.16
- Apollo Client 3.13.6

For production examples, see [references/examples.md](references/examples.md).
