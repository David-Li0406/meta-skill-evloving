# REST API Examples

Real-world REST API patterns from the YourCompany shared-mobile-modules project.

## Complete External Recipes API Implementation

From `src/data-access/query/external-recipes/`:

### Constants: Endpoints and Query Keys

```typescript
// constants.ts

/**
 * API endpoints for external recipes
 */
export const EXTERNAL_RECIPES_ENDPOINTS = {
  /** Base endpoint for external recipes CRUD operations */
  BASE: '/gw/cookbook/v1/external-recipes',
  /** Endpoint for creating a new external recipe */
  CREATE: '/gw/cookbook/v1/external-recipes',
  /** Endpoint for fetching external recipes with pagination */
  LIST: '/gw/cookbook/v1/external-recipes',
  /** Endpoint for deleting an external recipe by ID */
  DELETE: (id: string) => `/gw/cookbook/v1/external-recipes/${id}`,
  /** Endpoint for getting external recipe detail by ID */
  DETAIL: (id: string) => `/gw/cookbook/v1/external-recipes/${id}`,
  /** Endpoint for updating an external recipe by ID */
  UPDATE: (id: string) => `/gw/cookbook/v1/external-recipes/${id}`,
} as const;
```

**Key patterns:**
- Const assertion (`as const`) for type safety
- JSDoc comments for each endpoint
- Function for dynamic endpoints: `DETAIL: (id: string) => ...`
- Grouped by CRUD operations

### Service Functions with useFetch

```typescript
// service.ts
import type {
  DataAccessGet,
  DataAccessPost,
  DataAccessDelete,
} from '../schema';

/**
 * Get external recipes with pagination support
 */
export const getExternalRecipes: DataAccessGet<
  GetExternalRecipesResponse,
  GetExternalRecipesRequest
> = async (params, queryKey, fetch) => {
  const query: Record<string, string> = {};

  if (params.search) {
    query.search = params.search;
  }

  if (params.cursor) {
    query.cursor = params.cursor;
  }

  if (params.limit) {
    query.limit = params.limit.toString();
  }

  // fetch parameter comes from useFetch() - includes OpenTelemetry tracing
  const response = await fetch(EXTERNAL_RECIPES_ENDPOINTS.LIST, queryKey, {
    method: 'GET',
    query: Object.keys(query).length > 0 ? query : undefined,
  });

  const result = await response.json();

  // Validate response with Zod schema
  return validateGetExternalRecipesResponse(result);
};

/**
 * Get external recipe detail by ID
 */
export const getExternalRecipeDetail: DataAccessGet<
  ExternalRecipe,
  GetExternalRecipeDetailRequest
> = async (params, queryKey, fetch) => {
  const response = await fetch(
    EXTERNAL_RECIPES_ENDPOINTS.DETAIL(params.id),
    queryKey,
    {
      method: 'GET',
    }
  );

  const result = await response.json();
  const validated = validateExternalRecipe(result);

  return validated;
};

/**
 * Create a new external recipe
 */
export const createExternalRecipe: DataAccessPost<
  ExternalRecipeListItem,
  CreateExternalRecipeRequest
> = async (params, queryKey, fetch) => {
  const response = await fetch(EXTERNAL_RECIPES_ENDPOINTS.CREATE, queryKey, {
    method: 'POST',
    data: params,
  });

  const result = await response.json();
  return validateExternalRecipeListItem(result);
};
```

**Key patterns:**
- `fetch` parameter from `useFetch()` (not native fetch)
- Query params built conditionally
- Zod validation on responses
- Typed with `DataAccessGet`, `DataAccessPost`, etc.

### Custom Hooks with TanStack Query

```typescript
// hooks.ts
import {
  useQuery,
  useInfiniteQuery,
  useMutation,
  useQueryClient,
} from '@tanstack/react-query';
import { useMemo } from 'react';

import { useFetch } from '@libs/networking-client';

import { RequestIds } from '../RequestIds';
import type { UseQuery, UseMutation } from '../schema';
import { useLocalizeParams } from '../utils';

/**
 * Hook to fetch external recipes with pagination support
 */
export const useGetExternalRecipes: UseQuery<
  GetExternalRecipesResponse,
  GetExternalRecipesRequest
> = (params, options) => {
  const fetch = useFetch(); // OpenTelemetry traced fetch
  const localizeParams = useLocalizeParams(); // Adds locale, country
  const requestParams = useMemo(
    () => ({ ...params, ...localizeParams }),
    [params, localizeParams]
  );

  const queryKey = [RequestIds['external-recipes.list'], requestParams];

  return useQuery({
    queryKey,
    queryFn: () => getExternalRecipes(requestParams, queryKey, fetch),
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 10 * 60 * 1000, // 10 minutes
    ...options,
  });
};

/**
 * Hook to fetch external recipe detail by ID
 */
export const useGetExternalRecipeDetail: UseQuery<
  ExternalRecipe,
  GetExternalRecipeDetailRequest
> = (params, options) => {
  const fetch = useFetch();
  const localizeParams = useLocalizeParams();
  const requestParams = useMemo(
    () => ({ ...params, ...localizeParams }),
    [params, localizeParams]
  );

  const queryKey = [RequestIds['external-recipes.detail'], requestParams];

  return useQuery({
    queryKey,
    queryFn: () => getExternalRecipeDetail(requestParams, queryKey, fetch),
    staleTime: 10 * 60 * 1000, // 10 minutes - recipe details don't change frequently
    gcTime: 15 * 60 * 1000, // 15 minutes - keep in memory longer for navigation
    ...options,
  });
};
```

**Key patterns:**
- `useFetch()` hook provides traced fetch
- `useLocalizeParams()` adds locale/country automatically
- `useMemo()` for requestParams to prevent unnecessary re-renders
- `RequestIds` object for consistent query keys
- Stale time tuned based on data volatility (5min for lists, 10min for details)
- Spread `options` to allow overrides

### Infinite Query Hook

```typescript
// hooks.ts

/**
 * Hook to fetch external recipes with infinite pagination support
 */
export const useGetExternalRecipesInfinite = (
  params: GetExternalRecipesRequest
) => {
  const fetch = useFetch();
  const localizeParams = useLocalizeParams();
  const baseParams = useMemo(
    () => ({ ...params, ...localizeParams }),
    [params, localizeParams]
  );

  return useInfiniteQuery({
    queryKey: [RequestIds['external-recipes.list'], baseParams],
    queryFn: ({ pageParam }) => {
      const requestParams = { ...baseParams, cursor: pageParam };
      const queryKey = [RequestIds['external-recipes.list'], requestParams];
      return getExternalRecipes(requestParams, queryKey, fetch);
    },
    initialPageParam: undefined as string | undefined,
    getNextPageParam: (lastPage) => {
      return lastPage.pagination.has_more
        ? lastPage.pagination.next_cursor
        : undefined;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 10 * 60 * 1000, // 10 minutes
  });
};
```

**Key patterns:**
- `pageParam` from TanStack Query for cursor-based pagination
- `initialPageParam` typed explicitly
- `getNextPageParam` returns cursor or undefined when no more pages
- Same stale/gc time as regular list query

### Mutation Hook with Cache Invalidation

```typescript
// hooks.ts

/**
 * Hook to create a new external recipe
 */
export const useCreateExternalRecipe: UseMutation<
  ExternalRecipeListItem,
  CreateExternalRecipeRequest
> = (options) => {
  const fetch = useFetch();
  const localizeParams = useLocalizeParams();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (params: CreateExternalRecipeRequest) => {
      const requestParams = { ...params, ...localizeParams };
      const queryKey = [RequestIds['external-recipes.create'], requestParams];
      return createExternalRecipe(requestParams, queryKey, fetch);
    },
    onSuccess: () => {
      // Invalidate and refetch external recipes list after successful creation
      queryClient.invalidateQueries({
        queryKey: [RequestIds['external-recipes.list']],
      });
    },
    ...options,
  });
};
```

**Key patterns:**
- `useQueryClient()` for cache invalidation
- `onSuccess` invalidates list queries
- Spread `options` allows component-level callbacks
- Localizes params automatically

## Component Usage Examples

### Standard Query Usage

```typescript
import { useGetExternalRecipes } from '@data-access/query/external-recipes';

export const RecipeListScreen = () => {
  const { data, isLoading, error, refetch } = useGetExternalRecipes({
    limit: 20,
    search: '',
  });

  if (isLoading && !data) return <LoadingSpinner />;
  if (error && !data) return <ErrorMessage error={error} onRetry={refetch} />;
  if (!data?.data.length) return <EmptyState />;

  return (
    <FlatList
      data={data.data}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => <RecipeCard recipe={item} />}
    />
  );
};
```

**Pattern:** Loading state checks `isLoading && !data` to allow cached data to show during refetch.

### Infinite Scroll Usage

```typescript
import { useGetExternalRecipesInfinite } from '@data-access/query/external-recipes';

export const RecipeInfiniteListScreen = () => {
  const {
    data: infiniteData,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
    error,
  } = useGetExternalRecipesInfinite({ limit: 20 });

  // Flatten pages into single array
  const recipes = infiniteData?.pages.flatMap((page) => page.data) || [];

  if (isLoading && !infiniteData) return <LoadingSpinner />;
  if (error && !infiniteData) return <ErrorMessage error={error} />;
  if (!recipes.length) return <EmptyState />;

  return (
    <FlatList
      data={recipes}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => <RecipeCard recipe={item} />}
      onEndReached={() => {
        if (hasNextPage && !isFetchingNextPage) {
          fetchNextPage();
        }
      }}
      onEndReachedThreshold={0.5}
      ListFooterComponent={
        isFetchingNextPage ? <LoadingSpinner /> : null
      }
    />
  );
};
```

**Key patterns:**
- `flatMap()` flattens pages into single array
- `onEndReached` checks `hasNextPage && !isFetchingNextPage`
- `onEndReachedThreshold={0.5}` triggers 50% before end
- Footer shows loading spinner while fetching next page

### Mutation Usage

```typescript
import { useCreateExternalRecipe } from '@data-access/query/external-recipes';
import { useState } from 'react';

export const CreateRecipeForm = ({ onSuccess }) => {
  const [formData, setFormData] = useState({
    url: '',
    title: '',
    thumbnail_url: '',
  });

  const createMutation = useCreateExternalRecipe({
    onSuccess: (response) => {
      onSuccess?.(response);
      setFormData({ url: '', title: '', thumbnail_url: '' });
    },
  });

  return (
    <View>
      <TextInput
        value={formData.url}
        onChangeText={(url) => setFormData(prev => ({ ...prev, url }))}
        editable={!createMutation.isPending}
        placeholder="Recipe URL"
      />

      <TextInput
        value={formData.title}
        onChangeText={(title) => setFormData(prev => ({ ...prev, title }))}
        editable={!createMutation.isPending}
        placeholder="Recipe Title (optional)"
      />

      {createMutation.error && (
        <Text style={{ color: 'red' }}>
          {createMutation.error.message}
        </Text>
      )}

      <Button
        title={createMutation.isPending ? 'Creating...' : 'Create Recipe'}
        onPress={() => createMutation.mutate(formData)}
        disabled={createMutation.isPending || !formData.url}
      />
    </View>
  );
};
```

**Key patterns:**
- `isPending` replaces deprecated `isLoading`
- Disable inputs during mutation
- Clear form on success
- Component-level `onSuccess` callback
- Show error message from mutation

## Query Key Patterns

From `src/data-access/query/RequestIds.ts`:

```typescript
export const RequestIds = {
  // External recipes
  'external-recipes.list': 'external-recipes.list',
  'external-recipes.detail': 'external-recipes.detail',
  'external-recipes.create': 'external-recipes.create',
  'external-recipes.delete': 'external-recipes.delete',
  'external-recipes.update': 'external-recipes.update',

  // Customer data
  'customer.subscriptions': 'customer.subscriptions',
  'customer.profile': 'customer.profile',
  'customer.balance': 'customer.balance',
} as const;
```

**Pattern:** Centralized request IDs with domain.operation format.

### Usage in Query Keys

```typescript
// List query with params
const queryKey = [RequestIds['external-recipes.list'], requestParams];
// Result: ['external-recipes.list', { limit: 20, search: '' }]

// Detail query with ID
const queryKey = [RequestIds['external-recipes.detail'], { id: 'recipe-123' }];
// Result: ['external-recipes.detail', { id: 'recipe-123' }]

// Infinite query (same key as list)
const queryKey = [RequestIds['external-recipes.list'], baseParams];
// Result: ['external-recipes.list', { limit: 20 }]
```

## Type Definitions

From `src/data-access/query/schema.ts`:

```typescript
// Generic types for data access functions
export type DataAccessGet<TResponse, TParams> = (
  params: TParams,
  queryKey: string[],
  fetch: ReturnType<typeof useFetch>
) => Promise<TResponse>;

export type DataAccessPost<TResponse, TParams> = (
  params: TParams,
  queryKey: string[],
  fetch: ReturnType<typeof useFetch>
) => Promise<TResponse>;

export type DataAccessDelete<TResponse, TParams> = (
  params: TParams,
  queryKey: string[],
  fetch: ReturnType<typeof useFetch>
) => Promise<TResponse>;

export type DataAccessPut<TResponse, TParams> = (
  params: TParams,
  queryKey: string[],
  fetch: ReturnType<typeof useFetch>
) => Promise<TResponse>;

// Hook types
export type UseQuery<TResponse, TParams> = (
  params: TParams,
  options?: UseQueryOptions<TResponse>
) => UseQueryResult<TResponse>;

export type UseMutation<TResponse, TParams> = (
  options?: UseMutationOptions<TResponse, Error, TParams>
) => UseMutationResult<TResponse, Error, TParams>;
```

**Pattern:** Generic types ensure service functions and hooks have consistent signatures.

## Testing Examples

From `src/data-access/query/external-recipes/hooks.test.ts`:

```typescript
import { renderHook, waitFor } from '@testing-library/react-native';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useGetExternalRecipes } from './hooks';
import * as service from './service';

jest.mock('./service');
jest.mock('@libs/networking-client', () => ({
  useFetch: () => jest.fn(),
}));
jest.mock('../utils', () => ({
  useLocalizeParams: () => ({ locale: 'en', country: 'us' }),
}));

const mockGetExternalRecipes = service.getExternalRecipes as jest.MockedFunction<
  typeof service.getExternalRecipes
>;

describe('useGetExternalRecipes', () => {
  it('returns external recipes data', async () => {
    const mockResponse = {
      data: [
        {
          id: 'recipe-1',
          title: 'Test Recipe',
          url: 'https://example.com/recipe',
          thumbnail_url: 'https://example.com/image.jpg',
          has_recipe_extracted: false,
        },
      ],
      pagination: {
        next_cursor: undefined,
        has_more: false,
        limit: 20,
      },
    };

    mockGetExternalRecipes.mockResolvedValue(mockResponse);

    const queryClient = new QueryClient({
      defaultOptions: { queries: { retry: false } },
    });
    const wrapper = ({ children }) => (
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    );

    const { result } = renderHook(
      () => useGetExternalRecipes({ limit: 20 }),
      { wrapper }
    );

    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data).toEqual(mockResponse);
  });
});
```

**Key patterns:**
- Mock service functions, not hooks
- Mock `useFetch` and `useLocalizeParams`
- Create fresh QueryClient with `retry: false`
- Wrap with QueryClientProvider
- Use `waitFor` for async assertions

## Performance Optimization

### Stale Time Configuration

```typescript
// List data (changes frequently) - 5 minutes
staleTime: 5 * 60 * 1000

// Detail data (stable) - 10 minutes
staleTime: 10 * 60 * 1000

// Static configuration data - 30 minutes
staleTime: 30 * 60 * 1000
```

### Garbage Collection Time

```typescript
// Keep in memory 2x longer than stale time
gcTime: 10 * 60 * 1000 // When staleTime is 5 minutes
gcTime: 15 * 60 * 1000 // When staleTime is 10 minutes
```

**Pattern:** `gcTime` should be 1.5x-2x `staleTime` to allow navigation back without refetch.

## Error Handling

```typescript
// Service function with specific error messages
export const getExternalRecipeDetail = async (params, queryKey, fetch) => {
  const response = await fetch(
    EXTERNAL_RECIPES_ENDPOINTS.DETAIL(params.id),
    queryKey
  );

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error(`Recipe ${params.id} not found`);
    }
    if (response.status === 403) {
      throw new Error('Unauthorized to view this recipe');
    }
    throw new Error(`Failed to fetch recipe: ${response.status}`);
  }

  const result = await response.json();
  return validateExternalRecipe(result);
};
```

**Pattern:** Specific error messages for different status codes help debugging.
