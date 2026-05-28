# React Query v3 Patterns - Production Examples

This document contains real production code examples from the YourCompany web codebase demonstrating react-query v3.39.0 patterns.

## Example 1: useQuery with useFetch Integration

**File**: `app/data-access/voucher/validate.ts`

This example demonstrates the standard useQuery pattern with useFetch for OpenTelemetry tracing.

```typescript
import { useQuery } from 'react-query';
import localFetch, { useFetch } from '@/libs/fetch';
import { useSystemCountry } from '@/libs/system-country';
import { useSelectedLocale } from '@/libs/locale';

import { RequestIds } from '../RequestIds';

// Type definitions
export interface VoucherValidateParams {
  code: string;
}

export interface VoucherValidateResult {
  valid: boolean;
  voucherType: string;
  discount: number;
  expiryDate: string;
}

/**
 * Service function - fetches data using localFetch or useFetch
 */
export const validateVoucher = async (
  params: VoucherValidateParams,
  queryKey: string[],
  fetch = localFetch
): Promise<VoucherValidateResult> => {
  const response = await fetch(`/api/voucher/validate`, queryKey, {
    method: 'GET',
    query: {
      code: params.code,
    },
  });

  return response.json();
};

/**
 * Custom hook wrapping useQuery
 */
export const useValidateVoucher = (
  params: VoucherValidateParams,
  options = {}
) => {
  const { fetch } = useFetch(); // OpenTelemetry-traced fetch
  const country = useSystemCountry();
  const locale = useSelectedLocale();

  // Structured query key with RequestId
  const queryKey = [
    RequestIds['voucher.validate'],
    {
      ...params,
      country: country.toString(),
      locale: locale.toString(),
    },
  ];

  return useQuery<VoucherValidateResult>(
    queryKey,
    () => validateVoucher(params, queryKey, fetch),
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      retry: 2,
      ...options, // Allow component-level overrides
    }
  );
};

// Usage in component
export const VoucherInput = () => {
  const [code, setCode] = useState('');

  const { data, isLoading, error, refetch } = useValidateVoucher(
    { code },
    {
      enabled: code.length > 0, // Only fetch when code is entered
      onSuccess: (data) => {
        if (data.valid) {
          toast.success('Voucher applied!');
        }
      },
    }
  );

  return (
    <div>
      <input value={code} onChange={(e) => setCode(e.target.value)} />
      {isLoading && <Spinner />}
      {error && <Error message={error.message} />}
      {data?.valid && <Success discount={data.discount} />}
    </div>
  );
};
```

**Key patterns:**
- Service function separate from hook
- `fetch` parameter defaults to `localFetch`
- useFetch() hook provides traced fetch in component
- Structured query keys: `[RequestId, params]`
- Locale and country automatically added to query key
- `staleTime` and `cacheTime` configured
- `enabled` option for conditional queries
- Component-level `onSuccess` callback

## Example 2: useMutation with Cache Invalidation

**File**: `app/data-access/voucher-services/usePostDistributablesBenefits.ts`

This example shows mutation patterns with query invalidation.

```typescript
import { useMutation, useQueryClient } from 'react-query';
import { useFetch } from '@/libs/fetch';
import { useSystemCountry } from '@/libs/system-country';
import { RequestIds } from '../RequestIds';

interface PostDistributablesBenefitsParams {
  voucherCode: string;
  subscriptionId: string;
}

interface PostDistributablesBenefitsResponse {
  success: boolean;
  message: string;
}

/**
 * Service function for POST request
 */
export const postDistributablesBenefits = async (
  params: PostDistributablesBenefitsParams,
  queryKey: string[],
  fetch
): Promise<PostDistributablesBenefitsResponse> => {
  const response = await fetch('/api/voucher/distributable-benefits', queryKey, {
    method: 'POST',
    data: params,
  });

  return response.json();
};

/**
 * Mutation hook with automatic cache invalidation
 */
export const usePostDistributablesBenefits = (options = {}) => {
  const { fetch } = useFetch();
  const queryClient = useQueryClient();
  const country = useSystemCountry();

  return useMutation<
    PostDistributablesBenefitsResponse,
    Error,
    PostDistributablesBenefitsParams
  >(
    (params) => {
      const queryKey = [
        RequestIds['voucher.postDistributablesBenefits'],
        { ...params, country: country.toString() },
      ];
      return postDistributablesBenefits(params, queryKey, fetch);
    },
    {
      onSuccess: () => {
        // Invalidate related queries after successful mutation
        queryClient.invalidateQueries([RequestIds['voucher.validate']]);
        queryClient.invalidateQueries([RequestIds['subscription.current']]);
      },
      onError: (error) => {
        console.error('Failed to apply voucher:', error);
      },
      ...options,
    }
  );
};

// Usage in component
export const ApplyVoucherButton = ({ voucherCode, subscriptionId }) => {
  const mutation = usePostDistributablesBenefits({
    onSuccess: () => {
      toast.success('Voucher applied successfully!');
    },
    onError: (error) => {
      toast.error(`Failed: ${error.message}`);
    },
  });

  return (
    <button
      onClick={() => mutation.mutate({ voucherCode, subscriptionId })}
      disabled={mutation.isLoading}
    >
      {mutation.isLoading ? 'Applying...' : 'Apply Voucher'}
    </button>
  );
};
```

**Key patterns:**
- `useMutation` with generic types: `<Response, Error, Params>`
- `useQueryClient()` for cache access
- `invalidateQueries` after successful mutation
- Component-level and hook-level callbacks
- `mutation.mutate()` to trigger mutation
- `mutation.isLoading` for button state
- Error handling in both hook and component

## Example 3: Pagination Pattern

**File**: `app/data-access/reactivation/subscription.ts`

This example demonstrates pagination using page offset.

```typescript
import { useQuery } from 'react-query';
import { useFetch } from '@/libs/fetch';
import { useSystemCountry } from '@/libs/system-country';
import { useState } from 'react';

interface PaginatedSubscriptionsParams {
  page: number;
  limit: number;
}

interface PaginatedSubscriptionsResponse {
  data: Subscription[];
  total: number;
  page: number;
  totalPages: number;
}

export const getSubscriptions = async (
  params: PaginatedSubscriptionsParams,
  queryKey: string[],
  fetch
): Promise<PaginatedSubscriptionsResponse> => {
  const response = await fetch('/api/subscriptions', queryKey, {
    method: 'GET',
    query: {
      page: params.page.toString(),
      limit: params.limit.toString(),
    },
  });

  return response.json();
};

export const useSubscriptions = (limit = 20) => {
  const [page, setPage] = useState(1);
  const { fetch } = useFetch();
  const country = useSystemCountry();

  const queryKey = [
    RequestIds['subscriptions.list'],
    { page, limit, country: country.toString() },
  ];

  const query = useQuery(
    queryKey,
    () => getSubscriptions({ page, limit }, queryKey, fetch),
    {
      staleTime: 5 * 60 * 1000,
      keepPreviousData: true, // Keep previous page data while fetching
    }
  );

  return {
    ...query,
    page,
    setPage,
    nextPage: () => setPage((p) => p + 1),
    prevPage: () => setPage((p) => Math.max(1, p - 1)),
  };
};

// Usage in component
export const SubscriptionsList = () => {
  const { data, isLoading, isFetching, page, nextPage, prevPage } =
    useSubscriptions(10);

  return (
    <div>
      {isLoading && <Spinner />}
      {data?.data.map((subscription) => (
        <SubscriptionCard key={subscription.id} subscription={subscription} />
      ))}

      {isFetching && <div>Updating...</div>}

      <div>
        <button onClick={prevPage} disabled={page === 1}>
          Previous
        </button>
        <span>Page {page} of {data?.totalPages}</span>
        <button onClick={nextPage} disabled={page >= (data?.totalPages || 1)}>
          Next
        </button>
      </div>
    </div>
  );
};
```

**Key patterns:**
- Page number in state
- `keepPreviousData: true` prevents UI flash during pagination
- Helper functions: `nextPage`, `prevPage`
- `isLoading` for initial load, `isFetching` for updates
- Query key includes page number for separate caching per page

## Example 4: Conditional Query Execution

**File**: `app/data-access/subscription/current.ts`

This example shows using `enabled` option for conditional queries.

```typescript
import { useQuery } from 'react-query';
import { useFetch } from '@/libs/fetch';
import { useAuth } from '@/libs/auth';

export const useCurrentSubscription = (options = {}) => {
  const { fetch } = useFetch();
  const { isAuthenticated, customerId } = useAuth();

  const queryKey = [RequestIds['subscription.current'], { customerId }];

  return useQuery(
    queryKey,
    () => getCurrentSubscription({ customerId }, queryKey, fetch),
    {
      enabled: isAuthenticated && !!customerId, // Only fetch when authenticated
      staleTime: 5 * 60 * 1000,
      retry: false, // Don't retry if not authenticated
      ...options,
    }
  );
};

// Usage: Query automatically runs/stops based on auth state
export const SubscriptionStatus = () => {
  const { data, isLoading } = useCurrentSubscription();

  if (isLoading) return <Spinner />;
  if (!data) return <div>No subscription</div>;

  return <div>Status: {data.status}</div>;
};
```

**Key patterns:**
- `enabled` option controls query execution
- Multiple conditions: `isAuthenticated && !!customerId`
- Query automatically refetches when enabled changes from false to true
- `retry: false` when query depends on auth state
- No manual refetch needed - React Query handles it

## Example 5: Query with Transformations

**File**: `app/data-access/menu/recipes.ts`

This example shows transforming API data in the query function.

```typescript
import { useQuery } from 'react-query';
import { useFetch } from '@/libs/fetch';
import { useMemo } from 'react';

interface RecipeApiResponse {
  id: string;
  title: string;
  image_url: string;
  prep_time_minutes: number;
}

interface Recipe {
  id: string;
  title: string;
  imageUrl: string; // Transformed to camelCase
  prepTime: string; // Transformed to readable format
}

export const getRecipes = async (
  params,
  queryKey: string[],
  fetch
): Promise<RecipeApiResponse[]> => {
  const response = await fetch('/api/recipes', queryKey);
  return response.json();
};

export const useRecipes = (options = {}) => {
  const { fetch } = useFetch();
  const queryKey = [RequestIds['recipes.list']];

  const query = useQuery(
    queryKey,
    () => getRecipes({}, queryKey, fetch),
    {
      // Transform data in select option
      select: (data: RecipeApiResponse[]): Recipe[] => {
        return data.map((recipe) => ({
          id: recipe.id,
          title: recipe.title,
          imageUrl: recipe.image_url,
          prepTime: `${recipe.prep_time_minutes} min`,
        }));
      },
      staleTime: 10 * 60 * 1000,
      ...options,
    }
  );

  return query;
};

// Usage: data is already transformed
export const RecipesList = () => {
  const { data } = useRecipes();

  return data?.map((recipe) => (
    <div key={recipe.id}>
      <h3>{recipe.title}</h3>
      <img src={recipe.imageUrl} alt={recipe.title} />
      <span>{recipe.prepTime}</span>
    </div>
  ));
};
```

**Key patterns:**
- `select` option transforms data
- Transformation happens only when data changes
- Component receives transformed data
- TypeScript types for both API response and transformed data
- Transformation is memoized by React Query

## Common Anti-Patterns

### ❌ Not Using Structured Query Keys

```typescript
// DON'T: Simple string keys
const { data } = useQuery('voucher', () => fetchVoucher(code));

// DO: Structured keys with RequestIds
const queryKey = [RequestIds['voucher.validate'], { code, country }];
const { data } = useQuery(queryKey, () => fetchVoucher({ code }, queryKey, fetch));
```

### ❌ Not Using useFetch

```typescript
// DON'T: Native fetch (no tracing)
const { data } = useQuery('user', () =>
  fetch('/api/user').then(r => r.json())
);

// DO: Use useFetch for OpenTelemetry tracing
const { fetch } = useFetch();
const { data } = useQuery(
  queryKey,
  () => getUser({}, queryKey, fetch)
);
```

### ❌ Mixing react-query v3 and v5 APIs

```typescript
// DON'T: v5 API (won't work with v3!)
import { useQuery } from '@tanstack/react-query'; // Wrong package!

// DO: v3 API
import { useQuery } from 'react-query'; // Correct package for v3
```

### ❌ Not Invalidating After Mutations

```typescript
// DON'T: Mutation without invalidation
const mutation = useMutation(updateUser);

// DO: Invalidate related queries
const mutation = useMutation(updateUser, {
  onSuccess: () => {
    queryClient.invalidateQueries([RequestIds['user.profile']]);
  },
});
```

## Summary

The YourCompany web codebase uses react-query v3.39.0 with these patterns:

1. **Structured query keys** - `[RequestId, params]` format
2. **useFetch integration** - OpenTelemetry tracing on all requests
3. **Separate service functions** - Service functions separate from hooks
4. **Cache time configuration** - `staleTime` and `cacheTime` tuned per query
5. **Locale/country in keys** - Automatically added to prevent cache collisions
6. **Query invalidation** - Mutations invalidate related queries
7. **Conditional execution** - `enabled` option for auth-dependent queries
8. **keepPreviousData** - Used for pagination to prevent UI flash

**Key Libraries:**
- react-query v3.39.0 (NOT TanStack Query v5!)
- Import from `'react-query'` not `'@tanstack/react-query'`
- useFetch from `@/libs/fetch` for OpenTelemetry
- TypeScript 5.7.3

**Important:** This codebase uses react-query v3, which has different APIs than TanStack Query v5. Always import from `'react-query'` package.

For v3 documentation, see: https://react-query-v3.tanstack.com/
