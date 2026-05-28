# GraphQL Apollo Patterns - Implementation Patterns

Implementation patterns and anti-patterns for Apollo Client v3.9.2.

## Pattern: Use skip for Conditional Queries

Use skip option instead of conditional hook calls.

✅ **Good:**
```typescript
import { useQuery } from '@apollo/client';

function UserProfile({ userId }: { userId?: string }) {
  const { data, loading } = useQuery(GET_USER, {
    variables: { id: userId },
    skip: !userId, // Skip query if no userId
  });

  if (!userId) return <div>No user selected</div>;
  if (loading) return <div>Loading...</div>;

  return <div>{data?.user?.name}</div>;
}
```

❌ **Bad:**
```typescript
// Don't conditionally call hooks
function UserProfile({ userId }: { userId?: string }) {
  if (!userId) {
    return <div>No user selected</div>;
  }

  // Breaks Rules of Hooks!
  const { data, loading } = useQuery(GET_USER, {
    variables: { id: userId },
  });

  return <div>{data?.user?.name}</div>;
}
```

**Why:** Hooks must be called unconditionally:
- React requires consistent hook order
- Use `skip` to control execution
- Prevents "rendered fewer hooks" errors

## Pattern: Handle Loading and Error States

Always handle loading and error states explicitly.

✅ **Good:**
```typescript
const { data, loading, error } = useQuery(GET_USER, {
  variables: { id },
});

if (loading) return <Spinner />;
if (error) return <Error message={error.message} />;
if (!data) return <div>No data</div>;

return <UserCard user={data.user} />;
```

❌ **Bad:**
```typescript
const { data } = useQuery(GET_USER, {
  variables: { id },
});

// Crashes if loading or error
return <UserCard user={data.user} />;
```

**Why:** Three-state pattern:
- Prevents crashes
- Better UX with loading states
- Clear error handling
- Type-safe data access

## Pattern: Use onCompleted and onError Callbacks

Use callbacks for side effects on query completion.

✅ **Good:**
```typescript
const { data } = useQuery(GET_USER, {
  variables: { id },
  onCompleted: (data) => {
    console.log('User loaded:', data.user);
    trackEvent('user_loaded', { userId: data.user.id });
  },
  onError: (error) => {
    console.error('Failed to load user:', error);
    trackError('user_load_failed', error);
  },
});
```

❌ **Bad:**
```typescript
const { data, error } = useQuery(GET_USER, {
  variables: { id },
});

// Side effects in render
if (data) {
  trackEvent('user_loaded', { userId: data.user.id });
}
if (error) {
  trackError('user_load_failed', error);
}
```

**Why:** Callbacks:
- Run once on completion
- Don't run on every render
- Cleaner side effect handling
- Prevent duplicate tracking

## Pattern: Use fetchMore for Pagination

Use fetchMore to load additional pages.

✅ **Good:**
```typescript
const { data, fetchMore } = useQuery(GET_DELIVERIES, {
  variables: { first: 10, after: null },
});

const loadMore = async () => {
  await fetchMore({
    variables: {
      after: data?.deliveries?.pageInfo?.endCursor,
    },
  });
};

return (
  <div>
    {data?.deliveries?.edges?.map((edge) => (
      <DeliveryCard key={edge.node.id} delivery={edge.node} />
    ))}
    {data?.deliveries?.pageInfo?.hasNextPage && (
      <button onClick={loadMore}>Load More</button>
    )}
  </div>
);
```

❌ **Bad:**
```typescript
// Don't manually manage pagination
const [page, setPage] = useState(1);

const { data } = useQuery(GET_DELIVERIES, {
  variables: { page },
});

// Loses previous data on page change
return (
  <div>
    {data?.deliveries?.map((delivery) => (
      <DeliveryCard key={delivery.id} delivery={delivery} />
    ))}
    <button onClick={() => setPage(page + 1)}>Next Page</button>
  </div>
);
```

**Why:** `fetchMore`:
- Automatically merges data
- Preserves existing items
- Cursor-based pagination
- Better UX

## Pattern: useMutation with Refetch

Refetch queries after mutation to update UI.

✅ **Good:**
```typescript
const [createUser] = useMutation(CREATE_USER, {
  refetchQueries: ['GetUsers'],
  awaitRefetchQueries: true,
  onCompleted: () => {
    showNotification('User created successfully');
  },
});

const handleSubmit = async (formData) => {
  try {
    await createUser({
      variables: { input: formData },
    });
  } catch (error) {
    showError('Failed to create user');
  }
};
```

❌ **Bad:**
```typescript
const [createUser] = useMutation(CREATE_USER);
const { refetch } = useQuery(GET_USERS);

const handleSubmit = async (formData) => {
  await createUser({
    variables: { input: formData },
  });

  // Manual refetch
  await refetch();
};
```

**Why:** `refetchQueries`:
- Automatic cache updates
- No manual refetch needed
- Consistent data
- Less error-prone

## Pattern: Configure Cache Merge Functions

Set up merge functions for paginated queries.

✅ **Good:**
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

❌ **Bad:**
```typescript
// No merge function - overwrites existing data
const cache = new InMemoryCache();
```

**Why:** Merge functions:
- Append new pages correctly
- Preserve existing data
- Handle pagination properly
- Prevent data loss

## Pattern: Chain Apollo Links

Use link chain for middleware (auth, tracing, errors).

✅ **Good:**
```typescript
import { from } from '@apollo/client/link/core';

const link = from([
  authLink,      // Add authorization header
  tracerLink,    // OpenTelemetry tracing
  errorLink,     // Centralized error handling
  platformLink,  // Platform-specific headers
  httpLink,      // HTTP transport
]);

const client = new ApolloClient({
  cache: new InMemoryCache(),
  link,
});
```

❌ **Bad:**
```typescript
// No middleware, just HTTP link
const client = new ApolloClient({
  cache: new InMemoryCache(),
  link: createHttpLink({ uri: '/graphql' }),
});
```

**Why:** Link chain:
- Separation of concerns
- Reusable middleware
- Centralized logic
- Better maintainability

## Pattern: Memoize Apollo Client

Memoize client to prevent recreations.

✅ **Good:**
```typescript
export const GraphQLProvider = ({ children }: Props) => {
  const claim = useClaim();
  const tracer = useClientTracer();

  const client = useMemo(
    () => generateClient(claim, tracer),
    [claim, tracer]
  );

  return <ApolloProvider client={client}>{children}</ApolloProvider>;
}
```

❌ **Bad:**
```typescript
export const GraphQLProvider = ({ children }: Props) => {
  const claim = useClaim();
  const tracer = useClientTracer();

  // New client on every render!
  const client = generateClient(claim, tracer);

  return <ApolloProvider client={client}>{children}</ApolloProvider>;
}
```

**Why:** Memoization:
- Prevents client recreations
- Preserves cache
- Better performance
- Stable client reference

## Pattern: Use Appropriate Fetch Policy

Choose fetch policy based on data freshness needs.

✅ **Good:**
```typescript
// Frequently changing data - always fresh
const { data } = useQuery(GET_NOTIFICATIONS, {
  fetchPolicy: 'network-only',
  pollInterval: 5000,
});

// Rarely changing data - cache first
const { data } = useQuery(GET_USER_PROFILE, {
  fetchPolicy: 'cache-first',
});

// Critical fresh data - cache + network
const { data } = useQuery(GET_CART, {
  fetchPolicy: 'cache-and-network',
});
```

❌ **Bad:**
```typescript
// Always network-only (slow)
const { data } = useQuery(GET_USER_PROFILE, {
  fetchPolicy: 'network-only',
});

// Always cache-first for live data (stale)
const { data } = useQuery(GET_NOTIFICATIONS, {
  fetchPolicy: 'cache-first',
});
```

**Why:** Fetch policies:
- Balance freshness and performance
- `cache-first` for static data
- `network-only` for live data
- `cache-and-network` for critical data

## Pattern: notifyOnNetworkStatusChange

Enable for loading states during refetch.

✅ **Good:**
```typescript
const { data, loading, networkStatus, refetch } = useQuery(GET_USER, {
  variables: { id },
  notifyOnNetworkStatusChange: true,
});

const isRefetching = networkStatus === NetworkStatus.refetch;

return (
  <div>
    {isRefetching && <RefreshIndicator />}
    {data && <UserCard user={data.user} />}
    <button onClick={() => refetch()}>Refresh</button>
  </div>
);
```

❌ **Bad:**
```typescript
const { data, loading, refetch } = useQuery(GET_USER, {
  variables: { id },
});

// loading is false during refetch
return (
  <div>
    {loading && <Spinner />}
    {data && <UserCard user={data.user} />}
    <button onClick={() => refetch()}>Refresh</button>
  </div>
);
```

**Why:** `notifyOnNetworkStatusChange`:
- Updates loading during refetch
- Better refetch UX
- Network status tracking
- More granular control

## Anti-Pattern: Calling Hooks Conditionally

Never call hooks conditionally.

❌ **Bad:**
```typescript
function Component({ shouldFetch }: Props) {
  if (shouldFetch) {
    // Breaks Rules of Hooks!
    const { data } = useQuery(GET_DATA);
  }

  return <div>...</div>;
}
```

✅ **Good:**
```typescript
function Component({ shouldFetch }: Props) {
  const { data } = useQuery(GET_DATA, {
    skip: !shouldFetch,
  });

  return <div>...</div>;
}
```

**Why:** Rules of Hooks:
- Must be called in same order
- Use `skip` for conditional execution
- Prevents React errors

## Anti-Pattern: Ignoring Errors

Don't ignore error states.

❌ **Bad:**
```typescript
const { data } = useQuery(GET_USER);

// Crashes if error
return <div>{data.user.name}</div>;
```

✅ **Good:**
```typescript
const { data, error, loading } = useQuery(GET_USER);

if (loading) return <Spinner />;
if (error) return <Error message={error.message} />;
if (!data) return null;

return <div>{data.user.name}</div>;
```

**Why:** Error handling:
- Prevents crashes
- Better UX
- Clear error messages
- Type safety

## Anti-Pattern: Not Handling Pagination

Don't lose previous data on pagination.

❌ **Bad:**
```typescript
const [page, setPage] = useState(1);

const { data } = useQuery(GET_ITEMS, {
  variables: { page },
});

// Loses previous pages!
return (
  <div>
    {data?.items?.map((item) => <Item key={item.id} item={item} />)}
    <button onClick={() => setPage(page + 1)}>Next</button>
  </div>
);
```

✅ **Good:**
```typescript
const { data, fetchMore } = useQuery(GET_ITEMS, {
  variables: { first: 10, after: null },
});

const loadMore = () => {
  fetchMore({
    variables: { after: data.items.pageInfo.endCursor },
  });
};

// Preserves previous pages
return (
  <div>
    {data?.items?.edges?.map((edge) => (
      <Item key={edge.node.id} item={edge.node} />
    ))}
    <button onClick={loadMore}>Load More</button>
  </div>
);
```

**Why:** `fetchMore`:
- Preserves existing data
- Cursor-based pagination
- Better UX
- Automatic merge

## Summary

**Key Patterns:**
- Use `skip` for conditional queries (NOT conditional hooks)
- Handle loading, error, and data states explicitly
- Use `onCompleted` and `onError` for side effects
- Use `fetchMore` for pagination
- Use `refetchQueries` after mutations
- Configure cache merge functions for pagination
- Chain Apollo Links for middleware
- Memoize Apollo Client
- Choose appropriate fetch policy
- Enable `notifyOnNetworkStatusChange` for refetch UX

**Anti-Patterns to Avoid:**
- Calling hooks conditionally
- Ignoring error states
- Not handling loading states
- Manual refetch instead of `refetchQueries`
- No merge functions for pagination
- Creating new client on every render
- Using wrong fetch policy
- Losing data on pagination
