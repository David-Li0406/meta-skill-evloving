# API Layer

A well-architected API layer separates data fetching concerns from UI logic, enabling better testing, caching, and error handling.

##Table of Contents

- [Architecture Principles](#architecture-principles)
- [API Client Setup](#api-client-setup)
- [Request Organization](#request-organization)
- [Error Handling](#error-handling)
- [TypeScript Integration](#typescript-integration)
- [Authentication](#authentication)
- [Best Practices](#best-practices)

## Architecture Principles

### Single Responsibility

Each layer has a clear purpose:

```
Components → Hooks (React Query) → API Functions → API Client → Server
   UI          State & Cache        Business Logic    HTTP       Data
```

**Responsibilities:**
- **Components**: Render UI, handle user interaction
- **Hooks**: Manage query state, caching, refetching
- **API Functions**: Define request structure, validate data
- **API Client**: HTTP configuration, interceptors, base URL
- **Server**: Business logic, database access

### Separation of Concerns

```tsx
// ❌ Bad - mixing concerns
function UserProfile() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch('https://api.example.com/users/123', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(setUser);
  }, []);

  return <div>{user?.name}</div>;
}

// ✅ Good - separated concerns
function UserProfile({ userId }) {
  const { data: user } = useUser(userId); // Hook
  return <div>{user?.name}</div>;
}
```

## API Client Setup

### Axios Configuration

Create a configured Axios instance:

```tsx
// lib/api-client.ts
import axios, { type AxiosRequestConfig } from 'axios';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - handle errors
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    // Handle 401 - refresh token or logout
    if (error.response?.status === 401) {
      // Try to refresh token
      try {
        const newToken = await refreshAuthToken();
        error.config.headers.Authorization = `Bearer ${newToken}`;
        return apiClient(error.config); // Retry request
      } catch {
        // Refresh failed - logout
        logout();
        window.location.href = '/login';
      }
    }

    // Handle 403 - unauthorized
    if (error.response?.status === 403) {
      showNotification('You do not have permission to perform this action');
    }

    // Handle 500 - server error
    if (error.response?.status >= 500) {
      showNotification('Server error. Please try again later.');
    }

    return Promise.reject(error);
  }
);
```

### Fetch API Alternative

```tsx
// lib/api-client.ts
type RequestConfig = RequestInit & {
  baseURL?: string;
};

class APIClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  async request<T>(
    endpoint: string,
    config: RequestConfig = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const token = localStorage.getItem('auth_token');

    const response = await fetch(url, {
      ...config,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...config.headers,
      },
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Handle auth error
        logout();
        throw new Error('Unauthorized');
      }
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return response.json();
  }

  get<T>(endpoint: string, config?: RequestConfig) {
    return this.request<T>(endpoint, { ...config, method: 'GET' });
  }

  post<T>(endpoint: string, data?: unknown, config?: RequestConfig) {
    return this.request<T>(endpoint, {
      ...config,
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  put<T>(endpoint: string, data?: unknown, config?: RequestConfig) {
    return this.request<T>(endpoint, {
      ...config,
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  delete<T>(endpoint: string, config?: RequestConfig) {
    return this.request<T>(endpoint, { ...config, method: 'DELETE' });
  }
}

export const apiClient = new APIClient(import.meta.env.VITE_API_URL);
```

## Request Organization

### Feature-Based API Files

Organize by domain/feature:

```
features/
└── users/
    └── api/
        ├── get-user.ts
        ├── get-users.ts
        ├── create-user.ts
        ├── update-user.ts
        ├── delete-user.ts
        └── index.ts
```

### Request Declaration Pattern

Each API request follows this pattern:

```tsx
// features/users/api/get-user.ts
import { z } from 'zod';
import { apiClient } from '@/lib/api-client';
import { useQuery } from '@tanstack/react-query';

// 1. Response schema
const userSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
  role: z.enum(['admin', 'user', 'guest']),
  createdAt: z.string().datetime(),
});

export type User = z.infer<typeof userSchema>;

// 2. Request parameters schema
const getUserParamsSchema = z.object({
  userId: z.string(),
});

type GetUserParams = z.infer<typeof getUserParamsSchema>;

// 3. Fetcher function
export async function getUser(params: GetUserParams): Promise<User> {
  // Validate params
  const validatedParams = getUserParamsSchema.parse(params);

  const response = await apiClient.get(`/users/${validatedParams.userId}`);

  // Validate response
  return userSchema.parse(response.data);
}

// 4. React Query hook
export function useUser(userId: string) {
  return useQuery({
    queryKey: ['users', userId],
    queryFn: () => getUser({ userId }),
    enabled: !!userId, // Only fetch if userId exists
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}
```

### Mutations

```tsx
// features/users/api/create-user.ts
import { z } from 'zod';
import { apiClient } from '@/lib/api-client';
import { useMutation, useQueryClient } from '@tanstack/react-query';

// Input schema
const createUserInputSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

export type CreateUserInput = z.infer<typeof createUserInputSchema>;

// Fetcher
export async function createUser(input: CreateUserInput): Promise<User> {
  const validatedInput = createUserInputSchema.parse(input);

  const response = await apiClient.post('/users', validatedInput);

  return userSchema.parse(response.data);
}

// Hook
export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createUser,

    onSuccess: (newUser) => {
      // Invalidate users list
      queryClient.invalidateQueries({ queryKey: ['users'] });

      // Optionally add to cache
      queryClient.setQueryData(['users', newUser.id], newUser);

      showNotification('User created successfully');
    },

    onError: (error) => {
      showNotification(`Failed to create user: ${error.message}`);
    },
  });
}

// Usage in component
function CreateUserForm() {
  const createUser = useCreateUser();

  const handleSubmit = (data: CreateUserInput) => {
    createUser.mutate(data);
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
      <button type="submit" disabled={createUser.isPending}>
        {createUser.isPending ? 'Creating...' : 'Create User'}
      </button>
    </form>
  );
}
```

## Error Handling

### Error Types

Define custom error classes:

```tsx
// lib/errors.ts
export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public code?: string
  ) {
    super(message);
    this.name = 'APIError';
  }
}

export class ValidationError extends APIError {
  constructor(message: string, public fields?: Record<string, string[]>) {
    super(message, 400, 'VALIDATION_ERROR');
    this.name = 'ValidationError';
  }
}

export class AuthenticationError extends APIError {
  constructor(message: string = 'Authentication required') {
    super(message, 401, 'AUTHENTICATION_ERROR');
    this.name = 'AuthenticationError';
  }
}

export class AuthorizationError extends APIError {
  constructor(message: string = 'Permission denied') {
    super(message, 403, 'AUTHORIZATION_ERROR');
    this.name = 'AuthorizationError';
  }
}
```

### Global Error Boundary

```tsx
// components/ErrorBoundary.tsx
import { Component, type ReactNode } from 'react';

type Props = {
  children: ReactNode;
  fallback?: ReactNode;
};

type State = {
  hasError: boolean;
  error: Error | null;
};

export class ErrorBoundary extends Component<Props, State> {
  state: State = {
    hasError: false,
    error: null,
  };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    // Log to error tracking service
    // trackError(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div>
          <h1>Something went wrong</h1>
          <p>{this.state.error?.message}</p>
        </div>
      );
    }

    return this.props.children;
  }
}
```

## TypeScript Integration

### Type-Safe API Calls

```tsx
// Shared types
export type PaginationParams = {
  page?: number;
  perPage?: number;
};

export type PaginatedResponse<T> = {
  data: T[];
  total: number;
  page: number;
  perPage: number;
};

// Usage
async function getUsers(
  params: PaginationParams
): Promise<PaginatedResponse<User>> {
  const response = await apiClient.get('/users', { params });
  return response.data;
}
```

### Generic Request Function

```tsx
export async function apiRequest<TData, TParams = void>(
  endpoint: string,
  options: {
    method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
    params?: TParams;
    data?: unknown;
    schema: z.ZodSchema<TData>;
  }
): Promise<TData> {
  const response = await apiClient.request({
    url: endpoint,
    method: options.method || 'GET',
    params: options.params,
    data: options.data,
  });

  return options.schema.parse(response.data);
}

// Usage
const user = await apiRequest('/users/123', {
  schema: userSchema,
});
```

## Authentication

### Token Management

```tsx
// lib/auth.ts
const TOKEN_KEY = 'auth_token';
const REFRESH_TOKEN_KEY = 'refresh_token';

export const tokenStorage = {
  get: () => localStorage.getItem(TOKEN_KEY),
  set: (token: string) => localStorage.setItem(TOKEN_KEY, token),
  remove: () => localStorage.removeItem(TOKEN_KEY),

  getRefresh: () => localStorage.getItem(REFRESH_TOKEN_KEY),
  setRefresh: (token: string) => localStorage.setItem(REFRESH_TOKEN_KEY, token),
  removeRefresh: () => localStorage.removeItem(REFRESH_TOKEN_KEY),
};

export async function refreshAuthToken(): Promise<string> {
  const refreshToken = tokenStorage.getRefresh();

  if (!refreshToken) {
    throw new AuthenticationError('No refresh token available');
  }

  const response = await apiClient.post('/auth/refresh', {
    refreshToken,
  });

  const { token, refreshToken: newRefreshToken } = response.data;

  tokenStorage.set(token);
  tokenStorage.setRefresh(newRefreshToken);

  return token;
}
```

## Best Practices

### 1. Validate All Data

Use Zod to validate both requests and responses:

```tsx
// Always validate
const user = userSchema.parse(response.data); // Runtime validation
```

### 2. Centralize Configuration

Keep all API configuration in one place:

```tsx
// config/api.ts
export const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
  retryAttempts: 3,
  retryDelay: 1000,
} as const;
```

### 3. Handle Loading and Error States

```tsx
function UserProfile({ userId }) {
  const { data: user, isLoading, error } = useUser(userId);

  if (isLoading) return <Spinner />;
  if (error) return <ErrorMessage error={error} />;
  if (!user) return <NotFound />;

  return <div>{user.name}</div>;
}
```

### 4. Implement Retry Logic

```tsx
export function useUser(userId: string) {
  return useQuery({
    queryKey: ['users', userId],
    queryFn: () => getUser({ userId }),
    retry: (failureCount, error) => {
      // Don't retry on 4xx errors
      if (error instanceof APIError && error.status < 500) {
        return false;
      }
      return failureCount < 3;
    },
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  });
}
```

### 5. Cache Strategically

```tsx
export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: getUsers,
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 10 * 60 * 1000, // 10 minutes
    refetchOnWindowFocus: false,
    refetchOnReconnect: true,
  });
}
```

### 6. Optimistic Updates

```tsx
export function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateUser,

    onMutate: async (updatedUser) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['users', updatedUser.id] });

      // Snapshot previous value
      const previousUser = queryClient.getQueryData(['users', updatedUser.id]);

      // Optimistically update
      queryClient.setQueryData(['users', updatedUser.id], updatedUser);

      return { previousUser };
    },

    onError: (err, updatedUser, context) => {
      // Rollback on error
      if (context?.previousUser) {
        queryClient.setQueryData(
          ['users', updatedUser.id],
          context.previousUser
        );
      }
    },

    onSettled: (data, error, variables) => {
      // Refetch after mutation
      queryClient.invalidateQueries({ queryKey: ['users', variables.id] });
    },
  });
}
```

By following these patterns, you create an API layer that's type-safe, testable, and maintainable.
