# GraphQL Apollo Patterns - API Reference

**Version**: @apollo/client v3.9.2

## Official Documentation

- **Apollo Client**: https://www.apollographql.com/docs/react/
- **Apollo Client API**: https://www.apollographql.com/docs/react/api/react/hooks
- **GraphQL**: https://graphql.org/learn/

## Import Statements

```typescript
import {
  ApolloClient,
  ApolloProvider,
  InMemoryCache,
  useQuery,
  useMutation,
  useLazyQuery,
  gql,
} from '@apollo/client';
import { from } from '@apollo/client/link/core';
```

## ApolloClient

Create and configure Apollo Client instance.

```typescript
new ApolloClient({
  cache: InMemoryCache;
  link: ApolloLink;
  defaultOptions?: DefaultOptions;
});
```

**Usage:**
```typescript
const client = new ApolloClient({
  cache: new InMemoryCache(),
  link: httpLink,
  defaultOptions: {
    watchQuery: {
      fetchPolicy: 'cache-and-network',
    },
  },
});
```

## ApolloProvider

Wrap app to provide Apollo Client to components.

```typescript
<ApolloProvider client={client}>
  {children}
</ApolloProvider>
```

## useQuery()

Execute GraphQL query and return data, loading, error states.

```typescript
function useQuery<TData, TVariables>(
  query: DocumentNode,
  options?: QueryHookOptions<TData, TVariables>
): QueryResult<TData, TVariables>;

interface QueryResult<TData, TVariables> {
  data?: TData;
  loading: boolean;
  error?: ApolloError;
  refetch: (variables?: TVariables) => Promise<ApolloQueryResult<TData>>;
  fetchMore: (options: FetchMoreOptions<TVariables, TData>) => Promise<ApolloQueryResult<TData>>;
  networkStatus: NetworkStatus;
  called: boolean;
}
```

**Options:**
```typescript
interface QueryHookOptions<TData, TVariables> {
  variables?: TVariables;
  skip?: boolean;
  fetchPolicy?: FetchPolicy;
  errorPolicy?: ErrorPolicy;
  pollInterval?: number;
  notifyOnNetworkStatusChange?: boolean;
  context?: Record<string, any>;
  onCompleted?: (data: TData) => void;
  onError?: (error: ApolloError) => void;
}
```

**Usage:**
```typescript
const { data, loading, error, refetch } = useQuery(GET_USER, {
  variables: { id: '123' },
  skip: !id,
  fetchPolicy: 'cache-first',
  onCompleted: (data) => console.log('Loaded:', data),
});
```

## useMutation()

Execute GraphQL mutation for create, update, delete operations.

```typescript
function useMutation<TData, TVariables>(
  mutation: DocumentNode,
  options?: MutationHookOptions<TData, TVariables>
): MutationTuple<TData, TVariables>;

type MutationTuple<TData, TVariables> = [
  mutateFunction: (options?: MutationFunctionOptions<TData, TVariables>) => Promise<FetchResult<TData>>,
  result: MutationResult<TData>
];

interface MutationResult<TData> {
  data?: TData;
  loading: boolean;
  error?: ApolloError;
  called: boolean;
  reset: () => void;
}
```

**Options:**
```typescript
interface MutationHookOptions<TData, TVariables> {
  variables?: TVariables;
  refetchQueries?: Array<string | DocumentNode>;
  awaitRefetchQueries?: boolean;
  update?: MutationUpdaterFn<TData>;
  onCompleted?: (data: TData) => void;
  onError?: (error: ApolloError) => void;
  context?: Record<string, any>;
}
```

**Usage:**
```typescript
const [createUser, { data, loading, error }] = useMutation(CREATE_USER, {
  onCompleted: (data) => console.log('Created:', data),
  onError: (error) => console.error('Error:', error),
  refetchQueries: ['GetUsers'],
});

// Execute mutation
await createUser({
  variables: { name: 'John', email: 'john@example.com' },
});
```

## useLazyQuery()

Query that executes on demand, not on mount.

```typescript
function useLazyQuery<TData, TVariables>(
  query: DocumentNode,
  options?: LazyQueryHookOptions<TData, TVariables>
): QueryTuple<TData, TVariables>;

type QueryTuple<TData, TVariables> = [
  execute: (options?: QueryLazyOptions<TVariables>) => Promise<QueryResult<TData, TVariables>>,
  result: QueryResult<TData, TVariables>
];
```

**Usage:**
```typescript
const [loadUser, { data, loading, error }] = useLazyQuery(GET_USER);

// Execute when needed
const handleClick = () => {
  loadUser({ variables: { id: '123' } });
};
```

## gql

Parse GraphQL query/mutation strings into DocumentNode.

```typescript
const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      name
      email
    }
  }
`;

const CREATE_USER = gql`
  mutation CreateUser($name: String!, $email: String!) {
    createUser(input: { name: $name, email: $email }) {
      id
      name
      email
    }
  }
`;
```

## InMemoryCache

Apollo's normalized cache implementation.

```typescript
new InMemoryCache({
  typePolicies?: TypePolicies;
  possibleTypes?: PossibleTypesMap;
  dataIdFromObject?: (object: StoreObject) => string | undefined;
});
```

**Usage:**
```typescript
const cache = new InMemoryCache({
  typePolicies: {
    Query: {
      fields: {
        pastDeliveries: {
          keyArgs: ['locale', 'country', 'subscriptionID'],
          merge(existing = [], incoming) {
            return [...existing, ...incoming];
          },
        },
      },
    },
  },
});
```

## Apollo Links

Chainable middleware for requests.

### HttpLink

```typescript
import { createHttpLink } from '@apollo/client';

const httpLink = createHttpLink({
  uri: 'https://api.example.com/graphql',
  credentials: 'include',
});
```

### from()

Chain multiple links together.

```typescript
import { from } from '@apollo/client/link/core';

const link = from([
  authLink,
  errorLink,
  tracerLink,
  httpLink,
]);
```

### Custom Link

```typescript
import { ApolloLink } from '@apollo/client';

const authLink = new ApolloLink((operation, forward) => {
  operation.setContext(({ headers = {} }) => ({
    headers: {
      ...headers,
      authorization: `Bearer ${token}`,
    },
  }));

  return forward(operation);
});
```

## Fetch Policies

Control cache behavior.

```typescript
type FetchPolicy =
  | 'cache-first'      // Check cache first, network if miss (default)
  | 'cache-and-network' // Check cache + network, update cache
  | 'network-only'     // Always network, update cache
  | 'no-cache'         // Always network, don't update cache
  | 'cache-only';      // Only cache, never network
```

**Usage:**
```typescript
const { data } = useQuery(GET_USER, {
  fetchPolicy: 'cache-first',
});
```

## Error Policies

Control error handling.

```typescript
type ErrorPolicy =
  | 'none'         // Treat GraphQL errors as runtime errors
  | 'ignore'       // Ignore GraphQL errors, return data
  | 'all';         // Return both data and errors
```

**Usage:**
```typescript
const { data, error } = useQuery(GET_USER, {
  errorPolicy: 'all',
});
```

## Pagination

### fetchMore()

Fetch additional pages of data.

```typescript
const { data, fetchMore } = useQuery(GET_DELIVERIES, {
  variables: { first: 10 },
});

const loadMore = async () => {
  await fetchMore({
    variables: {
      after: data.deliveries.pageInfo.endCursor,
    },
  });
};
```

### Type Policies for Pagination

```typescript
const cache = new InMemoryCache({
  typePolicies: {
    Query: {
      fields: {
        deliveries: {
          keyArgs: ['subscriptionID'],
          merge(existing, incoming, { args }) {
            if (!existing) return incoming;

            const edges = existing.edges ? existing.edges.slice(0) : [];
            if (incoming.edges) {
              edges.push(...incoming.edges);
            }

            return {
              ...incoming,
              edges,
            };
          },
        },
      },
    },
  },
});
```

## Refetching

### refetch()

Re-execute query with same variables.

```typescript
const { data, refetch } = useQuery(GET_USER, {
  variables: { id: '123' },
});

const handleRefresh = async () => {
  await refetch();
};
```

### refetchQueries

Refetch queries after mutation.

```typescript
const [createUser] = useMutation(CREATE_USER, {
  refetchQueries: ['GetUsers', 'GetAllUsers'],
  awaitRefetchQueries: true,
});
```

## Network Status

Track detailed query state.

```typescript
enum NetworkStatus {
  loading = 1,
  setVariables = 2,
  fetchMore = 3,
  refetch = 4,
  poll = 6,
  ready = 7,
  error = 8,
}
```

**Usage:**
```typescript
const { data, networkStatus } = useQuery(GET_USER, {
  notifyOnNetworkStatusChange: true,
});

const isRefetching = networkStatus === NetworkStatus.refetch;
```

## ApolloError

Error object returned by queries and mutations.

```typescript
interface ApolloError extends Error {
  graphQLErrors: ReadonlyArray<GraphQLError>;
  networkError: Error | null;
  message: string;
  extraInfo: any;
}
```

**Usage:**
```typescript
const { error } = useQuery(GET_USER);

if (error) {
  if (error.networkError) {
    console.error('Network error:', error.networkError);
  }
  if (error.graphQLErrors.length > 0) {
    console.error('GraphQL errors:', error.graphQLErrors);
  }
}
```

## Common Patterns

### Conditional Query

```typescript
const { data, loading } = useQuery(GET_USER, {
  variables: { id },
  skip: !id,
});
```

### Polling

```typescript
const { data } = useQuery(GET_NOTIFICATIONS, {
  pollInterval: 5000, // Poll every 5 seconds
});
```

### Query with Callback

```typescript
const { data } = useQuery(GET_USER, {
  onCompleted: (data) => {
    console.log('User loaded:', data.user);
  },
  onError: (error) => {
    console.error('Failed to load user:', error);
  },
});
```

### Mutation with Cache Update

```typescript
const [createUser] = useMutation(CREATE_USER, {
  update(cache, { data }) {
    const existingUsers = cache.readQuery({ query: GET_USERS });

    cache.writeQuery({
      query: GET_USERS,
      data: {
        users: [...existingUsers.users, data.createUser],
      },
    });
  },
});
```

## Best Practices

1. **Use gql tag**: Parse queries at build time for type checking
2. **Set fetchPolicy**: Choose appropriate caching strategy
3. **Handle errors**: Use onError callbacks or error boundaries
4. **Use skip**: Conditionally execute queries
5. **Normalize cache**: Use keyArgs and merge functions for pagination
6. **Chain links**: Use middleware for auth, tracing, error handling
