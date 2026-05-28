# Repository Loading - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating repository loading patterns.

## Example 1: RepositoryLoader Component Implementation

**File**: `libs/repository-loader/RepositoryLoader.tsx`

This is the complete production implementation of RepositoryLoader used throughout the YourCompany app.

```typescript
import { useQueries } from '@tanstack/react-query';
import { View } from 'react-native';

import { AuthDataAccess } from '@data-access/native';

import { Spinner, Text, useZestStyles } from '@zest/react-native';

import {
  DATA_ACCESS_OBJECTS,
  createQueryConfig,
  LOADING_MESSAGES,
} from './constants';
import {
  getEnrichedResults,
  throwRepositoryLoadError,
  validateRepositoryKeys,
  validateRequiredProperties,
} from './helpers';
import { stylesConfig } from './styles';
import type {
  RepositoryLoaderProviderProps,
  RequiredRepositoryKeys,
} from './types';

/**
 * @context RepositoryLoader ensures critical repository data is loaded before rendering child components.
 * It uses React Query's useQueries to dynamically fetch multiple repositories simultaneously while
 * respecting React hook rules.
 *
 * @description
 * Key Features:
 * - Dynamically creates queries based on requiredRepositories prop
 * - Blocks child rendering until ALL required queries are successful
 * - Throws errors explicitly for ErrorBoundary to catch
 * - Provides user-friendly loading state while data is fetching
 *
 * Error Handling Strategy:
 * - Does not handle errors internally
 * - Throws errors explicitly to bubble up to ErrorBoundary
 * - Leverages existing ErrorBoundary infrastructure
 */
export const RepositoryLoader = ({
  requiredRepositories = {},
  loadingFallback: LoadingFallback,
  children,
}: RepositoryLoaderProviderProps) => {
  const styles = useZestStyles(stylesConfig);

  const { data: isSignedIn } = AuthDataAccess.queries.useIsSignedInState();

  const requiredKeys = Object.keys(
    requiredRepositories
  ) as RequiredRepositoryKeys[];

  validateRepositoryKeys(requiredKeys);

  const queryConfigs = requiredKeys.map((key) =>
    createQueryConfig(DATA_ACCESS_OBJECTS[key])
  );

  const queryResults = useQueries({ queries: queryConfigs });
  const enrichedResults = getEnrichedResults(requiredKeys, queryResults);

  const failed = enrichedResults.find(
    (result) => result.isError && result.error
  );
  if (failed) {
    throwRepositoryLoadError(failed.error);
  }

  const allSuccess = enrichedResults.every(
    (result) => result.isSuccess && result.isFetched
  );
  const anyLoading = enrichedResults.some(
    (result) => result.isLoading || result.isFetching
  );

  if (anyLoading || !allSuccess) {
    return LoadingFallback ? (
      <LoadingFallback />
    ) : (
      <View style={styles.loadingContainer}>
        <Spinner style={styles.spinner} />
        <Text style={styles.loadingText}>{LOADING_MESSAGES.initializing}</Text>
      </View>
    );
  }

  // Only validate appConfig properties if user is not signed in
  const resultsToValidate = isSignedIn
    ? enrichedResults
    : enrichedResults.filter((result) => result.repositoryKey === 'appConfig');

  validateRequiredProperties(resultsToValidate, requiredRepositories);

  return <>{children}</>;
};
```

**Key patterns demonstrated:**
- `useQueries` for parallel repository loading
- Dynamic query config creation based on `requiredRepositories`
- Error throwing to ErrorBoundary (no internal error handling)
- Loading state with custom fallback support
- Property validation before rendering children
- Conditional validation based on auth state

## Example 2: Helper Functions for Validation

**File**: `libs/repository-loader/helpers.ts`

This example shows the validation and error handling helpers used by RepositoryLoader.

```typescript
import type { UseQueryResult } from '@tanstack/react-query';

import { DATA_ACCESS_OBJECTS } from './constants';
import type {
  EnrichedQueryResult,
  RepositoryLoaderProviderProps,
  RepositorySchemaMap,
  RequiredRepositoryKeys,
} from './types';

/**
 * @context Validates repository keys to ensure they exist in the data access layer.
 * This is a critical validation step that runs before any data fetching occurs.
 *
 * @throws {Error} If any repository keys are not defined in DATA_ACCESS_OBJECTS
 */
export const validateRepositoryKeys = (
  keys: RequiredRepositoryKeys[]
): void => {
  const invalid = keys.filter((key) => !DATA_ACCESS_OBJECTS[key]);

  if (invalid.length > 0) {
    throw new Error(
      `RepositoryLoader: Unknown repository keys: ${invalid.join(', ')}.` +
        ' Please ensure all keys are defined in DATA_ACCESS_OBJECTS.'
    );
  }
};

/**
 * @context Enriches React Query results with repository context for better error handling and type safety.
 *
 * @throws {Error} If a repository key is missing for any result
 */
export const getEnrichedResults = (
  keys: RequiredRepositoryKeys[],
  results: UseQueryResult<unknown>[]
): Array<EnrichedQueryResult> => {
  return results.map((result, index) => {
    const repositoryKey = keys[index];

    if (!repositoryKey) {
      throw new Error(
        `getEnrichedResults: Missing repository key at index ${index}`
      );
    }

    return {
      ...result,
      repositoryKey,
    };
  });
};

/**
 * @context Ensures all required repository properties are present in the fetched data.
 * This is the final validation step before allowing children to render.
 *
 * @throws {Error} If data is missing for any repository
 * @throws {Error} If any required properties are missing from repository data
 */
export const validateRequiredProperties = (
  results: Array<
    UseQueryResult<unknown> & { repositoryKey: RequiredRepositoryKeys }
  >,
  requiredRepositories: RepositoryLoaderProviderProps['requiredRepositories']
): void => {
  for (const result of results) {
    const { repositoryKey, data } = result;

    if (!data) {
      throw new Error(
        `RepositoryLoader: Data for repository '${repositoryKey}' is missing.`
      );
    }

    type Schema = RepositorySchemaMap[typeof repositoryKey];
    const requiredProps = requiredRepositories[
      repositoryKey
    ] as (keyof Schema)[];

    const missing = requiredProps.filter((key) => !(key in (data as Schema)));

    if (missing.length > 0) {
      throw new Error(
        `RepositoryLoader: Missing required properties [${missing.join(', ')}] in '${repositoryKey}'.`
      );
    }
  }
};

/**
 * @context Standardizes error handling by wrapping all repository loading errors.
 * This ensures consistent error handling through the ErrorBoundary system.
 *
 * @throws {Error} Enhanced error with standardized format and preserved cause
 */
export const throwRepositoryLoadError = (error: unknown): never => {
  const baseError = error instanceof Error ? error : new Error('Unknown error');

  const wrapped = new Error(
    `Failed to load essential data: ${baseError.message}`,
    {
      cause: baseError,
    }
  );

  wrapped.name = 'RepositoryLoadError';
  throw wrapped;
};
```

**Key patterns demonstrated:**
- Pre-validation of repository keys against DATA_ACCESS_OBJECTS
- Enriching query results with repository context
- Type-safe property validation with TypeScript
- Detailed error messages for debugging
- Standardized error wrapping with cause preservation
- Named error types for ErrorBoundary handling

## Example 3: Data Access Objects Configuration

**File**: `libs/repository-loader/constants.ts`

This example shows how repositories are registered and query configs are created.

```typescript
import type { RepositoryName, DataAccessType } from '@data-access/native';
import {
  AppConfigDataAccess,
  PlanDataAccess,
  NavigationBarDataAccess,
  LoyaltyBannerDataAccess,
  LoyaltyProgramStateDataAccess,
} from '@data-access/native';
import { NATIVE_MODULES_REPOSITORY_QUERY_KEY } from '@data-access/native/constants';

/**
 * @context DATA_ACCESS_OBJECTS provides a centralized mapping of repository keys
 * to their data access objects. This eliminates duplication and uses the objects
 * that already contain fetch and repositoryKey properties.
 *
 * To add a new repository:
 * 1. Import the data access object from @data-access/native
 * 2. Add an entry using the repositoryKey from the object
 * 3. The object must have: fetch (function) and repositoryKey (string) properties
 */
export const DATA_ACCESS_OBJECTS: Partial<
  Record<RepositoryName, DataAccessType>
> = {
  appConfig: AppConfigDataAccess,
  plan: PlanDataAccess,
  navigationBar: NavigationBarDataAccess,
  loyaltyBanner: LoyaltyBannerDataAccess,
  loyaltyProgramState: LoyaltyProgramStateDataAccess,
  // Add new repositories here following the same pattern
} as const;

/**
 * Helper function to create query configuration from data access object
 */
export const createQueryConfig = (
  dataAccessObject: DataAccessType | undefined
) => {
  if (!dataAccessObject) {
    throw new Error('Data access object not found');
  }

  if (!dataAccessObject.repositoryKey) {
    throw new Error(`Data access object is missing repositoryKey`);
  }

  return {
    queryKey: [
      NATIVE_MODULES_REPOSITORY_QUERY_KEY,
      dataAccessObject.repositoryKey,
    ],
    queryFn: dataAccessObject.fetch,
  };
};

/**
 * User-friendly loading messages that don't expose implementation details
 */
export const LOADING_MESSAGES = {
  default: 'Getting things ready...',
  initializing: 'Initializing app...',
  loading: 'Loading...',
} as const;
```

**Key patterns demonstrated:**
- Centralized repository registration
- Query config creation from data access objects
- Type-safe Record mapping with RepositoryName
- User-friendly loading messages
- Clear documentation for adding new repositories

## Example 4: Navigation Stack Integration

**File**: `modules/store/stacks/store/StoreStack.tsx`

This example shows using `withNavigationEntryProvider` HOC to wrap a navigation stack with RepositoryLoader.

```typescript
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import { withNavigationEntryProvider } from '@entry-providers';
import { StackNavigatorIDs } from '@navigation';

import { REPOSITORY_KEYS } from '@data-access/native/constants';

import { AuthGuard } from '@libs/auth-guard';
import { useDeepLinkReady } from '@libs/deeplinking';
import { useNavigationBarManager } from '@libs/navigation-bar-manager';
import { TracingProvider } from '@libs/tracing';

import { StoreModals } from '@modules/store/components';
import { createStoreStackScreens } from '@modules/store/stacks/store/createStoreStackScreens';

import { linkingConfig } from './linking/';
import { StoreStackRoutes } from './routes';
import type { StoreStackParamsList, IStoreStackProps } from './types';

const Stack = createNativeStackNavigator<
  StoreStackParamsList,
  StackNavigatorIDs.Store
>();

const StoreStackInternal = (initialProps: IStoreStackProps) => {
  useNavigationBarManager({
    screensToHideNavBar: [
      StoreStackRoutes.ProductDetails,
      StoreStackRoutes.Cart,
      StoreStackRoutes.Promotion,
      StoreStackRoutes.OrderConfirmation,
    ],
  });

  // Signal when deeplinks can be processed safely
  // This prevents cold start race conditions with RepositoryLoader
  useDeepLinkReady({
    waitForPlan: false, // Plan data no longer required by RepositoryLoader
  });

  return (
    <TracingProvider moduleType="stack" moduleName="store" squad="storefront">
      <Stack.Navigator
        id={StackNavigatorIDs.Store}
        initialRouteName={
          initialProps.initialRouteName || StoreStackRoutes.Storefront
        }
        screenOptions={{
          headerShown: false,
        }}
      >
        {createStoreStackScreens({
          Stack,
          initialProps,
        })}
      </Stack.Navigator>
    </TracingProvider>
  );
};

export const StoreStackWithModals = (props: IStoreStackProps) => {
  return (
    <AuthGuard stackName="store">
      <StoreStackInternal {...props} />
      <StoreModals />
    </AuthGuard>
  );
};

// Export wrapped with RepositoryLoader via HOC
export const StoreStack = withNavigationEntryProvider(
  StoreStackWithModals,
  linkingConfig,
  {
    [REPOSITORY_KEYS.appConfig]: ['locale', 'country', 'brand', 'baseUrl'],
    // Plan repository removed to prevent race condition with native data population
  }
);
```

**Key patterns demonstrated:**
- `withNavigationEntryProvider` HOC wrapping entire navigation stack
- Repository requirements specified in third argument
- Deep link coordination with `useDeepLinkReady`
- AuthGuard integration for authentication
- Comment explaining why plan repository was removed (race condition)

## Example 5: Testing RepositoryLoader

**File**: `libs/repository-loader/RepositoryLoader.test.tsx`

This example shows comprehensive testing of RepositoryLoader with mocked useQueries.

```typescript
import {
  QueryClient,
  QueryClientProvider,
  useQueries,
} from '@tanstack/react-query';
import { render, screen } from '@testing-library/react-native';

import { ErrorBoundary } from '@libs/error-boundary';

import { Text } from '@zest/react-native';

jest.mock('@tanstack/react-query', () => ({
  ...jest.requireActual('@tanstack/react-query'),
  useQueries: jest.fn(),
}));

// Create a new client for each test
const createTestQueryClient = () =>
  new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

import { RepositoryLoader } from './RepositoryLoader';

// Mocked children to render
const TestChild = () => <Text testID="child">Loaded</Text>;

describe('RepositoryLoader', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = createTestQueryClient();
    jest.clearAllMocks();
    (useQueries as jest.Mock).mockReturnValue([]);
  });

  it('renders children immediately if no repositories are required', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <RepositoryLoader requiredRepositories={{}}>
          <TestChild />
        </RepositoryLoader>
      </QueryClientProvider>
    );

    expect(screen.getByTestId('child')).toBeTruthy();
  });

  it('renders fallback while loading', () => {
    const fallback = () => <Text testID="fallback">Loading...</Text>;

    // Simulate useQueries hook returning a loading state
    (useQueries as jest.Mock).mockReturnValue([
      {
        isLoading: true,
        isFetching: true,
        isSuccess: false,
        isError: false,
        isFetched: false,
      },
    ]);

    render(
      <QueryClientProvider client={queryClient}>
        <RepositoryLoader
          requiredRepositories={{ appConfig: ['locale'] }}
          loadingFallback={fallback}
        >
          <TestChild />
        </RepositoryLoader>
      </QueryClientProvider>
    );

    expect(screen.getByTestId('fallback')).toBeTruthy();
  });

  it('throws error and is caught by ErrorBoundary if a query fails', () => {
    const failingQuery = {
      isError: true,
      isSuccess: false,
      isFetched: false,
      isLoading: false,
      isFetching: false,
      error: new Error('Test failure'),
    };

    (useQueries as jest.Mock).mockReturnValue([failingQuery]);

    const onError = jest.fn();

    render(
      <QueryClientProvider client={queryClient}>
        <ErrorBoundary scope={{ moduleName: 'Test' }} onError={onError}>
          <RepositoryLoader requiredRepositories={{ appConfig: ['locale'] }}>
            <TestChild />
          </RepositoryLoader>
        </ErrorBoundary>
      </QueryClientProvider>
    );

    expect(onError).toHaveBeenCalled();
    expect(onError.mock.calls[0][0].message).toContain('Failed to load essential data');
  });

  it('renders children when all queries are successful', () => {
    const successfulQuery = {
      isError: false,
      isSuccess: true,
      isFetched: true,
      isLoading: false,
      isFetching: false,
      data: { locale: 'en-US' },
    };

    (useQueries as jest.Mock).mockReturnValue([successfulQuery]);

    render(
      <QueryClientProvider client={queryClient}>
        <RepositoryLoader requiredRepositories={{ appConfig: ['locale'] }}>
          <TestChild />
        </RepositoryLoader>
      </QueryClientProvider>
    );

    expect(screen.getByTestId('child')).toBeTruthy();
  });
});
```

**Key patterns demonstrated:**
- Mocking `useQueries` from `@tanstack/react-query`
- Testing all states: no repositories, loading, error, success
- ErrorBoundary integration testing with `onError` callback
- Custom loading fallback testing
- QueryClientProvider wrapper for tests
- Disabling retry for deterministic tests

## Summary

The YourCompany codebase consistently follows these repository loading patterns:

1. **RepositoryLoader component** wraps children requiring native data
2. **useQueries** for parallel repository loading (TanStack Query)
3. **requiredRepositories config** specifies data dependencies
4. **Validation helpers** check keys and properties before rendering
5. **Error throwing to ErrorBoundary** for consistent error handling
6. **withNavigationEntryProvider HOC** for navigation stack integration
7. **DATA_ACCESS_OBJECTS** centralized repository registration
8. **Custom loading fallback** for better UX
9. **Comprehensive testing** with mocked queries
10. **Type-safe validation** with TypeScript

These patterns ensure data is loaded and validated before components render, preventing null reference errors and providing clear loading/error states throughout the app.
