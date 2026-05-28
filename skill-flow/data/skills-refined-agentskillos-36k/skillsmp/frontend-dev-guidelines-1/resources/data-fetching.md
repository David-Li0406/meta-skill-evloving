# Data Fetching Patterns

Modern data fetching using TanStack Query with Suspense boundaries, cache-first strategies, and centralized API services.

---

## PRIMARY PATTERN: useSuspenseQuery

### Why useSuspenseQuery?

For **all new components**, use `useSuspenseQuery` instead of regular `useQuery`:

**Benefits:**
- No `isLoading` checks needed
- Integrates with Suspense boundaries
- Cleaner component code
- Consistent loading UX
- Better error handling with error boundaries

### Basic Pattern

```typescript
import { useSuspenseQuery } from '@tanstack/react-query';
import { myFeatureApi } from '../api/myFeatureApi';

export const MyComponent: React.FC<Props> = ({ id }) => {
    // No isLoading - Suspense handles it!
    const { data } = useSuspenseQuery({
        queryKey: ['myEntity', id],
        queryFn: () => myFeatureApi.getEntity(id),
    });

    // data is ALWAYS defined here (not undefined | Data)
    return <div>{data.name}</div>;
};

// Wrap in Suspense boundary
<SuspenseLoader>
    <MyComponent id={123} />
</SuspenseLoader>
```

### useSuspenseQuery vs useQuery

| Feature | useSuspenseQuery | useQuery |
|---------|------------------|----------|
| Loading state | Handled by Suspense | Manual `isLoading` check |
| Data type | Always defined | `Data \| undefined` |
| Use with | Suspense boundaries | Traditional components |
| Recommended for | **NEW components** | Legacy code only |
| Error handling | Error boundaries | Manual error state |

**When to use regular useQuery:**
- Maintaining legacy code
- Very simple cases without Suspense
- Polling with background updates

**For new components: Always prefer useSuspenseQuery**

---

## Cache-First Strategy

### Cache-First Pattern Example

**Smart caching** reduces API calls by checking React Query cache first:

```typescript
import { useSuspenseQuery, useQueryClient } from '@tanstack/react-query';
import { postApi } from '../api/postApi';

export function useSuspensePost(postId: number) {
    const queryClient = useQueryClient();

    return useSuspenseQuery({
        queryKey: ['post', postId],
        queryFn: async () => {
            // Strategy 1: Try to get from list cache first
            const cachedListData = queryClient.getQueryData<{ posts: Post[] }>([
                'posts',
                'list'
            ]);

            if (cachedListData?.posts) {
                const cachedPost = cachedListData.posts.find(
                    (post) => post.id === postId
                );

                if (cachedPost) {
                    return cachedPost;  // Return from cache!
                }
            }

            // Strategy 2: Not in cache, fetch from API
            return postApi.getPost(postId);
        },
        staleTime: 5 * 60 * 1000,      // Consider fresh for 5 minutes
        gcTime: 10 * 60 * 1000,         // Keep in cache for 10 minutes
        refetchOnWindowFocus: false,    // Don't refetch on focus
    });
}
```

**Key Points:**
- Check grid/list cache before API call
- Avoids redundant requests
- `staleTime`: How long data is considered fresh
- `gcTime`: How long unused data stays in cache
- `refetchOnWindowFocus: false`: User preference

---

## Parallel Data Fetching

### useSuspenseQueries

When fetching multiple independent resources:

```typescript
import { useSuspenseQueries } from '@tanstack/react-query';

export const MyComponent: React.FC = () => {
    const [userQuery, settingsQuery, preferencesQuery] = useSuspenseQueries({
        queries: [
            {
                queryKey: ['user'],
                queryFn: () => userApi.getCurrentUser(),
            },
            {
                queryKey: ['settings'],
                queryFn: () => settingsApi.getSettings(),
            },
            {
                queryKey: ['preferences'],
                queryFn: () => preferencesApi.getPreferences(),
            },
        ],
    });

    // All data available, Suspense handles loading
    const user = userQuery.data;
    const settings = settingsQuery.data;
    const preferences = preferencesQuery.data;

    return <Display user={user} settings={settings} prefs={preferences} />;
};
```

**Benefits:**
- All queries in parallel
- Single Suspense boundary
- Type-safe results

---

## Query Keys Organization

### Naming Convention

```typescript
// Entity list
['entities', blogId]
['entities', blogId, 'summary']    // With view mode
['entities', blogId, 'flat']

// Single entity
['entity', blogId, entityId]

// Related data
['entity', entityId, 'history']
['entity', entityId, 'comments']

// User-specific
['user', userId, 'profile']
['user', userId, 'permissions']
```

**Rules:**
- Start with entity name (plural for lists, singular for one)
- Include IDs for specificity
- Add view mode / relationship at end
- Consistent across app

### Query Key Examples

```typescript
// From useSuspensePost.ts
queryKey: ['post', blogId, postId]
queryKey: ['posts-v2', blogId, 'summary']

// Invalidation patterns
queryClient.invalidateQueries({ queryKey: ['post', blogId] });  // All posts for form
queryClient.invalidateQueries({ queryKey: ['post'] });          // All posts
```

---

## API Service Layer Pattern

### File Structure

Create centralized API service per feature:

```
features/
  my-feature/
    api/
      myFeatureApi.ts    # Service layer
```

### Service Pattern (from postApi.ts)

```typescript
/**
 * Centralized API service for my-feature operations
 * Uses apiClient for consistent error handling
 */
import { api } from '@/lib/api';
import type { MyEntity, UpdatePayload } from '../types';

export const myFeatureApi = {
    /**
     * Fetch a single entity
     */
    getEntity: async (id: number): Promise<MyEntity> => {
        return api.get(`/entities/${id}`);
    },

    /**
     * Fetch all entities
     */
    getEntities: async (params?: { filter?: string }): Promise<MyEntity[]> => {
        return api.get('/entities', { params });
    },

    /**
     * Update entity
     */
    updateEntity: async (
        id: number,
        payload: UpdatePayload
    ): Promise<MyEntity> => {
        return api.put(`/entities/${id}`, payload);
    },

    /**
     * Delete entity
     */
    deleteEntity: async (id: number): Promise<void> => {
        await api.delete(`/entities/${id}`);
    },
};
```

**Key Points:**
- Export single object with methods
- Use `api` (axios instance from `@/lib/api`)
- Type-safe parameters and returns
- JSDoc comments for each method
- Centralized error handling (api handles it)

---

## Route Format Rules

### API Endpoint Pattern

```typescript
// ✅ CORRECT - ActionPhase API routes
await api.get('/games');
await api.post('/games', gameData);
await api.put('/games/123', updates);
await api.delete('/games/123');

// Game-related endpoints
await api.get('/games/123/characters');
await api.post('/games/123/phases', phaseData);

// Auth endpoints
await api.post('/auth/login', credentials);
await api.post('/auth/refresh');
await api.post('/auth/logout');
```

**ActionPhase API Routes:**
- Games: `/games/*`
- Characters: `/characters/*`
- Messages: `/messages/*`
- Phases: `/phases/*`
- Auth: `/auth/*`
- Users: `/users/*`

**Note:** The api client handles the base URL and auth tokens automatically.

---

## Mutations

### Basic Mutation Pattern

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { myFeatureApi } from '../api/myFeatureApi';
import { toast } from 'react-hot-toast';

export const MyComponent: React.FC = () => {
    const queryClient = useQueryClient();

    const updateMutation = useMutation({
        mutationFn: (payload: UpdatePayload) =>
            myFeatureApi.updateEntity(id, payload),

        onSuccess: () => {
            // Invalidate and refetch
            queryClient.invalidateQueries({
                queryKey: ['entity', id]
            });
            toast.success('Entity updated successfully');
        },

        onError: (error) => {
            toast.error('Failed to update entity');
            console.error('Update error:', error);
        },
    });

    const handleUpdate = () => {
        updateMutation.mutate({ name: 'New Name' });
    };

    return (
        <Button
            onClick={handleUpdate}
            disabled={updateMutation.isPending}
        >
            {updateMutation.isPending ? 'Updating...' : 'Update'}
        </Button>
    );
};
```

### Optimistic Updates

```typescript
const updateMutation = useMutation({
    mutationFn: (payload) => myFeatureApi.update(id, payload),

    // Optimistic update
    onMutate: async (newData) => {
        // Cancel outgoing refetches
        await queryClient.cancelQueries({ queryKey: ['entity', id] });

        // Snapshot current value
        const previousData = queryClient.getQueryData(['entity', id]);

        // Optimistically update
        queryClient.setQueryData(['entity', id], (old) => ({
            ...old,
            ...newData,
        }));

        // Return rollback function
        return { previousData };
    },

    // Rollback on error
    onError: (err, newData, context) => {
        queryClient.setQueryData(['entity', id], context.previousData);
        toast.error('Update failed');
    },

    // Refetch after success or error
    onSettled: () => {
        queryClient.invalidateQueries({ queryKey: ['entity', id] });
    },
});
```

---

## Advanced Query Patterns

### Prefetching

```typescript
export function usePrefetchEntity() {
    const queryClient = useQueryClient();

    return (blogId: number, entityId: number) => {
        return queryClient.prefetchQuery({
            queryKey: ['entity', blogId, entityId],
            queryFn: () => myFeatureApi.getEntity(blogId, entityId),
            staleTime: 5 * 60 * 1000,
        });
    };
}

// Usage: Prefetch on hover
<div onMouseEnter={() => prefetch(blogId, id)}>
    <Link to={`/entity/${id}`}>View</Link>
</div>
```

### Cache Access Without Fetching

```typescript
export function useEntityFromCache(blogId: number, entityId: number) {
    const queryClient = useQueryClient();

    // Get from cache, don't fetch if missing
    const directCache = queryClient.getQueryData<MyEntity>(['entity', blogId, entityId]);

    if (directCache) return directCache;

    // Try grid cache
    const gridCache = queryClient.getQueryData<{ rows: MyEntity[] }>(['entities-v2', blogId]);

    return gridCache?.rows.find(row => row.id === entityId);
}
```

### Dependent Queries

```typescript
// Fetch user first, then user's settings
const { data: user } = useSuspenseQuery({
    queryKey: ['user', userId],
    queryFn: () => userApi.getUser(userId),
});

const { data: settings } = useSuspenseQuery({
    queryKey: ['user', userId, 'settings'],
    queryFn: () => settingsApi.getUserSettings(user.id),
    // Automatically waits for user to load due to Suspense
});
```

---

## API Client Configuration

### Using the API Client

```typescript
import { api } from '@/lib/api';

// api is a configured axios instance
// Automatically includes:
// - Base URL configuration
// - JWT authentication
// - Error interceptors
// - Response transformers
```

**Do NOT create new axios instances** - use the api client for consistency.

---

## Error Handling in Queries

### Error Handling

```typescript
import { toast } from 'react-hot-toast';

const { data } = useSuspenseQuery({
    queryKey: ['entity', id],
    queryFn: () => myFeatureApi.getEntity(id),
});

// Errors are handled by error boundaries with useSuspenseQuery
// For explicit error handling, use regular useQuery with error state
```

### Error Boundaries

Combine with Error Boundaries for comprehensive error handling:

```typescript
import { ErrorBoundary } from 'react-error-boundary';

<ErrorBoundary
    fallback={<ErrorDisplay />}
    onError={(error) => console.error(error)}
>
    <SuspenseLoader>
        <ComponentWithSuspenseQuery />
    </SuspenseLoader>
</ErrorBoundary>
```

---

## Complete Examples

### Example 1: Simple Entity Fetch

```typescript
import React from 'react';
import { useSuspenseQuery } from '@tanstack/react-query';
import { Card, CardBody } from '@/components/ui';
import { userApi } from '../api/userApi';

interface UserProfileProps {
    userId: string;
}

export const UserProfile: React.FC<UserProfileProps> = ({ userId }) => {
    const { data: user } = useSuspenseQuery({
        queryKey: ['user', userId],
        queryFn: () => userApi.getUser(userId),
        staleTime: 5 * 60 * 1000,
    });

    return (
        <Card variant="default" padding="md">
            <CardBody>
                <h2 className="text-xl font-semibold text-text-heading">{user.name}</h2>
                <p className="text-text-primary">{user.email}</p>
            </CardBody>
        </Card>
    );
};

// Usage with Suspense
<SuspenseLoader>
    <UserProfile userId='123' />
</SuspenseLoader>
```

### Example 2: Cache-First Strategy

```typescript
import { useSuspenseQuery, useQueryClient } from '@tanstack/react-query';
import { postApi } from '../api/postApi';
import type { Post } from '../types';

/**
 * Hook with cache-first strategy
 * Checks grid cache before API call
 */
export function useSuspensePost(blogId: number, postId: number) {
    const queryClient = useQueryClient();

    return useSuspenseQuery<Post, Error>({
        queryKey: ['post', blogId, postId],
        queryFn: async () => {
            // 1. Check grid cache first
            const gridCache = queryClient.getQueryData<{ rows: Post[] }>([
                'posts-v2',
                blogId,
                'summary'
            ]) || queryClient.getQueryData<{ rows: Post[] }>([
                'posts-v2',
                blogId,
                'flat'
            ]);

            if (gridCache?.rows) {
                const cached = gridCache.rows.find(row => row.S_ID === postId);
                if (cached) {
                    return cached;  // Reuse grid data
                }
            }

            // 2. Not in cache, fetch directly
            return postApi.getPost(blogId, postId);
        },
        staleTime: 5 * 60 * 1000,
        gcTime: 10 * 60 * 1000,
        refetchOnWindowFocus: false,
    });
}
```

**Benefits:**
- Avoids duplicate API calls
- Instant data if already loaded
- Falls back to API if not cached

### Example 3: Parallel Fetching

```typescript
import { useSuspenseQueries } from '@tanstack/react-query';

export const Dashboard: React.FC = () => {
    const [statsQuery, projectsQuery, notificationsQuery] = useSuspenseQueries({
        queries: [
            {
                queryKey: ['stats'],
                queryFn: () => statsApi.getStats(),
            },
            {
                queryKey: ['projects', 'active'],
                queryFn: () => projectsApi.getActiveProjects(),
            },
            {
                queryKey: ['notifications', 'unread'],
                queryFn: () => notificationsApi.getUnread(),
            },
        ],
    });

    return (
        <div className="space-y-6">
            <StatsCard data={statsQuery.data} />
            <ProjectsList projects={projectsQuery.data} />
            <Notifications items={notificationsQuery.data} />
        </div>
    );
};
```

---

## Mutations with Cache Invalidation

### Update Mutation

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { gameApi } from '../api/gameApi';
import { toast } from 'react-hot-toast';

export const useUpdateGame = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ gameId, data }: UpdateParams) =>
            gameApi.updateGame(gameId, data),

        onSuccess: (data, variables) => {
            // Invalidate specific game
            queryClient.invalidateQueries({
                queryKey: ['game', variables.gameId]
            });

            // Invalidate list to refresh grid
            queryClient.invalidateQueries({
                queryKey: ['games']
            });

            toast.success('Game updated');
        },

        onError: (error) => {
            toast.error('Failed to update game');
            console.error('Update error:', error);
        },
    });
};

// Usage
const updateGame = useUpdateGame();

const handleSave = () => {
    updateGame.mutate({
        gameId: 123,
        data: { name: 'Updated Name', description: 'New description' }
    });
};
```

### Delete Mutation

```typescript
export const useDeleteGame = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ gameId }: DeleteParams) =>
            gameApi.deleteGame(gameId),

        onSuccess: (data, variables) => {
            // Remove from cache manually (optimistic)
            queryClient.setQueryData<Game[]>(
                ['games'],
                (old) => old?.filter(game => game.id !== variables.gameId) || []
            );

            toast.success('Game deleted');
        },

        onError: (error, variables) => {
            // Rollback - refetch to get accurate state
            queryClient.invalidateQueries({
                queryKey: ['games']
            });
            toast.error('Failed to delete game');
        },
    });
};
```

---

## Query Configuration Best Practices

### Default Configuration

```typescript
// In QueryClientProvider setup
const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            staleTime: 1000 * 60 * 5,        // 5 minutes
            gcTime: 1000 * 60 * 10,           // 10 minutes (was cacheTime)
            refetchOnWindowFocus: false,       // Don't refetch on focus
            refetchOnMount: false,             // Don't refetch on mount if fresh
            retry: 1,                          // Retry failed queries once
        },
    },
});
```

### Per-Query Overrides

```typescript
// Frequently changing data - shorter staleTime
useSuspenseQuery({
    queryKey: ['notifications', 'unread'],
    queryFn: () => notificationApi.getUnread(),
    staleTime: 30 * 1000,  // 30 seconds
});

// Rarely changing data - longer staleTime
useSuspenseQuery({
    queryKey: ['form', blogId, 'structure'],
    queryFn: () => formApi.getStructure(blogId),
    staleTime: 30 * 60 * 1000,  // 30 minutes
});
```

---

## Summary

**Modern Data Fetching Recipe:**

1. **Create API Service**: `features/X/api/XApi.ts` using `@/lib/api`
2. **Use useSuspenseQuery**: In components wrapped by SuspenseLoader
3. **Cache-First**: Check list cache before API call
4. **Query Keys**: Consistent naming ['entity', id]
5. **Route Format**: Direct API paths like `/games` or `/characters`
6. **Mutations**: invalidateQueries after success
7. **Error Handling**: Error boundaries + toast notifications
8. **Type Safety**: Type all parameters and returns

**See Also:**
- [component-patterns.md](component-patterns.md) - Suspense integration
- [loading-and-error-states.md](loading-and-error-states.md) - SuspenseLoader usage
- [complete-examples.md](complete-examples.md) - Full working examples
