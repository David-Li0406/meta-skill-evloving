# Vue → Next.js Migration Patterns

This module provides detailed conversion patterns from Vue 2/3 to Next.js 16 with App Router.

## Component Structure

### Vue 2 Options API → React Function Component

**Before (Vue 2)**:
```vue
<template>
  <div class="user-card">
    <h2>{{ fullName }}</h2>
    <p>{{ user.email }}</p>
    <button @click="handleClick">Action</button>
  </div>
</template>

<script>
export default {
  name: 'UserCard',
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      isLoading: false
    }
  },
  computed: {
    fullName() {
      return `${this.user.firstName} ${this.user.lastName}`
    }
  },
  methods: {
    handleClick() {
      this.$emit('action', this.user.id)
    }
  },
  mounted() {
    console.log('Component mounted')
  }
}
</script>

<style scoped>
.user-card {
  padding: 1rem;
  border: 1px solid #ccc;
}
</style>
```

**After (Next.js)**:
```tsx
'use client'

import { useState, useEffect, useMemo } from 'react'

interface User {
  id: string
  firstName: string
  lastName: string
  email: string
}

interface UserCardProps {
  user: User
  onAction?: (userId: string) => void
}

export function UserCard({ user, onAction }: UserCardProps) {
  const [isLoading, setIsLoading] = useState(false)

  const fullName = useMemo(
    () => `${user.firstName} ${user.lastName}`,
    [user.firstName, user.lastName]
  )

  useEffect(() => {
    console.log('Component mounted')
  }, [])

  const handleClick = () => {
    onAction?.(user.id)
  }

  return (
    <div className="p-4 border border-gray-300 rounded">
      <h2 className="text-xl font-bold">{fullName}</h2>
      <p className="text-gray-600">{user.email}</p>
      <button
        onClick={handleClick}
        className="mt-2 px-4 py-2 bg-blue-500 text-white rounded"
      >
        Action
      </button>
    </div>
  )
}
```

### Vue 3 Composition API → React Hooks

**Before (Vue 3)**:
```vue
<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'

interface Props {
  initialCount?: number
}

const props = withDefaults(defineProps<Props>(), {
  initialCount: 0
})

const emit = defineEmits<{
  (e: 'change', value: number): void
}>()

const count = ref(props.initialCount)
const doubled = computed(() => count.value * 2)

const increment = () => {
  count.value++
  emit('change', count.value)
}

watch(count, (newVal) => {
  console.log('Count changed:', newVal)
})

onMounted(() => {
  console.log('Mounted with count:', count.value)
})
</script>

<template>
  <div>
    <p>Count: {{ count }}</p>
    <p>Doubled: {{ doubled }}</p>
    <button @click="increment">Increment</button>
  </div>
</template>
```

**After (Next.js)**:
```tsx
'use client'

import { useState, useMemo, useEffect, useCallback } from 'react'

interface CounterProps {
  initialCount?: number
  onChange?: (value: number) => void
}

export function Counter({ initialCount = 0, onChange }: CounterProps) {
  const [count, setCount] = useState(initialCount)

  const doubled = useMemo(() => count * 2, [count])

  const increment = useCallback(() => {
    setCount((prev) => {
      const newValue = prev + 1
      onChange?.(newValue)
      return newValue
    })
  }, [onChange])

  // Watch equivalent
  useEffect(() => {
    console.log('Count changed:', count)
  }, [count])

  // onMounted equivalent
  useEffect(() => {
    console.log('Mounted with count:', count)
  }, []) // Empty deps = onMounted

  return (
    <div>
      <p>Count: {count}</p>
      <p>Doubled: {doubled}</p>
      <button onClick={increment}>Increment</button>
    </div>
  )
}
```

## Template Directives

### v-if / v-else / v-else-if

**Vue**:
```vue
<template>
  <div v-if="status === 'loading'">Loading...</div>
  <div v-else-if="status === 'error'">Error occurred</div>
  <div v-else>{{ data }}</div>
</template>
```

**React**:
```tsx
{status === 'loading' ? (
  <div>Loading...</div>
) : status === 'error' ? (
  <div>Error occurred</div>
) : (
  <div>{data}</div>
)}
```

### v-for

**Vue**:
```vue
<template>
  <ul>
    <li v-for="(item, index) in items" :key="item.id">
      {{ index }}: {{ item.name }}
    </li>
  </ul>
</template>
```

**React**:
```tsx
<ul>
  {items.map((item, index) => (
    <li key={item.id}>
      {index}: {item.name}
    </li>
  ))}
</ul>
```

### v-model

**Vue**:
```vue
<template>
  <input v-model="searchQuery" />
  <select v-model="selectedOption">
    <option v-for="opt in options" :key="opt.value" :value="opt.value">
      {{ opt.label }}
    </option>
  </select>
</template>
```

**React**:
```tsx
<input
  value={searchQuery}
  onChange={(e) => setSearchQuery(e.target.value)}
/>
<select
  value={selectedOption}
  onChange={(e) => setSelectedOption(e.target.value)}
>
  {options.map((opt) => (
    <option key={opt.value} value={opt.value}>
      {opt.label}
    </option>
  ))}
</select>
```

### v-show

**Vue**:
```vue
<div v-show="isVisible">Content</div>
```

**React**:
```tsx
<div style={{ display: isVisible ? 'block' : 'none' }}>Content</div>
// Or with Tailwind:
<div className={isVisible ? 'block' : 'hidden'}>Content</div>
```

### v-bind / v-on

**Vue**:
```vue
<button
  :class="buttonClass"
  :disabled="isDisabled"
  @click="handleClick"
  @mouseenter="handleHover"
>
  Click me
</button>
```

**React**:
```tsx
<button
  className={buttonClass}
  disabled={isDisabled}
  onClick={handleClick}
  onMouseEnter={handleHover}
>
  Click me
</button>
```

## Lifecycle Hooks

| Vue 2 | Vue 3 | React |
|-------|-------|-------|
| `beforeCreate` | - | Constructor / useState initial |
| `created` | - | useState initial / useEffect |
| `beforeMount` | `onBeforeMount` | useLayoutEffect |
| `mounted` | `onMounted` | useEffect(() => {}, []) |
| `beforeUpdate` | `onBeforeUpdate` | useLayoutEffect |
| `updated` | `onUpdated` | useEffect |
| `beforeDestroy` | `onBeforeUnmount` | useEffect cleanup |
| `destroyed` | `onUnmounted` | useEffect cleanup |

**Vue 3 Lifecycle**:
```vue
<script setup>
import { onMounted, onUnmounted } from 'vue'

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>
```

**React Equivalent**:
```tsx
useEffect(() => {
  window.addEventListener('resize', handleResize)

  // Cleanup function = onUnmounted
  return () => {
    window.removeEventListener('resize', handleResize)
  }
}, [])
```

## State Management

### Vuex → Zustand

**Vuex Store**:
```typescript
// store/modules/user.ts
export default {
  namespaced: true,
  state: () => ({
    user: null,
    isAuthenticated: false
  }),
  mutations: {
    SET_USER(state, user) {
      state.user = user
      state.isAuthenticated = !!user
    }
  },
  actions: {
    async login({ commit }, credentials) {
      const user = await api.login(credentials)
      commit('SET_USER', user)
    },
    logout({ commit }) {
      commit('SET_USER', null)
    }
  },
  getters: {
    fullName: (state) => state.user
      ? `${state.user.firstName} ${state.user.lastName}`
      : ''
  }
}
```

**Zustand Store**:
```typescript
// stores/user-store.ts
import { create } from 'zustand'

interface User {
  id: string
  firstName: string
  lastName: string
}

interface UserState {
  user: User | null
  isAuthenticated: boolean
  login: (credentials: { email: string; password: string }) => Promise<void>
  logout: () => void
}

export const useUserStore = create<UserState>((set, get) => ({
  user: null,
  isAuthenticated: false,

  login: async (credentials) => {
    const user = await api.login(credentials)
    set({ user, isAuthenticated: true })
  },

  logout: () => {
    set({ user: null, isAuthenticated: false })
  },
}))

// Derived state (getter equivalent)
export const useFullName = () =>
  useUserStore((state) =>
    state.user ? `${state.user.firstName} ${state.user.lastName}` : ''
  )
```

### Pinia → Zustand

**Pinia Store**:
```typescript
// stores/cart.ts
import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [] as CartItem[]
  }),
  getters: {
    totalItems: (state) => state.items.length,
    totalPrice: (state) =>
      state.items.reduce((sum, item) => sum + item.price * item.quantity, 0)
  },
  actions: {
    addItem(item: CartItem) {
      this.items.push(item)
    },
    removeItem(id: string) {
      this.items = this.items.filter(item => item.id !== id)
    }
  }
})
```

**Zustand Store**:
```typescript
// stores/cart-store.ts
import { create } from 'zustand'

interface CartItem {
  id: string
  name: string
  price: number
  quantity: number
}

interface CartState {
  items: CartItem[]
  addItem: (item: CartItem) => void
  removeItem: (id: string) => void
}

export const useCartStore = create<CartState>((set) => ({
  items: [],

  addItem: (item) =>
    set((state) => ({ items: [...state.items, item] })),

  removeItem: (id) =>
    set((state) => ({
      items: state.items.filter((item) => item.id !== id)
    })),
}))

// Selectors (getter equivalent)
export const useTotalItems = () =>
  useCartStore((state) => state.items.length)

export const useTotalPrice = () =>
  useCartStore((state) =>
    state.items.reduce((sum, item) => sum + item.price * item.quantity, 0)
  )
```

## Routing

### Vue Router → Next.js App Router

**Vue Router Configuration**:
```typescript
// router/index.ts
const routes = [
  { path: '/', component: Home },
  { path: '/about', component: About },
  { path: '/users/:id', component: UserDetail },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } }
]
```

**Next.js App Router**:
```
app/
├── page.tsx              # /
├── about/
│   └── page.tsx          # /about
├── users/
│   └── [id]/
│       └── page.tsx      # /users/:id
└── dashboard/
    └── page.tsx          # /dashboard (with middleware for auth)
```

### Navigation

**Vue**:
```vue
<script setup>
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const goToUser = (id: string) => {
  router.push(`/users/${id}`)
}

// Access params
const userId = route.params.id
</script>
```

**Next.js**:
```tsx
'use client'

import { useRouter, useParams } from 'next/navigation'

export function Component() {
  const router = useRouter()
  const params = useParams()

  const goToUser = (id: string) => {
    router.push(`/users/${id}`)
  }

  // Access params
  const userId = params.id

  return // ...
}
```

## Slots → Children & Props

### Default Slot

**Vue**:
```vue
<!-- Card.vue -->
<template>
  <div class="card">
    <slot />
  </div>
</template>

<!-- Usage -->
<Card>
  <p>Card content</p>
</Card>
```

**React**:
```tsx
// card.tsx
interface CardProps {
  children: React.ReactNode
}

export function Card({ children }: CardProps) {
  return <div className="card">{children}</div>
}

// Usage
<Card>
  <p>Card content</p>
</Card>
```

### Named Slots

**Vue**:
```vue
<!-- Layout.vue -->
<template>
  <div class="layout">
    <header><slot name="header" /></header>
    <main><slot /></main>
    <footer><slot name="footer" /></footer>
  </div>
</template>

<!-- Usage -->
<Layout>
  <template #header>Header content</template>
  <p>Main content</p>
  <template #footer>Footer content</template>
</Layout>
```

**React**:
```tsx
// layout.tsx
interface LayoutProps {
  header?: React.ReactNode
  children: React.ReactNode
  footer?: React.ReactNode
}

export function Layout({ header, children, footer }: LayoutProps) {
  return (
    <div className="layout">
      <header>{header}</header>
      <main>{children}</main>
      <footer>{footer}</footer>
    </div>
  )
}

// Usage
<Layout
  header={<span>Header content</span>}
  footer={<span>Footer content</span>}
>
  <p>Main content</p>
</Layout>
```

---

Version: 1.0.0
