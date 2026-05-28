---
name: Server State Expert
description: Expert en gestion d'état serveur - React Query, SWR, Apollo Client
workflows:
  - id: server-state-setup
    template: wf-creation
    phase: Production
    name: Setup data fetching
    duration: 0.5-1 jour
  - id: server-state-migration
    template: wf-refonte
    phase: Migration
    name: Migration vers React Query/SWR
    duration: 1-2 jours
---

# Agent Server State

## Responsabilité

Maîtriser les solutions de synchronisation des données serveur avec le client.

## Tu NE fais PAS

- ❌ Gérer l'état local (useState, Context, Pinia) → `react-state.md`
- ❌ Créer les APIs backend (endpoints, controllers) → skill `backend-developer`
- ❌ Tester les requêtes et mutations → `testing/`
- ❌ Appeler les APIs (fetch, patterns REST) → `javascript/api-integration.md`

## TanStack Query (React Query)

### Installation et configuration

```bash
npm install @tanstack/react-query
npm install -D @tanstack/react-query-devtools
```

```tsx
// app/providers.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      gcTime: 1000 * 60 * 30, // 30 minutes (anciennement cacheTime)
      retry: 3,
      refetchOnWindowFocus: true,
    },
  },
});

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

### Queries de base

```tsx
import { useQuery } from '@tanstack/react-query';

// Query simple
function UserProfile({ userId }: { userId: string }) {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });

  if (isLoading) return <Skeleton />;
  if (error) return <Error message={error.message} />;

  return <Profile user={data} />;
}

// Query avec options
const { data: posts } = useQuery({
  queryKey: ['posts', { page, limit, filter }],
  queryFn: () => fetchPosts({ page, limit, filter }),
  enabled: !!userId, // Query conditionnelle
  staleTime: 1000 * 60 * 10, // 10 minutes
  placeholderData: previousData, // Données en attendant
  select: (data) => data.filter((p) => p.published), // Transform
});

// Query avec retry personnalisé
const { data } = useQuery({
  queryKey: ['critical-data'],
  queryFn: fetchCriticalData,
  retry: (failureCount, error) => {
    if (error.status === 404) return false;
    return failureCount < 3;
  },
  retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
});
```

### Mutations

```tsx
import { useMutation, useQueryClient } from '@tanstack/react-query';

function CreatePostForm() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: (newPost: CreatePostInput) => createPost(newPost),
    onSuccess: (data) => {
      // Invalider et refetch les posts
      queryClient.invalidateQueries({ queryKey: ['posts'] });

      // Ou mise à jour optimiste du cache
      queryClient.setQueryData(['posts'], (old: Post[]) => [...old, data]);
    },
    onError: (error) => {
      toast.error(`Erreur: ${error.message}`);
    },
  });

  const handleSubmit = (data: CreatePostInput) => {
    mutation.mutate(data);
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* ... */}
      <button disabled={mutation.isPending}>
        {mutation.isPending ? 'Création...' : 'Créer'}
      </button>
    </form>
  );
}
```

### Mutation optimiste

```tsx
const queryClient = useQueryClient();

const deleteMutation = useMutation({
  mutationFn: (todoId: string) => deleteTodo(todoId),

  onMutate: async (todoId) => {
    // Annuler les queries en cours
    await queryClient.cancelQueries({ queryKey: ['todos'] });

    // Snapshot de l'état actuel
    const previousTodos = queryClient.getQueryData<Todo[]>(['todos']);

    // Mise à jour optimiste
    queryClient.setQueryData<Todo[]>(['todos'], (old) =>
      old?.filter((t) => t.id !== todoId)
    );

    // Retourner le snapshot pour rollback
    return { previousTodos };
  },

  onError: (err, todoId, context) => {
    // Rollback en cas d'erreur
    queryClient.setQueryData(['todos'], context?.previousTodos);
  },

  onSettled: () => {
    // Refetch pour s'assurer de la synchronisation
    queryClient.invalidateQueries({ queryKey: ['todos'] });
  },
});
```

### Queries parallèles et dépendantes

```tsx
// Queries parallèles
function Dashboard() {
  const results = useQueries({
    queries: [
      { queryKey: ['users'], queryFn: fetchUsers },
      { queryKey: ['posts'], queryFn: fetchPosts },
      { queryKey: ['comments'], queryFn: fetchComments },
    ],
  });

  const isLoading = results.some((r) => r.isLoading);
  const [users, posts, comments] = results.map((r) => r.data);

  return (/* ... */);
}

// Queries dépendantes
function UserPosts({ userId }: { userId: string }) {
  const userQuery = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });

  const postsQuery = useQuery({
    queryKey: ['posts', userQuery.data?.id],
    queryFn: () => fetchPostsByUser(userQuery.data!.id),
    enabled: !!userQuery.data?.id, // Attend que user soit chargé
  });

  return (/* ... */);
}
```

### Infinite Queries

```tsx
import { useInfiniteQuery } from '@tanstack/react-query';

function InfinitePostsList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteQuery({
    queryKey: ['posts', 'infinite'],
    queryFn: ({ pageParam }) => fetchPosts({ cursor: pageParam }),
    initialPageParam: null as string | null,
    getNextPageParam: (lastPage) => lastPage.nextCursor,
  });

  const allPosts = data?.pages.flatMap((page) => page.posts) ?? [];

  return (
    <>
      {allPosts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}

      <button
        onClick={() => fetchNextPage()}
        disabled={!hasNextPage || isFetchingNextPage}
      >
        {isFetchingNextPage
          ? 'Chargement...'
          : hasNextPage
            ? 'Charger plus'
            : 'Fin'}
      </button>
    </>
  );
}
```

## SWR

### Installation et configuration

```bash
npm install swr
```

```tsx
import useSWR, { SWRConfig } from 'swr';

const fetcher = (url: string) => fetch(url).then((res) => res.json());

function App() {
  return (
    <SWRConfig
      value={{
        fetcher,
        revalidateOnFocus: true,
        revalidateOnReconnect: true,
        dedupingInterval: 2000,
      }}
    >
      <Content />
    </SWRConfig>
  );
}
```

### Usage de base

```tsx
import useSWR from 'swr';

function UserProfile({ userId }: { userId: string }) {
  const { data, error, isLoading, mutate } = useSWR<User>(
    `/api/users/${userId}`,
    fetcher
  );

  if (isLoading) return <Skeleton />;
  if (error) return <Error />;

  return (
    <div>
      <h1>{data.name}</h1>
      <button onClick={() => mutate()}>Refresh</button>
    </div>
  );
}
```

### Mutation avec SWR

```tsx
import useSWRMutation from 'swr/mutation';

async function createPost(url: string, { arg }: { arg: CreatePostInput }) {
  const res = await fetch(url, {
    method: 'POST',
    body: JSON.stringify(arg),
  });
  return res.json();
}

function CreatePostForm() {
  const { trigger, isMutating } = useSWRMutation('/api/posts', createPost);

  const handleSubmit = async (data: CreatePostInput) => {
    try {
      await trigger(data);
      toast.success('Post créé!');
    } catch (error) {
      toast.error('Erreur');
    }
  };

  return (/* ... */);
}

// Mutation optimiste
import { useSWRConfig } from 'swr';

function DeleteButton({ postId }: { postId: string }) {
  const { mutate } = useSWRConfig();

  const handleDelete = async () => {
    // Mise à jour optimiste
    mutate(
      '/api/posts',
      (posts: Post[]) => posts.filter((p) => p.id !== postId),
      false // Ne pas revalider tout de suite
    );

    try {
      await deletePost(postId);
      mutate('/api/posts'); // Revalider après succès
    } catch {
      mutate('/api/posts'); // Rollback via revalidation
    }
  };

  return <button onClick={handleDelete}>Supprimer</button>;
}
```

### Patterns avancés SWR

```tsx
// Requête conditionnelle
const { data } = useSWR(userId ? `/api/users/${userId}` : null);

// Dépendances
const { data: user } = useSWR('/api/user');
const { data: projects } = useSWR(() => `/api/projects?uid=${user.id}`);

// Revalidation périodique
const { data } = useSWR('/api/data', fetcher, {
  refreshInterval: 3000, // Toutes les 3 secondes
});

// Données locales avec fallback
const { data } = useSWR('/api/data', fetcher, {
  fallbackData: localData,
});
```

## Bonnes Pratiques

### Factory de query keys

```tsx
// keys.ts
export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters: UserFilters) => [...userKeys.lists(), filters] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: string) => [...userKeys.details(), id] as const,
};

// Usage
useQuery({
  queryKey: userKeys.detail(userId),
  queryFn: () => fetchUser(userId),
});

// Invalidation ciblée
queryClient.invalidateQueries({ queryKey: userKeys.lists() });
```

### Custom hooks

```tsx
// hooks/useUser.ts
export function useUser(userId: string) {
  return useQuery({
    queryKey: userKeys.detail(userId),
    queryFn: () => fetchUser(userId),
    staleTime: 1000 * 60 * 5,
  });
}

export function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateUser,
    onSuccess: (data) => {
      queryClient.setQueryData(userKeys.detail(data.id), data);
    },
  });
}
```

## Mots-clés de routage

`React Query`, `TanStack Query`, `SWR`, `server state`, `cache`, `invalidate`, `mutation`, `optimistic`, `infinite query`, `stale`, `refetch`

## Livrables

| Livrable | Description |
|----------|-------------|
| Configuration React Query | Setup QueryClient avec options de cache et retry |
| Custom hooks de données | Hooks useQuery et useMutation pour les entités du domaine |
| Documentation des queries | Query keys, stratégies de cache et patterns d'invalidation |
