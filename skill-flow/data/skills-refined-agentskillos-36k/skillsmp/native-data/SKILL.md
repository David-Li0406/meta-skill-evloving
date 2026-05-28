---
name: native-data
description: "WHAT: Access native iOS/Android repository data with TanStack Query. WHEN: fetching auth tokens, app config, plan data from native container. KEYWORDS: native, repository, fetchRepository, iOS, android, container, observables, DataAccess, nativeRepositories."
---

# Native Data Access Patterns

## Core Principles

**Use native data access ONLY for observables from the iOS/Android container.** For server data, use GraphQL or REST patterns. Native repositories provide a bridge between native modules and React Query, with event-driven updates and fallback handling.

**Why**: Native data access is specialized for container-provided observables (auth, config, plan). Using it for server data would bypass proper API patterns and lose features like request cancellation, retry logic, and error handling.

## When to Use This Skill

Use these patterns when:

- Accessing data from native iOS/Android container modules
- Working with observables provided by the container app
- Need event-driven updates from native layer
- Requires fallback to initial state when native doesn't respond
- Working with auth tokens, app config, or plan data
- Need consistent query keys for native repositories
- Building data access objects for RepositoryLoader

**⚠️ DO NOT USE for:**
- Server API calls (use GraphQL or REST patterns)
- Component state (use useState or Zustand)
- Derived data (compute in queries or components)

## Domain-Based File Organization

### Standard Structure

Each native repository follows this domain-based pattern:

```
data-access/native/[domain]/
├── constants.ts          # Query keys and constants
├── repository.ts         # fetchRepository implementation
├── schema.ts            # TypeScript schema
├── queries.ts           # TanStack Query hooks
├── events.ts            # Event emitters (optional)
└── types.ts             # Additional types (optional)
```

**Why**: Domain-based organization keeps related code together, makes repositories easy to find, and enforces consistent structure.

**Production Example**: `git-resources/shared-mobile-modules/src/data-access/native/plan/`

## Query Key Pattern

### Standard Query Keys

All native repositories use consistent query key structure:

```typescript
// constants.ts
export const NATIVE_MODULES_REPOSITORY_QUERY_KEY = 'nativeRepositories';
export const PLAN_QUERY_KEY = 'plan';

// queries.ts
import { NATIVE_MODULES_REPOSITORY_QUERY_KEY } from '../constants';
import { PLAN_QUERY_KEY } from './constants';

export const usePlanId = () =>
  useQuery({
    queryKey: [NATIVE_MODULES_REPOSITORY_QUERY_KEY, PLAN_QUERY_KEY],
    queryFn: fetchPlanRepository,
    select: (data) => data.planId,
  });
```

**Pattern**: `['nativeRepositories', domain]`

**Why**: Consistent query keys enable:
- Easy cache invalidation across all native repositories
- RepositoryLoader to dynamically create queries
- Clear separation from server data queries
- Centralized repository management

**Production Example**: `git-resources/shared-mobile-modules/src/data-access/native/plan/queries.ts:13`

## Repository Implementation

### fetchRepository Pattern

```typescript
// repository.ts
import { fetchRepository } from '@libs/query';
import { PLAN_QUERY_KEY } from './constants';
import type { PlanRepositorySchema } from './schema';

const initialState: PlanRepositorySchema = {
  subscriptionId: undefined,
  planId: undefined,
};

export const fetchPlanRepository = async () =>
  fetchRepository<PlanRepositorySchema>(PLAN_QUERY_KEY, initialState);
```

**Key elements:**
1. Import `fetchRepository` from `@libs/query`
2. Define typed `initialState` matching schema
3. Export domain-specific fetch function
4. Pass query key and initial state

**Why**: `fetchRepository` handles:
- Event-driven communication with native layer
- Timeout fallback to cached data or initial state
- Promise resolution when native responds
- Error handling with graceful degradation

**Production Example**: `git-resources/shared-mobile-modules/src/data-access/native/plan/repository.ts:1`

### fetchRepository Implementation

```typescript
// @libs/query/client.ts
export const fetchRepository = async <T>(
  repositoryName: RepositoryName,
  initialState: T
): Promise<T> => {
  return new Promise(async (resolve) => {
    console.debug(`[fetchRepository] Requesting repository: ${repositoryName}`);

    // Send event to native to start fetching the repository
    sendEvent(QueryEvents.getRepository, {
      repository: repositoryName,
    });

    // Listen for the setRepository event from native
    const subscription = SharedModulesEventEmitter.addListener(
      'setRepository',
      (payload) => {
        try {
          const { data, repository } = SetRepositoryPayload.parse(payload);

          if (repository !== repositoryName) {
            return;
          }

          console.debug(
            `[fetchRepository] Received repository data for: ${repository}`
          );

          const parsed = JSON.parse(data);
          subscription.remove();
          resolve(parsed as T);
        } catch (error) {
          console.error('Error handling setRepository payload:', error);
          subscription.remove();
          resolve(initialState);
        }
      }
    );

    // Fallback timeout in case native never responds
    setTimeout(() => {
      subscription.remove();
      console.warn(
        `[fetchRepository] Timeout waiting for repository: ${repositoryName}. Falling back to cached data or initial state.`
      );

      const cached = queryClient.getQueryData([
        NATIVE_MODULES_REPOSITORY_QUERY_KEY,
        repositoryName,
      ]);

      if (cached) {
        console.debug(
          `[fetchRepository] Using cached data for: ${repositoryName}`
        );
        resolve(cached as T);
      } else {
        console.debug(
          `[fetchRepository] No cached data, using initial state for: ${repositoryName}`
        );
        resolve(initialState);
      }
    }, 2000);
  });
};
```

**Key patterns:**
- Event-based communication with native layer
- Subscription cleanup after receiving data
- 2-second timeout with fallback to cache or initial state
- Error handling resolves to initial state (doesn't throw)

**Why**: Handles unreliable native communication gracefully without blocking UI.

**Production Example**: `git-resources/shared-mobile-modules/src/libs/query/client.ts:29`

## Schema Definition

### TypeScript Schema

```typescript
// schema.ts
export interface PlanRepositorySchema {
  planId?: string;
  subscriptionId?: string;
}
```

**Patterns:**
- Optional properties (native may not provide all data)
- Clear, descriptive property names
- Exported interface for type safety

**Why**: Schema documents expected data shape and enables TypeScript validation throughout the application.

**Production Example**: `git-resources/shared-mobile-modules/src/data-access/native/plan/schema.ts:1`

## Query Hooks

### Custom Hooks with select

```typescript
// queries.ts
import { useQuery } from '@tanstack/react-query';
import { NATIVE_MODULES_REPOSITORY_QUERY_KEY } from '../constants';
import { PLAN_QUERY_KEY } from './constants';
import { fetchPlanRepository } from './repository';

/**
 * Get the planId from the plan repository.
 */
export const usePlanId = () =>
  useQuery({
    queryKey: [NATIVE_MODULES_REPOSITORY_QUERY_KEY, PLAN_QUERY_KEY],
    queryFn: fetchPlanRepository,
    select: (data) => data.planId,
  });

/**
 * Get the subscriptionId from the plan repository.
 */
export const useSubscriptionId = () =>
  useQuery({
    queryKey: [NATIVE_MODULES_REPOSITORY_QUERY_KEY, PLAN_QUERY_KEY],
    queryFn: fetchPlanRepository,
    select: (data) => data.subscriptionId,
  });
```

**Patterns:**
- One hook per property using `select`
- Same query key and queryFn (TanStack Query deduplicates)
- JSDoc comments for each hook
- Consistent naming: `use{Property}` pattern

**Why**: Multiple components can select different properties without duplicate network requests. TanStack Query caches the full repository and computes selectors efficiently.

**Production Example**: `git-resources/shared-mobile-modules/src/data-access/native/plan/queries.ts:1`

### Complex select Logic

```typescript
// queries.ts
import { useQuery } from '@tanstack/react-query';
import { isCustomerAuth } from '@libs/networking-client';
import { localStorage } from '@libs/persistent-storage';

const customerToken = localStorage.getString(LOCALSTORE_CUSTOMER_TOKEN)
  ? JSON.parse(localStorage.getString(LOCALSTORE_CUSTOMER_TOKEN))
  : undefined;

export const useAuthState = () =>
  useQuery({
    queryKey: [NATIVE_MODULES_REPOSITORY_QUERY_KEY, AUTH_QUERY_KEY],
    queryFn: fetchAuthRepository,
    select: (data) => data.authToken || customerToken,
  });

export const useIsSignedInState = () =>
  useQuery({
    queryKey: [NATIVE_MODULES_REPOSITORY_QUERY_KEY, AUTH_QUERY_KEY],
    queryFn: fetchAuthRepository,
    select: (data) =>
      Boolean(data.authToken && isCustomerAuth(data.authToken)) ||
      Boolean(customerToken && isCustomerAuth(customerToken)),
  });
```

**Patterns:**
- Fallback logic in select (authToken || customerToken)
- Boolean derivation for authentication state
- Multiple hooks share same query (different selectors)

**Why**: Keeps complex logic in queries layer, not components. Components get computed values directly.

**Production Example**: `git-resources/shared-mobile-modules/src/data-access/native/auth/queries.ts:46`

## Event Integration

### Event Definitions

```typescript
// events.ts
import { sendEvent } from '@libs/native-modules/events';
import type { UpdatePlanEventData } from './types';

export enum PlanEvents {
  updatePlan = 'updatePlan',
}

export type PlanEventNames = PlanEvents.updatePlan;

/**
 * Emits an update event to the native layer.
 */
export const updatePlan = async (data: UpdatePlanEventData) =>
  sendEvent(PlanEvents.updatePlan, {
    payload: JSON.stringify(data),
  });
```

**Patterns:**
- Enum for event names
- Type alias for event names union
- Event emitter functions with typed data
- JSON.stringify for payload

**Why**: Type-safe event communication with native layer. Enum prevents typos, types ensure correct data structure.

**Production Example**: `git-resources/shared-mobile-modules/src/data-access/native/plan/events.ts:1`

## DataAccess Objects

### Centralized Export Pattern

```typescript
// index.ts
import { REPOSITORY_KEYS } from '@data-access/native/constants';

import * as AppConfigEvents from './app-config/events';
import * as AppConfigQueries from './app-config/queries';
import { fetchAppConfigRepository } from './app-config/repository';
import * as AuthEvents from './auth/events';
import * as AuthQueries from './auth/queries';
import { fetchAuthRepository } from './auth/repository';
import * as PlanEvents from './plan/events';
import * as PlanQueries from './plan/queries';
import { fetchPlanRepository } from './plan/repository';

export const AuthDataAccess = {
  events: AuthEvents,
  queries: AuthQueries,
  fetch: fetchAuthRepository,
  repositoryKey: REPOSITORY_KEYS.auth,
} as const;

export const AppConfigDataAccess = {
  events: AppConfigEvents,
  queries: AppConfigQueries,
  fetch: fetchAppConfigRepository,
  repositoryKey: REPOSITORY_KEYS.appConfig,
} as const;

export const PlanDataAccess = {
  events: PlanEvents,
  queries: PlanQueries,
  fetch: fetchPlanRepository,
  repositoryKey: REPOSITORY_KEYS.plan,
} as const;
```

**Structure:**
- `events`: Event emitters namespace
- `queries`: Query hooks namespace
- `fetch`: Repository fetch function
- `repositoryKey`: Constant for REPOSITORY_KEYS mapping

**Why**: DataAccess objects provide:
- Single import for all domain functionality
- Used by RepositoryLoader for dynamic query creation
- Consistent API across all repositories
- Type-safe access with `as const`

**Production Example**: `git-resources/shared-mobile-modules/src/data-access/native/index.ts:34`

## Constants

### Repository Keys

```typescript
// constants.ts
export const NATIVE_MODULES_REPOSITORY_QUERY_KEY = 'nativeRepositories';

export const REPOSITORY_KEYS = {
  auth: AUTH_QUERY_KEY,
  appConfig: APP_CONFIG_QUERY_KEY,
  plan: PLAN_QUERY_KEY,
  navigationBar: NAVIGATION_BAR_QUERY_KEY,
  nativeNavigation: NATIVE_NAVIGATION_RESULT_QUERY_KEY,
  loyaltyBanner: LOYALTY_BANNER_QUERY_KEY,
  inboxSalesforce: INBOX_SALESFORCE_QUERY_KEY,
  loyaltyProgramState: LOYALTY_PROGRAM_STATE_QUERY_KEY,
} as const;
```

**Patterns:**
- Single NATIVE_MODULES_REPOSITORY_QUERY_KEY for all repositories
- REPOSITORY_KEYS object mapping repository names to their keys
- `as const` for type safety

**Why**: Centralized keys enable:
- RepositoryLoader to dynamically load repositories
- Consistent query key structure
- Type-safe repository key references
- Easy addition of new repositories

**Production Example**: `git-resources/shared-mobile-modules/src/data-access/native/constants.ts:1`

## Usage in Components

### Basic Usage

```typescript
import { PlanDataAccess } from '@data-access/native';

export const CheckoutScreen = () => {
  const { data: planId, isLoading } = PlanDataAccess.queries.usePlanId();

  if (isLoading) return <LoadingSpinner />;
  if (!planId) return <ErrorMessage />;

  return <CheckoutFlow planId={planId} />;
};
```

**Patterns:**
- Import DataAccess object
- Use queries through DataAccess namespace
- Handle loading and undefined states
- Pass data to child components

**Why**: Components get clean API without knowing about query keys or fetch functions.

### Multiple Properties

```typescript
import { AppConfigDataAccess } from '@data-access/native';

export const LocalizedScreen = () => {
  const { data: locale } = AppConfigDataAccess.queries.useLocale();
  const { data: country } = AppConfigDataAccess.queries.useCountry();
  const { data: brand } = AppConfigDataAccess.queries.useBrand();

  // All three hooks share same query - no duplicate requests
  return (
    <LocalizedContent
      locale={locale}
      country={country}
      brand={brand}
    />
  );
};
```

**Why**: TanStack Query deduplicates requests automatically. Multiple hooks selecting different properties is efficient.

## Common Mistakes to Avoid

❌ **Don't use for server data**:

```typescript
// ❌ Wrong - Native data access is NOT for API calls
export const fetchProductsRepository = async () =>
  fetchRepository<Product[]>('products', []);

// ✅ Correct - Use GraphQL or REST
export const useGetProductsQuery = () =>
  useQuery({
    queryKey: ['products'],
    queryFn: () => apiClient.get('/products'),
  });
```

❌ **Don't skip initial state**:

```typescript
// ❌ Missing initial state - will be undefined on timeout
export const fetchPlanRepository = async () =>
  fetchRepository<PlanRepositorySchema>(PLAN_QUERY_KEY);

// ✅ Always provide initial state
const initialState: PlanRepositorySchema = {
  subscriptionId: undefined,
  planId: undefined,
};

export const fetchPlanRepository = async () =>
  fetchRepository<PlanRepositorySchema>(PLAN_QUERY_KEY, initialState);
```

❌ **Don't use different query keys**:

```typescript
// ❌ Inconsistent query keys
export const usePlanId = () =>
  useQuery({
    queryKey: ['plan'], // Wrong!
    queryFn: fetchPlanRepository,
    select: (data) => data.planId,
  });

// ✅ Always use NATIVE_MODULES_REPOSITORY_QUERY_KEY
export const usePlanId = () =>
  useQuery({
    queryKey: [NATIVE_MODULES_REPOSITORY_QUERY_KEY, PLAN_QUERY_KEY],
    queryFn: fetchPlanRepository,
    select: (data) => data.planId,
  });
```

❌ **Don't create duplicate queries**:

```typescript
// ❌ Multiple hooks with different query keys
export const usePlanId = () =>
  useQuery({
    queryKey: ['planId'],
    queryFn: async () => {
      const data = await fetchPlanRepository();
      return data.planId;
    },
  });

// ✅ Share same query with select
export const usePlanId = () =>
  useQuery({
    queryKey: [NATIVE_MODULES_REPOSITORY_QUERY_KEY, PLAN_QUERY_KEY],
    queryFn: fetchPlanRepository,
    select: (data) => data.planId,
  });
```

✅ **Do follow domain-based structure**:

```typescript
// ✅ Correct structure
data-access/native/plan/
├── constants.ts
├── repository.ts
├── schema.ts
├── queries.ts
└── events.ts
```

✅ **Do use DataAccess objects**:

```typescript
// ✅ Centralized export
export const PlanDataAccess = {
  events: PlanEvents,
  queries: PlanQueries,
  fetch: fetchPlanRepository,
  repositoryKey: REPOSITORY_KEYS.plan,
} as const;
```

✅ **Do provide fallback logic**:

```typescript
// ✅ Fallback to cached data or initial state
setTimeout(() => {
  const cached = queryClient.getQueryData([
    NATIVE_MODULES_REPOSITORY_QUERY_KEY,
    repositoryName,
  ]);

  if (cached) {
    resolve(cached as T);
  } else {
    resolve(initialState);
  }
}, 2000);
```

✅ **Do use select for property access**:

```typescript
// ✅ Efficient property selection
export const usePlanId = () =>
  useQuery({
    queryKey: [NATIVE_MODULES_REPOSITORY_QUERY_KEY, PLAN_QUERY_KEY],
    queryFn: fetchPlanRepository,
    select: (data) => data.planId,
  });
```

## Testing

### Mock fetchRepository

```typescript
import { fetchRepository } from '@libs/query';

jest.mock('@libs/query', () => ({
  fetchRepository: jest.fn(),
  queryClient: {
    getQueryData: jest.fn(),
  },
}));

describe('fetchPlanRepository', () => {
  it('returns plan data from native', async () => {
    const mockData = {
      planId: 'plan-123',
      subscriptionId: 'sub-456',
    };

    (fetchRepository as jest.Mock).mockResolvedValue(mockData);

    const result = await fetchPlanRepository();

    expect(fetchRepository).toHaveBeenCalledWith(
      PLAN_QUERY_KEY,
      expect.objectContaining({
        planId: undefined,
        subscriptionId: undefined,
      })
    );
    expect(result).toEqual(mockData);
  });

  it('returns initial state on timeout', async () => {
    (fetchRepository as jest.Mock).mockResolvedValue({
      planId: undefined,
      subscriptionId: undefined,
    });

    const result = await fetchPlanRepository();

    expect(result.planId).toBeUndefined();
    expect(result.subscriptionId).toBeUndefined();
  });
});
```

**Patterns:**
- Mock `fetchRepository` from `@libs/query`
- Verify correct query key and initial state passed
- Test both success and timeout scenarios
- Assert returned data matches expected shape

**Why**: Testing mocked fetchRepository ensures repository functions call it correctly without depending on native layer.

### Mock Query Hooks

```typescript
import { renderHook } from '@testing-library/react-native';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { usePlanId } from './queries';

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  return ({ children }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};

describe('usePlanId', () => {
  it('returns planId from repository', async () => {
    (fetchRepository as jest.Mock).mockResolvedValue({
      planId: 'plan-123',
      subscriptionId: 'sub-456',
    });

    const { result } = renderHook(() => usePlanId(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(result.current.data).toBe('plan-123');
  });
});
```

**Why**: Tests verify hooks correctly select properties from repository data.

## Quick Reference

**File Structure:**
- `constants.ts`: Query keys and constants
- `repository.ts`: fetchRepository implementation
- `schema.ts`: TypeScript interface
- `queries.ts`: TanStack Query hooks
- `events.ts`: Event emitters (optional)
- `index.ts`: DataAccess object export

**Query Key Pattern:**
```typescript
[NATIVE_MODULES_REPOSITORY_QUERY_KEY, DOMAIN_QUERY_KEY]
// Example: ['nativeRepositories', 'plan']
```

**Repository Pattern:**
```typescript
const initialState: Schema = { /* defaults */ };
export const fetch{Domain}Repository = async () =>
  fetchRepository<Schema>(DOMAIN_QUERY_KEY, initialState);
```

**Query Hook Pattern:**
```typescript
export const use{Property} = () =>
  useQuery({
    queryKey: [NATIVE_MODULES_REPOSITORY_QUERY_KEY, DOMAIN_QUERY_KEY],
    queryFn: fetch{Domain}Repository,
    select: (data) => data.property,
  });
```

**DataAccess Object Pattern:**
```typescript
export const {Domain}DataAccess = {
  events: {Domain}Events,
  queries: {Domain}Queries,
  fetch: fetch{Domain}Repository,
  repositoryKey: REPOSITORY_KEYS.{domain},
} as const;
```

**Key Libraries:**
- TanStack Query (React Query) 5.59.16
- React Native 0.75.4

**⚠️ Remember**: Native data access is ONLY for native observables. Use GraphQL or REST for server data.

For production examples, see [references/examples.md](references/examples.md).
