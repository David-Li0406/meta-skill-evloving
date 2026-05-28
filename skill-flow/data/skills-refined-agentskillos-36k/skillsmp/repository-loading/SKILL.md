---
name: repository-loading
description: "WHAT: Validate native repository data before rendering with RepositoryLoader. WHEN: blocking UI until data loads, validating required properties, handling data dependencies. KEYWORDS: RepositoryLoader, requiredRepositories, loadingFallback, useQueries, validation, ErrorBoundary, data loading."
---

# Repository Loading Patterns

## Core Principles

**Use RepositoryLoader to validate required native data is loaded before rendering.** Configure requiredRepositories to specify data dependencies, provide loadingFallback for UX, and let errors bubble to ErrorBoundary.

**Why**: Pre-rendering validation prevents downstream null errors, improves error handling, and provides clear loading states. Parallel loading with TanStack Query minimizes load time.

## When to Use This Skill

Use these patterns when:

- Loading critical data from native modules before rendering
- Validating required repository properties exist
- Preventing null reference errors from missing data
- Providing loading states during data fetch
- Handling data loading errors with ErrorBoundary
- Wrapping navigation stacks with data requirements
- Testing components with repository dependencies

## RepositoryLoader Component

### Basic Usage

```typescript
import { RepositoryLoader } from '@libs/repository-loader';
import { REPOSITORY_KEYS } from '@data-access/native/constants';

<RepositoryLoader
  requiredRepositories={{
    [REPOSITORY_KEYS.appConfig]: ['locale', 'country', 'brand'],
    [REPOSITORY_KEYS.auth]: ['authToken'],
  }}
  loadingFallback={LoadingSpinner}
>
  <App />
</RepositoryLoader>
```

**Why**: RepositoryLoader blocks rendering until all required data is loaded and validated, preventing null reference errors downstream.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/repository-loader/RepositoryLoader.tsx:59`

### Component Structure

```typescript
import { useQueries } from '@tanstack/react-query';
import { View } from 'react-native';

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

/**
 * RepositoryLoader ensures critical repository data is loaded before rendering child components.
 * It uses React Query's useQueries to dynamically fetch multiple repositories simultaneously.
 *
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

  const requiredKeys = Object.keys(
    requiredRepositories
  ) as RequiredRepositoryKeys[];

  // Validate all keys exist in DATA_ACCESS_OBJECTS
  validateRepositoryKeys(requiredKeys);

  // Create query configs for all required repositories
  const queryConfigs = requiredKeys.map((key) =>
    createQueryConfig(DATA_ACCESS_OBJECTS[key])
  );

  // Load all repositories in parallel
  const queryResults = useQueries({ queries: queryConfigs });
  const enrichedResults = getEnrichedResults(requiredKeys, queryResults);

  // Throw errors to ErrorBoundary
  const failed = enrichedResults.find(
    (result) => result.isError && result.error
  );
  if (failed) {
    throwRepositoryLoadError(failed.error);
  }

  // Check if all queries are successful
  const allSuccess = enrichedResults.every(
    (result) => result.isSuccess && result.isFetched
  );
  const anyLoading = enrichedResults.some(
    (result) => result.isLoading || result.isFetching
  );

  // Show loading fallback while data is loading
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

  // Validate required properties exist in data
  validateRequiredProperties(enrichedResults, requiredRepositories);

  return <>{children}</>;
};
```

**Why**: This structure ensures data is loaded, validated, and available before children render.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/repository-loader/RepositoryLoader.tsx:1`

## Configuration

### requiredRepositories

Specify which repositories and properties must be loaded:

```typescript
const requiredRepositories = {
  // Repository key: Array of required properties
  [REPOSITORY_KEYS.appConfig]: ['locale', 'country', 'brand', 'baseUrl'],
  [REPOSITORY_KEYS.auth]: ['authToken'],
  [REPOSITORY_KEYS.plan]: ['currentPlan', 'deliveryDay'],
};

<RepositoryLoader requiredRepositories={requiredRepositories}>
  <Screen />
</RepositoryLoader>
```

**Format**:
- **Key**: Repository key from `REPOSITORY_KEYS` constants
- **Value**: Array of required property names (strings)

**Why**: Explicit configuration documents data dependencies and enables validation.

### loadingFallback

Provide custom loading component:

```typescript
// With component reference
<RepositoryLoader
  requiredRepositories={requiredRepositories}
  loadingFallback={LoadingSpinner}
>
  <App />
</RepositoryLoader>

// With inline component
<RepositoryLoader
  requiredRepositories={requiredRepositories}
  loadingFallback={() => (
    <View style={styles.loading}>
      <ActivityIndicator size="large" />
      <Text>Loading app data...</Text>
    </View>
  )}
>
  <App />
</RepositoryLoader>
```

**Why**: Custom loading fallback provides better UX during initial data load. If omitted, uses default Spinner with "Initializing app..." text.

## Error Handling

### Throws to ErrorBoundary

RepositoryLoader throws errors instead of handling them internally:

```typescript
// In RepositoryLoader implementation
const failed = enrichedResults.find(
  (result) => result.isError && result.error
);
if (failed) {
  throwRepositoryLoadError(failed.error); // Throws to ErrorBoundary
}

// Validate required properties
validateRequiredProperties(enrichedResults, requiredRepositories);
// Throws if properties are missing
```

**Error Types**:
- Query failures (network errors, native module errors)
- Missing repository data
- Missing required properties

**Why**: Throwing errors enables ErrorBoundary to handle failures with consistent UI and retry logic.

### Validation Errors

Throws error if required properties are missing:

```typescript
/**
 * Ensures all required repository properties are present in the fetched data.
 * This is the final validation step before allowing children to render.
 *
 * @throws {Error} If data is missing for any repository
 * @throws {Error} If any required properties are missing from repository data
 */
export const validateRequiredProperties = (
  results: Array<EnrichedQueryResult>,
  requiredRepositories: RequiredRepositories
): void => {
  for (const result of results) {
    const { repositoryKey, data } = result;

    if (!data) {
      throw new Error(
        `RepositoryLoader: Data for repository '${repositoryKey}' is missing.`
      );
    }

    const requiredProps = requiredRepositories[repositoryKey];
    const missing = requiredProps.filter((key) => !(key in data));

    if (missing.length > 0) {
      throw new Error(
        `RepositoryLoader: Missing required properties [${missing.join(', ')}] in '${repositoryKey}'.`
      );
    }
  }
};
```

**Why**: Validation ensures all required data is present before rendering, providing clear error messages for debugging.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/repository-loader/helpers.ts:83`

### Error Recovery with ErrorBoundary

```typescript
<ErrorBoundary
  scope={{ moduleName: 'App' }}
  fallback={({ error, resetError }) => (
    <View>
      <Text>Failed to load app data</Text>
      <Text>{error.message}</Text>
      <Button onPress={resetError}>Retry</Button>
    </View>
  )}
>
  <RepositoryLoader
    requiredRepositories={{
      [REPOSITORY_KEYS.appConfig]: ['locale', 'country'],
    }}
  >
    <App />
  </RepositoryLoader>
</ErrorBoundary>
```

**Why**: Reset mechanism allows users to retry after failures.

## Integration with Navigation

### withNavigationEntryProvider HOC

Wrap navigation stacks with RepositoryLoader:

```typescript
import { withNavigationEntryProvider } from '@entry-providers';
import { REPOSITORY_KEYS } from '@data-access/native/constants';

// Internal stack component
const StoreStackInternal = (props: IStoreStackProps) => {
  return (
    <Stack.Navigator>
      {/* screens */}
    </Stack.Navigator>
  );
};

// Export wrapped with RepositoryLoader
export const StoreStack = withNavigationEntryProvider(
  StoreStackInternal,
  linkingConfig,
  {
    [REPOSITORY_KEYS.appConfig]: ['locale', 'country', 'brand', 'baseUrl'],
  }
);
```

**Why**: Wrapping NavigationContainer ensures data is loaded before any screens render.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/store/stacks/store/StoreStack.tsx:70`

## Repository Keys

### Define Constants

Create constants for all repository keys:

```typescript
// data-access/native/constants.ts
export const REPOSITORY_KEYS = {
  appConfig: 'appConfig',
  auth: 'auth',
  plan: 'plan',
  navigationBar: 'navigationBar',
  loyaltyBanner: 'loyaltyBanner',
  loyaltyProgramState: 'loyaltyProgramState',
} as const;
```

**Why**: Constants prevent typos and enable IDE autocomplete.

### Data Access Objects Mapping

Map repository keys to data access objects:

```typescript
import {
  AppConfigDataAccess,
  PlanDataAccess,
  NavigationBarDataAccess,
} from '@data-access/native';

/**
 * DATA_ACCESS_OBJECTS provides centralized mapping of repository keys
 * to their data access objects.
 *
 * Each object must have: fetch (function) and repositoryKey (string) properties
 */
export const DATA_ACCESS_OBJECTS: Partial<
  Record<RepositoryName, DataAccessType>
> = {
  appConfig: AppConfigDataAccess,
  plan: PlanDataAccess,
  navigationBar: NavigationBarDataAccess,
  // Add new repositories here
} as const;

/**
 * Helper to create query configuration from data access object
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
    queryKey: [NATIVE_MODULES_REPOSITORY_QUERY_KEY, dataAccessObject.repositoryKey],
    queryFn: dataAccessObject.fetch,
  };
};
```

**Why**: Centralized mapping eliminates duplication and ensures consistent query creation.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/repository-loader/constants.ts:21`

## Performance

### Parallel Loading

RepositoryLoader uses `useQueries` to load repositories in parallel:

```typescript
// Create query configs for all required repositories
const queryConfigs = requiredKeys.map((key) =>
  createQueryConfig(DATA_ACCESS_OBJECTS[key])
);

// Loads all repositories simultaneously
const queryResults = useQueries({ queries: queryConfigs });
```

**Why**: Parallel loading minimizes total load time compared to sequential loading.

### Caching

Repositories use TanStack Query caching:

```typescript
// Repositories are cached and reused across components
const { data: appConfig } = useAppConfigState(); // Cache hit if already loaded

// TanStack Query handles cache invalidation and refetch logic
```

**Why**: Caching prevents redundant API calls and improves performance.

## Testing

### Mock RepositoryLoader

Mock RepositoryLoader in tests:

```typescript
jest.mock('@libs/repository-loader', () => ({
  RepositoryLoader: ({ children }: { children: React.ReactNode }) => children,
}));

test('renders app when data is loaded', () => {
  render(
    <NavigationEntryProvider
      requiredRepositories={{
        [REPOSITORY_KEYS.appConfig]: ['locale'],
      }}
    >
      <App />
    </NavigationEntryProvider>
  );

  expect(screen.getByText('Home')).toBeTruthy();
});
```

**Why**: Mocking simplifies tests by removing data loading dependencies.

### Test with useQueries Mock

```typescript
import { useQueries } from '@tanstack/react-query';
import { render, screen } from '@testing-library/react-native';

jest.mock('@tanstack/react-query', () => ({
  ...jest.requireActual('@tanstack/react-query'),
  useQueries: jest.fn(),
}));

describe('RepositoryLoader', () => {
  it('renders fallback while loading', () => {
    const fallback = () => <Text testID="fallback">Loading...</Text>;

    // Simulate loading state
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
      <RepositoryLoader
        requiredRepositories={{ appConfig: ['locale'] }}
        loadingFallback={fallback}
      >
        <TestChild />
      </RepositoryLoader>
    );

    expect(screen.getByTestID('fallback')).toBeTruthy();
  });

  it('throws error and is caught by ErrorBoundary', () => {
    // Simulate error state
    (useQueries as jest.Mock).mockReturnValue([
      {
        isError: true,
        isSuccess: false,
        isFetched: false,
        isLoading: false,
        isFetching: false,
        error: new Error('Test failure'),
      },
    ]);

    const onError = jest.fn();

    render(
      <ErrorBoundary scope={{ moduleName: 'Test' }} onError={onError}>
        <RepositoryLoader requiredRepositories={{ appConfig: ['locale'] }}>
          <TestChild />
        </RepositoryLoader>
      </ErrorBoundary>
    );

    expect(onError).toHaveBeenCalled();
  });
});
```

**Why**: Testing loading and error states ensures RepositoryLoader behaves correctly in all scenarios.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/repository-loader/RepositoryLoader.test.tsx:1`

## Common Mistakes to Avoid

❌ **Don't skip validation**:

```typescript
// ❌ Missing RepositoryLoader - may render with undefined data
<NavigationContainer>
  <Stack.Screen component={ScreenNeedingAppConfig} />
</NavigationContainer>
```

❌ **Don't require unnecessary properties**:

```typescript
// ❌ Requires unused property
requiredRepositories={{
  [REPOSITORY_KEYS.appConfig]: [
    'locale',
    'country',
    'brand',
    'theme', // Not actually used - unnecessary requirement
  ],
}}
```

❌ **Don't handle errors internally**:

```typescript
// ❌ Don't try/catch in RepositoryLoader
try {
  validateRequiredProperties(results, requiredRepositories);
} catch (error) {
  // Don't handle here - let it bubble to ErrorBoundary
}
```

❌ **Don't use sequential loading**:

```typescript
// ❌ Sequential loading (slow)
const appConfig = await fetchAppConfig();
const auth = await fetchAuth();
const plan = await fetchPlan();

// ✅ Parallel loading (fast)
const queryResults = useQueries({ queries: queryConfigs });
```

✅ **Do validate required data**:

```typescript
// ✅ Validate with RepositoryLoader
<RepositoryLoader
  requiredRepositories={{
    [REPOSITORY_KEYS.appConfig]: ['locale', 'country'], // Only what's needed
  }}
  loadingFallback={LoadingSpinner}
>
  <App />
</RepositoryLoader>
```

✅ **Do provide meaningful loading states**:

```typescript
// ✅ Custom loading message
<RepositoryLoader
  requiredRepositories={requiredRepositories}
  loadingFallback={() => (
    <View>
      <Spinner size="lg" />
      <Text>Loading your preferences...</Text>
    </View>
  )}
>
  <App />
</RepositoryLoader>
```

✅ **Do throw errors to ErrorBoundary**:

```typescript
// ✅ Let errors bubble to ErrorBoundary
if (failed) {
  throwRepositoryLoadError(failed.error);
}
```

✅ **Do load in parallel**:

```typescript
// ✅ useQueries loads all repositories simultaneously
const queryResults = useQueries({ queries: queryConfigs });
```

## Common Patterns

### App-Level Loading

Require app configuration and authentication at app root:

```typescript
<ErrorBoundary scope={{ moduleName: 'App' }}>
  <NavigationEntryProvider
    requiredRepositories={{
      [REPOSITORY_KEYS.appConfig]: ['locale', 'country', 'brand'],
      [REPOSITORY_KEYS.auth]: ['authToken'],
    }}
    repositoryLoadingFallback={AppLoadingScreen}
  >
    <MainNavigator />
  </NavigationEntryProvider>
</ErrorBoundary>
```

**Why**: App-level validation prevents screens from rendering without critical data.

### Feature-Level Loading

Require feature-specific data at feature entry:

```typescript
<RepositoryLoader
  requiredRepositories={{
    [REPOSITORY_KEYS.plan]: ['currentPlan', 'deliveryDay'],
    [REPOSITORY_KEYS.loyaltyBanner]: ['isEligible'],
  }}
  loadingFallback={FeatureLoadingScreen}
>
  <CheckoutFlow />
</RepositoryLoader>
```

**Why**: Feature-level validation ensures feature has required data.

## Quick Reference

**Basic Setup:**
- Import `RepositoryLoader` from `@libs/repository-loader`
- Import `REPOSITORY_KEYS` from `@data-access/native/constants`
- Configure `requiredRepositories` object
- Provide `loadingFallback` component
- Wrap children that depend on data

**Configuration:**
- `requiredRepositories`: `{ [REPOSITORY_KEYS.key]: ['prop1', 'prop2'] }`
- `loadingFallback`: Component or function returning component
- `children`: Components to render after data loads

**Error Handling:**
- Throws to ErrorBoundary on query failure
- Throws on missing repository data
- Throws on missing required properties
- Use ErrorBoundary wrapper for retry logic

**Performance:**
- Uses `useQueries` for parallel loading
- TanStack Query caching prevents redundant calls
- Validates keys before creating queries
- Enriches results with repository context

**Testing:**
- Mock `RepositoryLoader` to bypass in tests
- Mock `useQueries` for state testing
- Use ErrorBoundary for error testing
- Test loading, success, and error states

**Key Libraries:**
- TanStack Query (React Query) 5.59.16
- @zest/react-native 1.3.1

For production examples, see [references/examples.md](references/examples.md).
