# Apollo Client API Reference

**Version**: 3.13.6

## Official Documentation

- **Queries**: https://www.apollographql.com/docs/react/data/queries
- **Mutations**: https://www.apollographql.com/docs/react/data/mutations
- **Fragments**: https://www.apollographql.com/docs/react/data/fragments
- **Error Handling**: https://www.apollographql.com/docs/react/data/error-handling
- **Testing**: https://www.apollographql.com/docs/react/development-testing/testing

## Core Hooks

### useQuery

Execute GraphQL queries and manage loading/error states.

```typescript
const { data, loading, error, refetch, fetchMore } = useQuery(QUERY, {
  variables: { id: '123' },
  fetchPolicy: 'cache-first',
  errorPolicy: 'all',
  pollInterval: 5000,
  skip: false,
  onCompleted: (data) => {},
  onError: (error) => {},
});
```

**Key Options**:
- `variables` - Query variables object
- `fetchPolicy` - `cache-first` | `cache-and-network` | `network-only` | `cache-only` | `no-cache`
- `errorPolicy` - `none` | `all` | `ignore`
- `pollInterval` - Polling interval in milliseconds
- `skip` - Skip query execution if true
- `notifyOnNetworkStatusChange` - Re-render on network status changes

**Return Values**:
- `data` - Query result data
- `loading` - Loading state boolean
- `error` - ApolloError object
- `refetch()` - Function to re-execute query
- `fetchMore()` - Function for pagination
- `networkStatus` - Detailed network status
- `called` - Whether query has been called

### useMutation

Execute GraphQL mutations with optimistic updates.

```typescript
const [mutate, { data, loading, error, reset }] = useMutation(MUTATION, {
  variables: { input: {} },
  refetchQueries: [{ query: GET_ITEMS }],
  awaitRefetchQueries: true,
  onCompleted: (data) => {},
  onError: (error) => {},
  optimisticResponse: {},
  update: (cache, { data }) => {},
});

// Execute mutation
mutate({ variables: { id: '123' } });
```

**Key Options**:
- `variables` - Mutation variables
- `refetchQueries` - Queries to refetch after mutation
- `awaitRefetchQueries` - Wait for refetch before resolving
- `onCompleted` - Success callback
- `onError` - Error callback
- `optimisticResponse` - Optimistic UI data
- `update` - Manual cache update function
- `errorPolicy` - Error handling policy

**Return Values**:
- `mutate()` - Function to execute mutation
- `data` - Mutation result data
- `loading` - Loading state
- `error` - ApolloError object
- `called` - Whether mutation has been called
- `reset()` - Reset mutation state

### useFragment

Read fragment data from Apollo cache.

```typescript
const { data, complete } = useFragment({
  fragment: FRAGMENT,
  fragmentName: 'RecipeFragment',
  from: { __typename: 'Recipe', id: '123' },
});
```

**Key Options**:
- `fragment` - GraphQL fragment document
- `fragmentName` - Name of fragment to read
- `from` - Cache identifier object

**Return Values**:
- `data` - Fragment data from cache
- `complete` - Whether all fragment fields are cached

## Error Handling

### ApolloError

```typescript
interface ApolloError {
  message: string;
  graphQLErrors: ReadonlyArray<GraphQLError>;
  networkError: Error | null;
  extraInfo: any;
}
```

### Error Policies

- **`none`** (default) - Errors throw, no partial data returned
- **`all`** - Both errors and partial data returned
- **`ignore`** - Errors ignored, only partial data returned

## Cache Operations

### Cache.writeFragment

```typescript
client.cache.writeFragment({
  id: 'Recipe:123',
  fragment: RECIPE_FRAGMENT,
  data: { id: '123', title: 'New Title' },
});
```

### Cache.readFragment

```typescript
const recipe = client.cache.readFragment({
  id: 'Recipe:123',
  fragment: RECIPE_FRAGMENT,
});
```

### Cache.modify

```typescript
client.cache.modify({
  id: 'Recipe:123',
  fields: {
    title: () => 'New Title',
  },
});
```

## Network Status Values

```typescript
enum NetworkStatus {
  loading = 1,        // Initial load
  setVariables = 2,   // Variables changed
  fetchMore = 3,      // Fetching more data
  refetch = 4,        // Refetching
  poll = 6,           // Polling
  ready = 7,          // Query ready
  error = 8,          // Query error
}
```

## Testing Utilities

### MockedProvider

```typescript
import { MockedProvider } from '@apollo/client/testing';

const mocks = [
  {
    request: { query: GET_RECIPE, variables: { id: '123' } },
    result: { data: { recipe: { id: '123', title: 'Test' } } },
  },
];

<MockedProvider mocks={mocks} addTypename={false}>
  <Component />
</MockedProvider>
```

## Common Patterns

### Refetch After Mutation

```typescript
const [deleteRecipe] = useMutation(DELETE_RECIPE, {
  refetchQueries: [{ query: GET_RECIPES }],
  awaitRefetchQueries: true,
});
```

### Optimistic Updates

```typescript
const [updateRecipe] = useMutation(UPDATE_RECIPE, {
  optimisticResponse: {
    updateRecipe: {
      __typename: 'Recipe',
      id: '123',
      title: 'Optimistic Title',
    },
  },
});
```

### Manual Cache Updates

```typescript
const [createRecipe] = useMutation(CREATE_RECIPE, {
  update: (cache, { data: { createRecipe } }) => {
    const existing = cache.readQuery({ query: GET_RECIPES });
    cache.writeQuery({
      query: GET_RECIPES,
      data: { recipes: [...existing.recipes, createRecipe] },
    });
  },
});
```

### Fragment Composition

```typescript
const RECIPE_FRAGMENT = gql`
  fragment RecipeFields on Recipe {
    id
    title
    servings
    ...IngredientFields
  }
`;

const GET_RECIPE = gql`
  query GetRecipe($id: ID!) {
    recipe(id: $id) {
      ...RecipeFields
    }
  }
  ${RECIPE_FRAGMENT}
`;
```

## Version-Specific Features

**Apollo Client 3.13.6**:
- Enhanced TypeScript support
- Improved error handling with `errorPolicy`
- Fragment masking for better type safety
- Network status tracking
- Suspense support (experimental)

## Key Considerations

- Always define fragments for reusable field sets
- Use `errorPolicy: 'all'` for partial data with errors
- Leverage `refetchQueries` instead of manual cache updates when possible
- Use `optimisticResponse` for better UX
- Test with `MockedProvider` for isolated component tests
- Prefer `useFragment` over `readFragment` for reactive updates
