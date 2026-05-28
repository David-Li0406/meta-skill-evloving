---
name: swr
description: SWR for lightweight data fetching and caching
workflows:
  - id: swr-setup
    template: wf-creation
    phase: Production
    name: Setup SWR data fetching
    duration: 0.5 jour
---

# SWR - Data Fetching Léger

## Rôle

Implémentation de SWR (Stale-While-Revalidate) pour le data fetching et caching dans React.

## Tu NE fais PAS

- ❌ Implémenter les APIs backend → `backend-developer`
- ❌ Configurer les librairies de state management (Zustand, Redux) → `../state/`
- ❌ Implémenter l'UI des composants → `../components/`
- ❌ Définir la stratégie de tests → `testing-process`

## Installation

```bash
npm install swr
```

## Principe SWR

1. Retourner les données du cache (stale)
2. Envoyer la requête (revalidate)
3. Mettre à jour avec les nouvelles données

## useSWR - Lecture de Base

### Fetcher global

```tsx
// lib/fetcher.ts
export const fetcher = async (url: string) => {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error('Fetch failed');
  }
  return response.json();
};
```

### Configuration globale

```tsx
// App.tsx
import { SWRConfig } from 'swr';
import { fetcher } from './lib/fetcher';

function App() {
  return (
    <SWRConfig
      value={{
        fetcher,
        revalidateOnFocus: true,
        revalidateOnReconnect: true,
        dedupingInterval: 2000,
        errorRetryCount: 3,
      }}
    >
      <MainApp />
    </SWRConfig>
  );
}
```

### Usage basique

```tsx
import useSWR from 'swr';

interface User {
  id: string;
  name: string;
  email: string;
}

function UserProfile({ userId }: { userId: string }) {
  const { data, error, isLoading, mutate } = useSWR<User>(
    `/api/users/${userId}`
  );

  if (isLoading) return <Spinner />;
  if (error) return <Error message={error.message} />;
  if (!data) return null;

  return (
    <div>
      <h1>{data.name}</h1>
      <p>{data.email}</p>
      <button onClick={() => mutate()}>Refresh</button>
    </div>
  );
}
```

## Options de Configuration

```tsx
const { data, error, isLoading, isValidating, mutate } = useSWR(key, fetcher, {
  // Revalidation
  revalidateOnFocus: true,
  revalidateOnReconnect: true,
  revalidateIfStale: true,
  refreshInterval: 0, // Polling en ms (0 = désactivé)
  refreshWhenHidden: false,
  refreshWhenOffline: false,

  // Retry
  errorRetryCount: 3,
  errorRetryInterval: 5000,

  // Cache & Deduplication
  dedupingInterval: 2000,
  focusThrottleInterval: 5000,

  // Performance
  keepPreviousData: true,
  suspense: false,

  // Callbacks
  onSuccess: (data, key, config) => {},
  onError: (error, key, config) => {},
  onErrorRetry: (error, key, config, revalidate, { retryCount }) => {},
});
```

## Conditional Fetching

```tsx
// Conditionnel avec null
const { data } = useSWR(userId ? `/api/users/${userId}` : null);

// Avec fonction
const { data } = useSWR(() => (isReady ? `/api/data` : null));
```

## Mutations

### Mutation locale

```tsx
function TodoItem({ todo }: { todo: Todo }) {
  const { mutate } = useSWRConfig();

  const handleToggle = async () => {
    // 1. Mise à jour optimiste
    mutate(
      '/api/todos',
      (todos: Todo[]) =>
        todos.map((t) =>
          t.id === todo.id ? { ...t, completed: !t.completed } : t
        ),
      { revalidate: false }
    );

    // 2. Appel API
    try {
      await fetch(`/api/todos/${todo.id}`, {
        method: 'PATCH',
        body: JSON.stringify({ completed: !todo.completed }),
      });
    } catch {
      // 3. Rollback en cas d'erreur
      mutate('/api/todos');
    }
  };

  return (
    <div onClick={handleToggle}>
      {todo.completed ? '✓' : '○'} {todo.text}
    </div>
  );
}
```

### Avec useSWRMutation

```tsx
import useSWRMutation from 'swr/mutation';

async function updateUser(url: string, { arg }: { arg: Partial<User> }) {
  const response = await fetch(url, {
    method: 'PUT',
    body: JSON.stringify(arg),
  });
  return response.json();
}

function UpdateUserForm({ userId }: { userId: string }) {
  const { trigger, isMutating, error } = useSWRMutation(
    `/api/users/${userId}`,
    updateUser
  );

  const handleSubmit = async (data: Partial<User>) => {
    try {
      await trigger(data);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* ... */}
      <button disabled={isMutating}>Save</button>
    </form>
  );
}
```

## Pagination

### Page-based

```tsx
function PaginatedPosts() {
  const [page, setPage] = useState(1);

  const { data, isLoading } = useSWR<Post[]>(
    `/api/posts?page=${page}`,
    { keepPreviousData: true }
  );

  return (
    <div>
      {data?.map((post) => <PostCard key={post.id} post={post} />)}

      <button onClick={() => setPage((p) => p - 1)} disabled={page === 1}>
        Previous
      </button>
      <button onClick={() => setPage((p) => p + 1)}>Next</button>
    </div>
  );
}
```

### Infinite Loading

```tsx
import useSWRInfinite from 'swr/infinite';

interface PostsResponse {
  posts: Post[];
  nextCursor: string | null;
}

function InfinitePosts() {
  const getKey = (pageIndex: number, previousPageData: PostsResponse | null) => {
    if (previousPageData && !previousPageData.nextCursor) return null;
    if (pageIndex === 0) return '/api/posts';
    return `/api/posts?cursor=${previousPageData?.nextCursor}`;
  };

  const { data, size, setSize, isLoading, isValidating } = useSWRInfinite<PostsResponse>(
    getKey
  );

  const posts = data?.flatMap((page) => page.posts) ?? [];
  const hasMore = data?.[data.length - 1]?.nextCursor != null;

  return (
    <div>
      {posts.map((post) => <PostCard key={post.id} post={post} />)}

      {hasMore && (
        <button onClick={() => setSize(size + 1)} disabled={isValidating}>
          {isValidating ? 'Loading...' : 'Load More'}
        </button>
      )}
    </div>
  );
}
```

## Prefetching

```tsx
import { preload } from 'swr';
import { fetcher } from './lib/fetcher';

// Prefetch avant navigation
function UserLink({ userId }: { userId: string }) {
  return (
    <Link
      to={`/users/${userId}`}
      onMouseEnter={() => preload(`/api/users/${userId}`, fetcher)}
    >
      View Profile
    </Link>
  );
}

// Ou avec useSWR
function prefetchUser(userId: string) {
  mutate(`/api/users/${userId}`, fetch(`/api/users/${userId}`).then(r => r.json()));
}
```

## Suspense Mode

```tsx
import useSWR from 'swr';

function Profile() {
  const { data } = useSWR('/api/user', fetcher, { suspense: true });
  return <div>Hello, {data.name}</div>;
}

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Profile />
    </Suspense>
  );
}
```

## Custom Hooks

```tsx
// hooks/useUser.ts
export function useUser(id: string | null) {
  const { data, error, isLoading, mutate } = useSWR<User>(
    id ? `/api/users/${id}` : null
  );

  return {
    user: data,
    isLoading,
    isError: !!error,
    error,
    mutate,
  };
}

// hooks/useUsers.ts
export function useUsers(filters?: UserFilters) {
  const params = new URLSearchParams(filters as Record<string, string>);
  return useSWR<User[]>(`/api/users?${params}`);
}
```

## Cache Manipulation

```tsx
import { useSWRConfig } from 'swr';

function useManualCache() {
  const { mutate, cache } = useSWRConfig();

  // Mettre à jour une clé
  const updateUser = (user: User) => {
    mutate(`/api/users/${user.id}`, user, { revalidate: false });
  };

  // Invalider et refetch
  const refreshUsers = () => {
    mutate('/api/users');
  };

  // Effacer le cache
  const clearCache = () => {
    mutate(() => true, undefined, { revalidate: false });
  };

  return { updateUser, refreshUsers, clearCache };
}
```

## Comparaison SWR vs React Query

| Fonctionnalité | SWR | React Query |
|----------------|-----|-------------|
| Taille | ~4 KB | ~12 KB |
| Mutations | Basique | Avancé |
| Devtools | Limité | Excellent |
| Infinite | Oui | Oui |
| Optimistic | Manuel | Intégré |
| Prefetching | Oui | Oui |

## Bonnes Pratiques

1. **Fetcher global** - DRY, gestion d'erreurs centralisée
2. **Custom hooks** - Encapsuler la logique
3. **Keys cohérentes** - URLs ou strings uniques
4. **keepPreviousData** - UX de pagination fluide
5. **Conditional fetching** - `null` pour désactiver

## Voir aussi

- `react-query.md` - Alternative plus complète
- `suspense.md` - Intégration Suspense
- `../state/context.md` - Pour le client state

## Livrables

| Livrable | Description |
|----------|-------------|
| useSWR hooks | Custom hooks avec useSWR/useSWRMutation |
| Configuration SWR | SWRConfig avec fetcher et options revalidation |
| Gestion cache | Stratégies de mutate et invalidation |
