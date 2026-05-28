---
name: graphql-apollo-patterns
description: "WHAT: Apollo Client v3.9.2 patterns for web GraphQL data fetching. WHEN: using useQuery, useMutation, managing cache, implementing pagination. KEYWORDS: apollo, graphql, useQuery, useMutation, cache, fetchMore, fetchPolicy, web, tracing."
---

# GraphQL Apollo Patterns - Web

GraphQL data fetching patterns using @apollo/client v3.9.2 for React web applications.

## Documentation

This skill has comprehensive documentation:

- **[Production Examples](./references/examples.md)** - Real-world code examples from the codebase
- **[API Reference](./references/api-docs.md)** - Complete API documentation with official links
- **[Implementation Patterns](./references/patterns.md)** - Best practices and anti-patterns

## When to Use

Use Apollo Client for:
- GraphQL API integration
- Complex data requirements with nested relationships
- Real-time subscriptions
- Normalized caching across queries
- Optimistic UI updates

**Don't use Apollo Client for:**
- REST APIs (use react-query instead)
- Simple data fetching (react-query is lighter)

## Core Principles

### 1. Apollo Provider Setup

**Wrap your app with ApolloProvider and configure the client.**

✅ **Good:**
```typescript
// app/spaces/deliveries/modules/past-deliveries/experiments/graphql/utils/graphql/GraphQLProvider.tsx:1
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
}: React.PropsWithChildren<{ uri?: string }>) => {
  const claim = useClaim();
  const tracer = useClientTracer();

  const client = useMemo(
    () => generateClient(claim, tracer, uri),
    [claim, tracer, uri]
  );

  return <ApolloProvider client={client}>{children}</ApolloProvider>;
};
```

**Why:** Apollo Link chain allows middleware for auth, tracing, and error handling. Memoizing the client prevents unnecessary recreations.

### 2. useQuery Hook

**Use useQuery for fetching data from GraphQL queries.**

✅ **Good:**
```typescript
// app/spaces/deliveries/modules/past-deliveries/experiments/graphql/hooks/useGraphQLPastDeliveries.ts:1
import { useQuery } from '@apollo/client';

import { useSelectedLocale } from '@/libs/locale';
import { useSystemCountry } from '@/libs/system-country';

import { pastDeliveriesQuery } from '../utils/gql-data-access/past-deliveries';

export const useGraphQLPastDeliveries = () => {
  const { current } = useSubscriptions();

  const locale = useSelectedLocale();
  const country = useSystemCountry();

  const queryResult = useQuery(pastDeliveriesQuery, {
    variables: {
      locale: locale.toString(),
      country: country.toString(),
      subscriptionID: current?.id ?? '',
    },
    skip: !current?.id,
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
        /* Error handling */
      }
    },
  };
};
```

**Why:** useQuery handles loading, error, and data states automatically. The skip option prevents unnecessary queries.

### 3. useMutation Hook

**Use useMutation for GraphQL mutations (create, update, delete).**

✅ **Good:**
```typescript
// app/spaces/deliveries/modules/past-deliveries/hooks/useRate.ts:29
import { useMutation } from '@apollo/client';

import { rateMutation } from '../experiments/graphql';

export const useRate = ({ recipe, menuId, week }: Props) => {
  const [rateGraphQL] = useMutation(rateMutation, {
    // Error handler to prevent unhandled errors
    onError: () => {},
  });

  const onRate = async (rating: number) => {
    try {
      await rateGraphQL({
        variables: {
          rating,
          recipeId: recipe?.id,
          menuId,
          week,
        },
      });
    } catch (error) {
      // Handle error
    }
  };

  return { onRate };
};
```

**Why:** useMutation returns a function to trigger the mutation. The onError callback allows centralized error handling.

### 4. Pagination with fetchMore

**Use fetchMore for cursor-based pagination.**

✅ **Good:**
```typescript
// app/spaces/deliveries/modules/past-deliveries/experiments/graphql/hooks/useGraphQLPastDeliveries.ts:30
const queryResult = useQuery(pastDeliveriesQuery, {
  variables: { locale, country, subscriptionID },
});

const fetchNextGraphQLPage = async () => {
  try {
    await queryResult.fetchMore({
      variables: {
        after: queryResult.data?.pastDeliveries?.pageInfo?.endCursor,
      },
    });
  } catch {
    /* Error handling */
  }
};
```

**Why:** fetchMore automatically merges new data with existing cache, handling pagination seamlessly.

### 5. Conditional Queries

**Use skip option to conditionally execute queries.**

✅ **Good:**
```typescript
const { data, loading } = useQuery(pastDeliveriesQuery, {
  variables: { subscriptionID },
  skip: !subscriptionID, // Don't run query if no subscription
});
```

❌ **Bad:**
```typescript
// Don't conditionally call useQuery
if (subscriptionID) {
  const { data } = useQuery(pastDeliveriesQuery, { variables: { subscriptionID } });
}
```

**Why:** Hooks must be called unconditionally. Use skip to control execution.

## Query Options

### Common Options

```typescript
useQuery(query, {
  variables: { id: '123' },
  skip: !id,                    // Skip if condition not met
  fetchPolicy: 'cache-first',    // Default: check cache first
  pollInterval: 5000,            // Poll every 5 seconds
  notifyOnNetworkStatusChange: true, // Update loading on refetch
  onCompleted: (data) => {},     // Called on success
  onError: (error) => {},        // Called on error
});
```

### Fetch Policies

```typescript
// cache-first (default) - Check cache, then network
fetchPolicy: 'cache-first'

// network-only - Always fetch from network
fetchPolicy: 'network-only'

// cache-only - Only use cache, never network
fetchPolicy: 'cache-only'

// no-cache - Fetch from network, don't update cache
fetchPolicy: 'no-cache'

// cache-and-network - Use cache, then refetch
fetchPolicy: 'cache-and-network'
```

## Mutation Options

### Common Options

```typescript
useMutation(mutation, {
  variables: { id: '123' },
  onCompleted: (data) => {},        // Success callback
  onError: (error) => {},           // Error callback
  refetchQueries: ['GetPastDeliveries'], // Refetch after mutation
  update: (cache, { data }) => {    // Manual cache update
    cache.modify({
      fields: {
        pastDeliveries(existing) {
          return [data.newDelivery, ...existing];
        }
      }
    });
  },
  optimisticResponse: {             // Optimistic UI
    rateRecipe: {
      __typename: 'Recipe',
      id: recipeId,
      rating: newRating,
    }
  },
});
```

## Cache Management

### Reading from Cache

```typescript
import { useApolloClient } from '@apollo/client';

const client = useApolloClient();

// Read query
const data = client.readQuery({
  query: pastDeliveriesQuery,
  variables: { subscriptionID },
});

// Read fragment
const recipe = client.readFragment({
  id: 'Recipe:123',
  fragment: gql`
    fragment RecipeData on Recipe {
      id
      name
      rating
    }
  `,
});
```

### Writing to Cache

```typescript
// Write query
client.writeQuery({
  query: pastDeliveriesQuery,
  data: { pastDeliveries: [...] },
});

// Write fragment
client.writeFragment({
  id: 'Recipe:123',
  fragment: gql`
    fragment RecipeData on Recipe {
      id
      rating
    }
  `,
  data: {
    rating: 5,
  },
});
```

## Error Handling

### Query Errors

```typescript
const { data, loading, error } = useQuery(query);

if (error) {
  return <div>Error: {error.message}</div>;
}
```

### Mutation Errors

```typescript
const [mutate, { error }] = useMutation(mutation, {
  onError: (error) => {
    console.error('Mutation failed:', error);
  },
});

try {
  await mutate({ variables: { ... } });
} catch (error) {
  // Handle error
}
```

## File Organization

```
graphql/
├── hooks/
│   ├── useGraphQLPastDeliveries.ts  # Query hooks
│   └── useGraphQLEnabled.ts         # Feature flags
├── utils/
│   ├── gql-data-access/
│   │   └── past-deliveries.ts       # Query definitions
│   └── graphql/
│       ├── GraphQLProvider.tsx      # Provider setup
│       └── links/                   # Apollo Links
│           ├── auth.ts
│           ├── error.ts
│           ├── tracer.ts
│           └── http-factory.ts
└── index.ts
```

## Common Mistakes

1. **Calling useQuery conditionally** - Use skip option instead
2. **Not handling errors** - Always provide onError or check error state
3. **Forgetting to memoize client** - Client recreation causes unnecessary rerenders
4. **Not using TypeScript** - Apollo works best with generated types
5. **Overusing fetchPolicy: 'network-only'** - Defeats caching benefits

## Quick Reference

### Basic Query

```typescript
import { useQuery, gql } from '@apollo/client';

const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      name
      email
    }
  }
`;

function User({ id }) {
  const { data, loading, error } = useQuery(GET_USER, {
    variables: { id },
  });

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return <div>{data.user.name}</div>;
}
```

### Basic Mutation

```typescript
import { useMutation, gql } from '@apollo/client';

const UPDATE_USER = gql`
  mutation UpdateUser($id: ID!, $name: String!) {
    updateUser(id: $id, name: $name) {
      id
      name
    }
  }
`;

function UpdateUserButton() {
  const [updateUser, { loading }] = useMutation(UPDATE_USER);

  return (
    <button
      onClick={() => updateUser({ variables: { id: '1', name: 'New Name' } })}
      disabled={loading}
    >
      Update User
    </button>
  );
}
```

### With Provider

```typescript
import { ApolloClient, InMemoryCache, ApolloProvider } from '@apollo/client';

const client = new ApolloClient({
  uri: 'https://api.example.com/graphql',
  cache: new InMemoryCache(),
});

function App() {
  return (
    <ApolloProvider client={client}>
      <YourApp />
    </ApolloProvider>
  );
}
```
