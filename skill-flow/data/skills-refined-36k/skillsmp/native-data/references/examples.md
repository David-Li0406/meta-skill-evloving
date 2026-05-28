# Native Data Access - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating native data access patterns.

## Example 1: Plan Repository Implementation

**File**: `data-access/native/plan/repository.ts`

This example shows the complete pattern for implementing a native repository.

```typescript
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

**Key patterns demonstrated:**
- Import `fetchRepository` from `@libs/query`
- Define typed `initialState` matching schema
- Export async repository fetch function
- Type parameter ensures type safety

**Schema Definition** (`schema.ts`):

```typescript
export interface PlanRepositorySchema {
  planId?: string;
  subscriptionId?: string;
}
```

**Key patterns demonstrated:**
- Optional properties (native may not provide all data)
- Clear, descriptive property names
- Exported interface for type safety across app

## Example 2: Query Hooks with select

**File**: `data-access/native/plan/queries.ts`

This example demonstrates creating multiple hooks that share the same query but select different properties.

```typescript
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

**Key patterns demonstrated:**
- Multiple hooks share same query key and queryFn
- `select` extracts specific properties
- TanStack Query deduplicates requests automatically
- JSDoc comments for each hook
- Consistent naming: `use{Property}` pattern

**Why this works efficiently:**
TanStack Query caches the full repository response once. Both hooks reference the same cache entry and compute their selectors. No duplicate network requests occur.

## Example 3: Auth Repository with Fallback Logic

**File**: `data-access/native/auth/queries.ts`

This example shows complex select logic with fallback handling.

```typescript
import { useQuery } from '@tanstack/react-query';

import type { Auth } from '@libs/networking-client';
import { isCustomerAuth } from '@libs/networking-client';
import { localStorage } from '@libs/persistent-storage';
import { queryClient } from '@libs/query';

import { NATIVE_MODULES_REPOSITORY_QUERY_KEY } from '../constants';

import {
  AUTH_QUERY_KEY,
  LOCALSTORE_CUSTOMER_TOKEN,
  LOCALSTORE_HAS_LAUNCHED_BEFORE,
} from './constants';
import { fetchAuthRepository } from './repository';

const hasLaunchedBefore = localStorage.getBoolean(
  LOCALSTORE_HAS_LAUNCHED_BEFORE
);

const customerTokenFromStorage = localStorage.getString(
  LOCALSTORE_CUSTOMER_TOKEN
);

if (!hasLaunchedBefore) {
  localStorage.remove(LOCALSTORE_CUSTOMER_TOKEN);
  localStorage.set(LOCALSTORE_HAS_LAUNCHED_BEFORE, true);
}

const customerToken = customerTokenFromStorage
  ? (JSON.parse(customerTokenFromStorage) as Auth)
  : undefined;

export const getAuthFromQueryClient = async () => {
  const authRepository = await queryClient.fetchQuery({
    queryKey: [NATIVE_MODULES_REPOSITORY_QUERY_KEY, AUTH_QUERY_KEY],
    queryFn: fetchAuthRepository,
  });

  // If authRepository.authToken is defined, return it. Otherwise return customerToken which is
  // shared from the old whitelabel-mobile app through local storage (MMKV), and is only defined
  // on first launch of the new app.
  return authRepository.authToken || customerToken;
};

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

// Only used by the shell app
export const useUsernameState = () =>
  useQuery({
    queryKey: [NATIVE_MODULES_REPOSITORY_QUERY_KEY, AUTH_QUERY_KEY],
    queryFn: fetchAuthRepository,
    select: (data) =>
      data.authToken && isCustomerAuth(data.authToken)
        ? data.authToken.user_data.username
        : undefined,
  });
```

**Key patterns demonstrated:**
- Fallback to localStorage for migration scenarios
- `select` with OR logic (authToken || customerToken)
- Boolean derivation for computed state
- Multiple hooks with different selectors
- Utility function using queryClient.fetchQuery
- Migration cleanup (remove old token after first launch)

**Repository Implementation** (`repository.ts`):

```typescript
import { fetchRepository } from '@libs/query';

import { AUTH_QUERY_KEY } from './constants';
import type { AuthRepositorySchema } from './schema';

const initialState: AuthRepositorySchema = {
  authToken: undefined,
};

export const fetchAuthRepository = async () =>
  fetchRepository<AuthRepositorySchema>(AUTH_QUERY_KEY, initialState);
```

## Example 4: fetchRepository Core Implementation

**File**: `libs/query/client.ts`

This example shows the complete implementation of `fetchRepository` that all repositories use.

```typescript
import { QueryClient } from '@tanstack/react-query';

import {
  NATIVE_MODULES_REPOSITORY_QUERY_KEY,
  type RepositoryName,
} from '@data-access/native';

import {
  sendEvent,
  SharedModulesEventEmitter,
} from '@libs/native-modules/events';

import { QueryEvents } from './events';
import { SetRepositoryPayload } from './listener';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // We use an approach where we notify JS from native side
      // when some data changes.
      staleTime: Infinity,
      // The query client is not responsible for retrying requests.
      // Instead, the fetch client handles retrying requests on 401
      retry: false,
    },
  },
});

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
    // and resolve the promise when we receive it.
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

**Key patterns demonstrated:**
- Event-based communication with native layer
- Send `getRepository` event to request data
- Listen for `setRepository` event response
- 2-second timeout with fallback logic
- Falls back to cached data if available
- Falls back to initial state if no cache
- Subscription cleanup after receiving data
- Error handling resolves to initial state (doesn't throw)
- QueryClient configured with `staleTime: Infinity` (event-driven updates)

**Why this works:**
1. React Query calls `fetchRepository` when query is needed
2. `fetchRepository` sends event to native layer
3. Native layer responds with `setRepository` event
4. Promise resolves with parsed data
5. If native doesn't respond within 2s, falls back gracefully
6. TanStack Query caches result with `staleTime: Infinity`
7. Future requests use cache until invalidated by events

## Example 5: Event Integration

**File**: `data-access/native/plan/events.ts`

This example shows event emitters for communicating with native layer.

```typescript
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

**Key patterns demonstrated:**
- Enum for event names (prevents typos)
- Type alias for union of event names
- Async event emitter functions
- JSON.stringify for payload serialization
- JSDoc comments for public API

**Why this matters:**
- Type-safe event communication with native
- Components can trigger native updates
- Native can respond with updated repository data
- TanStack Query automatically refetches when cache invalidated

## Example 6: DataAccess Objects Export

**File**: `data-access/native/index.ts`

This example shows centralized DataAccess objects that expose all repository functionality.

```typescript
import { REPOSITORY_KEYS } from '@data-access/native/constants';

import {
  DELIVERIES_UPDATED_EVENT,
  onDeliveriesUpdated,
  useDeliveriesUpdateHandler,
  useDeliveriesUpdateRefetch,
} from '@libs/native-modules/events';

import * as AppConfigEvents from './app-config/events';
import * as AppConfigQueries from './app-config/queries';
import { fetchAppConfigRepository } from './app-config/repository';
import * as AuthEvents from './auth/events';
import * as AuthQueries from './auth/queries';
import { fetchAuthRepository } from './auth/repository';
import { fetchInboxSalesforceRepository } from './inbox-salesforce/repository';
import * as LoyaltyBannerQueries from './loyalty-banner/queries';
import { fetchLoyaltyBannerRepository } from './loyalty-banner/repository';
import * as LoyaltyProgramStateQueries from './loyalty-program-state/queries';
import { fetchLoyaltyProgramStateRepository } from './loyalty-program-state/repository';
import * as NavigationEvents from './navigation/events';
import * as NavigationBarEvents from './navigation-bar/events';
import * as NavigationBarQueries from './navigation-bar/queries';
import { fetchNavigationBarRepository } from './navigation-bar/repository';
import * as PlanEvents from './plan/events';
import * as PlanQueries from './plan/queries';
import { fetchPlanRepository } from './plan/repository';

export { NATIVE_MODULES_REPOSITORY_QUERY_KEY } from './constants';
export { ENVIRONMENT } from './app-config/constants';
export type { RepositoryName } from './repositorySchema';
export type { DataAccessType } from './types';

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

export const NavigationDataAccess = {
  events: NavigationEvents,
  repositoryKey: REPOSITORY_KEYS.nativeNavigation,
} as const;

export const NavigationBarDataAccess = {
  events: NavigationBarEvents,
  queries: NavigationBarQueries,
  fetch: fetchNavigationBarRepository,
  repositoryKey: REPOSITORY_KEYS.navigationBar,
} as const;

export const LoyaltyBannerDataAccess = {
  queries: LoyaltyBannerQueries,
  fetch: fetchLoyaltyBannerRepository,
  repositoryKey: REPOSITORY_KEYS.loyaltyBanner,
} as const;

export const LoyaltyProgramStateDataAccess = {
  queries: LoyaltyProgramStateQueries,
  fetch: fetchLoyaltyProgramStateRepository,
  repositoryKey: REPOSITORY_KEYS.loyaltyProgramState,
} as const;

export const DeliveriesDataAccess = {
  events: {
    DELIVERIES_UPDATED_EVENT: DELIVERIES_UPDATED_EVENT,
    onDeliveriesUpdated: onDeliveriesUpdated,
  },
  handlers: {
    useDeliveriesUpdateHandler: useDeliveriesUpdateHandler,
    useDeliveriesUpdateRefetch: useDeliveriesUpdateRefetch,
  },
};

export const SalesforceInboxDataAccess = {
  fetch: fetchInboxSalesforceRepository,
  repositoryKey: REPOSITORY_KEYS.inboxSalesforce,
} as const;
```

**Key patterns demonstrated:**
- Namespace imports for events and queries
- DataAccess object structure: `{ events, queries, fetch, repositoryKey }`
- `as const` for type safety
- Some repositories only have queries (no events)
- Some have only events (no queries)
- Consistent structure regardless of what's available

**Why this structure:**
- Single import for all domain functionality: `import { PlanDataAccess } from '@data-access/native'`
- Used by RepositoryLoader: `DATA_ACCESS_OBJECTS[key].fetch`
- Type-safe with `as const`
- Consistent API across all repositories
- Easy to add new repositories following same pattern

## Example 7: Repository Keys Constants

**File**: `data-access/native/constants.ts`

This example shows centralized repository keys used throughout the app.

```typescript
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

**Key patterns demonstrated:**
- Single `NATIVE_MODULES_REPOSITORY_QUERY_KEY` for all native repositories
- `REPOSITORY_KEYS` object mapping names to query keys
- `as const` for type safety and IDE autocomplete
- Used by RepositoryLoader to reference repositories

**Why this matters:**
- RepositoryLoader uses REPOSITORY_KEYS to dynamically load repositories
- Consistent query key structure: `[NATIVE_MODULES_REPOSITORY_QUERY_KEY, domain]`
- Type-safe repository key references
- Easy to add new repositories

## Anti-Patterns from Codebase Review

### ❌ Using Native Data Access for Server Data

```typescript
// DON'T: fetchRepository is only for native observables
export const fetchProductsRepository = async () =>
  fetchRepository<Product[]>('products', []);

// DO: Use GraphQL or REST for server data
export const useGetProductsQuery = () =>
  useQuery({
    queryKey: ['products'],
    queryFn: () => apiClient.get('/products'),
  });
```

### ❌ Missing Initial State

```typescript
// DON'T: No initial state - will be undefined on timeout
export const fetchPlanRepository = async () =>
  fetchRepository<PlanRepositorySchema>(PLAN_QUERY_KEY);

// DO: Always provide initial state
const initialState: PlanRepositorySchema = {
  subscriptionId: undefined,
  planId: undefined,
};

export const fetchPlanRepository = async () =>
  fetchRepository<PlanRepositorySchema>(PLAN_QUERY_KEY, initialState);
```

### ❌ Inconsistent Query Keys

```typescript
// DON'T: Different query key structure
export const usePlanId = () =>
  useQuery({
    queryKey: ['plan'], // Wrong!
    queryFn: fetchPlanRepository,
    select: (data) => data.planId,
  });

// DO: Use consistent query key pattern
export const usePlanId = () =>
  useQuery({
    queryKey: [NATIVE_MODULES_REPOSITORY_QUERY_KEY, PLAN_QUERY_KEY],
    queryFn: fetchPlanRepository,
    select: (data) => data.planId,
  });
```

### ❌ Duplicate Queries Instead of select

```typescript
// DON'T: Multiple queries with different keys
export const usePlanId = () =>
  useQuery({
    queryKey: ['planId'],
    queryFn: async () => {
      const data = await fetchPlanRepository();
      return data.planId;
    },
  });

export const useSubscriptionId = () =>
  useQuery({
    queryKey: ['subscriptionId'],
    queryFn: async () => {
      const data = await fetchPlanRepository();
      return data.subscriptionId;
    },
  });

// DO: Share query with select
export const usePlanId = () =>
  useQuery({
    queryKey: [NATIVE_MODULES_REPOSITORY_QUERY_KEY, PLAN_QUERY_KEY],
    queryFn: fetchPlanRepository,
    select: (data) => data.planId,
  });

export const useSubscriptionId = () =>
  useQuery({
    queryKey: [NATIVE_MODULES_REPOSITORY_QUERY_KEY, PLAN_QUERY_KEY],
    queryFn: fetchPlanRepository,
    select: (data) => data.subscriptionId,
  });
```

## Summary

The YourCompany codebase consistently follows these native data access patterns:

1. **Domain-based file organization** with constants, repository, schema, queries, events
2. **fetchRepository pattern** with initial state for timeout fallback
3. **Query key pattern**: `['nativeRepositories', domain]`
4. **Multiple hooks with select** for efficient property access
5. **DataAccess objects** centralize events, queries, fetch, and repositoryKey
6. **Event-driven updates** with native layer communication
7. **Fallback logic** to cached data or initial state on timeout
8. **Type-safe schemas** with optional properties
9. **QueryClient with staleTime: Infinity** for event-driven invalidation
10. **Specialized for native observables** - NOT for server data

These patterns ensure reliable native data access with graceful degradation, type safety, and efficient caching throughout the app.
