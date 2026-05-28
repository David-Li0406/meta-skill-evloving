---
name: client-fetching
description: Fetching côté client avec SWR et React Query
workflows:
  - id: client-fetching-impl
    template: wf-creation
    phase: Production
    name: Implémentation client fetching
    duration: 0.5 jour
---

# Client-Side Fetching

Tu es l'agent responsable du **data fetching côté client**.

## Ta Responsabilité Unique

Implémenter le fetching côté client avec SWR, React Query ou fetch.

## Tu NE fais PAS

- ❌ Server-side fetching → `data-fetching.md`
- ❌ Server Actions → `server-actions.md`
- ❌ State management global → `react-expert`
- ❌ WebSockets/real-time → Spécialisé

## Input Attendu

- Données à fetcher côté client
- Besoins de cache/revalidation
- UX de chargement

## Output Produit

- Code de fetching client
- Configuration de cache
- Gestion loading/error

## Quand Utiliser Client Fetching

```
✅ Données utilisateur après auth
✅ Infinite scroll / pagination
✅ Polling / real-time
✅ Données après interaction
✅ Dashboards avec refresh

❌ Données initiales de page (préférer SSR)
❌ SEO-critical content
❌ Données statiques
```

## SWR (Stale-While-Revalidate)

### Installation

```bash
npm install swr
```

### Utilisation Basique

```tsx
'use client'

import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then(res => res.json())

export function UserProfile() {
  const { data, error, isLoading } = useSWR('/api/user', fetcher)

  if (isLoading) return <div>Chargement...</div>
  if (error) return <div>Erreur de chargement</div>

  return <div>Bonjour {data.name}</div>
}
```

### Configuration Globale

```tsx
// app/providers.tsx
'use client'

import { SWRConfig } from 'swr'

const fetcher = async (url: string) => {
  const res = await fetch(url)
  if (!res.ok) throw new Error('Erreur fetch')
  return res.json()
}

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <SWRConfig
      value={{
        fetcher,
        revalidateOnFocus: true,
        revalidateOnReconnect: true,
        dedupingInterval: 2000,
      }}
    >
      {children}
    </SWRConfig>
  )
}

// app/layout.tsx
import { Providers } from './providers'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
```

### Mutation avec SWR

```tsx
'use client'

import useSWR, { useSWRConfig } from 'swr'

export function TodoList() {
  const { data: todos, mutate } = useSWR('/api/todos')
  const { mutate: globalMutate } = useSWRConfig()

  async function addTodo(title: string) {
    // Optimistic update
    mutate(
      async () => {
        const res = await fetch('/api/todos', {
          method: 'POST',
          body: JSON.stringify({ title }),
        })
        return res.json()
      },
      {
        optimisticData: [...todos, { id: 'temp', title, completed: false }],
        rollbackOnError: true,
      }
    )
  }

  return (
    <div>
      {todos?.map(todo => <TodoItem key={todo.id} todo={todo} />)}
      <AddTodoForm onAdd={addTodo} />
    </div>
  )
}
```

### SWR Infinite (Pagination)

```tsx
'use client'

import useSWRInfinite from 'swr/infinite'

const PAGE_SIZE = 10

export function InfinitePostList() {
  const getKey = (pageIndex: number, previousPageData: any) => {
    if (previousPageData && !previousPageData.length) return null
    return `/api/posts?page=${pageIndex}&limit=${PAGE_SIZE}`
  }

  const { data, size, setSize, isLoading, isValidating } = useSWRInfinite(getKey)

  const posts = data ? data.flat() : []
  const isLoadingMore = isLoading || (size > 0 && data && typeof data[size - 1] === 'undefined')
  const isEmpty = data?.[0]?.length === 0
  const isReachingEnd = isEmpty || (data && data[data.length - 1]?.length < PAGE_SIZE)

  return (
    <div>
      {posts.map(post => <PostCard key={post.id} post={post} />)}

      <button
        onClick={() => setSize(size + 1)}
        disabled={isLoadingMore || isReachingEnd}
      >
        {isLoadingMore ? 'Chargement...' : isReachingEnd ? 'Fin' : 'Charger plus'}
      </button>
    </div>
  )
}
```

## React Query (TanStack Query)

### Installation

```bash
npm install @tanstack/react-query
```

### Configuration

```tsx
// app/providers.tsx
'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useState } from 'react'

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60 * 1000, // 1 minute
        gcTime: 5 * 60 * 1000, // 5 minutes
      },
    },
  }))

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )
}
```

### Utilisation Basique

```tsx
'use client'

import { useQuery } from '@tanstack/react-query'

async function fetchUser() {
  const res = await fetch('/api/user')
  if (!res.ok) throw new Error('Network error')
  return res.json()
}

export function UserProfile() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['user'],
    queryFn: fetchUser,
  })

  if (isLoading) return <div>Chargement...</div>
  if (error) return <div>Erreur: {error.message}</div>

  return <div>Bonjour {data.name}</div>
}
```

### Mutations avec React Query

```tsx
'use client'

import { useMutation, useQueryClient } from '@tanstack/react-query'

export function AddTodoButton() {
  const queryClient = useQueryClient()

  const mutation = useMutation({
    mutationFn: (newTodo: { title: string }) =>
      fetch('/api/todos', {
        method: 'POST',
        body: JSON.stringify(newTodo),
      }).then(res => res.json()),
    onSuccess: () => {
      // Invalider et refetch
      queryClient.invalidateQueries({ queryKey: ['todos'] })
    },
  })

  return (
    <button
      onClick={() => mutation.mutate({ title: 'Nouvelle tâche' })}
      disabled={mutation.isPending}
    >
      {mutation.isPending ? 'Ajout...' : 'Ajouter'}
    </button>
  )
}
```

## Fetch API Native

### Hook Personnalisé

```tsx
// hooks/useFetch.ts
'use client'

import { useState, useEffect } from 'react'

export function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    const controller = new AbortController()

    async function fetchData() {
      try {
        setIsLoading(true)
        const res = await fetch(url, { signal: controller.signal })
        if (!res.ok) throw new Error('Fetch error')
        const json = await res.json()
        setData(json)
      } catch (err) {
        if (err instanceof Error && err.name !== 'AbortError') {
          setError(err)
        }
      } finally {
        setIsLoading(false)
      }
    }

    fetchData()

    return () => controller.abort()
  }, [url])

  return { data, isLoading, error }
}

// Utilisation
export function Component() {
  const { data, isLoading, error } = useFetch<User>('/api/user')
  // ...
}
```

## Polling Pattern

```tsx
'use client'

import useSWR from 'swr'

export function LiveStockPrice({ symbol }: { symbol: string }) {
  const { data } = useSWR(`/api/stocks/${symbol}`, fetcher, {
    refreshInterval: 5000, // Polling toutes les 5 secondes
  })

  return <div>{data?.price}</div>
}

// Ou avec React Query
const { data } = useQuery({
  queryKey: ['stock', symbol],
  queryFn: () => fetchStock(symbol),
  refetchInterval: 5000,
})
```

## Bonnes Pratiques

```
✅ SWR ou React Query pour cache intelligent
✅ Configuration globale des fetchers
✅ Optimistic updates pour UX réactive
✅ Gestion explicite loading/error
✅ AbortController pour cleanup

❌ Ne pas fetcher les données initiales côté client
❌ Éviter polling trop fréquent
❌ Ne pas ignorer les erreurs réseau
❌ Éviter fetch dans useEffect sans cleanup
```

## Escalades

| Situation | Action |
|-----------|--------|
| Données initiales | → `data-fetching.md` (SSR) |
| Mutations serveur | → `server-actions.md` |
| State global | → `react-expert` |
| WebSockets | → Spécialisé |


## Livrables

| Livrable | Description |
|----------|-------------|
| Configuration client fetching | Setup SWR/TanStack Query |
| Hooks de data fetching | Custom hooks réutilisables |
| Documentation | Guide d'utilisation côté client |
