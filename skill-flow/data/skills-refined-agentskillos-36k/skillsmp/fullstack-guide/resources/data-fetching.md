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
| Loading state | Suspense handles | Manual check |
| Data type | `T` (always defined) | `T \| undefined` |
| Error handling | Error boundary | Manual |
| Code simplicity | Cleaner | More boilerplate |
| **Use when** | New components | Legacy or special cases |

---

## API Service Layer

### Creating API Services

```typescript
// features/users/api/userApi.ts
import { apiClient } from '@/lib/apiClient';
import type { User, CreateUserDTO, UpdateUserDTO } from '~types/user';

export const userApi = {
    getAll: async (): Promise<User[]> => {
        const response = await apiClient.get('/users');
        return response.data;
    },

    getById: async (id: number): Promise<User> => {
        const response = await apiClient.get(`/users/${id}`);
        return response.data;
    },

    create: async (data: CreateUserDTO): Promise<User> => {
        const response = await apiClient.post('/users', data);
        return response.data;
    },

    update: async (id: number, data: UpdateUserDTO): Promise<User> => {
        const response = await apiClient.put(`/users/${id}`, data);
        return response.data;
    },

    delete: async (id: number): Promise<void> => {
        await apiClient.delete(`/users/${id}`);
    },
};
```

---

## Mutations

### Basic Mutation Pattern

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { userApi } from '../api/userApi';
import { useMuiSnackbar } from '@/hooks/useMuiSnackbar';

export const useCreateUser = () => {
    const queryClient = useQueryClient();
    const { showSnackbar } = useMuiSnackbar();

    return useMutation({
        mutationFn: userApi.create,
        onSuccess: () => {
            // Invalidate and refetch
            queryClient.invalidateQueries({ queryKey: ['users'] });
            showSnackbar('User created successfully', 'success');
        },
        onError: (error) => {
            showSnackbar('Failed to create user', 'error');
        },
    });
};
```

### Using Mutations

```typescript
const createUser = useCreateUser();

const handleSubmit = (data: CreateUserDTO) => {
    createUser.mutate(data);
};
```

---

## Query Keys

### Naming Convention

```typescript
// Entity lists
['users']
['posts']

// Single entity
['user', userId]
['post', postId]

// Filtered/scoped queries
['users', { role: 'admin' }]
['posts', { status: 'published' }]

// Nested resources
['user', userId, 'posts']
['post', postId, 'comments']
```

### Consistent Keys

```typescript
// Query keys file
export const queryKeys = {
    users: {
        all: ['users'] as const,
        detail: (id: number) => ['user', id] as const,
        byRole: (role: string) => ['users', { role }] as const,
    },
    posts: {
        all: ['posts'] as const,
        detail: (id: number) => ['post', id] as const,
    },
};

// Usage
const { data } = useSuspenseQuery({
    queryKey: queryKeys.users.detail(userId),
    queryFn: () => userApi.getById(userId),
});
```

---

## Caching Configuration

### Global Defaults

```typescript
const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            staleTime: 5 * 60 * 1000,           // 5 minutes
            gcTime: 10 * 60 * 1000,             // 10 minutes
            refetchOnWindowFocus: false,
            refetchOnMount: false,
            retry: 1,
        },
    },
});
```

### Per-Query Overrides

```typescript
// Frequently changing data
useSuspenseQuery({
    queryKey: ['notifications', 'unread'],
    queryFn: () => notificationApi.getUnread(),
    staleTime: 30 * 1000,  // 30 seconds
});

// Rarely changing data
useSuspenseQuery({
    queryKey: ['settings'],
    queryFn: () => settingsApi.get(),
    staleTime: 30 * 60 * 1000,  // 30 minutes
});
```

---

## Summary

**Modern Data Fetching Recipe:**

1. **Create API Service**: `features/X/api/XApi.ts`
2. **Use useSuspenseQuery**: In components wrapped by SuspenseLoader
3. **Query Keys**: Consistent naming `['entity', id]`
4. **Mutations**: invalidateQueries after success
5. **Error Handling**: onError + useMuiSnackbar
6. **Type Safety**: Type all parameters and returns

**See Also:**
- [component-patterns.md](component-patterns.md) - Suspense integration
- [loading-and-error-states.md](loading-and-error-states.md) - SuspenseLoader usage
