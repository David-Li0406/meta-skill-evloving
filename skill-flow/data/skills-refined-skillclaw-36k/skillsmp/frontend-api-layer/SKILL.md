---
name: frontend-api-layer
description: Provides patterns for structuring the API layer in React applications. This skill should be used when setting up API clients, defining API request declarations, or integrating with TanStack Query for data fetching.
---

# Frontend API Layer

This skill provides patterns for structuring the API layer in React applications, based on Bulletproof React best practices.

## Core Principles

### Single API Client Instance

Create a single, pre-configured API client instance that can be reused throughout the application.

**Benefits**:
- Centralized configuration (base URL, headers, interceptors)
- Consistent error handling
- Easier to mock for testing
- Single source of truth for API communication

**Example** (`src/lib/api-client.ts`):

```typescript
import axios from 'axios';

// Create axios instance with default config
export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - attach auth token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor - handle errors globally
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized - redirect to login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

### API Request Declaration Structure

Define API requests in a structured, colocated manner. Each API request declaration should include:

1. **Types and validation schemas** - Request/response data types
2. **Fetcher function** - Function that calls the endpoint
3. **Hook** - React hook that uses TanStack Query to manage data fetching

**Benefits**:
- All API-related code is colocated
- Type-safe requests and responses
- Easy to track available endpoints
- Consistent data fetching patterns

## Implementation Patterns

### Query (GET) Request

**File**: `src/features/discussions/api/get-discussions.ts`

```typescript
import { useQuery } from '@tanstack/react-query';
import { z } from 'zod';
import { apiClient } from '@/lib/api-client';

// 1. Define response schema and type
export const discussionSchema = z.object({
  id: z.string(),
  title: z.string(),
  body: z.string(),
  created_at: z.string(),
  author: z.object({
    id: z.string(),
    name: z.string(),
  }),
});

export type Discussion = z.infer<typeof discussionSchema>;

const discussionsResponseSchema = z.object({
  data: z.array(discussionSchema),
  total: z.number(),
});

export type DiscussionsResponse = z.infer<typeof discussionsResponseSchema>;

// 2. Define fetcher function
export async function getDiscussions(page = 1, limit = 10): Promise<DiscussionsResponse> {
  const response = await apiClient.get('/discussions', {
    params: { page, limit },
  });
  
  // Validate response
  return discussionsResponseSchema.parse(response.data);
}

// 3. Define React Query hook
export function useDiscussions(page = 1, limit = 10) {
  return useQuery({
    queryKey: ['discussions', page, limit],
    queryFn: () => getDiscussions(page, limit),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}
```

**Usage in component**:

```typescript
import { useDiscussions } from '@/features/discussions/api/get-discussions';

function DiscussionsList() {
  const { data, isLoading, error } = useDiscussions(1, 20);

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <ul>
      {data.data.map((discussion) => (
        <li key={discussion.id}>{discussion.title}</li>
      ))}
    </ul>
  );
}
```

### Mutation (POST/PUT/DELETE) Request

**File**: `src/features/discussions/api/create-discussion.ts`

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { z } from 'zod';
import { apiClient } from '@/lib/api-client';
import { discussionSchema, type Discussion } from './get-discussions';

// 1. Define request schema and type
export const createDiscussionSchema = z.object({
  title: z.string().min(1, 'Title is required'),
  body: z.string().min(10, 'Body must be at least 10 characters'),
});

export type CreateDiscussionDto = z.infer<typeof createDiscussionSchema>;

// 2. Define fetcher function
export async function createDiscussion(data: CreateDiscussionDto): Promise<Discussion> {
  const response = await apiClient.post('/discussions', data);
  return discussionSchema.parse(response.data);
}

// 3. Define React Query mutation hook
export function useCreateDiscussion() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createDiscussion,
    onSuccess: () => {
      // Invalidate and refetch discussions list
      queryClient.invalidateQueries({ queryKey: ['discussions'] });
    },
  });
}
```

**Usage in component**:

```typescript
import { useCreateDiscussion, createDiscussionSchema } from '@/features/discussions/api/create-discussion';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

function CreateDiscussionForm() {
  const createDiscussion = useCreateDiscussion();
  
  const form = useForm({
    resolver: zodResolver(createDiscussionSchema),
  });

  const onSubmit = form.handleSubmit((data) => {
    createDiscussion.mutate(data, {
      onSuccess: () => {
        form.reset();
        // Show success message
      },
    });
  });

  return (
    <form onSubmit={onSubmit}>
      <input {...form.register('title')} />
      <textarea {...form.register('body')} />
      <button type="submit" disabled={createDiscussion.isPending}>
        {createDiscussion.isPending ? 'Creating...' : 'Create'}
      </button>
    </form>
  );
}
```

## File Organization

### Colocation with Features

API declarations should be colocated with the features that use them:

```
src/features/discussions/
├── api/
│   ├── get-discussions.ts      # Query
│   ├── get-discussion.ts       # Single item query
│   ├── create-discussion.ts    # Mutation
│   ├── update-discussion.ts    # Mutation
│   └── delete-discussion.ts    # Mutation
├── components/
│   ├── DiscussionsList.tsx
│   └── DiscussionForm.tsx
└── routes/
    ├── discussions.tsx
    └── discussion.$id.tsx
```

### Shared API Folder (Alternative)

For applications with many shared API calls, you can use a dedicated `api` folder:

```
src/api/
├── discussions/
│   ├── get-discussions.ts
│   └── create-discussion.ts
├── users/
│   ├── get-users.ts
│   └── update-user.ts
└── index.ts  # Re-export all API functions
```

**When to use**:
- Many API calls shared across features
- Centralized API documentation needed
- API calls don't map cleanly to features

## Integration with Shared Types

Use types from `@eridu/api-types` for API contracts:

```typescript
import { type UserApiResponse, userApiResponseSchema } from '@eridu/api-types/users';
import { apiClient } from '@/lib/api-client';

export async function getUser(id: string): Promise<UserApiResponse> {
  const response = await apiClient.get(`/users/${id}`);
  return userApiResponseSchema.parse(response.data);
}
```

## Best Practices

1. **Always validate responses** - Use Zod schemas to validate API responses at runtime
2. **Type everything** - Infer TypeScript types from Zod schemas
3. **Colocate API calls** - Keep API declarations close to where they're used
4. **Use query keys consistently** - Follow a consistent pattern for query keys
5. **Handle loading and error states** - Always handle loading, error, and success states in components
6. **Invalidate queries on mutations** - Update cache after mutations to keep UI in sync
7. **Set appropriate stale times** - Configure stale times based on data freshness requirements

## Checklist

- [ ] Single API client instance configured with interceptors
- [ ] API requests follow the structure: schema → fetcher → hook
- [ ] All responses are validated with Zod schemas
- [ ] Types are inferred from schemas (not manually duplicated)
- [ ] API declarations are colocated with features
- [ ] Query keys follow a consistent pattern
- [ ] Mutations invalidate relevant queries
- [ ] Loading and error states are handled in components
