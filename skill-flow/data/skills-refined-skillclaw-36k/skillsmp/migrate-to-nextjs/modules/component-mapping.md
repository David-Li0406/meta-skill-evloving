# Component Mapping Strategy

Detailed mapping patterns from source frameworks to Next.js 16 App Router.

## Vue → Next.js

| Vue Pattern | Next.js Equivalent |
|-------------|-------------------|
| `<template>` | JSX/TSX |
| `<script setup>` | Function component |
| `<style scoped>` | CSS Modules / Tailwind |
| `ref()`, `reactive()` | `useState` |
| `computed()` | `useMemo` |
| `watch()` | `useEffect` |
| `onMounted()` | `useEffect(() => {}, [])` |
| `v-if` / `v-else` | `{condition && ...}` |
| `v-for` | `.map()` |
| `v-model` | Controlled component |
| Vue Router | App Router |
| Vuex / Pinia | Zustand |

### Vue Example Conversion

**Before (Vue 3 Composition API)**:
```vue
<template>
  <div v-if="isLoading">Loading...</div>
  <ul v-else>
    <li v-for="item in filteredItems" :key="item.id">
      {{ item.name }}
    </li>
  </ul>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const items = ref([])
const filter = ref('')
const isLoading = ref(true)

const filteredItems = computed(() =>
  items.value.filter(i => i.name.includes(filter.value))
)

onMounted(async () => {
  items.value = await fetchItems()
  isLoading.value = false
})
</script>
```

**After (Next.js)**:
```tsx
'use client'

import { useState, useMemo, useEffect } from 'react'

export default function ItemList() {
  const [items, setItems] = useState([])
  const [filter, setFilter] = useState('')
  const [isLoading, setIsLoading] = useState(true)

  const filteredItems = useMemo(
    () => items.filter(i => i.name.includes(filter)),
    [items, filter]
  )

  useEffect(() => {
    fetchItems().then(data => {
      setItems(data)
      setIsLoading(false)
    })
  }, [])

  if (isLoading) return <div>Loading...</div>

  return (
    <ul>
      {filteredItems.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  )
}
```

---

## React CRA → Next.js

| CRA Pattern | Next.js Equivalent |
|-------------|-------------------|
| `src/index.js` entry | `app/layout.tsx` |
| `react-router-dom` | App Router (file-based) |
| `BrowserRouter` | Remove (built-in) |
| `useNavigate()` | `useRouter()` from `next/navigation` |
| `<Link>` | `<Link>` from `next/link` |
| `process.env.REACT_APP_*` | `process.env.NEXT_PUBLIC_*` |

### CRA Router Migration

**Before (react-router-dom)**:
```tsx
import { BrowserRouter, Routes, Route, Link, useNavigate } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/users/:id" element={<UserDetail />} />
      </Routes>
    </BrowserRouter>
  )
}

function UserDetail() {
  const navigate = useNavigate()
  const { id } = useParams()

  return (
    <button onClick={() => navigate('/users')}>
      Back to Users
    </button>
  )
}
```

**After (Next.js App Router)**:
```tsx
// app/layout.tsx
import Link from 'next/link'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <nav>
          <Link href="/">Home</Link>
          <Link href="/about">About</Link>
        </nav>
        {children}
      </body>
    </html>
  )
}

// app/page.tsx
export default function Home() { ... }

// app/about/page.tsx
export default function About() { ... }

// app/users/[id]/page.tsx
'use client'
import { useRouter, useParams } from 'next/navigation'

export default function UserDetail() {
  const router = useRouter()
  const params = useParams()
  const id = params.id

  return (
    <button onClick={() => router.push('/users')}>
      Back to Users
    </button>
  )
}
```

---

## Angular → Next.js

| Angular Pattern | Next.js Equivalent |
|-----------------|-------------------|
| `@Component` | Function component |
| `@Injectable` | Context / Custom hooks |
| `@NgModule` | Remove (not needed) |
| `*ngIf` | Conditional rendering |
| `*ngFor` | `.map()` |
| `[(ngModel)]` | Controlled component |
| Angular Router | App Router |
| RxJS | React Query / SWR |

### Angular Service Migration

**Before (Angular Service)**:
```typescript
@Injectable({ providedIn: 'root' })
export class UserService {
  private users$ = new BehaviorSubject<User[]>([])

  constructor(private http: HttpClient) {}

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>('/api/users').pipe(
      tap(users => this.users$.next(users))
    )
  }
}
```

**After (React Custom Hook)**:
```typescript
// hooks/useUsers.ts
import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then(res => res.json())

export function useUsers() {
  const { data, error, isLoading, mutate } = useSWR<User[]>(
    '/api/users',
    fetcher
  )

  return {
    users: data ?? [],
    isLoading,
    isError: error,
    refresh: mutate
  }
}
```

---

## Svelte → Next.js

| Svelte Pattern | Next.js Equivalent |
|----------------|-------------------|
| `.svelte` files | `.tsx` files |
| `$:` reactive | `useMemo` / `useEffect` |
| `{#if}` / `{:else}` | Conditional rendering |
| `{#each}` | `.map()` |
| `bind:value` | Controlled component |
| Stores | Zustand |
| `onMount` | `useEffect` |
| `<slot>` | `children` prop |

### Svelte Store Migration

**Before (Svelte Store)**:
```svelte
<script>
  import { writable, derived } from 'svelte/store'

  const count = writable(0)
  const doubled = derived(count, $count => $count * 2)

  function increment() {
    count.update(n => n + 1)
  }
</script>

<button on:click={increment}>
  Count: {$count}, Doubled: {$doubled}
</button>
```

**After (Zustand)**:
```tsx
// stores/counter.ts
import { create } from 'zustand'

interface CounterStore {
  count: number
  increment: () => void
}

export const useCounterStore = create<CounterStore>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 }))
}))

// components/Counter.tsx
'use client'
import { useCounterStore } from '@/stores/counter'
import { useMemo } from 'react'

export function Counter() {
  const { count, increment } = useCounterStore()
  const doubled = useMemo(() => count * 2, [count])

  return (
    <button onClick={increment}>
      Count: {count}, Doubled: {doubled}
    </button>
  )
}
```

---

## State Migration Decision Tree

```
Is the state...
│
├─ Global (app-wide)?
│   ├─ Complex with actions? → Zustand
│   ├─ Simple shared state? → React Context
│   └─ Server state? → React Query / SWR
│
├─ Component-local?
│   ├─ Primitive value? → useState
│   ├─ Object/Array? → useState with immutable updates
│   └─ Derived value? → useMemo
│
└─ Form state?
    ├─ Simple form? → useState + controlled
    └─ Complex form? → react-hook-form + zod
```

---

Version: 2.1.0
Source: jikime-migration-to-nextjs SKILL.md
