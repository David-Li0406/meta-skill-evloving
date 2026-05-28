---
name: graphql-api
description: "WHAT: GraphQL queries and mutations with Apollo Client and code generation. WHEN: fetching GraphQL data, creating type-safe queries, composing fragments, testing Apollo. KEYWORDS: graphql, apollo, query, mutation, fragment, useQuery, useMutation, codegen, gql, mobile."
---

# GraphQL API Patterns with Apollo Client

## Core Principles

**Define queries in .graphql files and wrap them in custom hooks.** Use code generation for TypeScript types, organize by domain, compose with fragments, and handle errors with errorPolicy.

**Why**: GraphQL with Apollo Client provides type-safe server state management with automatic caching, request deduplication, and optimistic updates. Code generation ensures TypeScript types stay in sync with the backend schema, preventing runtime errors.

## When to Use This Skill

Use these patterns when:

- Fetching data from GraphQL APIs
- Building type-safe queries and mutations
- Organizing GraphQL operations by feature domain
- Reusing common data shapes with fragments
- Handling partial data and errors gracefully
- Testing components with GraphQL dependencies
- Generating TypeScript types from schema
- Managing server state with caching

## File Organization

### Domain-Based Structure

```
data-access/graphql/
├── store/
│   ├── GetStoreProducts.graphql      # Query definition
│   ├── GetInitialStore.graphql       # Complex query
│   ├── queries.ts                     # Custom hooks
│   └── index.ts                       # Public exports
├── cart/
│   ├── GetCartQuery.graphql          # Query definition
│   ├── UpdateCartMutation.graphql    # Mutation definition
│   ├── queries.ts                     # Query hooks
│   ├── mutations.ts                   # Mutation hooks
│   └── index.ts                       # Public exports
├── fragments/
│   ├── CartFragment.graphql          # Reusable fragment
│   ├── ProductFragment.graphql       # Reusable fragment
│   └── DeliveryFragment.graphql      # Reusable fragment
└── README.md
```

**Why**: Domain-based organization keeps related GraphQL operations together, making them easier to find, maintain, and test. Fragment reuse prevents duplication and ensures consistency.

**Production Example**: `git-resources/shared-mobile-modules/src/data-access/graphql/`

### Required Files Per Domain

```
domain/
├── OperationName.graphql  # Query/mutation/subscription definition
├── queries.ts             # Custom hooks for queries
├── mutations.ts           # Custom hooks for mutations (if needed)
└── index.ts               # Public exports only
```

**Why**: This structure enforces separation of concerns: `.graphql` files define operations, `.ts` files wrap them in hooks, `index.ts` controls the public API.

## Query Definition

### Basic Query in .graphql File

```graphql
# data-access/graphql/store/GetStoreProducts.graphql
query GetStoreProducts(
  $selectedWeek: WeekId!
  $categoryId: CategoryId!
  $filters: [FilterInput!]
) {
  customer {
    id
    plans(type: RTE) {
      id
      items {
        deliveries(
          first: 1
          filter: {
            range: { start: $selectedWeek, size: 1 }
            states: [PAUSED, UPCOMING]
          }
        ) {
          edges {
            node {
              menu {
                products(
                  first: 100
                  filter: {
                    category: { categoryId: $categoryId }
                    filters: $filters
                  }
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
      }
    }
  }
}
```

**Why**: Defining queries in `.graphql` files enables:
- IDE autocomplete with GraphQL plugins
- Automatic TypeScript type generation
- Schema validation at build time
- Syntax highlighting and error detection

**Production Example**: `git-resources/shared-mobile-modules/src/data-access/graphql/store/GetStoreProducts.graphql`

### Naming Conventions

```graphql
# ✅ Use PascalCase for operations
query GetStoreProducts { ... }
query GetInitialStoreData { ... }
mutation UpdateCart { ... }
mutation FavoriteProduct { ... }

# ✅ Name descriptively with action + resource
query GetProductDetails { ... }
mutation CreateOrder { ... }
mutation DeleteRecipe { ... }

# ✅ Variables use camelCase
query GetStoreProducts(
  $selectedWeek: WeekId!
  $categoryId: CategoryId!
) { ... }
```

**Why**: Consistent naming makes operations discoverable and predictable. Code generation creates `GetStoreProductsDocument` and `GetStoreProductsQuery` types from operation names.

## Custom Hooks Pattern

### Wrapping Queries

```typescript
// data-access/graphql/store/queries.ts
import type { QueryHookOptions } from '@apollo/client';
import { useQuery } from '@apollo/client';

import { GetStoreProductsDocument } from '@data-access/graphql';
import type {
  GetStoreProductsQuery,
  GetStoreProductsQueryVariables,
} from '@data-access/graphql';

/**
 * Custom hook for fetching store products
 *
 * @param options - Apollo query options
 * @returns Query result with loading, error, data states
 */
export const useGetStoreProductsQuery = (
  options: QueryHookOptions<
    GetStoreProductsQuery,
    GetStoreProductsQueryVariables
  >
) => {
  return useQuery(GetStoreProductsDocument, options);
};
```

**Why**: Custom hooks provide a consistent API, enable additional processing (data extraction, error handling), and make operations easier to mock in tests.

**Production Example**: `git-resources/shared-mobile-modules/src/data-access/graphql/store/queries.ts:226`

### Wrapping Mutations

```typescript
// data-access/graphql/cart/mutations.ts
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

**Why**: Mutation hooks follow the same pattern as query hooks, providing consistency across the codebase and enabling easy testing.

**Production Example**: `git-resources/shared-mobile-modules/src/data-access/graphql/cart/mutations.ts:10`

### Public Exports

```typescript
// data-access/graphql/store/index.ts
export { useGetStoreProductsQuery } from './queries';
export { useGetInitialStoreQuery } from './queries';
export type { InitialStoreData } from './queries';
```

**Why**: Exporting through `index.ts` controls the public API, allowing internal refactoring without breaking consumers.

## Fragment Composition

### Defining Fragments

```graphql
# data-access/graphql/fragments/CartFragment.graphql
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
      }
    }
  }
  prices {
    ...ProductPricingFragment
  }
  config {
    ...ConfigFragment
  }
}

fragment ProductSelectionFragment on ProductSelection {
  id
  legacyCourseIndex
  quantity
  pairedWith
  subscription {
    quantity
    status
  }
}
```

**Why**: Fragments define reusable data shapes, ensuring consistency across queries and reducing duplication. Fragment composition (nesting fragments) creates a hierarchy of reusable pieces.

**Production Example**: `git-resources/shared-mobile-modules/src/data-access/graphql/fragments/CartFragment.graphql`

### Using Fragments in Queries

```graphql
# data-access/graphql/store/GetInitialStore.graphql
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
        selectedDelivery: deliveries(
          first: 1
          filter: {
            range: { start: $selectedWeek, size: 1 }
            states: [PAUSED, UPCOMING]
          }
        ) {
          edges {
            node {
              ...DeliveryFragment
              menu {
                categories {
                  ...CategoryFragment
                }
                filters {
                  ...FilterFragment
                }
                products(first: 100) {
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
      }
    }
  }
}
```

**Why**: Fragments keep queries readable and maintainable. When fragment definition changes, all queries using it automatically get the updated fields.

**Production Example**: `git-resources/shared-mobile-modules/src/data-access/graphql/store/GetInitialStore.graphql`

## Data Processing Pattern

### Extracting and Processing Data

```typescript
import type { QueryHookOptions } from '@apollo/client';
import { useQuery } from '@apollo/client';

import { GetStoreInitialDataDocument } from '@data-access/graphql';
import type {
  GetStoreInitialDataQuery,
  GetStoreInitialDataQueryVariables,
  DeliveryFragmentFragment,
} from '@data-access/graphql';

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
 */
export const useGetInitialStoreQuery = (
  options: QueryHookOptions<
    GetStoreInitialDataQuery,
    GetStoreInitialDataQueryVariables
  >
) => {
  const actualQuery = useQuery(GetStoreInitialDataDocument, options);

  // Process data if available
  const processedDeliveryList = actualQuery.data
    ? extractDeliveryList(actualQuery.data)
    : undefined;

  return {
    ...actualQuery,
    data: actualQuery.error || actualQuery.loading
      ? undefined
      : { processedDeliveryList },
  };
};
```

**Why**: Processing raw GraphQL responses into domain-specific data shapes isolates complexity, provides type-safe access, and makes components easier to test.

**Production Example**: `git-resources/shared-mobile-modules/src/data-access/graphql/store/queries.ts:156`

## Error Handling

### Using errorPolicy

```typescript
// data-access/graphql/cart/queries.ts
import { useQuery } from '@apollo/client';
import { GetCartDocument } from '@data-access/graphql';

export const useGetCartQuery = (options: QueryHookOptions) => {
  return useQuery(GetCartDocument, {
    ...options,
    errorPolicy: 'ignore', // Ignore GraphQL errors, return partial data
  });
};
```

**Error Policy Options**:

```typescript
// 'none' (default) - Errors terminate query, no data returned
errorPolicy: 'none'

// 'ignore' - Ignore GraphQL errors, return data if available
errorPolicy: 'ignore'

// 'all' - Return both partial data AND errors
errorPolicy: 'all'
```

**Why**: `errorPolicy: 'ignore'` or `'all'` enables graceful degradation when parts of a query fail. Users see available data instead of a blank screen.

**Production Example**: `git-resources/shared-mobile-modules/src/data-access/graphql/cart/queries.ts:23`

### Conditional Error Handling

```typescript
export const useGetStoreProductsQuery = (
  options: QueryHookOptions<
    GetStoreProductsQuery,
    GetStoreProductsQueryVariables
  >
) => {
  const actualQuery = useQuery(GetStoreProductsDocument, options);

  const processedData = actualQuery.data
    ? extractProducts(actualQuery.data)
    : undefined;

  // Only consider an error if products are not present AND there are errors
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

**Why**: Conditional error handling allows showing partial data when available, only treating it as an error when no data can be displayed.

**Production Example**: `git-resources/shared-mobile-modules/src/data-access/graphql/store/queries.ts:226`

## Query Options

### Common Query Options

```typescript
import { useGetStoreProductsQuery } from '@data-access/graphql/store';

export const ProductList = () => {
  const { data, loading, error, refetch } = useGetStoreProductsQuery({
    variables: {
      selectedWeek: '2024-W10',
      categoryId: 'meals',
    },
    // Fetch from network first, then use cache
    fetchPolicy: 'cache-first',
    // Continue even if query has errors
    errorPolicy: 'all',
    // Polling interval (ms)
    pollInterval: 30000,
    // Skip query execution
    skip: !selectedWeek,
    // Callback on success
    onCompleted: (data) => {
      console.log('Query completed', data);
    },
    // Callback on error
    onError: (error) => {
      console.error('Query failed', error);
    },
  });

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;

  return <ProductGrid products={data} />;
};
```

**Fetch Policy Options**:

```typescript
// 'cache-first' - Use cache if available, otherwise fetch from network
fetchPolicy: 'cache-first'

// 'cache-only' - Only use cache, never fetch from network
fetchPolicy: 'cache-only'

// 'network-only' - Always fetch from network, update cache
fetchPolicy: 'network-only'

// 'no-cache' - Fetch from network, don't write to cache
fetchPolicy: 'no-cache'

// 'cache-and-network' - Use cache immediately, then fetch from network
fetchPolicy: 'cache-and-network'
```

**Why**: Fetch policies control cache behavior, enabling offline support, optimistic UI, and performance optimization.

### useMemo for Variables

```typescript
import { useMemo } from 'react';
import { useGetInitialStoreQuery } from '@data-access/graphql/store';

export const useInitialStoreDataLoader = ({
  categoryId,
  selectedWeek,
  startWeek,
}: Props) => {
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
    fetchPolicy: 'cache-first',
  });

  return result;
};
```

**Why**: Memoizing variables prevents Apollo cache misses caused by new object references on every render, improving performance and preventing unnecessary network requests.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/store/screens/storefront/hooks/use-initial-store-data-loader/useInitialStoreDataLoader.ts:119`

## Mutations

### Mutation Definition

```graphql
# data-access/graphql/cart/UpdateCartMutation.graphql
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

**Production Example**: `git-resources/shared-mobile-modules/src/data-access/graphql/cart/UpdateCartMutation.graphql`

### Using Mutations

```typescript
import { useUpdateCartMutation } from '@data-access/graphql/cart';

export const useCartActions = () => {
  const [updateCart, { loading, error }] = useUpdateCartMutation({
    onCompleted: (data) => {
      if (data.updateCart.errors.length === 0) {
        console.log('Cart updated successfully');
      }
    },
    onError: (error) => {
      console.error('Failed to update cart', error);
    },
    // Update cache after mutation
    update: (cache, { data }) => {
      // Modify cache directly
      cache.modify({
        id: cache.identify({ __typename: 'Cart', id: cartId }),
        fields: {
          selections: () => data.updateCart.selections,
        },
      });
    },
  });

  const handleAddToCart = async (productId: string, quantity: number) => {
    try {
      await updateCart({
        variables: {
          planId: currentPlanId,
          deliveryId: currentDeliveryId,
          selectionInput: [{ productId, quantity }],
          isSeamlessDowngradeEnabled: true,
        },
      });
    } catch (error) {
      // Error handling
      console.error(error);
    }
  };

  return { handleAddToCart, loading, error };
};
```

**Why**: Mutations modify server state and can update the Apollo cache automatically. `onCompleted` and `onError` callbacks enable side effects like navigation or toast notifications.

## Type Generation

### Setup Code Generation

```json
// package.json
{
  "scripts": {
    "graphql:generate": "graphql-codegen --config codegen.yml",
    "graphql:generate:watch": "graphql-codegen --config codegen.yml --watch"
  }
}
```

```yaml
# codegen.yml
overwrite: true
schema: 'https://api.example.com/graphql'
documents: 'src/data-access/graphql/**/*.graphql'
generates:
  src/data-access/graphql/types.ts:
    plugins:
      - typescript
      - typescript-operations
      - typescript-react-apollo
    config:
      withHooks: true
      withComponent: false
      withHOC: false
```

**Why**: Code generation creates TypeScript types from `.graphql` files and the schema, ensuring type safety and preventing runtime errors from schema changes.

### Generated Types

```typescript
// Generated types from GetStoreProducts.graphql
export type GetStoreProductsQueryVariables = Exact<{
  selectedWeek: Scalars['WeekId'];
  categoryId: Scalars['CategoryId'];
  filters?: InputMaybe<Array<FilterInput> | FilterInput>;
}>;

export type GetStoreProductsQuery = {
  __typename?: 'Query';
  customer?: {
    __typename?: 'Customer';
    id: string;
    plans: Array<{
      __typename?: 'Plan';
      id: string;
      items: Array<{
        __typename?: 'PlanItem';
        deliveries: {
          edges: Array<{
            node: {
              menu: {
                products: {
                  edges: Array<{
                    node: ShoppableProductCardFragmentFragment;
                  }>;
                };
              };
            };
          }>;
        };
      }>;
    }>;
  };
};

// Generated document for Apollo Client
export const GetStoreProductsDocument = gql`
  query GetStoreProducts($selectedWeek: WeekId!, $categoryId: CategoryId!) {
    customer {
      id
      plans(type: RTE) {
        # ... query definition
      }
    }
  }
`;
```

**Why**: Generated types provide autocomplete, type checking, and prevent typos in query variables and response fields.

## Testing

### Mocking Apollo Client Hooks

```typescript
import { useQuery } from '@apollo/client';
import { renderHook } from '@testing-library/react-native';

import { GetStoreProductsDocument } from '@data-access/graphql';
import type { ShoppableProductCardFragmentFragment } from '@data-access/graphql';

import { useGetStoreProductsQuery } from '../queries';

// Mock Apollo useQuery hook
jest.mock('@apollo/client', () => ({
  useQuery: jest.fn(),
  NetworkStatus: {
    ready: 7,
    loading: 1,
    error: 8,
  },
}));

const mockUseQuery = useQuery as jest.Mock;

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
    };

    mockUseQuery.mockReturnValue(mockQueryResult);

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
    expect(result.current.data).toEqual(mockProducts);
    expect(result.current.loading).toBe(false);
  });
});
```

**Why**: Mocking Apollo hooks enables testing custom hook logic without real API calls, making tests fast and deterministic.

**Production Example**: `git-resources/shared-mobile-modules/src/data-access/graphql/store/__tests__/useGetStoreProductsQuery.test.ts`

### Testing Loading and Error States

```typescript
describe('useGetStoreProductsQuery', () => {
  it('should return loading state', () => {
    mockUseQuery.mockReturnValue({
      data: undefined,
      loading: true,
      error: undefined,
      networkStatus: 1,
      refetch: jest.fn(),
    });

    const { result } = renderHook(() =>
      useGetStoreProductsQuery({
        variables: { selectedWeek: '2023-W20' },
      })
    );

    expect(result.current.loading).toBe(true);
    expect(result.current.data).toBeUndefined();
  });

  it('should return error state', () => {
    const mockError = new Error('Network error');

    mockUseQuery.mockReturnValue({
      data: undefined,
      loading: false,
      error: mockError,
      networkStatus: 8,
      refetch: jest.fn(),
    });

    const { result } = renderHook(() =>
      useGetStoreProductsQuery({
        variables: { selectedWeek: '2023-W20' },
      })
    );

    expect(result.current.error).toBe(mockError);
    expect(result.current.loading).toBe(false);
  });
});
```

**Why**: Testing loading and error states ensures components handle all query states correctly.

## Common Mistakes to Avoid

❌ **Don't define queries inline**:

```typescript
// ❌ No type safety, no IDE support
const { data } = useQuery(gql`
  query GetProducts {
    products {
      id
      name
    }
  }
`);
```

❌ **Don't skip custom hooks**:

```typescript
// ❌ Direct Apollo usage in components
import { useQuery } from '@apollo/client';
import { GetProductsDocument } from '@data-access/graphql';

export const ProductList = () => {
  const { data } = useQuery(GetProductsDocument); // Hard to mock in tests
  return <List items={data} />;
};
```

❌ **Don't forget to memoize query variables**:

```typescript
// ❌ New object every render causes cache miss
export const ProductList = ({ categoryId }: Props) => {
  const { data } = useGetStoreProductsQuery({
    variables: { categoryId, selectedWeek: '2024-W10' }, // New object every render!
  });
  return <List items={data} />;
};
```

❌ **Don't ignore error handling**:

```typescript
// ❌ No error handling
export const ProductList = () => {
  const { data } = useGetStoreProductsQuery({
    variables: { selectedWeek: '2024-W10' },
  });
  return <List items={data} />; // Will crash if query fails
};
```

✅ **Do define queries in .graphql files**:

```graphql
# ✅ Type-safe with IDE support
# data-access/graphql/store/GetStoreProducts.graphql
query GetStoreProducts($categoryId: CategoryId!) {
  products(categoryId: $categoryId) {
    id
    name
  }
}
```

✅ **Do use custom hooks**:

```typescript
// ✅ Easy to mock and test
import { useGetStoreProductsQuery } from '@data-access/graphql/store';

export const ProductList = () => {
  const { data } = useGetStoreProductsQuery({
    variables: { categoryId: 'meals' },
  });
  return <List items={data} />;
};
```

✅ **Do memoize query variables**:

```typescript
// ✅ Prevents cache misses
import { useMemo } from 'react';

export const ProductList = ({ categoryId }: Props) => {
  const variables = useMemo(
    () => ({ categoryId, selectedWeek: '2024-W10' }),
    [categoryId]
  );

  const { data } = useGetStoreProductsQuery({ variables });
  return <List items={data} />;
};
```

✅ **Do handle errors gracefully**:

```typescript
// ✅ Proper error handling
export const ProductList = () => {
  const { data, loading, error, refetch } = useGetStoreProductsQuery({
    variables: { selectedWeek: '2024-W10' },
    errorPolicy: 'all', // Return partial data on error
  });

  if (loading) return <LoadingSpinner />;
  if (error && !data) return <ErrorMessage error={error} onRetry={refetch} />;

  return <List items={data || []} />;
};
```

## Quick Reference

**File Organization:**
- Create domain folders in `data-access/graphql/`
- Define operations in `.graphql` files
- Wrap in custom hooks in `queries.ts`/`mutations.ts`
- Export through `index.ts`
- Store reusable fragments in `fragments/`

**Naming Conventions:**
- Operations: PascalCase (GetStoreProducts, UpdateCart)
- Variables: camelCase ($selectedWeek, $categoryId)
- Hooks: use prefix (useGetStoreProductsQuery)
- Files: Match operation name (GetStoreProducts.graphql)

**Code Generation:**
- Run `yarn graphql:generate --watch` during development
- Generates TypeScript types from schema + operations
- Creates `Document` exports for Apollo Client
- Provides type-safe query/mutation variables

**Custom Hooks:**
- Wrap `useQuery` and `useMutation` from Apollo Client
- Add data processing logic (extraction, transformation)
- Provide consistent error handling
- Enable easy testing with mocks

**Error Handling:**
- `errorPolicy: 'none'` - No data on error (default)
- `errorPolicy: 'ignore'` - Return data, ignore errors
- `errorPolicy: 'all'` - Return both data and errors
- Use `onError` callback for logging/tracking

**Testing:**
- Mock `useQuery` and `useMutation` from `@apollo/client`
- Test loading, error, and success states
- Verify correct document and variables passed
- Use `renderHook` for custom hook testing

**Key Libraries:**
- Apollo Client 3.13.6
- GraphQL Code Generator
- TypeScript 5.1.6

For production examples, see [references/examples.md](references/examples.md).
