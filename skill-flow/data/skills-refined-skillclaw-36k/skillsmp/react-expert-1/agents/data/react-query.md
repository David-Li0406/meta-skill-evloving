---
name: react-query
description: TanStack Query for server state management and data fetching
workflows:
  - id: react-query-setup
    template: wf-creation
    phase: Production
    name: Setup React Query
    duration: 0.5-1 jour
---

# React Query (TanStack Query) - Server State Management

## Rôle

Implémentation de TanStack Query pour le data fetching, caching et synchronisation avec le serveur.

## Tu NE fais PAS

- ❌ Implémenter les APIs backend → `backend-developer`
- ❌ Configurer les librairies de state management (Zustand, Redux) → `../state/`
- ❌ Implémenter l'UI des composants → `../components/`
- ❌ Définir la stratégie de tests → `testing-process`

## Installation

```bash
npm install @tanstack/react-query
npm install @tanstack/react-query-devtools  # DevTools
```

## Configuration

### QueryClient

```tsx
// lib/queryClient.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      gcTime: 1000 * 60 * 30, // 30 minutes (anciennement cacheTime)
      retry: 3,
      refetchOnWindowFocus: true,
    },
    mutations: {
      retry: 1,
    },
  },
});
```

### Provider

```tsx
// main.tsx
import { QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { queryClient } from './lib/queryClient';

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <MainApp />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

## useQuery - Lectures

### Query de base

```tsx
import { useQuery } from '@tanstack/react-query';

interface User {
  id: string;
  name: string;
  email: string;
}

async function fetchUser(userId: string): Promise<User> {
  const response = await fetch(`/api/users/${userId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch user');
  }
  return response.json();
}

function UserProfile({ userId }: { userId: string }) {
  const {
    data: user,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
    enabled: !!userId, // N'exécute pas si userId est falsy
  });

  if (isLoading) return <Spinner />;
  if (isError) return <Error message={error.message} onRetry={refetch} />;

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

### Query avec options avancées

```tsx
const { data, status, fetchStatus } = useQuery({
  queryKey: ['products', { category, page, sort }],
  queryFn: () => fetchProducts({ category, page, sort }),

  // Timing
  staleTime: 1000 * 60 * 5, // Données fraîches pendant 5 min
  gcTime: 1000 * 60 * 30,   // Gardé en cache 30 min

  // Refetch
  refetchOnMount: true,
  refetchOnWindowFocus: true,
  refetchInterval: false, // Ou nombre en ms pour polling

  // Transformation
  select: (data) => data.filter((p) => p.inStock),

  // Données initiales
  initialData: cachedProducts,
  placeholderData: previousProducts, // keepPreviousData

  // Retry
  retry: 3,
  retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
});
```

## useMutation - Écritures

### Mutation de base

```tsx
import { useMutation, useQueryClient } from '@tanstack/react-query';

async function createUser(data: CreateUserInput): Promise<User> {
  const response = await fetch('/api/users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error('Failed to create user');
  return response.json();
}

function CreateUserForm() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: createUser,
    onSuccess: (newUser) => {
      // Invalider et refetch
      queryClient.invalidateQueries({ queryKey: ['users'] });
      // Ou mise à jour manuelle du cache
      queryClient.setQueryData(['users'], (old: User[]) => [...old, newUser]);
    },
    onError: (error) => {
      toast.error(error.message);
    },
  });

  const handleSubmit = (data: CreateUserInput) => {
    mutation.mutate(data);
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* ... */}
      <button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? 'Creating...' : 'Create User'}
      </button>
    </form>
  );
}
```

### Optimistic Updates

```tsx
const mutation = useMutation({
  mutationFn: updateTodo,
  onMutate: async (newTodo) => {
    // Annuler les queries en cours
    await queryClient.cancelQueries({ queryKey: ['todos'] });

    // Snapshot précédent
    const previousTodos = queryClient.getQueryData(['todos']);

    // Mise à jour optimiste
    queryClient.setQueryData(['todos'], (old: Todo[]) =>
      old.map((todo) =>
        todo.id === newTodo.id ? { ...todo, ...newTodo } : todo
      )
    );

    // Retourner le contexte avec le snapshot
    return { previousTodos };
  },
  onError: (_error, _newTodo, context) => {
    // Rollback en cas d'erreur
    queryClient.setQueryData(['todos'], context?.previousTodos);
  },
  onSettled: () => {
    // Refetch pour s'assurer de la sync
    queryClient.invalidateQueries({ queryKey: ['todos'] });
  },
});
```

## Infinite Queries

```tsx
import { useInfiniteQuery } from '@tanstack/react-query';

interface PostsPage {
  posts: Post[];
  nextCursor: string | null;
}

function InfinitePostsList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
  } = useInfiniteQuery({
    queryKey: ['posts'],
    queryFn: ({ pageParam }) => fetchPosts({ cursor: pageParam }),
    initialPageParam: null as string | null,
    getNextPageParam: (lastPage) => lastPage.nextCursor,
  });

  if (isLoading) return <Spinner />;

  const allPosts = data?.pages.flatMap((page) => page.posts) ?? [];

  return (
    <div>
      {allPosts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}

      {hasNextPage && (
        <button
          onClick={() => fetchNextPage()}
          disabled={isFetchingNextPage}
        >
          {isFetchingNextPage ? 'Loading...' : 'Load More'}
        </button>
      )}
    </div>
  );
}
```

## Query Keys

### Conventions

```tsx
// Simple
['users']

// Avec ID
['user', userId]

// Avec filtres (objet)
['users', { status: 'active', page: 1 }]

// Hiérarchie
['users', userId, 'posts']
['users', userId, 'posts', postId]
```

### Invalidation

```tsx
// Toutes les queries "users"
queryClient.invalidateQueries({ queryKey: ['users'] });

// Query spécifique
queryClient.invalidateQueries({ queryKey: ['user', userId] });

// Avec predicate
queryClient.invalidateQueries({
  predicate: (query) =>
    query.queryKey[0] === 'posts' && query.state.data?.length > 10,
});
```

## Parallel & Dependent Queries

### Queries parallèles

```tsx
function Dashboard() {
  // Ces queries s'exécutent en parallèle
  const usersQuery = useQuery({ queryKey: ['users'], queryFn: fetchUsers });
  const postsQuery = useQuery({ queryKey: ['posts'], queryFn: fetchPosts });
  const statsQuery = useQuery({ queryKey: ['stats'], queryFn: fetchStats });

  // Ou avec useQueries
  const results = useQueries({
    queries: [
      { queryKey: ['users'], queryFn: fetchUsers },
      { queryKey: ['posts'], queryFn: fetchPosts },
      { queryKey: ['stats'], queryFn: fetchStats },
    ],
  });
}
```

### Queries dépendantes

```tsx
function UserPosts({ userId }: { userId: string }) {
  // Première query
  const userQuery = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });

  // Query dépendante
  const postsQuery = useQuery({
    queryKey: ['posts', userId],
    queryFn: () => fetchUserPosts(userId),
    enabled: !!userQuery.data, // N'exécute que si user est chargé
  });
}
```

## Prefetching

```tsx
// Dans un event handler
function UserList({ users }: { users: User[] }) {
  const queryClient = useQueryClient();

  const prefetchUser = (userId: string) => {
    queryClient.prefetchQuery({
      queryKey: ['user', userId],
      queryFn: () => fetchUser(userId),
      staleTime: 1000 * 60 * 5,
    });
  };

  return (
    <ul>
      {users.map((user) => (
        <li
          key={user.id}
          onMouseEnter={() => prefetchUser(user.id)}
        >
          <Link to={`/users/${user.id}`}>{user.name}</Link>
        </li>
      ))}
    </ul>
  );
}
```

## Suspense Mode

```tsx
import { useSuspenseQuery } from '@tanstack/react-query';

function UserProfile({ userId }: { userId: string }) {
  // Pas besoin de gérer isLoading - Suspense s'en charge
  const { data: user } = useSuspenseQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });

  return <div>{user.name}</div>;
}

// Usage avec Suspense
function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <UserProfile userId="123" />
    </Suspense>
  );
}
```

## Custom Hooks

```tsx
// hooks/useUser.ts
export function useUser(userId: string) {
  return useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
    enabled: !!userId,
  });
}

// hooks/useUpdateUser.ts
export function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateUser,
    onSuccess: (data, variables) => {
      queryClient.setQueryData(['user', variables.id], data);
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
}
```

## Bonnes Pratiques

1. **Query keys cohérentes** - Hiérarchie prévisible
2. **Custom hooks** - Encapsuler les queries
3. **staleTime approprié** - Réduire les refetch inutiles
4. **Optimistic updates** - UX réactive
5. **DevTools** - Toujours en développement

## Voir aussi

- `swr.md` - Alternative légère
- `suspense.md` - Intégration Suspense
- `../state/zustand.md` - Pour le client state

## Livrables

| Livrable | Description |
|----------|-------------|
| Query hooks | Custom hooks avec useQuery/useMutation |
| Configuration cache | QueryClient setup avec staleTime et gcTime |
| Gestion d'erreurs | Error handling et retry logic |
