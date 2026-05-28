# React Query Patterns

**Preferred approach for all new data fetching.** Use React Query for server state management.

## Table of Contents

1. [When to Use React Query](#when-to-use-react-query)
2. [Query Structure](#query-structure)
3. [Query Keys](#query-keys)
4. [Query Options](#query-options)
5. [Mutations](#mutations)
6. [Optimistic Updates](#optimistic-updates)
7. [Cache Management](#cache-management)

---

## When to Use React Query

Use React Query for:

- All API data fetching
- Server state that needs caching
- Data that multiple components consume
- Polling or real-time data
- Paginated or infinite scroll data

React Query provides:

- Automatic caching and deduplication
- Background refetching
- Loading/error states
- Optimistic updates
- Cache invalidation

---

## Query Structure

### Basic Query Hook

```javascript
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

const KEYS = {
  workouts: () => [ 'workouts' ],
  workout: ( id ) => [ 'workouts', id ],
};

const fetchWorkouts = async () => {
  const response = await axios.get( '/api/v1/workouts.json' );
  return response.data.data;
};

export const useWorkouts = ( { enabled = true } = {} ) => useQuery( {
  queryKey: KEYS.workouts(),
  queryFn: fetchWorkouts,
  enabled,
} );
```

### Query with Parameters

```javascript
const fetchWorkout = async ( id ) => {
  const response = await axios.get( `/api/v1/workouts/${id}.json` );
  return response.data.data;
};

export const useWorkout = ( { id, enabled = true } ) => useQuery( {
  queryKey: KEYS.workout( id ),
  queryFn: () => fetchWorkout( id ),
  enabled: enabled && Boolean( id ),
} );
```

### Dependent Queries

```javascript
export const useClientWorkouts = ( { clientId } ) => {
  // First query
  const clientQuery = useClient( { id: clientId } );

  // Dependent query - waits for client
  const workoutsQuery = useQuery( {
    queryKey: [ 'clients', clientId, 'workouts' ],
    queryFn: () => fetchClientWorkouts( clientId ),
    enabled: Boolean( clientQuery.data ),
  } );

  return {
    client: clientQuery.data,
    workouts: workoutsQuery.data,
    isLoading: clientQuery.isLoading || workoutsQuery.isLoading,
  };
};
```

---

## Query Keys

### Key Naming Conventions

```javascript
const KEYS = {
  // List queries
  workouts: () => [ 'workouts' ],
  clients: () => [ 'clients' ],

  // Single item queries
  workout: ( id ) => [ 'workouts', id ],
  client: ( id ) => [ 'clients', id ],

  // Filtered queries
  workoutsByClient: ( clientId ) => [ 'workouts', { clientId } ],
  workoutsByDate: ( date ) => [ 'workouts', { date } ],

  // Nested resources
  clientWorkouts: ( clientId ) => [ 'clients', clientId, 'workouts' ],
  workoutExercises: ( workoutId ) => [ 'workouts', workoutId, 'exercises' ],
};
```

### Key Hierarchy Benefits

```javascript
// Invalidate all workouts (list + all individual)
queryClient.invalidateQueries( { queryKey: [ 'workouts' ] } );

// Invalidate specific workout only
queryClient.invalidateQueries( { queryKey: KEYS.workout( workoutId ) } );

// Invalidate all client-related data
queryClient.invalidateQueries( { queryKey: [ 'clients', clientId ] } );
```

---

## Query Options

### Common Options

```javascript
export const useWorkouts = () => useQuery( {
  queryKey: KEYS.workouts(),
  queryFn: fetchWorkouts,

  // Cache time settings
  staleTime: 5 * 60 * 1000,      // 5 min - data considered fresh
  gcTime: 30 * 60 * 1000,        // 30 min - cache garbage collection

  // Refetch behavior
  refetchOnWindowFocus: true,    // default: true
  refetchOnMount: true,          // default: true
  refetchOnReconnect: true,      // default: true

  // Error handling
  retry: 3,                      // default: 3
  retryDelay: ( attempt ) => Math.min( 1000 * 2 ** attempt, 30000 ),
} );
```

### Stale Time Guidelines

| Data Type | staleTime | Example |
|-----------|-----------|---------|
| Real-time | 0 | Chat messages, notifications |
| Frequently changing | 30s - 1min | Dashboard stats |
| Moderately changing | 5min | User profiles, workouts |
| Rarely changing | Infinity | Static config, exercise library |

```javascript
// Static data - never refetch automatically
export const useExerciseLibrary = () => useQuery( {
  queryKey: [ 'exercises', 'library' ],
  queryFn: fetchExerciseLibrary,
  staleTime: Infinity,
} );
```

### Placeholder Data

```javascript
export const useWorkout = ( { id } ) => useQuery( {
  queryKey: KEYS.workout( id ),
  queryFn: () => fetchWorkout( id ),

  // Show cached list item while fetching full details
  placeholderData: () => {
    return queryClient
      .getQueryData( KEYS.workouts() )
      ?.find( ( w ) => w.id === id );
  },
} );
```

---

## Mutations

### Basic Mutation

```javascript
import { useMutation, useQueryClient } from '@tanstack/react-query';

const createWorkout = async ( data ) => {
  const response = await axios.post( '/api/v1/workouts.json', { workout: data } );
  return response.data.data;
};

export const useCreateWorkout = () => {
  const queryClient = useQueryClient();

  return useMutation( {
    mutationFn: createWorkout,
    onSuccess: () => {
      // Invalidate and refetch workouts list
      queryClient.invalidateQueries( { queryKey: KEYS.workouts() } );
    },
  } );
};
```

### Mutation with Variables

```javascript
export const useUpdateWorkout = () => {
  const queryClient = useQueryClient();

  return useMutation( {
    mutationFn: ( { id, data } ) => updateWorkout( id, data ),
    onSuccess: ( result, { id } ) => {
      // Update the specific workout in cache
      queryClient.setQueryData( KEYS.workout( id ), result );
      // Invalidate list to refetch
      queryClient.invalidateQueries( { queryKey: KEYS.workouts() } );
    },
  } );
};

// Usage
const { mutate } = useUpdateWorkout();
mutate( { id: workoutId, data: { name: 'New Name' } } );
```

---

## Optimistic Updates

Update the UI immediately, rollback on error.

### Simple Optimistic Update

```javascript
export const useToggleFavorite = () => {
  const queryClient = useQueryClient();

  return useMutation( {
    mutationFn: ( { id, isFavorite } ) => toggleFavorite( id, isFavorite ),

    onMutate: async ( { id, isFavorite } ) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries( { queryKey: KEYS.workout( id ) } );

      // Snapshot previous value
      const previous = queryClient.getQueryData( KEYS.workout( id ) );

      // Optimistically update
      queryClient.setQueryData( KEYS.workout( id ), ( old ) => ( {
        ...old,
        isFavorite,
      } ) );

      return { previous };
    },

    onError: ( err, { id }, context ) => {
      // Rollback on error
      queryClient.setQueryData( KEYS.workout( id ), context.previous );
    },

    onSettled: ( data, error, { id } ) => {
      // Refetch to ensure consistency
      queryClient.invalidateQueries( { queryKey: KEYS.workout( id ) } );
    },
  } );
};
```

### Optimistic Update in List

```javascript
export const useDeleteWorkout = () => {
  const queryClient = useQueryClient();

  return useMutation( {
    mutationFn: deleteWorkout,

    onMutate: async ( workoutId ) => {
      await queryClient.cancelQueries( { queryKey: KEYS.workouts() } );

      const previous = queryClient.getQueryData( KEYS.workouts() );

      // Remove from list optimistically
      queryClient.setQueryData( KEYS.workouts(), ( old ) =>
        old?.filter( ( w ) => w.id !== workoutId )
      );

      return { previous };
    },

    onError: ( err, workoutId, context ) => {
      queryClient.setQueryData( KEYS.workouts(), context.previous );
    },

    onSettled: () => {
      queryClient.invalidateQueries( { queryKey: KEYS.workouts() } );
    },
  } );
};
```

---

## Cache Management

### Manual Cache Updates

```javascript
// Set data directly
queryClient.setQueryData( KEYS.workout( id ), newData );

// Update existing data
queryClient.setQueryData( KEYS.workout( id ), ( old ) => ( {
  ...old,
  name: 'Updated Name',
} ) );

// Add item to list
queryClient.setQueryData( KEYS.workouts(), ( old ) => [
  ...( old || [] ),
  newWorkout,
] );
```

### Prefetching

```javascript
// Prefetch on hover
const handleMouseEnter = ( workoutId ) => {
  queryClient.prefetchQuery( {
    queryKey: KEYS.workout( workoutId ),
    queryFn: () => fetchWorkout( workoutId ),
    staleTime: 60 * 1000,
  } );
};

// Prefetch after mutation
const { mutate } = useMutation( {
  mutationFn: createWorkout,
  onSuccess: ( newWorkout ) => {
    // Prefetch the new workout's detail page
    queryClient.prefetchQuery( {
      queryKey: KEYS.workout( newWorkout.id ),
      queryFn: () => fetchWorkout( newWorkout.id ),
    } );
  },
} );
```

### Invalidation Patterns

```javascript
// Invalidate exact key
queryClient.invalidateQueries( { queryKey: KEYS.workout( id ), exact: true } );

// Invalidate all matching keys
queryClient.invalidateQueries( { queryKey: [ 'workouts' ] } );

// Invalidate with predicate
queryClient.invalidateQueries( {
  predicate: ( query ) =>
    query.queryKey[ 0 ] === 'workouts' &&
    query.queryKey[ 1 ]?.clientId === clientId,
} );

// Remove from cache entirely
queryClient.removeQueries( { queryKey: KEYS.workout( id ) } );
```
