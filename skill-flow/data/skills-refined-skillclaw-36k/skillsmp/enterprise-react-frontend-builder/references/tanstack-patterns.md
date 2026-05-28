# TanStack Query & Router Patterns

This document contains comprehensive patterns for TanStack Query and TanStack Router usage in enterprise applications.

## TanStack Query Setup

### Installation

```bash
npm install @tanstack/react-query @tanstack/react-query-devtools
```

### Configuration

```tsx
// src/main.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import '@takeoff-ui/core/dist/core/core.css'
import App from './App'

// Create QueryClient with default options
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      gcTime: 1000 * 60 * 10, // 10 minutes (formerly cacheTime)
      retry: 3,
      refetchOnWindowFocus: false,
      refetchOnReconnect: true,
    },
    mutations: {
      retry: 1,
    },
  },
})

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
      {import.meta.env.DEV && <ReactQueryDevtools initialIsOpen={false} />}
    </QueryClientProvider>
  </StrictMode>
)
```

## Query Patterns

### Basic Query

```tsx
// src/api/endpoints/users.ts
import { useQuery } from '@tanstack/react-query'
import { apiClient } from '../client'
import type { User } from '@/types/models'

export const useUsers = () => {
  return useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const { data } = await apiClient.get<User[]>('/users')
      return data
    },
  })
}

// Usage in component
function UsersPage() {
  const { data, isLoading, error, isError } = useUsers()
  
  if (isLoading) return <Spinner />
  if (isError) return <ErrorBoundary error={error} />
  
  return <DataTable data={data} />
}
```

### Query with Parameters

```tsx
export const useUser = (userId: string) => {
  return useQuery({
    queryKey: ['users', userId],
    queryFn: async () => {
      const { data } = await apiClient.get<User>(`/users/${userId}`)
      return data
    },
    enabled: !!userId, // Only run if userId is truthy
  })
}
```

### Paginated Query

```tsx
export const useUsersPaginated = (page: number, pageSize: number) => {
  return useQuery({
    queryKey: ['users', 'paginated', page, pageSize],
    queryFn: async () => {
      const { data } = await apiClient.get<PaginatedResponse<User>>('/users', {
        params: { page, pageSize },
      })
      return data
    },
    placeholderData: (previousData) => previousData, // Keep previous data while fetching
  })
}
```

### Infinite Query

```tsx
import { useInfiniteQuery } from '@tanstack/react-query'

export const useInfiniteUsers = () => {
  return useInfiniteQuery({
    queryKey: ['users', 'infinite'],
    queryFn: async ({ pageParam = 1 }) => {
      const { data } = await apiClient.get<PaginatedResponse<User>>('/users', {
        params: { page: pageParam, pageSize: 20 },
      })
      return data
    },
    getNextPageParam: (lastPage) => {
      if (lastPage.page < lastPage.totalPages) {
        return lastPage.page + 1
      }
      return undefined
    },
    initialPageParam: 1,
  })
}

// Usage
function UsersInfiniteList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteUsers()
  
  return (
    <div>
      {data?.pages.map((page) =>
        page.items.map((user) => <UserCard key={user.id} user={user} />)
      )}
      
      {hasNextPage && (
        <TkButton
          label={isFetchingNextPage ? 'Loading...' : 'Load More'}
          onClick={() => fetchNextPage()}
          disabled={isFetchingNextPage}
        />
      )}
    </div>
  )
}
```

### Dependent Queries

```tsx
export const useUserOrders = (userId: string) => {
  const { data: user } = useUser(userId)
  
  return useQuery({
    queryKey: ['orders', userId],
    queryFn: async () => {
      const { data } = await apiClient.get(`/users/${userId}/orders`)
      return data
    },
    enabled: !!user, // Only fetch orders if user is loaded
  })
}
```

### Parallel Queries

```tsx
function DashboardPage() {
  const usersQuery = useUsers()
  const productsQuery = useProducts()
  const ordersQuery = useOrders()
  
  if (usersQuery.isLoading || productsQuery.isLoading || ordersQuery.isLoading) {
    return <Spinner />
  }
  
  return (
    <div>
      <StatsCard title="Users" count={usersQuery.data?.length} />
      <StatsCard title="Products" count={productsQuery.data?.length} />
      <StatsCard title="Orders" count={ordersQuery.data?.length} />
    </div>
  )
}
```

## Mutation Patterns

### Basic Mutation

```tsx
import { useMutation, useQueryClient } from '@tanstack/react-query'

export const useCreateUser = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (data: CreateUserDto) => {
      const response = await apiClient.post<User>('/users', data)
      return response.data
    },
    onSuccess: () => {
      // Invalidate and refetch users query
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
    onError: (error) => {
      console.error('Failed to create user:', error)
    },
  })
}

// Usage
function CreateUserForm() {
  const createUser = useCreateUser()
  
  const handleSubmit = (data: CreateUserDto) => {
    createUser.mutate(data, {
      onSuccess: (user) => {
        toast.success(`User ${user.name} created successfully`)
        navigate({ to: '/users' })
      },
      onError: (error) => {
        toast.error('Failed to create user')
      },
    })
  }
  
  return (
    <DynamicForm
      schema={userSchema}
      onSubmit={handleSubmit}
      isLoading={createUser.isPending}
    />
  )
}
```

### Optimistic Updates

```tsx
export const useUpdateUser = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async ({ id, data }: { id: string; data: UpdateUserDto }) => {
      const response = await apiClient.put<User>(`/users/${id}`, data)
      return response.data
    },
    onMutate: async ({ id, data }) => {
      // Cancel outgoing queries
      await queryClient.cancelQueries({ queryKey: ['users', id] })
      
      // Snapshot previous value
      const previousUser = queryClient.getQueryData<User>(['users', id])
      
      // Optimistically update
      queryClient.setQueryData<User>(['users', id], (old) => ({
        ...old!,
        ...data,
      }))
      
      // Return context with snapshot
      return { previousUser }
    },
    onError: (err, variables, context) => {
      // Rollback on error
      if (context?.previousUser) {
        queryClient.setQueryData(['users', variables.id], context.previousUser)
      }
    },
    onSettled: (data, error, variables) => {
      // Refetch after error or success
      queryClient.invalidateQueries({ queryKey: ['users', variables.id] })
    },
  })
}
```

### Delete Mutation

```tsx
export const useDeleteUser = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (id: string) => {
      await apiClient.delete(`/users/${id}`)
    },
    onSuccess: (_, deletedId) => {
      // Remove from cache
      queryClient.setQueryData<User[]>(['users'], (old) =>
        old?.filter((user) => user.id !== deletedId)
      )
    },
  })
}
```

## Query Invalidation Strategies

### Invalidate All Queries

```tsx
queryClient.invalidateQueries()
```

### Invalidate Specific Query

```tsx
queryClient.invalidateQueries({ queryKey: ['users'] })
```

### Invalidate with Predicate

```tsx
queryClient.invalidateQueries({
  predicate: (query) => query.queryKey[0] === 'users' && query.queryKey[1] === userId,
})
```

### Refetch Queries

```tsx
queryClient.refetchQueries({ queryKey: ['users'] })
```

### Reset Queries

```tsx
queryClient.resetQueries({ queryKey: ['users'] })
```

## TanStack Router Setup

### Installation

```bash
npm install @tanstack/react-router @tanstack/router-devtools
```

### Basic Router Configuration

```tsx
// src/routes/index.tsx
import { createRouter, createRootRoute, createRoute } from '@tanstack/react-router'
import RootLayout from './layouts/RootLayout'
import DashboardPage from '@/pages/Dashboard'
import UsersPage from '@/pages/Users'
import UserDetailPage from '@/pages/Users/UserDetailPage'
import LoginPage from '@/pages/Auth/LoginPage'
import NotFoundPage from '@/pages/NotFoundPage'

// Root route
const rootRoute = createRootRoute({
  component: RootLayout,
})

// Index route
const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/',
  component: DashboardPage,
})

// Users routes
const usersRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/users',
  component: UsersPage,
})

const userDetailRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/users/$userId',
  component: UserDetailPage,
})

// Auth routes
const loginRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/login',
  component: LoginPage,
})

// 404 route
const notFoundRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '*',
  component: NotFoundPage,
})

// Build route tree
const routeTree = rootRoute.addChildren([
  indexRoute,
  usersRoute,
  userDetailRoute,
  loginRoute,
  notFoundRoute,
])

// Create router
export const router = createRouter({ routeTree })

// Register router for type safety
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}
```

### Root Layout with Auth Guards

```tsx
// src/routes/layouts/RootLayout.tsx
import { Outlet, useRouter } from '@tanstack/react-router'
import { useAuth } from '@/auth/useAuth'
import { useEffect } from 'react'

export default function RootLayout() {
  const { isAuthenticated } = useAuth()
  const router = useRouter()
  
  useEffect(() => {
    const publicPaths = ['/login', '/register', '/forgot-password']
    const currentPath = router.state.location.pathname
    
    if (!isAuthenticated && !publicPaths.includes(currentPath)) {
      router.navigate({ to: '/login' })
    }
  }, [isAuthenticated, router])
  
  return (
    <div className="min-h-screen bg-gray-50">
      <Outlet />
    </div>
  )
}
```

### Route with Loader (Data Prefetching)

```tsx
import { createRoute } from '@tanstack/react-router'
import { queryClient } from '@/main'
import { usersApi } from '@/api/endpoints/users'

const userDetailRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/users/$userId',
  loader: async ({ params }) => {
    // Prefetch user data
    await queryClient.ensureQueryData({
      queryKey: ['users', params.userId],
      queryFn: () => usersApi.getById(params.userId),
    })
  },
  component: UserDetailPage,
})
```

### Nested Routes with Layout

```tsx
// Authenticated layout route
const authenticatedRoute = createRoute({
  getParentRoute: () => rootRoute,
  id: 'authenticated',
  component: () => {
    const { isAuthenticated } = useAuth()
    const router = useRouter()
    
    if (!isAuthenticated) {
      router.navigate({ to: '/login' })
      return null
    }
    
    return (
      <div className="flex min-h-screen">
        <Sidebar />
        <main className="flex-1">
          <Header />
          <Outlet />
        </main>
      </div>
    )
  },
})

// Nested routes
const dashboardRoute = createRoute({
  getParentRoute: () => authenticatedRoute,
  path: '/dashboard',
  component: DashboardPage,
})

const usersRoute = createRoute({
  getParentRoute: () => authenticatedRoute,
  path: '/users',
  component: UsersPage,
})
```

### Lazy Loading Routes

```tsx
import { lazy } from 'react'
import { createRoute } from '@tanstack/react-router'

const DashboardPage = lazy(() => import('@/pages/Dashboard'))

const dashboardRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/dashboard',
  component: DashboardPage,
})
```

### Search Params Handling

```tsx
import { z } from 'zod'

const usersRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/users',
  validateSearch: z.object({
    page: z.number().optional().default(1),
    pageSize: z.number().optional().default(10),
    search: z.string().optional(),
    role: z.enum(['admin', 'user']).optional(),
  }),
  component: UsersPage,
})

// Usage in component
function UsersPage() {
  const { page, pageSize, search, role } = useSearch({ from: '/users' })
  const navigate = useNavigate({ from: '/users' })
  
  const { data } = useUsersPaginated(page, pageSize, { search, role })
  
  const handlePageChange = (newPage: number) => {
    navigate({ search: { page: newPage, pageSize, search, role } })
  }
  
  return <DataTable data={data} onPageChange={handlePageChange} />
}
```

### Navigation Examples

```tsx
import { useNavigate, Link } from '@tanstack/react-router'

function Navigation() {
  const navigate = useNavigate()
  
  // Programmatic navigation
  const goToUsers = () => {
    navigate({ to: '/users' })
  }
  
  const goToUserDetail = (userId: string) => {
    navigate({ to: '/users/$userId', params: { userId } })
  }
  
  const goToUsersWithSearch = () => {
    navigate({
      to: '/users',
      search: { page: 1, role: 'admin' },
    })
  }
  
  return (
    <div>
      {/* Declarative navigation */}
      <Link to="/">Home</Link>
      <Link to="/users">Users</Link>
      <Link to="/users/$userId" params={{ userId: '123' }}>
        User 123
      </Link>
      
      {/* Buttons */}
      <TkButton label="Go to Users" onClick={goToUsers} />
    </div>
  )
}
```

## Advanced Patterns

### Query Prefetching on Hover

```tsx
import { useQueryClient } from '@tanstack/react-query'
import { usersApi } from '@/api/endpoints/users'

function UserLink({ userId }: { userId: string }) {
  const queryClient = useQueryClient()
  
  const prefetchUser = () => {
    queryClient.prefetchQuery({
      queryKey: ['users', userId],
      queryFn: () => usersApi.getById(userId),
      staleTime: 1000 * 60, // Only prefetch if older than 1 minute
    })
  }
  
  return (
    <Link
      to="/users/$userId"
      params={{ userId }}
      onMouseEnter={prefetchUser}
      className="text-blue-600 hover:underline"
    >
      View User
    </Link>
  )
}
```

### Background Refetching

```tsx
export const useUsers = () => {
  return useQuery({
    queryKey: ['users'],
    queryFn: usersApi.getAll,
    refetchInterval: 1000 * 60, // Refetch every minute
    refetchIntervalInBackground: true, // Continue refetching when tab is not active
  })
}
```

### Suspense Mode

```tsx
export const useUser = (userId: string) => {
  return useSuspenseQuery({
    queryKey: ['users', userId],
    queryFn: () => usersApi.getById(userId),
  })
}

// Usage with Suspense boundary
function UserDetailPage() {
  return (
    <Suspense fallback={<Spinner />}>
      <UserDetail />
    </Suspense>
  )
}

function UserDetail() {
  const { userId } = useParams({ from: '/users/$userId' })
  const { data: user } = useUser(userId) // No loading state needed
  
  return <div>{user.name}</div>
}
```

### Query Cancellation

```tsx
export const useSearchUsers = (searchTerm: string) => {
  return useQuery({
    queryKey: ['users', 'search', searchTerm],
    queryFn: async ({ signal }) => {
      const { data } = await apiClient.get('/users/search', {
        params: { q: searchTerm },
        signal, // Pass AbortSignal to axios
      })
      return data
    },
    enabled: searchTerm.length > 2,
  })
}
```

### Global Loading State

```tsx
import { useIsFetching, useIsMutating } from '@tanstack/react-query'

function GlobalLoadingIndicator() {
  const isFetching = useIsFetching()
  const isMutating = useIsMutating()
  
  if (!isFetching && !isMutating) return null
  
  return (
    <div className="fixed top-0 left-0 right-0 h-1 bg-blue-600 animate-pulse" />
  )
}
```

## Error Handling

### Query-level Error Handling

```tsx
export const useUsers = () => {
  return useQuery({
    queryKey: ['users'],
    queryFn: usersApi.getAll,
    throwOnError: false, // Handle errors at component level
  })
}

function UsersPage() {
  const { data, error, isError } = useUsers()
  
  if (isError) {
    return <ErrorMessage error={error} />
  }
  
  return <DataTable data={data} />
}
```

### Global Error Handling

```tsx
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      onError: (error) => {
        toast.error('An error occurred while fetching data')
        console.error(error)
      },
    },
    mutations: {
      onError: (error) => {
        toast.error('An error occurred while saving data')
        console.error(error)
      },
    },
  },
})
```

## Best Practices

1. **Query Keys:** Use arrays with hierarchical structure: `['users']`, `['users', userId]`, `['users', userId, 'orders']`
2. **Stale Time:** Set appropriate stale times based on data volatility
3. **Cache Time (gcTime):** Keep cache longer than stale time for better UX
4. **Refetch on Window Focus:** Disable for most queries to reduce server load
5. **Optimistic Updates:** Use for better perceived performance
6. **Query Invalidation:** Invalidate related queries after mutations
7. **Error Boundaries:** Use React error boundaries for graceful error handling
8. **Loading States:** Always handle loading, error, and success states
9. **Type Safety:** Use TypeScript generics for query and mutation data types
10. **DevTools:** Keep React Query DevTools enabled in development

## Summary

TanStack Query and Router provide:

- **Declarative data fetching** - No manual loading/error states
- **Automatic caching** - Reduces server load and improves UX
- **Background updates** - Keep data fresh automatically
- **Optimistic updates** - Instant UI feedback
- **Type-safe routing** - Catch routing errors at compile time
- **Prefetching** - Improve perceived performance
- **Request deduplication** - Automatic optimization

Use these patterns consistently across your application for maintainable, performant code.