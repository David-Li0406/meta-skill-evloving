# GraphQL API - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating GraphQL patterns with Apollo Client.

## Example 1: Query Definition with Fragments

**File**: `data-access/graphql/store/GetInitialStore.graphql`

This example demonstrates a complex query using multiple fragments for data composition.

```graphql
query GetStoreInitialData(
  $selectedWeek: WeekId!
  $startWeek: WeekId!
  $categoryId: CategoryId!
) {
  customer {
    id
    plans(type: RTE) {
      id
      items {
        id: planId
        selectedDelivery: deliveries(
          first: 1
          filter: {
            range: { start: $selectedWeek, size: 1 }
            states: [PAUSED, UPCOMING]
          }
        ) {
          edges {
            node {
              id
              menu {
                id
                categories {
                  ...CategoryFragment
                }
                filters {
                  ...FilterFragment
                }
                sorting {
                  ...FilterFragment
                }
                products(
                  first: 100
                  filter: { category: { categoryId: $categoryId } }
                ) {
                  edges {
                    node {
                      ...ShoppableProductCardFragment
                    }
                  }
                }
              }
            }
          }
        }
        deliveries(
          filter: {
            range: { start: $startWeek, size: 7 }
            states: [PAUSED, UPCOMING]
          }
        ) {
          edges {
            node {
              ...DeliveryFragment
            }
          }
        }
      }
    }
  }
}
```

**Key patterns demonstrated:**
- Multiple query variables with custom scalar types (WeekId, CategoryId)
- Nested query structure with aliased fields (`selectedDelivery`)
- Fragment composition (CategoryFragment, FilterFragment, ShoppableProductCardFragment, DeliveryFragment)
- Filter arguments for data subsetting
- Edge/node GraphQL pagination pattern

## Example 2: Fragment Definition with Nested Fragments

**File**: `data-access/graphql/fragments/CartFragment.graphql`

This example shows fragment composition and inline fragments for union types.

```graphql
fragment CartFragment on Cart {
  id
  mealChoiceDone
  selections {
    ...ProductSelectionFragment
  }
  actionOverrides {
    disableAllActions
    productOverrides {
      productId
      actionsOverrides {
        type: __typename
        allowed
        reason
        ... on IncreaseQuantity {
          step
        }
        ... on DecreaseQuantity {
          step
        }
        ... on Subscribe {
          limit
        }
      }
    }
  }
  prices {
    ...ProductPricingFragment
  }
  productAvailability {
    id
    state
  }
  config {
    ...ConfigFragment
  }
}

fragment ProductSelectionFragment on ProductSelection {
  id
  legacyCourseIndex
  legacyProductSku
  quantity
  pairedWith
  subscription {
    quantity
    status
  }
}
```

**Key patterns demonstrated:**
- Fragment composition with nested fragments (ProductSelectionFragment, ProductPricingFragment, ConfigFragment)
- Inline fragments for union/interface types (`... on IncreaseQuantity`)
- `__typename` for discriminating union types
- Reusable fragment for consistent cart data shape

## Example 3: Custom Query Hook with Data Processing

**File**: `data-access/graphql/store/queries.ts`

This example shows wrapping Apollo Client `useQuery` in a custom hook with data extraction and processing.

```typescript
import type { QueryHookOptions } from '@apollo/client';
import { NetworkStatus, useQuery } from '@apollo/client';

import {
  GetStoreProductsDocument,
  GetStoreInitialDataDocument,
} from '@data-access/graphql';
import type {
  GetStoreProductsQuery,
  GetStoreProductsQueryVariables,
  ShoppableProductCardFragmentFragment,
  GetStoreInitialDataQuery,
  GetStoreInitialDataQueryVariables,
  DeliveryFragmentFragment,
  CategoryFragmentFragment,
  FilterFragmentFragment,
} from '@data-access/graphql';

import { extractProducts } from './utils';

/**
 * Type for the initial store data
 */
export type InitialStoreData = {
  processedDeliveryList: DeliveryFragmentFragment[];
  processedCurrentDelivery: DeliveryFragmentFragment;
  processedCategoryList: CategoryFragmentFragment[];
  processedFilterList: FilterFragmentFragment[];
  processedProductsForSelectedDelivery: ShoppableProductCardFragmentFragment[];
  planId: string;
};

/**
 * Extract deliveries from the GraphQL response
 *
 * @param data - Raw GraphQL response
 * @returns Array of DeliveryFragmentFragment
 */
export const extractDeliveryList = (
  data: GetStoreInitialDataQuery
): DeliveryFragmentFragment[] => {
  const edges = data?.customer?.plans?.[0]?.items?.[0]?.deliveries?.edges;

  if (!edges || !edges.length) {
    return [];
  }

  return edges.reduce((acc, edge) => {
    const delivery = edge?.node;

    if (!delivery || delivery?.isPostCutOff) {
      return acc;
    }

    return [...acc, delivery];
  }, [] as DeliveryFragmentFragment[]);
};

/**
 * Custom hook for fetching initial store data
 *
 * @param options - Apollo query options
 * @returns Query result with extracted delivery list, current delivery, category list, filter list, products for selected delivery
 */
export const useGetInitialStoreQuery = (
  options: QueryHookOptions<
    GetStoreInitialDataQuery,
    GetStoreInitialDataQueryVariables
  >
) => {
  // Standard Apollo query
  const actualQuery = useQuery(GetStoreInitialDataDocument, options);

  const dataToProccess = actualQuery.data;

  const processedDeliveryList = dataToProccess
    ? extractDeliveryList(dataToProccess)
    : undefined;

  const processedCurrentDelivery = dataToProccess
    ? extractCurrentDelivery(dataToProccess)
    : undefined;

  const processedCategoryList = dataToProccess
    ? extractCategoryList(dataToProccess)
    : undefined;

  const processedFilterList = dataToProccess
    ? extractFilterList(dataToProccess)
    : undefined;

  const processedProductsForSelectedDelivery = dataToProccess
    ? extractProductsForSelectedDelivery(dataToProccess)
    : undefined;

  const processedPlanId = dataToProccess
    ? extractPlanId(dataToProccess)
    : undefined;

  const processedData: InitialStoreData = {
    processedDeliveryList: processedDeliveryList || [],
    processedCurrentDelivery:
      processedCurrentDelivery || ({} as DeliveryFragmentFragment),
    processedCategoryList: processedCategoryList || [],
    processedFilterList: processedFilterList || [],
    processedProductsForSelectedDelivery:
      processedProductsForSelectedDelivery || [],
    planId: processedPlanId || '',
  };

  return {
    ...actualQuery,
    data: actualQuery.error || actualQuery.loading ? undefined : processedData,
  };
};

/**
 * Custom hook for fetching store products
 *
 * @param options - Apollo query options
 * @returns Query result with extracted products data
 */
export const useGetStoreProductsQuery = (
  options: QueryHookOptions<
    GetStoreProductsQuery,
    GetStoreProductsQueryVariables
  >
) => {
  const actualQuery = useQuery(GetStoreProductsDocument, options);

  // Process the actual query data if available
  const processedData = actualQuery.data
    ? extractProducts(actualQuery.data)
    : undefined;

  // We only consider an error if products are not present, and there are errors in the response
  if ((!processedData || processedData.length === 0) && actualQuery.error) {
    return {
      ...actualQuery,
      loading: actualQuery.networkStatus === NetworkStatus.refetch,
      error: actualQuery.error,
      data: processedData,
      retry: actualQuery.refetch,
    };
  }

  return {
    ...actualQuery,
    error: undefined, // Clear error if we have data
    data: processedData,
    loading: actualQuery.loading,
    retry: actualQuery.refetch,
  };
};
```

**Key patterns demonstrated:**
- Custom hooks wrapping `useQuery` from Apollo Client
- Extraction functions for processing raw GraphQL data
- Domain-specific return types (InitialStoreData)
- Conditional error handling (only error if no data available)
- `retry` function mapping to `refetch`
- Null-safe data access with optional chaining
- Array reduction for filtering

## Example 4: Mutation Hook

**File**: `data-access/graphql/cart/mutations.ts`

This example shows a simple mutation hook wrapper.

```typescript
import type { MutationHookOptions } from '@apollo/client';
import { useMutation } from '@apollo/client';

import { UpdateCartDocument } from '@data-access/graphql';
import type {
  UpdateCartMutation,
  UpdateCartMutationVariables,
} from '@data-access/graphql';

export const useUpdateCartMutation = (
  options: MutationHookOptions<UpdateCartMutation, UpdateCartMutationVariables>
) => useMutation(UpdateCartDocument, options);
```

**Key patterns demonstrated:**
- Mutation hook wrapper following same pattern as query hooks
- Type-safe variables and response with generated types
- Forwarding all Apollo mutation options to caller

## Example 5: Mutation Definition

**File**: `data-access/graphql/cart/UpdateCartMutation.graphql`

This example shows a mutation with multiple variables and error handling.

```graphql
mutation UpdateCart(
  $planId: PlanId!
  $deliveryId: DeliveryId!
  $selectionInput: [UpdateSelectionInput!]!
  $isSeamlessDowngradeEnabled: Boolean!
) {
  updateCart(
    planId: $planId
    deliveryId: $deliveryId
    selection: $selectionInput
    isSeamlessDowngradeEnabled: $isSeamlessDowngradeEnabled
  ) {
    errors {
      productId
      type
    }
    seamlessDowngraded
  }
}
```

**Key patterns demonstrated:**
- Multiple mutation variables with custom scalars and input types
- Array input type (`[UpdateSelectionInput!]!`)
- Non-null modifiers (`!`)
- Error field in mutation response for validation errors

## Example 6: Query with errorPolicy

**File**: `data-access/graphql/cart/queries.ts`

This example demonstrates using `errorPolicy` to handle partial data gracefully.

```typescript
import type { QueryHookOptions } from '@apollo/client';
import { useQuery } from '@apollo/client';

import { GetCartDocument } from '@data-access/graphql';
import type {
  GetCartQuery,
  GetCartQueryVariables,
} from '@data-access/graphql';

export const useGetCartQuery = (
  options: QueryHookOptions<GetCartQuery, GetCartQueryVariables>
) => {
  return useQuery(GetCartDocument, {
    ...options,
    errorPolicy: 'ignore', // Ignore GraphQL errors, return partial data if available
  });
};
```

**Key patterns demonstrated:**
- `errorPolicy: 'ignore'` for graceful degradation
- Spread operator to forward all options
- Override specific option (errorPolicy) while preserving others

## Example 7: Memoized Query Variables

**File**: `modules/store/screens/storefront/hooks/use-initial-store-data-loader/useInitialStoreDataLoader.ts`

This example shows memoizing query variables to prevent Apollo cache misses.

```typescript
import { useMemo } from 'react';
import { useGetInitialStoreQuery } from '@data-access/graphql/store';
import { useStorefrontStore } from '@modules/store/zustand-store';

/**
 * This hook implements a "load-once" pattern for initial store data to prevent unnecessary
 * network requests when users switch between weeks or navigate between stacks.
 */
export const useInitialStoreDataLoader = ({
  categoryId,
  selectedWeek,
  startWeek,
}: Props) => {
  const { isInitialStoreDataLoaded, setIsInitialStoreDataLoaded } =
    useStorefrontStore();

  // Memoize variables to prevent unnecessary re-renders and Apollo cache misses
  const memoizedVariables = useMemo(
    () => ({
      categoryId,
      selectedWeek,
      startWeek,
    }),
    [categoryId, selectedWeek, startWeek]
  );

  const result = useGetInitialStoreQuery({
    variables: memoizedVariables,
    onCompleted: () => {
      // Mark as attempted globally after successful completion
      setIsInitialStoreDataLoaded(true);
    },
    onError: () => {
      // Mark as attempted globally after error to prevent infinite retry loops
      setIsInitialStoreDataLoaded(true);
    },
    // Use cache-only after first load to prevent backend calls
    // Use cache-first on first load to fetch from network if cache is empty
    fetchPolicy: isInitialStoreDataLoaded ? 'cache-only' : 'cache-first',
    // Continue on errors to ensure the completion callback can still fire
    errorPolicy: 'all',
  });

  return result;
};
```

**Key patterns demonstrated:**
- `useMemo` to memoize query variables object
- Dynamic `fetchPolicy` based on load state (cache-first then cache-only)
- `onCompleted` and `onError` callbacks for side effects
- Global flag to track if data was already loaded
- `errorPolicy: 'all'` to return partial data with errors

## Example 8: Testing Query Hook

**File**: `data-access/graphql/store/__tests__/useGetStoreProductsQuery.test.ts`

This example shows testing a custom query hook with mocked Apollo Client.

```typescript
import { useQuery } from '@apollo/client';
import { renderHook } from '@testing-library/react-native';

import { GetStoreProductsDocument } from '@data-access/graphql';
import type { ShoppableProductCardFragmentFragment } from '@data-access/graphql';

import { useGetStoreProductsQuery } from '../queries';
import { extractProducts } from '../utils';

// Mock Apollo useQuery hook
jest.mock('@apollo/client', () => ({
  useQuery: jest.fn(),
  NetworkStatus: {
    ready: 7,
    loading: 1,
    error: 8,
  },
}));

// Mock utils
jest.mock('../utils', () => ({
  extractProducts: jest.fn(),
}));

const mockUseQuery = useQuery as jest.Mock;
const mockExtractProducts = extractProducts as jest.Mock;

describe('useGetStoreProductsQuery', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should return extracted data when data is available', () => {
    // Arrange
    const mockProducts: ShoppableProductCardFragmentFragment[] = [
      { id: 'product-1', __typename: 'ShoppableProduct' },
      { id: 'product-2', __typename: 'ShoppableProduct' },
    ] as ShoppableProductCardFragmentFragment[];

    const mockQueryResult = {
      data: { products: mockProducts },
      loading: false,
      error: undefined,
      networkStatus: 7,
      refetch: jest.fn(),
      fetchMore: jest.fn(),
    };

    mockUseQuery.mockReturnValue(mockQueryResult);
    mockExtractProducts.mockReturnValue(mockProducts);

    // Act
    const { result } = renderHook(() =>
      useGetStoreProductsQuery({
        variables: { selectedWeek: '2023-W20' },
      })
    );

    // Assert
    expect(mockUseQuery).toHaveBeenCalledWith(GetStoreProductsDocument, {
      variables: { selectedWeek: '2023-W20' },
    });
    expect(mockExtractProducts).toHaveBeenCalledWith(mockQueryResult.data);
    expect(result.current.data).toEqual(mockProducts);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeUndefined();
  });

  it('should return loading state', () => {
    // Arrange
    const mockQueryResult = {
      data: undefined,
      loading: true,
      error: undefined,
      networkStatus: 1,
      refetch: jest.fn(),
      fetchMore: jest.fn(),
    };

    mockUseQuery.mockReturnValue(mockQueryResult);

    // Act
    const { result } = renderHook(() =>
      useGetStoreProductsQuery({
        variables: { selectedWeek: '2023-W20' },
      })
    );

    // Assert
    expect(result.current.data).toEqual(undefined);
    expect(result.current.loading).toBe(true);
    expect(result.current.error).toBeUndefined();
  });

  it('should return error when query has error', () => {
    // Arrange
    const mockError = new Error('Test error');
    const mockQueryResult = {
      data: undefined,
      loading: false,
      error: mockError,
      networkStatus: 8,
      refetch: jest.fn(),
      fetchMore: jest.fn(),
    };

    mockUseQuery.mockReturnValue(mockQueryResult);

    // Act
    const { result } = renderHook(() =>
      useGetStoreProductsQuery({
        variables: { selectedWeek: '2023-W20' },
      })
    );

    // Assert
    expect(result.current.data).toEqual(undefined);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(mockError);
  });

  it('should call retry function which calls refetch', () => {
    // Arrange
    const mockRefetch = jest.fn();
    const mockQueryResult = {
      data: undefined,
      loading: false,
      error: undefined,
      networkStatus: 7,
      refetch: mockRefetch,
      fetchMore: jest.fn(),
    };

    mockUseQuery.mockReturnValue(mockQueryResult);

    // Act
    const { result } = renderHook(() =>
      useGetStoreProductsQuery({
        variables: { selectedWeek: '2023-W20' },
      })
    );

    result.current.retry();

    // Assert
    expect(mockRefetch).toHaveBeenCalledTimes(1);
  });
});
```

**Key patterns demonstrated:**
- Mocking `useQuery` from `@apollo/client`
- Mocking utility functions (extractProducts)
- Testing all query states: success, loading, error
- Verifying correct document and variables passed to Apollo
- Testing retry functionality
- Type-safe mocked data with TypeScript

## Anti-Patterns from Codebase Review

### ❌ Defining Queries Inline

```typescript
// DON'T: No type generation, no IDE support
import { gql, useQuery } from '@apollo/client';

const GET_PRODUCTS = gql`
  query GetProducts {
    products {
      id
      name
    }
  }
`;

export const ProductList = () => {
  const { data } = useQuery(GET_PRODUCTS);
  return <List items={data?.products} />;
};
```

### ❌ Skipping Custom Hooks

```typescript
// DON'T: Direct Apollo usage in components
import { useQuery } from '@apollo/client';
import { GetProductsDocument } from '@data-access/graphql';

export const ProductList = () => {
  // Hard to mock in tests, no data processing
  const { data } = useQuery(GetProductsDocument);
  return <List items={data} />;
};

// DO: Use custom hooks
import { useGetProductsQuery } from '@data-access/graphql/products';

export const ProductList = () => {
  const { data } = useGetProductsQuery();
  return <List items={data} />;
};
```

### ❌ Not Memoizing Variables

```typescript
// DON'T: New object every render causes cache miss
export const ProductList = ({ categoryId }: Props) => {
  const { data } = useGetStoreProductsQuery({
    variables: { categoryId, selectedWeek: '2024-W10' }, // Cache miss on every render!
  });
  return <List items={data} />;
};

// DO: Memoize variables
export const ProductList = ({ categoryId }: Props) => {
  const variables = useMemo(
    () => ({ categoryId, selectedWeek: '2024-W10' }),
    [categoryId]
  );

  const { data } = useGetStoreProductsQuery({ variables });
  return <List items={data} />;
};
```

### ❌ Ignoring Error States

```typescript
// DON'T: No error handling
export const ProductList = () => {
  const { data } = useGetStoreProductsQuery({
    variables: { selectedWeek: '2024-W10' },
  });
  // Will crash if query fails
  return <List items={data} />;
};

// DO: Handle errors
export const ProductList = () => {
  const { data, loading, error, refetch } = useGetStoreProductsQuery({
    variables: { selectedWeek: '2024-W10' },
    errorPolicy: 'all',
  });

  if (loading) return <LoadingSpinner />;
  if (error && !data) return <ErrorMessage error={error} onRetry={refetch} />;

  return <List items={data || []} />;
};
```

## Summary

The YourCompany codebase consistently follows these GraphQL patterns:

1. **Query definitions in .graphql files** for type generation and IDE support
2. **Custom hooks wrapping Apollo Client** for consistent API and testability
3. **Fragment composition** for reusable data shapes
4. **Data extraction functions** to process raw GraphQL responses
5. **Memoized query variables** to prevent Apollo cache misses
6. **errorPolicy configuration** for graceful error handling
7. **Domain-based organization** for maintainability
8. **Comprehensive testing** with mocked Apollo hooks
9. **Type-safe operations** with generated TypeScript types
10. **Load-once patterns** with dynamic fetchPolicy

These patterns ensure type safety, optimal caching, graceful error handling, and maintainable GraphQL operations throughout the app.
