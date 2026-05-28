---
name: react-query-v3-patterns
description: "WHAT: React Query v3.39.0 patterns for web data fetching with OpenTelemetry. WHEN: using useQuery v3, useMutation v3, implementing caching on web. KEYWORDS: react-query, v3, useQuery, useMutation, useFetch, cache, web, tracing, RequestIds."
---

# React Query v3 Patterns - Web

Data fetching patterns using react-query v3.39.0 (NOT TanStack Query v5) with custom useFetch hook and OpenTelemetry tracing.

## Documentation

This skill has comprehensive documentation:

- **[Production Examples](./references/examples.md)** - Real-world code examples from the codebase
- **[API Reference](./references/api-docs.md)** - Complete API documentation with official links
- **[Implementation Patterns](./references/patterns.md)** - Best practices and anti-patterns

## When to Use

Use React Query for:
- Fetching, caching, and synchronizing server state
- API calls with automatic caching and revalidation
- Data mutations with optimistic updates
- Infinite scrolling or pagination
- Background data refetching

**Note:** This codebase uses react-query v3.39.0, not the newer @tanstack/react-query v5. The API is different!

## Core Principles

### 1. useQuery for Data Fetching

**Use useQuery hook with query keys and custom useFetch integration.**

✅ **Good:**
```typescript
// app/data-access/voucher/validate.ts:1
import { useQuery } from 'react-query';
import localFetch, { useFetch } from '@/libs/fetch';
import { useLocalizeParams } from '../utils';
import RequestIds from '../RequestIds';

export const useValidateVoucher: UseQuery<
  VoucherValidateResult,
  VoucherValidateParams
> = (params, options = {}) => {
  const { fetch } = useFetch();

  const localizedParams = {
    ...params,
    ...useLocalizeParams(),
  };

  const queryKey = [RequestIds['voucher.validate'], localizedParams];

  return useQuery<VoucherValidateResult>(
    queryKey,
    () => {
      return validateVoucher(localizedParams, queryKey, fetch);
    },
    options
  );
};
```

**Why:** Query keys enable automatic caching and invalidation. The useFetch hook provides OpenTelemetry tracing and error handling.

### 2. Structured Query Keys

**Use arrays with RequestIds and params for consistent query keys.**

✅ **Good:**
```typescript
// app/data-access/reactivation/subscription.ts:1
import { useQuery } from 'react-query';
import RequestIds from '../RequestIds';

const queryKey = [
  RequestIds['reactivation.subscription'],
  {
    subscriptionId,
    locale,
    systemCountry,
    ...otherParams
  }
];

return useQuery<SubscriptionResponse>(queryKey, fetchFunction, options);
```

❌ **Bad:**
```typescript
// Don't use string-only keys
const queryKey = 'subscription';

// Don't use unstructured keys
const queryKey = ['subscription', subscriptionId, locale];
```

**Why:** Structured keys with RequestIds ensure uniqueness and make cache invalidation easier. Including params in the key ensures cache correctness.

### 3. useMutation for Data Changes

**Use useMutation for POST, PUT, DELETE operations.**

✅ **Good:**
```typescript
// app/data-access/voucher-services/usePostDistributablesBenefits.ts:69
import { useMutation } from 'react-query';
import { useFetch } from '@/libs/fetch';

export const usePostDistributablesBenefitsMutation: UseMutation<
  PostDistributablesBenefitsResponse,
  PostDistributablesBenefitsParams
> = (options = {}) => {
  const { fetch } = useFetch();
  const localizedParams = useLocalizeParams();

  const mutationKey = [
    RequestIds['voucher-service.distributables.mutate.benefits'],
  ];

  return useMutation(
    (params) =>
      postDistributablesBenefits(
        { ...params, ...localizedParams },
        mutationKey,
        fetch
      ),
    options
  );
};
```

**Why:** Mutations handle side effects like creating/updating data and can trigger cache invalidations.

### 4. Integration with useFetch + OpenTelemetry

**Always use custom useFetch hook for tracing and error handling.**

✅ **Good:**
```typescript
// app/data-access/voucher-services/usePostDistributablesBenefits.ts:1
import localFetch, { useFetch } from '@/libs/fetch';

const postDistributablesBenefits: DataAccessPost<
  PostDistributablesBenefitsResponse,
  PostDistributablesBenefitsParams
> = async (params, queryKey, fetch = localFetch) => {
  const response = await fetch(
    `/voucher-service/distributables/${voucherCode}/benefits`,
    queryKey,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      data: {
        customer_id: customerId,
        plan_id: planId,
      },
      query: {
        country: systemCountry,
        locale,
      },
      parentSpan,  // OpenTelemetry span for tracing
    }
  );

  return response.json();
};

export const useMutation = (options = {}) => {
  const { fetch } = useFetch();  // Get traced fetch instance

  return useMutation(
    (params) => postDistributablesBenefits(params, mutationKey, fetch),
    options
  );
};
```

**Why:** The useFetch hook adds OpenTelemetry tracing to all API calls, enabling performance monitoring and debugging.

### 5. TypeScript Generic Types

**Use TypeScript generics for type-safe queries and mutations.**

✅ **Good:**
```typescript
import { UseQueryOptions } from 'react-query';

export const getReactivateSubscriptions: DataAccessGet<
  SubscriptionResponse,
  GetReactivationSubscriptionsParams
> = async (params, queryKey, fetch = localFetch) => {
  const result = await fetch('/reactivation-subscription', queryKey, {
    method: 'GET',
    query: {
      country: params.systemCountry,
      locale: params.locale,
    },
  });

  return result.json();
};
```

**Why:** Type safety ensures params and responses are correct at compile time.

## Query Options

### Common Options

```typescript
// Retry configuration
useQuery(queryKey, fetchFn, {
  retry: 3,  // Retry failed requests 3 times
});

// Stale time
useQuery(queryKey, fetchFn, {
  staleTime: 5 * 60 * 1000,  // 5 minutes
});

// Cache time
useQuery(queryKey, fetchFn, {
  cacheTime: 10 * 60 * 1000,  // 10 minutes
});

// Enabled/disabled
useQuery(queryKey, fetchFn, {
  enabled: !!subscriptionId,  // Only run when subscriptionId exists
});

// Callbacks
useQuery(queryKey, fetchFn, {
  onSuccess: (data) => {
    console.log('Data fetched successfully', data);
  },
  onError: (error) => {
    console.error('Fetch failed', error);
  },
});
```

## Data Access Pattern

### Standard Structure

```typescript
// 1. Define types
type Params = { ... };
type Response = { ... };

// 2. Define fetch function
const fetchData: DataAccessGet<Response, Params> = async (
  params,
  queryKey,
  fetch = localFetch
) => {
  const result = await fetch('/endpoint', queryKey, {
    method: 'GET',
    query: params,
    parentSpan,
  });
  return result.json();
};

// 3. Define hook
export const useDataHook: UseQuery<Response, Params> = (
  params,
  options = {}
) => {
  const { fetch } = useFetch();
  const localizedParams = { ...params, ...useLocalizeParams() };
  const queryKey = [RequestIds['endpoint.name'], localizedParams];

  return useQuery<Response>(
    queryKey,
    () => fetchData(localizedParams, queryKey, fetch),
    options
  );
};
```

## File Organization

```
data-access/
├── RequestIds.ts              # Centralized query key constants
├── schema.ts                  # Shared types
├── utils.ts                   # useLocalizeParams, etc.
├── reactivation/
│   ├── subscription.ts        # Query hooks
│   ├── subscription.test.ts   # Tests
│   └── schema.ts              # Types
└── voucher/
    ├── validate.ts            # Query hooks
    ├── validate.spec.ts       # Tests
    └── schema.ts              # Types
```

## Common Mistakes

1. **Using TanStack Query v5 syntax** - This codebase uses react-query v3, not v5!
2. **Forgetting useFetch integration** - Always use useFetch for OpenTelemetry tracing
3. **String-only query keys** - Use arrays with RequestIds and params
4. **Not including params in query key** - Cache won't update when params change
5. **Importing from wrong package** - Use 'react-query' NOT '@tanstack/react-query'

## Quick Reference

### v3 API (Current)

```typescript
// Import from react-query (v3)
import { useQuery, useMutation } from 'react-query';

// useQuery
const { data, isLoading, error } = useQuery(queryKey, fetchFn, options);

// useMutation
const { mutate, isLoading } = useMutation(mutateFn, {
  onSuccess: (data) => { },
  onError: (error) => { },
});

// Call mutation
mutate({ param: 'value' });
```

### With useFetch Integration

```typescript
import { useFetch } from '@/libs/fetch';

const useSomeData = (params, options = {}) => {
  const { fetch } = useFetch();
  const queryKey = [RequestIds['some.data'], params];

  return useQuery(
    queryKey,
    () => fetchData(params, queryKey, fetch),
    options
  );
};
```

### Testing

```typescript
import { QueryClient, QueryClientProvider } from 'react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: false },
  },
});

render(
  <QueryClientProvider client={queryClient}>
    <Component />
  </QueryClientProvider>
);
```
