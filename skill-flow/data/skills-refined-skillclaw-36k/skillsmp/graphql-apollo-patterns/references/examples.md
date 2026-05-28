# GraphQL Apollo Patterns - Production Examples

This document contains real production code examples from the YourCompany web codebase demonstrating @apollo/client v3.9.2 patterns.

## Example 1: GraphQL Query Definition

**File**: `app/spaces/deliveries/modules/past-deliveries/experiments/graphql/utils/gql-data-access/past-deliveries/past-deliveries.ts`

This example demonstrates defining a GraphQL query with the gql tag from the code generator.

```typescript
import { gql } from '../../graphql';

export const pastDeliveriesQuery = gql(`
  query GetPastDeliveries($first: Int = 4, $after: String = "", $locale: String!, $subscriptionID: String!, $country: String!) {
    pastDeliveries(first: $first, after: $after, locale: $locale, subscriptionID: $subscriptionID, country: $country) {
      pageInfo {
        endCursor
        hasNextPage
      }
      edges {
        cursor
        node {
          id
          week
          delivery {
            deliveryDate
          }
          selectedProducts {
            ... on MealKit {
              id
              name
              headline
              image
              label {
                handle
                text
                style {
                  foregroundColor
                  backgroundColor
                }
              }
            }
            ... on Addon {
              id
              name
              headline
              image
              label {
                handle
                text
                style {
                  foregroundColor
                  backgroundColor
                }
              }
            }
            userFavorite {
              isFavorite
            }
            userFeedback {
              rating
              comment
            }
          }
        }
      }
    }
  }
`);
```

**Key patterns:**
- Import `gql` from generated code (not from @apollo/client)
- Query defined with template literal syntax
- Variables with TypeScript-like syntax and defaults
- Cursor-based pagination with `pageInfo` pattern
- Union types with inline fragments (`... on MealKit`)
- Nested selections for related data
- Export query constant for reuse

## Example 2: useQuery with Pagination

**File**: `app/spaces/deliveries/modules/past-deliveries/experiments/graphql/hooks/useGraphQLPastDeliveries.ts`

This example shows using Apollo's useQuery hook with cursor-based pagination.

```typescript
import { useQuery } from '@apollo/client';

import { useSelectedLocale } from '@/libs/locale';
import { useSystemCountry } from '@/libs/system-country';
import { useSubscriptions } from '@/spaces/deliveries/modules/shared/__shared_context';

import { pastDeliveriesQuery } from '../utils/gql-data-access/past-deliveries';
import { useGraphQLEnabled } from './useGraphQLEnabled';

export const useGraphQLPastDeliveries = () => {
  const { current } = useSubscriptions();
  const isGraphQLIntegrationEnabled = useGraphQLEnabled();

  const locale = useSelectedLocale();
  const country = useSystemCountry();

  const queryResult = useQuery(pastDeliveriesQuery, {
    variables: {
      locale: locale.toString(),
      country: country.toString(),
      subscriptionID: current?.id ?? '',
    },
    skip: !isGraphQLIntegrationEnabled || !current?.id,
  });

  return {
    ...queryResult,
    fetchNextGraphQLPage: async () => {
      try {
        await queryResult.fetchMore({
          variables: {
            after: queryResult.data?.pastDeliveries?.pageInfo?.endCursor,
          },
        });
      } catch {
        /* Potential notification trigger */
      }
    },
  };
};

// Usage in component
export const PastDeliveriesList = () => {
  const {
    data,
    loading,
    error,
    fetchNextGraphQLPage,
  } = useGraphQLPastDeliveries();

  if (loading) return <Spinner />;
  if (error) return <Error message={error.message} />;

  const hasNextPage = data?.pastDeliveries?.pageInfo?.hasNextPage;

  return (
    <div>
      {data?.pastDeliveries?.edges.map(({ node }) => (
        <DeliveryCard key={node.id} delivery={node} />
      ))}

      {hasNextPage && (
        <button onClick={fetchNextGraphQLPage}>Load More</button>
      )}
    </div>
  );
};
```

**Key patterns:**
- `useQuery` with query document and options
- `variables` object passes query variables
- `skip` option for conditional query execution
- `fetchMore` for cursor-based pagination
- Custom hook wraps useQuery for enhanced API
- Spread `queryResult` to expose all Apollo properties
- Add convenience method `fetchNextGraphQLPage`
- Use `endCursor` from previous response for next page
- Error handling with try/catch in custom method

## Example 3: GraphQL Mutation Definition

**File**: `app/spaces/deliveries/modules/past-deliveries/experiments/graphql/utils/gql-data-access/past-deliveries/favorite-mutation.ts`

This example demonstrates defining a GraphQL mutation.

```typescript
import { gql } from '../../graphql';

export const favoriteMutation = gql(`
  mutation FavoriteProduct($input: FavoriteProductInput!) {
    favoriteProduct(favorite: $input) {
      product {
        id
      }
      isFavorite
    }
  }
`);

// Second mutation example
// File: rate-mutation.ts
export const rateMutation = gql(`
  mutation RateProduct($input: RateProductInput) {
    rateProduct(rate: $input) {
      product {
        id
      }
      rating
    }
  }
`);
```

**Key patterns:**
- Mutation keyword instead of query
- Input object pattern (`$input` parameter)
- Return updated fields for cache update
- Mutation name describes the action
- Export mutation constant

## Example 4: useMutation Pattern

**Inferred from codebase patterns** (standard Apollo Client usage)

This example shows using Apollo's useMutation hook.

```typescript
import { useMutation } from '@apollo/client';
import { favoriteMutation } from '../utils/gql-data-access/past-deliveries';

export const useFavoriteProduct = () => {
  const [favoriteProduct, { loading, error }] = useMutation(favoriteMutation, {
    // Optimistic response for instant UI update
    optimisticResponse: (variables) => ({
      favoriteProduct: {
        __typename: 'FavoriteProductPayload',
        product: {
          __typename: 'Product',
          id: variables.input.productId,
        },
        isFavorite: variables.input.isFavorite,
      },
    }),
    // Update Apollo cache after mutation
    update: (cache, { data }) => {
      if (data?.favoriteProduct) {
        cache.modify({
          id: cache.identify({
            __typename: 'Product',
            id: data.favoriteProduct.product.id,
          }),
          fields: {
            userFavorite() {
              return {
                __typename: 'UserFavorite',
                isFavorite: data.favoriteProduct.isFavorite,
              };
            },
          },
        });
      }
    },
    // Refetch queries after mutation
    refetchQueries: ['GetPastDeliveries'],
    // Show success notification
    onCompleted: (data) => {
      if (data.favoriteProduct.isFavorite) {
        toast.success('Added to favorites!');
      } else {
        toast.success('Removed from favorites!');
      }
    },
    // Show error notification
    onError: (error) => {
      toast.error(`Failed: ${error.message}`);
    },
  });

  return { favoriteProduct, loading, error };
};

// Usage in component
export const ProductCard = ({ product }) => {
  const { favoriteProduct, loading } = useFavoriteProduct();

  const handleToggleFavorite = () => {
    favoriteProduct({
      variables: {
        input: {
          productId: product.id,
          isFavorite: !product.userFavorite.isFavorite,
        },
      },
    });
  };

  return (
    <Card>
      <h3>{product.name}</h3>
      <button onClick={handleToggleFavorite} disabled={loading}>
        {loading ? 'Updating...' : 'Toggle Favorite'}
      </button>
    </Card>
  );
};
```

**Key patterns:**
- `useMutation` returns tuple: `[mutate, result]`
- `optimisticResponse` for instant UI update
- `update` function for manual cache updates
- `cache.modify` to update specific fields
- `refetchQueries` to refresh related queries
- `onCompleted` and `onError` callbacks
- Call mutation function with `variables` object
- Destructure `loading` and `error` from result

## Example 5: Apollo Client Setup with Links

**File**: `app/spaces/deliveries/modules/past-deliveries/experiments/graphql/utils/graphql/GraphQLProvider.tsx`

This example demonstrates setting up Apollo Client with custom links.

```typescript
import { useMemo } from 'react';
import { ApolloClient, ApolloProvider, InMemoryCache } from '@apollo/client';
import { from } from '@apollo/client/link/core';

import { Claim, useClaim } from '@/libs/governance';
import { ClientTracer, useClientTracer } from '@/libs/tracing';

import authLink from './links/auth';
import errorLink from './links/error';
import tracerLink from './links/tracer';
import platformLink from './links/platform';
import httpLinkFactory from './links/http-factory';
import contextLinkFactory from './links/context-factory';

type Props = {
  uri?: string;
};

const generateClient = (
  claim: Claim | null,
  tracer: ClientTracer,
  uri?: string
) =>
  new ApolloClient({
    cache: new InMemoryCache(),
    link: from([
      contextLinkFactory(claim, tracer),
      tracerLink,
      errorLink,
      platformLink,
      authLink,
      httpLinkFactory(uri),
    ]),
  });

export const GraphQLProvider = ({
  children,
  uri,
}: React.PropsWithChildren<Props>) => {
  const claim = useClaim();
  const tracer = useClientTracer();

  const client = useMemo(
    () => generateClient(claim, tracer, uri),
    [claim, tracer, uri]
  );

  return <ApolloProvider client={client}>{children}</ApolloProvider>;
};

// Usage in app
export const App = () => (
  <GraphQLProvider uri="https://api.example.com/graphql">
    <Routes />
  </GraphQLProvider>
);
```

**Key patterns:**
- `ApolloClient` with cache and link configuration
- `InMemoryCache` for caching GraphQL data
- `from([...links])` chains multiple links
- Link order matters (context → tracing → error → auth → http)
- `useMemo` prevents client recreation
- Wrap app with `ApolloProvider`
- Custom links for auth, tracing, error handling
- Factory functions for links that need configuration

## Example 6: Error Link for Sentry Integration

**File**: `app/spaces/deliveries/modules/past-deliveries/experiments/graphql/utils/graphql/links/error.ts`

This example shows creating a custom error link for error tracking.

```typescript
import { onError } from '@apollo/client/link/error';

import { getFileClaim } from '@/libs/governance';
import { captureSentryError } from '@/libs/sentry';

const errorLink = onError(
  ({ networkError, operation: { operationName, getContext } }) => {
    if (networkError) {
      const { claim } = getContext();

      captureSentryError(claim || getFileClaim(), networkError, {
        tags: { type: 'graphql', queryName: operationName },
      });
    }
  }
);

export default errorLink;
```

**Key patterns:**
- `onError` from @apollo/client/link/error
- Destructure `networkError` and `operation`
- Access operation context via `getContext()`
- Send errors to Sentry with metadata
- Tag errors with query/mutation name
- Handle network errors separately from GraphQL errors

## Example 7: Tracer Link for OpenTelemetry

**File**: `app/spaces/deliveries/modules/past-deliveries/experiments/graphql/utils/graphql/links/tracer.ts`

This example demonstrates creating a custom link for tracing.

```typescript
import { ApolloLink, Observable } from '@apollo/client';

const tracerLink = new ApolloLink((operation, forward) => {
  return new Observable((observer) => {
    const { getContext, operationName } = operation;
    const context = getContext();

    const span = context.tracer?.startSpan('graphql.query');
    span?.setAttributes({
      'graphql.query-key': operationName,
    });

    const observable = forward(operation);
    const subscription = observable.subscribe({
      next(value) {
        observer.next(value);
      },
      error(networkError) {
        const errors = networkError?.result?.errors;

        span?.setAttributes({
          'graphql.statusCode': networkError?.statusCode,
          'graphql.error.name': networkError?.name,
          'graphql.error.message': networkError?.message,
          'graphql.error.errors': errors ? JSON.stringify(errors) : undefined,
          'graphql.error.bodyText': networkError?.bodyText,
        });

        span?.end();
        observer.error(networkError);
      },
      complete() {
        span?.end();
        observer.complete();
      },
    });

    return () => subscription.unsubscribe();
  });
});

export default tracerLink;
```

**Key patterns:**
- Custom `ApolloLink` with Observable
- `forward(operation)` passes request to next link
- Start span before request
- End span on complete or error
- Set span attributes for debugging
- Subscribe to observable for lifecycle hooks
- Return unsubscribe function for cleanup

## Common Anti-Patterns

### ❌ Not Using Code Generation

```typescript
// DON'T: Import gql from @apollo/client
import { gql } from '@apollo/client';

const query = gql`
  query GetUser {
    user { id name }
  }
`;

// DO: Use generated gql from codegen
import { gql } from './graphql';

const query = gql(`
  query GetUser {
    user { id name }
  }
`);
```

### ❌ Not Using skip for Conditional Queries

```typescript
// DON'T: Conditionally call useQuery
const MyComponent = ({ userId }) => {
  if (!userId) return null;

  const { data } = useQuery(userQuery, {
    variables: { userId },
  });
};

// DO: Use skip option
const MyComponent = ({ userId }) => {
  const { data } = useQuery(userQuery, {
    variables: { userId },
    skip: !userId,
  });

  if (!userId) return null;
  // ...
};
```

### ❌ Not Handling Loading and Error States

```typescript
// DON'T: Ignore loading and error
const { data } = useQuery(myQuery);

return <div>{data?.user?.name}</div>;

// DO: Handle all states
const { data, loading, error } = useQuery(myQuery);

if (loading) return <Spinner />;
if (error) return <Error message={error.message} />;

return <div>{data?.user?.name}</div>;
```

### ❌ Not Using Optimistic Updates

```typescript
// DON'T: Wait for server response
const [updateUser] = useMutation(updateUserMutation);

// UI updates slowly after mutation completes

// DO: Use optimistic response
const [updateUser] = useMutation(updateUserMutation, {
  optimisticResponse: (variables) => ({
    updateUser: {
      __typename: 'User',
      id: variables.id,
      name: variables.name,
    },
  }),
});

// UI updates instantly
```

## Summary

The YourCompany web codebase uses @apollo/client v3.9.2 with these patterns:

1. **Code generation** - Use generated `gql` tag for type safety
2. **Cursor pagination** - `pageInfo` with `endCursor` and `hasNextPage`
3. **Custom hooks** - Wrap useQuery/useMutation for enhanced API
4. **Skip option** - Conditional query execution
5. **Custom links** - Error tracking, tracing, authentication
6. **Link chaining** - `from([...links])` for middleware pipeline
7. **Cache updates** - `update` function and `cache.modify`
8. **Optimistic updates** - Instant UI feedback before server response
9. **Error handling** - Sentry integration via error link
10. **OpenTelemetry** - Custom tracer link for observability

**Key Libraries:**
- @apollo/client v3.9.2
- @graphql-codegen for type generation
- TypeScript 5.7.3

**Important patterns:**
- Import `gql` from generated code, not @apollo/client
- Always handle `loading` and `error` states
- Use `skip` for conditional queries
- Chain links in correct order: context → trace → error → auth → http

For Apollo Client v3 documentation, see: https://www.apollographql.com/docs/react/v3
