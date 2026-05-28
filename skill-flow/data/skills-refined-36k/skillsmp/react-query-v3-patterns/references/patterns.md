# React Query v3 Implementation Patterns

Implementation patterns and anti-patterns for react-query v3.39.0.

## Pattern: Structured Query Keys

Use array format with RequestId and parameters.

✅ **Good:**
```typescript
import { RequestIds } from '../RequestIds';

// Structured key
const queryKey = [
  RequestIds['voucher.validate'],
  {
    code: params.code,
    country: country.toString(),
    locale: locale.toString(),
  },
];

const { data } = useQuery(queryKey, () => validateVoucher(params, queryKey, fetch));
```

❌ **Bad:**
```typescript
// String key - no structure
const { data } = useQuery('voucher', () => validateVoucher(code));

// Missing dependencies
const { data } = useQuery(['voucher', code], () => validateVoucher(code, country));
// country not in key!
```

**Why:** Structured keys:
- Unique per parameter combination
- Automatic cache invalidation
- Prevent cache collisions
- Include all dependencies

## Pattern: Separate Service Functions

Keep query functions separate from hooks.

✅ **Good:**
```typescript
// Service function
export const validateVoucher = async (
  params: VoucherParams,
  queryKey: string[],
  fetch = localFetch
): Promise<VoucherResult> => {
  const response = await fetch(`/api/voucher/validate`, queryKey, {
    method: 'GET',
    query: { code: params.code },
  });
  return response.json();
};

// Custom hook
export const useValidateVoucher = (params: VoucherParams, options = {}) => {
  const { fetch } = useFetch();
  const queryKey = [RequestIds['voucher.validate'], params];

  return useQuery(
    queryKey,
    () => validateVoucher(params, queryKey, fetch),
    options
  );
};
```

❌ **Bad:**
```typescript
// Mixing service and hook logic
export const useValidateVoucher = (code: string) => {
  const { fetch } = useFetch();

  return useQuery(['voucher', code], async () => {
    const response = await fetch(`/api/voucher/validate`, ['voucher', code], {
      method: 'GET',
      query: { code },
    });
    return response.json();
  });
};
```

**Why:** Separate functions:
- Reusable service functions
- Testable without React
- Clear separation of concerns
- Can use service in non-React code

## Pattern: useFetch Integration

Always use useFetch for OpenTelemetry tracing.

✅ **Good:**
```typescript
import { useFetch } from '@/libs/fetch';

export const useRecipes = (options = {}) => {
  const { fetch } = useFetch(); // OpenTelemetry traced
  const queryKey = [RequestIds['recipes.list']];

  return useQuery(
    queryKey,
    () => getRecipes({}, queryKey, fetch),
    options
  );
};
```

❌ **Bad:**
```typescript
// Native fetch - no tracing
export const useRecipes = () => {
  return useQuery(['recipes'], async () => {
    const response = await fetch('/api/recipes');
    return response.json();
  });
};
```

**Why:** useFetch:
- OpenTelemetry tracing
- Automatic span creation
- Error tracking
- Performance monitoring

## Pattern: Cache Invalidation After Mutations

Invalidate related queries after mutations.

✅ **Good:**
```typescript
export const usePostDistributablesBenefits = (options = {}) => {
  const { fetch } = useFetch();
  const queryClient = useQueryClient();

  return useMutation(
    (params) => postDistributablesBenefits(params, queryKey, fetch),
    {
      onSuccess: () => {
        // Invalidate related queries
        queryClient.invalidateQueries([RequestIds['voucher.validate']]);
        queryClient.invalidateQueries([RequestIds['subscription.current']]);
      },
      ...options,
    }
  );
};
```

❌ **Bad:**
```typescript
// No invalidation - stale data
export const usePostDistributablesBenefits = () => {
  return useMutation((params) => postDistributablesBenefits(params));
};
```

**Why:** Invalidation:
- Keeps cache fresh
- Automatic refetch
- Consistent UI state
- No manual refetch needed

## Pattern: Conditional Queries with enabled

Use `enabled` option for conditional execution.

✅ **Good:**
```typescript
export const useCurrentSubscription = (options = {}) => {
  const { fetch } = useFetch();
  const { isAuthenticated, customerId } = useAuth();

  return useQuery(
    [RequestIds['subscription.current'], { customerId }],
    () => getCurrentSubscription({ customerId }, queryKey, fetch),
    {
      enabled: isAuthenticated && !!customerId,
      retry: false,
      ...options,
    }
  );
};
```

❌ **Bad:**
```typescript
// Conditional hook call - breaks rules of hooks
export const MyComponent = ({ customerId }) => {
  if (!customerId) return null;

  const { data } = useQuery(['subscription', customerId], fetchSubscription);

  return <div>{data.status}</div>;
};
```

**Why:** `enabled` option:
- Follows hooks rules
- Query runs when conditions met
- Automatic refetch when enabled changes
- No manual refetch needed

## Pattern: keepPreviousData for Pagination

Use `keepPreviousData` to prevent UI flash during pagination.

✅ **Good:**
```typescript
export const useSubscriptions = (limit = 20) => {
  const [page, setPage] = useState(1);
  const { fetch } = useFetch();

  const query = useQuery(
    [RequestIds['subscriptions.list'], { page, limit }],
    () => getSubscriptions({ page, limit }, queryKey, fetch),
    {
      keepPreviousData: true, // Keep old data while fetching
    }
  );

  return {
    ...query,
    page,
    nextPage: () => setPage((p) => p + 1),
    prevPage: () => setPage((p) => Math.max(1, p - 1)),
  };
};
```

❌ **Bad:**
```typescript
// No keepPreviousData - UI flashes on page change
const query = useQuery(
  ['subscriptions', page],
  () => getSubscriptions(page)
);
```

**Why:** keepPreviousData:
- Shows old data while loading new
- Prevents UI flash
- Better UX
- `isFetching` indicates background update

## Pattern: Data Transformation with select

Transform data in the query using `select`.

✅ **Good:**
```typescript
export const useRecipes = (options = {}) => {
  const { fetch } = useFetch();

  return useQuery(
    [RequestIds['recipes.list']],
    () => getRecipes({}, queryKey, fetch),
    {
      select: (data: RecipeApiResponse[]): Recipe[] => {
        return data.map((recipe) => ({
          id: recipe.id,
          title: recipe.title,
          imageUrl: recipe.image_url,
          prepTime: `${recipe.prep_time_minutes} min`,
        }));
      },
      ...options,
    }
  );
};
```

❌ **Bad:**
```typescript
// Transform in component - runs every render
const Component = () => {
  const { data: rawData } = useRecipes();

  const data = rawData?.map((recipe) => ({
    id: recipe.id,
    title: recipe.title,
    imageUrl: recipe.image_url,
    prepTime: `${recipe.prep_time_minutes} min`,
  }));

  return <div>{data?.map(...)}</div>;
};
```

**Why:** `select` option:
- Transformation memoized by React Query
- Only runs when data changes
- Better performance
- Cleaner component code

## Pattern: Custom Hook with Enhanced API

Wrap useQuery with convenience methods.

✅ **Good:**
```typescript
export const useSubscriptions = (limit = 20) => {
  const [page, setPage] = useState(1);
  const { fetch } = useFetch();

  const query = useQuery(
    [RequestIds['subscriptions.list'], { page, limit }],
    () => getSubscriptions({ page, limit }, queryKey, fetch),
    { keepPreviousData: true }
  );

  return {
    ...query,
    page,
    setPage,
    nextPage: () => setPage((p) => p + 1),
    prevPage: () => setPage((p) => Math.max(1, p - 1)),
  };
};

// Clean component usage
const { data, nextPage, prevPage, page } = useSubscriptions(10);
```

❌ **Bad:**
```typescript
// Component manages pagination
const Component = () => {
  const [page, setPage] = useState(1);
  const { data } = useQuery(['subscriptions', page], () => fetchSubscriptions(page));

  return (
    <div>
      <button onClick={() => setPage((p) => p + 1)}>Next</button>
    </div>
  );
};
```

**Why:** Custom hooks:
- Encapsulate logic
- Reusable pagination
- Cleaner API
- Easier to test

## Pattern: Component-Level Callbacks

Allow component-level callbacks via options.

✅ **Good:**
```typescript
export const useValidateVoucher = (params: VoucherParams, options = {}) => {
  const { fetch } = useFetch();
  const queryKey = [RequestIds['voucher.validate'], params];

  return useQuery(
    queryKey,
    () => validateVoucher(params, queryKey, fetch),
    {
      staleTime: 5 * 60 * 1000,
      ...options, // Allow component-level overrides
    }
  );
};

// Component can add callbacks
const { data } = useValidateVoucher(
  { code },
  {
    onSuccess: (data) => {
      if (data.valid) toast.success('Voucher applied!');
    },
  }
);
```

❌ **Bad:**
```typescript
// Hard-coded callbacks in hook
export const useValidateVoucher = (params) => {
  return useQuery(['voucher', params], fetchVoucher, {
    onSuccess: (data) => {
      toast.success('Done'); // Can't customize per component
    },
  });
};
```

**Why:** Options spreading:
- Component-specific behavior
- Reusable hooks
- Flexible callbacks
- Better composability

## Anti-Pattern: Using v5 Syntax

Don't use TanStack Query v5 syntax in this codebase.

❌ **Bad:**
```typescript
// v5 syntax - WRONG for this codebase
import { useQuery } from '@tanstack/react-query';

const { data } = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
});
```

✅ **Good:**
```typescript
// v3 syntax - CORRECT for this codebase
import { useQuery } from 'react-query';

const { data } = useQuery(['todos'], fetchTodos);
```

**Why:** Version mismatch:
- This codebase uses v3.39.0
- v5 has breaking changes
- Different API syntax
- Import from wrong package

## Anti-Pattern: Not Handling Loading/Error

Always handle loading and error states.

❌ **Bad:**
```typescript
const Component = () => {
  const { data } = useValidateVoucher({ code });

  return <div>{data.discount}</div>; // Crashes while loading
};
```

✅ **Good:**
```typescript
const Component = () => {
  const { data, isLoading, error } = useValidateVoucher({ code });

  if (isLoading) return <Spinner />;
  if (error) return <Error message={error.message} />;
  if (!data) return null;

  return <div>{data.discount}</div>;
};
```

**Why:** Proper handling:
- Prevents crashes
- Better UX
- Shows feedback
- Handles all states

## Anti-Pattern: Not Using useFetch

Don't skip useFetch wrapper.

❌ **Bad:**
```typescript
// Native fetch - no tracing
const { data } = useQuery(['user'], async () => {
  const response = await fetch('/api/user');
  return response.json();
});
```

✅ **Good:**
```typescript
const { fetch } = useFetch();
const { data } = useQuery(
  [RequestIds['user.profile']],
  () => getUser({}, queryKey, fetch)
);
```

**Why:** useFetch:
- OpenTelemetry tracing
- Error tracking
- Performance monitoring
- Consistent patterns

## Anti-Pattern: Missing Query Key Dependencies

Include all dependencies in query key.

❌ **Bad:**
```typescript
// Missing country/locale in key - cache collisions
const { data } = useQuery(
  ['voucher'],
  () => validateVoucher(code, country, locale)
);
```

✅ **Good:**
```typescript
// All dependencies in key
const { data } = useQuery(
  [RequestIds['voucher.validate'], { code, country, locale }],
  () => validateVoucher({ code }, queryKey, fetch)
);
```

**Why:** Complete keys:
- Unique cache entries
- No collisions
- Automatic refetch on changes
- Correct invalidation

## Summary

**Key Patterns:**
- Structured query keys with RequestId
- Separate service functions
- useFetch for tracing
- Cache invalidation after mutations
- Conditional queries with `enabled`
- keepPreviousData for pagination
- Data transformation with `select`
- Custom hooks with enhanced API
- Component-level callbacks via options

**Anti-Patterns to Avoid:**
- Using v5 syntax (use v3!)
- Not handling loading/error
- Not using useFetch
- Missing query key dependencies
- Skipping cache invalidation
- Transforming data in components
- Hard-coded callbacks in hooks

**Version Notes:**
- Use react-query v3.39.0 (NOT TanStack Query v5)
- Import from `'react-query'` (NOT `'@tanstack/react-query'`)
- Use v3 API syntax
