# Vue.js Best Practices

**Version 1.0.0**  
January 2026

> **Note:**  
> This document is primarily for AI agents and LLMs to follow when maintaining,  
> generating, or refactoring Vue.js and Nuxt codebases. Humans may also find it useful,  
> but guidance here is optimized for automation and consistency by AI-assisted workflows.

---

## Abstract

Comprehensive performance optimization guide for Vue 3 and Nuxt 3 applications, designed for AI agents and LLMs. Contains 50+ rules across 10 categories, prioritized by impact from critical (reactivity optimization, bundle size) to incremental (advanced patterns). Each rule includes detailed explanations, real-world examples comparing incorrect vs. correct implementations, and specific impact metrics to guide automated refactoring and code generation.

---

## Table of Contents

1. [Reactivity Optimization](#1-reactivity-optimization) — **CRITICAL**
2. [Bundle Size Optimization](#2-bundle-size-optimization) — **CRITICAL**
3. [Nuxt 3 Server Performance](#3-nuxt-3-server-performance) — **HIGH**
4. [Component Design Patterns](#4-component-design-patterns) — **HIGH**
5. [Composition API Patterns](#5-composition-api-patterns) — **MEDIUM-HIGH**
6. [State Management - Pinia](#6-state-management---pinia) — **MEDIUM-HIGH**
7. [Rendering Performance](#7-rendering-performance) — **MEDIUM**
8. [TypeScript Integration](#8-typescript-integration) — **MEDIUM**
9. [Testing Patterns](#9-testing-patterns) — **LOW-MEDIUM**
10. [Advanced Patterns](#10-advanced-patterns) — **LOW**

---

## 1. Reactivity Optimization

**Impact: CRITICAL**

Vue's reactivity system is powerful but can cause performance issues when misused. Understanding when to use shallow vs deep reactivity is essential.

### 1.1 Use shallowRef for Large Objects

**Impact: HIGH (avoids deep proxy overhead)**

When you have large objects that are replaced entirely (not mutated), use `shallowRef` to avoid the overhead of deep reactivity.

**Incorrect: deep reactivity for replaced objects**

```vue
<script setup lang="ts">
import { ref } from 'vue'

interface DataSet {
  items: Array<{ id: number; name: string; metadata: Record<string, any> }>
  total: number
  page: number
}

// Deep reactivity tracks every nested property - expensive!
const dataset = ref<DataSet>({
  items: [],
  total: 0,
  page: 1
})

async function fetchData() {
  const response = await $fetch('/api/data')
  // Even though we replace entirely, Vue tracked all nested properties
  dataset.value = response
}
</script>
```

**Correct: shallow reactivity for replaced objects**

```vue
<script setup lang="ts">
import { shallowRef, triggerRef } from 'vue'

interface DataSet {
  items: Array<{ id: number; name: string; metadata: Record<string, any> }>
  total: number
  page: number
}

// Only tracks .value replacement, not nested properties
const dataset = shallowRef<DataSet>({
  items: [],
  total: 0,
  page: 1
})

async function fetchData() {
  const response = await $fetch('/api/data')
  // Efficient - just replaces reference
  dataset.value = response
}

// If you need to mutate and trigger update:
function updateItem(index: number, newName: string) {
  dataset.value.items[index].name = newName
  triggerRef(dataset) // Manually trigger update
}
</script>
```

**When to use shallowRef:**
- API response data that's replaced entirely
- Large arrays (1000+ items)
- Complex nested objects from external sources
- Data from libraries that shouldn't be proxied

### 1.2 Use shallowReactive for Flat Objects

**Impact: MEDIUM (reduces proxy depth)**

For objects where only top-level properties change, use `shallowReactive`.

**Incorrect: deep reactivity for flat state**

```vue
<script setup lang="ts">
import { reactive } from 'vue'

// Tracks all nested properties unnecessarily
const formState = reactive({
  name: '',
  email: '',
  settings: {
    theme: 'dark',
    notifications: true
  }
})
</script>
```

**Correct: shallow reactivity for known structure**

```vue
<script setup lang="ts">
import { shallowReactive } from 'vue'

// Only tracks top-level property changes
const formState = shallowReactive({
  name: '',
  email: '',
  // For nested objects, replace entirely when updating
  settings: {
    theme: 'dark',
    notifications: true
  }
})

function updateSettings(newSettings: typeof formState.settings) {
  // Replace the entire nested object
  formState.settings = { ...newSettings }
}
</script>
```

### 1.3 Leverage Computed for Expensive Calculations

**Impact: HIGH (automatic caching)**

`computed` properties are cached and only re-evaluate when dependencies change. Always use them for derived state.

**Incorrect: recalculates on every render**

```vue
<script setup lang="ts">
import { ref } from 'vue'

const items = ref<{ price: number; quantity: number }[]>([])

// This runs on EVERY render, even if items didn't change
const getTotal = () => {
  console.log('Calculating total...')
  return items.value.reduce((sum, item) => sum + item.price * item.quantity, 0)
}
</script>

<template>
  <div>Total: {{ getTotal() }}</div>
  <div>With tax: {{ getTotal() * 1.1 }}</div> <!-- Calculates twice! -->
</template>
```

**Correct: cached computed property**

```vue
<script setup lang="ts">
import { ref, computed } from 'vue'

const items = ref<{ price: number; quantity: number }[]>([])

// Cached - only recalculates when items changes
const total = computed(() => {
  console.log('Calculating total...')
  return items.value.reduce((sum, item) => sum + item.price * item.quantity, 0)
})

// Computed can depend on other computed
const totalWithTax = computed(() => total.value * 1.1)
</script>

<template>
  <div>Total: {{ total }}</div>
  <div>With tax: {{ totalWithTax }}</div> <!-- Uses cached value -->
</template>
```

### 1.4 Use toRaw for External Libraries

**Impact: MEDIUM (prevents proxy issues)**

When passing reactive objects to external libraries (charts, maps, etc.), use `toRaw()` to avoid proxy-related issues.

**Incorrect: passing proxy to external library**

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Chart from 'chart.js/auto'

const chartData = ref({
  labels: ['Jan', 'Feb', 'Mar'],
  datasets: [{ data: [10, 20, 30] }]
})

onMounted(() => {
  // Chart.js may not handle Vue proxies correctly
  new Chart(canvas, {
    type: 'line',
    data: chartData.value // ❌ Proxy object
  })
})
</script>
```

**Correct: using toRaw for external libraries**

```vue
<script setup lang="ts">
import { ref, toRaw, onMounted } from 'vue'
import Chart from 'chart.js/auto'

const chartData = ref({
  labels: ['Jan', 'Feb', 'Mar'],
  datasets: [{ data: [10, 20, 30] }]
})

onMounted(() => {
  // Pass raw object to external library
  new Chart(canvas, {
    type: 'line',
    data: toRaw(chartData.value) // ✅ Plain object
  })
})
</script>
```

### 1.5 Use markRaw for Non-Reactive Objects

**Impact: MEDIUM (prevents unnecessary proxying)**

Use `markRaw()` for objects that should never be made reactive, like class instances or third-party objects.

**Incorrect: Vue proxies class instance**

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Editor } from '@tiptap/core'

// Vue will proxy the Editor instance - can cause issues!
const editor = ref<Editor | null>(null)

onMounted(() => {
  editor.value = new Editor({
    content: '<p>Hello</p>'
  })
})
</script>
```

**Correct: marking class instance as raw**

```vue
<script setup lang="ts">
import { shallowRef, markRaw, onMounted, onUnmounted } from 'vue'
import { Editor } from '@tiptap/core'

// Use shallowRef + markRaw for class instances
const editor = shallowRef<Editor | null>(null)

onMounted(() => {
  editor.value = markRaw(new Editor({
    content: '<p>Hello</p>'
  }))
})

onUnmounted(() => {
  editor.value?.destroy()
})
</script>
```

### 1.6 Use effectScope for Batch Cleanup

**Impact: LOW-MEDIUM (cleaner effect management)**

When creating multiple effects that should be cleaned up together, use `effectScope()`.

**Incorrect: manual cleanup of multiple effects**

```vue
<script setup lang="ts">
import { ref, watch, watchEffect, onUnmounted } from 'vue'

const count = ref(0)
const name = ref('')

const stop1 = watch(count, (val) => console.log('count:', val))
const stop2 = watch(name, (val) => console.log('name:', val))
const stop3 = watchEffect(() => console.log('effect:', count.value, name.value))

onUnmounted(() => {
  stop1()
  stop2()
  stop3()
})
</script>
```

**Correct: using effectScope for batch cleanup**

```vue
<script setup lang="ts">
import { ref, watch, watchEffect, effectScope, onUnmounted } from 'vue'

const count = ref(0)
const name = ref('')

const scope = effectScope()

scope.run(() => {
  watch(count, (val) => console.log('count:', val))
  watch(name, (val) => console.log('name:', val))
  watchEffect(() => console.log('effect:', count.value, name.value))
})

onUnmounted(() => {
  scope.stop() // Stops all effects at once
})
</script>
```

---

## 2. Bundle Size Optimization

**Impact: CRITICAL**

Reducing bundle size improves initial load time and Time to Interactive.

### 2.1 Tree-Shakeable Imports

**Impact: HIGH (significant bundle reduction)**

Always import from 'vue' directly, not from internal packages.

**Incorrect: importing from internal packages**

```typescript
// ❌ May not tree-shake properly
import { ref } from '@vue/reactivity'
import { h } from '@vue/runtime-core'
```

**Correct: importing from vue**

```typescript
// ✅ Proper tree-shaking
import { ref, h, computed, watch } from 'vue'
```

### 2.2 Async Components for Heavy Components

**Impact: CRITICAL (code splitting)**

Use `defineAsyncComponent` for components that are large or not immediately needed.

**Incorrect: synchronous import of heavy component**

```vue
<script setup lang="ts">
import HeavyChart from './HeavyChart.vue' // 200KB component
import HeavyEditor from './HeavyEditor.vue' // 300KB component
</script>

<template>
  <div>
    <HeavyChart v-if="showChart" />
    <HeavyEditor v-if="showEditor" />
  </div>
</template>
```

**Correct: async components with loading states**

```vue
<script setup lang="ts">
import { defineAsyncComponent, h } from 'vue'

const HeavyChart = defineAsyncComponent({
  loader: () => import('./HeavyChart.vue'),
  loadingComponent: () => h('div', 'Loading chart...'),
  delay: 200,
  timeout: 10000,
  errorComponent: () => h('div', 'Failed to load chart')
})

const HeavyEditor = defineAsyncComponent(() => import('./HeavyEditor.vue'))
</script>

<template>
  <div>
    <HeavyChart v-if="showChart" />
    <HeavyEditor v-if="showEditor" />
  </div>
</template>
```

### 2.3 Dynamic Imports for Routes

**Impact: CRITICAL (route-level code splitting)**

Always use dynamic imports in Vue Router for route components.

**Incorrect: static imports in router**

```typescript
// router/index.ts
import Home from '@/pages/Home.vue'
import About from '@/pages/About.vue'
import Dashboard from '@/pages/Dashboard.vue'
import Settings from '@/pages/Settings.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/about', component: About },
  { path: '/dashboard', component: Dashboard },
  { path: '/settings', component: Settings },
]
```

**Correct: dynamic imports (automatic code splitting)**

```typescript
// router/index.ts
// Vite automatically handles chunk naming based on file paths
// For Webpack projects, you can use /* webpackChunkName: "name" */ comments
const routes = [
  { 
    path: '/', 
    component: () => import('@/pages/Home.vue')
  },
  { 
    path: '/about', 
    component: () => import('@/pages/About.vue')
  },
  { 
    path: '/dashboard', 
    component: () => import('@/pages/Dashboard.vue')
  },
  { 
    path: '/settings', 
    component: () => import('@/pages/Settings.vue')
  },
]
```

### 2.4 Direct Icon Imports

**Impact: HIGH (avoid loading entire icon library)**

Import icons directly instead of from barrel files.

**Incorrect: barrel import loads all icons**

```vue
<script setup lang="ts">
// ❌ This may load the entire icon library (500KB+)
import { CheckIcon, XIcon, MenuIcon } from '@heroicons/vue/24/solid'
</script>
```

**Correct: direct imports**

```vue
<script setup lang="ts">
// ✅ Only loads specific icons (~1KB each)
import CheckIcon from '@heroicons/vue/24/solid/CheckIcon'
import XIcon from '@heroicons/vue/24/solid/XIcon'
import MenuIcon from '@heroicons/vue/24/solid/MenuIcon'
</script>
```

**Alternative: use unplugin-icons**

```typescript
// vite.config.ts
import Icons from 'unplugin-icons/vite'

export default defineConfig({
  plugins: [
    Icons({ compiler: 'vue3' })
  ]
})
```

```vue
<script setup lang="ts">
// Auto-imported, only what you use
import IconCheck from '~icons/heroicons/check-solid'
</script>
```

### 2.5 Lodash-ES with Specific Imports

**Impact: MEDIUM (reduces lodash from 70KB to ~2KB per function)**

Never import from 'lodash', use 'lodash-es' with specific imports.

**Incorrect: full lodash import**

```typescript
// ❌ Imports entire library (~70KB)
import _ from 'lodash'
const result = _.debounce(fn, 300)

// ❌ Still imports more than needed
import { debounce } from 'lodash'
```

**Correct: lodash-es with direct imports**

```typescript
// ✅ Only imports debounce (~2KB)
import debounce from 'lodash-es/debounce'
const result = debounce(fn, 300)

// Or use VueUse which has tree-shakeable utilities
import { useDebounceFn } from '@vueuse/core'
const debouncedFn = useDebounceFn(fn, 300)
```

---

## 3. Nuxt 3 Server Performance

**Impact: HIGH**

Optimizing server-side rendering and data fetching in Nuxt 3.

### 3.1 Use useFetch for SSR-Friendly Data Fetching

**Impact: CRITICAL (SSR + client hydration)**

Always use `useFetch` or `useAsyncData` in components for SSR compatibility.

**Incorrect: using $fetch in component setup**

```vue
<script setup lang="ts">
// ❌ Runs on both server AND client (double fetch)
const data = ref(null)
const loading = ref(true)

onMounted(async () => {
  loading.value = true
  data.value = await $fetch('/api/users')
  loading.value = false
})
</script>
```

**Correct: using useFetch**

```vue
<script setup lang="ts">
// ✅ Runs on server, hydrates on client (single fetch)
const { data, pending, error, refresh } = await useFetch('/api/users')

// With options
const { data: users } = await useFetch('/api/users', {
  // Transform response
  transform: (response) => response.data,
  // Pick specific fields (reduces payload)
  pick: ['id', 'name', 'email'],
  // Cache key
  key: 'users-list',
  // Lazy loading (doesn't block navigation)
  lazy: true,
})
</script>

<template>
  <div v-if="pending">Loading...</div>
  <div v-else-if="error">Error: {{ error.message }}</div>
  <ul v-else>
    <li v-for="user in users" :key="user.id">{{ user.name }}</li>
  </ul>
</template>
```

### 3.2 Lazy Components in Nuxt

**Impact: HIGH (automatic code splitting)**

Prefix components with `Lazy` for automatic lazy loading.

**Incorrect: loading all components immediately**

```vue
<template>
  <div>
    <HeavyChart v-if="showChart" />
    <HeavyTable v-if="showTable" />
    <HeavyEditor v-if="showEditor" />
  </div>
</template>
```

**Correct: using Lazy prefix**

```vue
<template>
  <div>
    <!-- Automatically lazy-loaded -->
    <LazyHeavyChart v-if="showChart" />
    <LazyHeavyTable v-if="showTable" />
    <LazyHeavyEditor v-if="showEditor" />
  </div>
</template>
```

### 3.3 Minimize Payload with Transform

**Impact: HIGH (reduces SSR payload size)**

Use `transform` and `pick` options to reduce the data sent to client.

**Incorrect: sending entire API response**

```vue
<script setup lang="ts">
// ❌ Sends entire user object to client
const { data } = await useFetch('/api/user/1')
// Response: { id, name, email, password_hash, created_at, updated_at, settings: {...}, permissions: [...] }
</script>
```

**Correct: picking only needed fields**

```vue
<script setup lang="ts">
// ✅ Only sends needed fields to client
const { data } = await useFetch('/api/user/1', {
  pick: ['id', 'name', 'email'],
  // Or transform for more control
  transform: (user) => ({
    id: user.id,
    displayName: `${user.name} (${user.email})`,
    isAdmin: user.permissions.includes('admin')
  })
})
</script>
```

### 3.4 Route Rules for Caching

**Impact: HIGH (CDN and server caching)**

Configure route rules in `nuxt.config.ts` for caching strategies.

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  routeRules: {
    // Static pages - prerender at build time
    '/': { prerender: true },
    '/about': { prerender: true },
    
    // ISR - revalidate every hour
    '/blog/**': { isr: 3600 },
    
    // SWR - stale-while-revalidate
    '/products/**': { swr: 600 },
    
    // API routes - cache on CDN
    '/api/products': { 
      cache: { 
        maxAge: 60 * 60,
        staleMaxAge: 60 * 60 * 24
      }
    },
    
    // No caching for user-specific content
    '/dashboard/**': { ssr: true, cache: false },
    
    // Client-side only
    '/admin/**': { ssr: false },
  }
})
```

### 3.5 Server Components (.server.vue)

**Impact: MEDIUM (reduces client bundle)**

Use `.server.vue` extension for components that only render on server.

```vue
<!-- components/ServerOnlyAnalytics.server.vue -->
<script setup lang="ts">
// This code ONLY runs on server
// Database calls, sensitive API keys, etc.
const { data } = await useFetch('/api/admin/analytics', {
  headers: {
    'Authorization': `Bearer ${process.env.ADMIN_API_KEY}`
  }
})
</script>

<template>
  <div class="analytics-summary">
    <p>Total users: {{ data?.totalUsers }}</p>
    <p>Revenue: {{ data?.revenue }}</p>
  </div>
</template>
```

```vue
<!-- pages/admin/dashboard.vue -->
<template>
  <div>
    <h1>Admin Dashboard</h1>
    <!-- Server component - no JS sent to client -->
    <ServerOnlyAnalytics />
  </div>
</template>
```

### 3.6 Nuxt Islands for Partial Hydration

**Impact: MEDIUM (reduces hydration cost)**

Use Nuxt Islands for interactive widgets in otherwise static content.

```vue
<!-- components/InteractiveWidget.vue -->
<script setup lang="ts">
const count = ref(0)
</script>

<template>
  <button @click="count++">Count: {{ count }}</button>
</template>
```

```vue
<!-- pages/blog/[slug].vue -->
<template>
  <article>
    <h1>{{ post.title }}</h1>
    <div v-html="post.content" />
    
    <!-- Only this widget is hydrated -->
    <NuxtIsland name="InteractiveWidget" />
    
    <div v-html="post.footer" />
  </article>
</template>
```

### 3.7 Nitro Caching for API Routes

**Impact: HIGH (reduces server load)**

Use Nitro's caching for API routes.

```typescript
// server/api/products.ts
export default defineCachedEventHandler(async (event) => {
  const products = await db.product.findMany()
  return products
}, {
  maxAge: 60 * 60, // Cache for 1 hour
  staleMaxAge: 60 * 60 * 24, // Serve stale for 24 hours while revalidating
  swr: true,
  // Cache key based on query params
  getKey: (event) => {
    const query = getQuery(event)
    return `products:${query.category || 'all'}:${query.page || 1}`
  }
})
```

```typescript
// server/api/user/[id].ts
export default defineCachedEventHandler(async (event) => {
  const id = getRouterParam(event, 'id')
  const user = await db.user.findUnique({ where: { id } })
  
  if (!user) {
    throw createError({ statusCode: 404, message: 'User not found' })
  }
  
  return user
}, {
  maxAge: 60 * 5, // Cache for 5 minutes
  // Different cache per user
  getKey: (event) => `user:${getRouterParam(event, 'id')}`
})
```

---

## 4. Component Design Patterns

**Impact: HIGH**

Well-structured components improve maintainability and performance.

### 4.1 Always Use `<script setup>`

**Impact: HIGH (better performance, cleaner code)**

`<script setup>` is more performant and concise than Options API.

**Incorrect: Options API**

```vue
<script lang="ts">
import { defineComponent, ref, computed } from 'vue'

export default defineComponent({
  props: {
    title: String
  },
  emits: ['update'],
  setup(props, { emit }) {
    const count = ref(0)
    const doubled = computed(() => count.value * 2)
    
    function increment() {
      count.value++
      emit('update', count.value)
    }
    
    return { count, doubled, increment }
  }
})
</script>
```

**Correct: `<script setup>`**

```vue
<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps<{
  title: string
}>()

const emit = defineEmits<{
  update: [value: number]
}>()

const count = ref(0)
const doubled = computed(() => count.value * 2)

function increment() {
  count.value++
  emit('update', count.value)
}
</script>
```

### 4.2 Props Destructuring with Reactivity

**Impact: MEDIUM (maintains reactivity)**

Vue 3.3+ supports reactive props destructuring.

**Incorrect: losing reactivity with destructure**

```vue
<script setup lang="ts">
const props = defineProps<{
  count: number
  name: string
}>()

// ❌ Before Vue 3.3: loses reactivity!
const { count, name } = props

// Won't update when props change
watchEffect(() => console.log(count)) // Always logs initial value
</script>
```

**Correct: reactive destructuring (Vue 3.3+)**

```vue
<script setup lang="ts">
// ✅ Vue 3.3+: reactive destructuring with defaults
const { count = 0, name = 'Guest' } = defineProps<{
  count?: number
  name?: string
}>()

// Reactive!
watchEffect(() => console.log(count))
</script>
```

**Alternative: toRefs for earlier versions**

```vue
<script setup lang="ts">
import { toRefs } from 'vue'

const props = defineProps<{
  count: number
  name: string
}>()

// ✅ Maintains reactivity
const { count, name } = toRefs(props)

watchEffect(() => console.log(count.value))
</script>
```

### 4.3 Typed Emits

**Impact: MEDIUM (type safety)**

Always define emits with TypeScript for type checking.

**Incorrect: untyped emits**

```vue
<script setup lang="ts">
// ❌ No type safety
const emit = defineEmits(['update', 'delete', 'submit'])

// No error even with wrong payload
emit('update', { wrong: 'payload' })
</script>
```

**Correct: typed emits**

```vue
<script setup lang="ts">
// ✅ Full type safety
const emit = defineEmits<{
  update: [id: number, value: string]
  delete: [id: number]
  submit: [data: FormData]
}>()

// Type error if payload doesn't match
emit('update', 1, 'new value') // ✅
emit('update', 'wrong') // ❌ Type error
</script>
```

### 4.4 Typed Slots with defineSlots

**Impact: MEDIUM (type safety for slots)**

Use `defineSlots` for type-safe slot props.

```vue
<script setup lang="ts">
interface Item {
  id: number
  name: string
}

const props = defineProps<{
  items: Item[]
}>()

// Define slot types
const slots = defineSlots<{
  default(props: { item: Item; index: number }): any
  header(props: { count: number }): any
  empty(): any
}>()
</script>

<template>
  <div>
    <header>
      <slot name="header" :count="items.length" />
    </header>
    
    <ul v-if="items.length">
      <li v-for="(item, index) in items" :key="item.id">
        <slot :item="item" :index="index" />
      </li>
    </ul>
    
    <slot v-else name="empty" />
  </div>
</template>
```

### 4.5 Use v-once for Static Content

**Impact: MEDIUM (skip re-renders)**

Use `v-once` for content that never changes.

```vue
<template>
  <div>
    <!-- Static header - rendered once, never updates -->
    <header v-once>
      <h1>{{ appName }}</h1>
      <nav>
        <a href="/">Home</a>
        <a href="/about">About</a>
      </nav>
    </header>
    
    <!-- Dynamic content -->
    <main>
      <div v-for="item in items" :key="item.id">
        {{ item.name }}
      </div>
    </main>
  </div>
</template>
```

### 4.6 Use v-memo for List Optimization

**Impact: HIGH (skip unnecessary list item updates)**

`v-memo` caches template subtrees based on dependency array.

```vue
<script setup lang="ts">
import { ref } from 'vue'

const selectedId = ref<number | null>(null)
const items = ref([
  { id: 1, name: 'Item 1' },
  { id: 2, name: 'Item 2' },
  // ... many items
])
</script>

<template>
  <div>
    <!-- Only re-renders items where id or selected state changed -->
    <div
      v-for="item in items"
      :key="item.id"
      v-memo="[item.id, item.id === selectedId]"
      :class="{ selected: item.id === selectedId }"
      @click="selectedId = item.id"
    >
      {{ item.name }}
    </div>
  </div>
</template>
```

### 4.7 Use Teleport for Modals

**Impact: MEDIUM (proper DOM structure)**

Use `Teleport` to render modals/tooltips outside component tree.

```vue
<script setup lang="ts">
import { ref } from 'vue'

const showModal = ref(false)
</script>

<template>
  <button @click="showModal = true">Open Modal</button>
  
  <Teleport to="body">
    <div v-if="showModal" class="modal-overlay" @click="showModal = false">
      <div class="modal-content" @click.stop>
        <h2>Modal Title</h2>
        <p>Modal content here</p>
        <button @click="showModal = false">Close</button>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
}
</style>
```

---

## 5. Composition API Patterns

**Impact: MEDIUM-HIGH**

Well-structured composables improve code reuse and maintainability.

### 5.1 Composable Naming Convention

**Impact: LOW (consistency)**

Always prefix composables with 'use'.

```typescript
// ✅ Correct naming
export function useAuth() { }
export function useLocalStorage() { }
export function useDebounce() { }

// ❌ Incorrect naming
export function auth() { }
export function getLocalStorage() { }
export function createDebounce() { }
```

### 5.2 Return Object from Composables

**Impact: MEDIUM (better DX)**

Return objects instead of arrays for named destructuring.

**Incorrect: array return (positional)**

```typescript
// composables/useCounter.ts
export function useCounter(initial = 0) {
  const count = ref(initial)
  const increment = () => count.value++
  const decrement = () => count.value--
  
  // ❌ Array - must remember order
  return [count, increment, decrement]
}

// Usage - error-prone
const [count, increment, decrement] = useCounter()
const [value, , decrease] = useCounter() // Confusing
```

**Correct: object return (named)**

```typescript
// composables/useCounter.ts
export function useCounter(initial = 0) {
  const count = ref(initial)
  const increment = () => count.value++
  const decrement = () => count.value--
  const reset = () => count.value = initial
  
  // ✅ Object - named properties
  return {
    count,
    increment,
    decrement,
    reset
  }
}

// Usage - clear and flexible
const { count, increment, decrement } = useCounter()
const { count: value, decrement: decrease } = useCounter() // Easy renaming
```

### 5.3 Handle Cleanup in Composables

**Impact: HIGH (prevents memory leaks)**

Always clean up side effects when component unmounts.

**Incorrect: no cleanup**

```typescript
// composables/useWindowSize.ts
export function useWindowSize() {
  const width = ref(window.innerWidth)
  const height = ref(window.innerHeight)
  
  // ❌ Listener never removed!
  window.addEventListener('resize', () => {
    width.value = window.innerWidth
    height.value = window.innerHeight
  })
  
  return { width, height }
}
```

**Correct: with cleanup**

```typescript
// composables/useWindowSize.ts
import { ref, onMounted, onUnmounted } from 'vue'

export function useWindowSize() {
  const width = ref(0)
  const height = ref(0)
  
  function update() {
    width.value = window.innerWidth
    height.value = window.innerHeight
  }
  
  onMounted(() => {
    update()
    window.addEventListener('resize', update)
  })
  
  onUnmounted(() => {
    window.removeEventListener('resize', update)
  })
  
  return { width, height }
}
```

**Even better: use VueUse**

```typescript
import { useWindowSize } from '@vueuse/core'

// Already handles cleanup, SSR, and more
const { width, height } = useWindowSize()
```

### 5.4 Async Composables Pattern

**Impact: HIGH (proper async state handling)**

Handle loading, error, and data states properly.

```typescript
// composables/useAsyncData.ts
import { ref, Ref } from 'vue'

interface UseAsyncDataReturn<T> {
  data: Ref<T | null>
  error: Ref<Error | null>
  loading: Ref<boolean>
  execute: () => Promise<void>
}

export function useAsyncData<T>(
  fetcher: () => Promise<T>
): UseAsyncDataReturn<T> {
  const data = ref<T | null>(null) as Ref<T | null>
  const error = ref<Error | null>(null)
  const loading = ref(false)
  
  async function execute() {
    loading.value = true
    error.value = null
    
    try {
      data.value = await fetcher()
    } catch (e) {
      error.value = e instanceof Error ? e : new Error(String(e))
    } finally {
      loading.value = false
    }
  }
  
  return { data, error, loading, execute }
}

// Usage
const { data: users, error, loading, execute: fetchUsers } = useAsyncData(
  () => $fetch('/api/users')
)

await fetchUsers()
```

### 5.5 SSR-Safe Composables

**Impact: HIGH (prevents SSR errors)**

Check for browser environment in composables that use browser APIs.

```typescript
// composables/useLocalStorage.ts
import { ref, watch } from 'vue'

export function useLocalStorage<T>(key: string, defaultValue: T) {
  const data = ref<T>(defaultValue)
  
  // Only run on client
  if (import.meta.client) {
    // Read initial value
    const stored = localStorage.getItem(key)
    if (stored) {
      try {
        data.value = JSON.parse(stored)
      } catch {
        data.value = defaultValue
      }
    }
    
    // Persist changes
    watch(data, (newValue) => {
      localStorage.setItem(key, JSON.stringify(newValue))
    }, { deep: true })
  }
  
  return data
}
```

### 5.6 Type-Safe Provide/Inject

**Impact: MEDIUM (type safety)**

Use `InjectionKey` for type-safe provide/inject.

```typescript
// injection-keys.ts
import type { InjectionKey, Ref } from 'vue'

export interface UserContext {
  user: Ref<User | null>
  login: (credentials: Credentials) => Promise<void>
  logout: () => void
}

export const UserKey: InjectionKey<UserContext> = Symbol('user')
```

```vue
<!-- App.vue (Provider component) -->
<script setup lang="ts">
import { ref, provide } from 'vue'
import { UserKey } from './injection-keys'

const user = ref<User | null>(null)
const login = async (credentials: Credentials) => { /* ... */ }
const logout = () => { user.value = null }

provide(UserKey, { user, login, logout })
</script>
```

```vue
<!-- ChildComponent.vue (Consumer component) -->
<script setup lang="ts">
import { inject } from 'vue'
import { UserKey } from './injection-keys'

const userContext = inject(UserKey)

if (!userContext) {
  throw new Error('UserContext not provided')
}

const { user, login, logout } = userContext
</script>
```

### 5.7 Leverage VueUse

**Impact: HIGH (don't reinvent the wheel)**

VueUse provides 200+ composables for common use cases.

```typescript
import {
  // Browser
  useLocalStorage,
  useClipboard,
  useMediaQuery,
  
  // Sensors
  useMouse,
  useScroll,
  useElementSize,
  
  // State
  useRefHistory,
  useDebouncedRef,
  useThrottleFn,
  
  // Network
  useFetch,
  useWebSocket,
  
  // Animation
  useTransition,
  useInterval,
  
  // Component
  useVModel,
  onClickOutside,
} from '@vueuse/core'

// Examples
const isDark = useMediaQuery('(prefers-color-scheme: dark)')
const { copy, copied } = useClipboard()
const storage = useLocalStorage('my-key', { count: 0 })
```

---

## 6. State Management - Pinia

**Impact: MEDIUM-HIGH**

Pinia is the official state management solution for Vue 3.

### 6.1 Setup Stores (Recommended)

**Impact: MEDIUM (more flexible)**

Prefer setup stores over options stores for better TypeScript support.

**Options store (older style):**

```typescript
// stores/counter.ts
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0,
    name: 'Counter'
  }),
  getters: {
    doubleCount: (state) => state.count * 2
  },
  actions: {
    increment() {
      this.count++
    }
  }
})
```

**Setup store (recommended):**

```typescript
// stores/counter.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCounterStore = defineStore('counter', () => {
  // State
  const count = ref(0)
  const name = ref('Counter')
  
  // Getters (computed)
  const doubleCount = computed(() => count.value * 2)
  
  // Actions (functions)
  function increment() {
    count.value++
  }
  
  async function incrementAsync() {
    await new Promise(resolve => setTimeout(resolve, 1000))
    count.value++
  }
  
  return {
    count,
    name,
    doubleCount,
    increment,
    incrementAsync
  }
})
```

### 6.2 Use storeToRefs for Reactivity

**Impact: HIGH (maintains reactivity)**

When destructuring store state, use `storeToRefs` to maintain reactivity.

**Incorrect: loses reactivity**

```vue
<script setup lang="ts">
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()

// ❌ Destructuring loses reactivity!
const { count, name } = store

// count won't update when store changes
</script>
```

**Correct: using storeToRefs**

```vue
<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()

// ✅ State/getters - use storeToRefs
const { count, name, doubleCount } = storeToRefs(store)

// ✅ Actions - destructure directly (they're just functions)
const { increment, incrementAsync } = store
</script>

<template>
  <div>
    <p>Count: {{ count }}</p>
    <p>Double: {{ doubleCount }}</p>
    <button @click="increment">+1</button>
  </div>
</template>
```

### 6.3 Actions for Async Operations

**Impact: MEDIUM (proper async handling)**

Use actions for async operations, not getters.

**Incorrect: async in getter**

```typescript
// ❌ Getters should be synchronous
export const useUserStore = defineStore('user', () => {
  const userId = ref<number | null>(null)
  
  // ❌ Don't do async in computed
  const user = computed(async () => {
    if (!userId.value) return null
    return await $fetch(`/api/users/${userId.value}`)
  })
  
  return { userId, user }
})
```

**Correct: async in action**

```typescript
export const useUserStore = defineStore('user', () => {
  const userId = ref<number | null>(null)
  const user = ref<User | null>(null)
  const loading = ref(false)
  const error = ref<Error | null>(null)
  
  // ✅ Async in action
  async function fetchUser() {
    if (!userId.value) return
    
    loading.value = true
    error.value = null
    
    try {
      user.value = await $fetch(`/api/users/${userId.value}`)
    } catch (e) {
      error.value = e as Error
    } finally {
      loading.value = false
    }
  }
  
  // Watch for userId changes
  watch(userId, () => fetchUser(), { immediate: true })
  
  return { userId, user, loading, error, fetchUser }
})
```

### 6.4 Persist State with Plugin

**Impact: MEDIUM (state persistence)**

Use `pinia-plugin-persistedstate` for localStorage persistence.

```typescript
// plugins/pinia-persist.ts
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.$pinia.use(piniaPluginPersistedstate)
})
```

```typescript
// stores/settings.ts
export const useSettingsStore = defineStore('settings', () => {
  const theme = ref<'light' | 'dark'>('light')
  const language = ref('en')
  
  return { theme, language }
}, {
  persist: {
    // Persist to localStorage
    storage: persistedState.localStorage,
    // Only persist specific keys
    pick: ['theme', 'language'],
  }
})
```

### 6.5 Store Reset Pattern

**Impact: LOW-MEDIUM (clean state management)**

Implement `$reset` for setup stores.

```typescript
export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([])
  const coupon = ref<string | null>(null)
  
  const total = computed(() => 
    items.value.reduce((sum, item) => sum + item.price * item.quantity, 0)
  )
  
  function addItem(item: CartItem) {
    items.value.push(item)
  }
  
  function removeItem(id: string) {
    const index = items.value.findIndex(i => i.id === id)
    if (index > -1) items.value.splice(index, 1)
  }
  
  // Custom reset function for setup stores
  function $reset() {
    items.value = []
    coupon.value = null
  }
  
  return { items, coupon, total, addItem, removeItem, $reset }
})
```

### 6.6 Subscribe to Store Changes

**Impact: LOW-MEDIUM (side effects)**

Use `$subscribe` for side effects on store changes.

```typescript
// In a component or plugin
const store = useCartStore()

// Subscribe to mutations
store.$subscribe((mutation, state) => {
  // Log every mutation
  console.log('Mutation:', mutation.type, mutation.storeId)
  
  // Sync to analytics
  analytics.track('cart_updated', {
    itemCount: state.items.length,
    total: store.total
  })
})

// Subscribe to actions
store.$onAction(({ name, args, after, onError }) => {
  const start = Date.now()
  
  after((result) => {
    console.log(`Action ${name} took ${Date.now() - start}ms`)
  })
  
  onError((error) => {
    console.error(`Action ${name} failed:`, error)
  })
})
```

---

## 7. Rendering Performance

**Impact: MEDIUM**

Optimizing how Vue renders components.

### 7.1 v-show vs v-if

**Impact: MEDIUM (correct conditional rendering)**

Use `v-show` for frequent toggles, `v-if` for rare conditions.

```vue
<template>
  <!-- v-if: removes from DOM, good for:
       - Expensive components
       - Initial hidden state
       - Rarely toggled content -->
  <HeavyComponent v-if="showHeavy" />
  
  <!-- v-show: toggles display, good for:
       - Frequently toggled content
       - Tabs, dropdowns
       - Simple elements -->
  <div v-show="isDropdownOpen" class="dropdown">
    <slot />
  </div>
  
  <!-- v-if with v-else for conditional components -->
  <LoadingSpinner v-if="loading" />
  <DataTable v-else :data="data" />
</template>
```

### 7.2 Unique Keys in v-for

**Impact: HIGH (correct list reconciliation)**

Always use unique, stable keys in `v-for`.

**Incorrect: index as key**

```vue
<template>
  <!-- ❌ Using index can cause bugs when list changes -->
  <div v-for="(item, index) in items" :key="index">
    <input v-model="item.value" />
  </div>
</template>
```

**Correct: unique ID as key**

```vue
<template>
  <!-- ✅ Unique ID ensures correct element tracking -->
  <div v-for="item in items" :key="item.id">
    <input v-model="item.value" />
  </div>
</template>
```

### 7.3 Virtual Scrolling for Long Lists

**Impact: HIGH (handles large lists)**

Use virtual scrolling for lists with 100+ items.

```vue
<script setup lang="ts">
import { useVirtualList } from '@vueuse/core'

interface Item {
  id: number
  name: string
}

const props = defineProps<{
  items: Item[]
}>()

const { list, containerProps, wrapperProps } = useVirtualList(
  computed(() => props.items),
  {
    itemHeight: 50,
    overscan: 10
  }
)
</script>

<template>
  <div v-bind="containerProps" class="h-96 overflow-auto">
    <div v-bind="wrapperProps">
      <div
        v-for="{ data: item, index } in list"
        :key="item.id"
        class="h-[50px] flex items-center px-4"
      >
        {{ index }}: {{ item.name }}
      </div>
    </div>
  </div>
</template>
```

### 7.4 KeepAlive for Component Caching

**Impact: MEDIUM (preserves component state)**

Use `KeepAlive` to cache component instances.

```vue
<script setup lang="ts">
const currentTab = ref('home')
</script>

<template>
  <div>
    <button 
      v-for="tab in ['home', 'profile', 'settings']" 
      :key="tab"
      @click="currentTab = tab"
    >
      {{ tab }}
    </button>
    
    <!-- Cache all tab components -->
    <KeepAlive>
      <component :is="currentTab" />
    </KeepAlive>
    
    <!-- Or with specific includes/excludes -->
    <KeepAlive :include="['HomeTab', 'ProfileTab']" :max="5">
      <component :is="currentTab" />
    </KeepAlive>
  </div>
</template>
```

### 7.5 Suspense for Async Components

**Impact: MEDIUM (better loading UX)**

Use `Suspense` for handling async component loading states.

```vue
<template>
  <Suspense>
    <!-- Main async content -->
    <template #default>
      <AsyncDashboard />
    </template>
    
    <!-- Loading state -->
    <template #fallback>
      <div class="flex items-center justify-center h-64">
        <LoadingSpinner />
      </div>
    </template>
  </Suspense>
</template>

<script setup lang="ts">
// AsyncDashboard.vue - has async setup
const AsyncDashboard = defineAsyncComponent(() => 
  import('./Dashboard.vue')
)
</script>
```

```vue
<!-- Dashboard.vue -->
<script setup lang="ts">
// Async setup - component won't render until this resolves
const { data } = await useFetch('/api/dashboard')
</script>

<template>
  <div>{{ data }}</div>
</template>
```

---

## 8. TypeScript Integration

**Impact: MEDIUM**

Proper TypeScript usage improves developer experience and catches bugs.

### 8.1 Props with Interface

**Impact: MEDIUM (better type organization)**

Define props with interface for complex types.

```vue
<script setup lang="ts">
// ✅ Interface for complex props
interface User {
  id: number
  name: string
  email: string
  avatar?: string
}

interface Props {
  user: User
  showAvatar?: boolean
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  showAvatar: true,
  size: 'md'
})
</script>
```

### 8.2 Explicit Ref Types

**Impact: MEDIUM (type inference)**

Explicitly type refs when TypeScript can't infer.

```vue
<script setup lang="ts">
import { ref } from 'vue'

// ✅ Explicit types when needed
const userId = ref<number | null>(null)
const users = ref<User[]>([])
const error = ref<Error | null>(null)

// ✅ Type is inferred for simple values
const count = ref(0) // Ref<number>
const name = ref('') // Ref<string>
const isOpen = ref(false) // Ref<boolean>
</script>
```

### 8.3 Template Refs

**Impact: MEDIUM (DOM type safety)**

Properly type template refs.

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'

// HTML element ref
const inputRef = ref<HTMLInputElement | null>(null)

// Component ref
const modalRef = ref<InstanceType<typeof Modal> | null>(null)

onMounted(() => {
  // TypeScript knows inputRef.value is HTMLInputElement
  inputRef.value?.focus()
  
  // Access component methods
  modalRef.value?.open()
})
</script>

<template>
  <input ref="inputRef" type="text" />
  <Modal ref="modalRef" />
</template>
```

### 8.4 Generic Components

**Impact: MEDIUM (reusable typed components)**

Create generic components for reusable patterns.

```vue
<!-- GenericList.vue -->
<script setup lang="ts" generic="T extends { id: string | number }">
defineProps<{
  items: T[]
  selected?: T
}>()

defineEmits<{
  select: [item: T]
  delete: [item: T]
}>()

defineSlots<{
  default(props: { item: T; index: number }): any
  empty(): any
}>()
</script>

<template>
  <ul v-if="items.length">
    <li 
      v-for="(item, index) in items" 
      :key="item.id"
      :class="{ selected: selected?.id === item.id }"
      @click="$emit('select', item)"
    >
      <slot :item="item" :index="index" />
      <button @click.stop="$emit('delete', item)">Delete</button>
    </li>
  </ul>
  <slot v-else name="empty">No items</slot>
</template>
```

```vue
<!-- Usage -->
<script setup lang="ts">
interface Product {
  id: number
  name: string
  price: number
}

const products = ref<Product[]>([])
const selectedProduct = ref<Product>()
</script>

<template>
  <!-- Full type inference! -->
  <GenericList
    :items="products"
    :selected="selectedProduct"
    @select="selectedProduct = $event"
    @delete="removeProduct($event)"
  >
    <template #default="{ item }">
      {{ item.name }} - ${{ item.price }}
    </template>
  </GenericList>
</template>
```

### 8.5 Event Handler Types

**Impact: LOW-MEDIUM (type safety)**

Properly type event handlers.

```vue
<script setup lang="ts">
function handleInput(event: Event) {
  const target = event.target as HTMLInputElement
  console.log(target.value)
}

function handleSubmit(event: Event) {
  event.preventDefault()
  const form = event.target as HTMLFormElement
  const formData = new FormData(form)
}

function handleKeydown(event: KeyboardEvent) {
  if (event.key === 'Enter' && event.metaKey) {
    submit()
  }
}

function handleClick(event: MouseEvent) {
  console.log(event.clientX, event.clientY)
}
</script>

<template>
  <form @submit="handleSubmit">
    <input @input="handleInput" @keydown="handleKeydown" />
    <button type="submit">Submit</button>
  </form>
</template>
```

---

## 9. Testing Patterns

**Impact: LOW-MEDIUM**

Testing Vue components and composables effectively.

### 9.1 Component Testing with Vue Test Utils

```typescript
// components/__tests__/Counter.spec.ts
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Counter from '../Counter.vue'

describe('Counter', () => {
  it('renders initial count', () => {
    const wrapper = mount(Counter, {
      props: { initialCount: 5 }
    })
    expect(wrapper.text()).toContain('5')
  })
  
  it('increments count when button clicked', async () => {
    const wrapper = mount(Counter)
    
    await wrapper.find('button').trigger('click')
    
    expect(wrapper.text()).toContain('1')
  })
  
  it('emits update event', async () => {
    const wrapper = mount(Counter)
    
    await wrapper.find('button').trigger('click')
    
    expect(wrapper.emitted('update')).toBeTruthy()
    expect(wrapper.emitted('update')![0]).toEqual([1])
  })
})
```

### 9.2 Testing Composables

```typescript
// composables/__tests__/useCounter.spec.ts
import { describe, it, expect } from 'vitest'
import { useCounter } from '../useCounter'

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { count } = useCounter()
    expect(count.value).toBe(0)
  })
  
  it('initializes with provided value', () => {
    const { count } = useCounter(10)
    expect(count.value).toBe(10)
  })
  
  it('increments count', () => {
    const { count, increment } = useCounter()
    
    increment()
    
    expect(count.value).toBe(1)
  })
  
  it('resets to initial value', () => {
    const { count, increment, reset } = useCounter(5)
    
    increment()
    increment()
    reset()
    
    expect(count.value).toBe(5)
  })
})
```

### 9.3 Testing Pinia Stores

```typescript
// stores/__tests__/cart.spec.ts
import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useCartStore } from '../cart'

describe('Cart Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })
  
  it('starts with empty cart', () => {
    const store = useCartStore()
    expect(store.items).toHaveLength(0)
    expect(store.total).toBe(0)
  })
  
  it('adds items to cart', () => {
    const store = useCartStore()
    
    store.addItem({ id: '1', name: 'Product', price: 10, quantity: 2 })
    
    expect(store.items).toHaveLength(1)
    expect(store.total).toBe(20)
  })
  
  it('removes items from cart', () => {
    const store = useCartStore()
    store.addItem({ id: '1', name: 'Product', price: 10, quantity: 1 })
    
    store.removeItem('1')
    
    expect(store.items).toHaveLength(0)
  })
})
```

### 9.4 Testing with Nuxt

```typescript
// tests/pages/index.spec.ts
import { describe, it, expect } from 'vitest'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import IndexPage from '~/pages/index.vue'

describe('Index Page', () => {
  it('renders welcome message', async () => {
    const wrapper = await mountSuspended(IndexPage)
    expect(wrapper.text()).toContain('Welcome')
  })
})
```

---

## 10. Advanced Patterns

**Impact: LOW**

Advanced patterns for specific use cases.

### 10.1 Render Functions

**Impact: LOW (dynamic component generation)**

Use render functions for highly dynamic components.

```typescript
import { h, defineComponent } from 'vue'

export default defineComponent({
  props: {
    level: {
      type: Number,
      required: true,
      validator: (v: number) => v >= 1 && v <= 6
    }
  },
  setup(props, { slots }) {
    return () => h(
      `h${props.level}`,
      { class: 'heading' },
      slots.default?.()
    )
  }
})

// Or with <script setup>
<script setup lang="ts">
import { h } from 'vue'

const props = defineProps<{
  level: 1 | 2 | 3 | 4 | 5 | 6
}>()

const slots = defineSlots<{
  default(): any
}>()

const Heading = () => h(
  `h${props.level}`,
  { class: 'heading' },
  slots.default?.()
)
</script>

<template>
  <Heading />
</template>
```

### 10.2 Custom Directives

**Impact: LOW (DOM manipulation)**

Create custom directives for reusable DOM behavior.

```typescript
// directives/vFocus.ts
import type { Directive } from 'vue'

export const vFocus: Directive<HTMLElement> = {
  mounted(el) {
    el.focus()
  }
}

// directives/vClickOutside.ts
// Extend HTMLElement to include our custom property
interface HTMLElementWithClickOutside extends HTMLElement {
  _clickOutside?: (event: MouseEvent) => void
}

export const vClickOutside: Directive<HTMLElementWithClickOutside, () => void> = {
  mounted(el, binding) {
    el._clickOutside = (event: MouseEvent) => {
      if (!el.contains(event.target as Node)) {
        binding.value()
      }
    }
    document.addEventListener('click', el._clickOutside)
  },
  unmounted(el) {
    if (el._clickOutside) {
      document.removeEventListener('click', el._clickOutside)
    }
  }
}
```

**Usage:**

```vue
<script setup lang="ts">
import { vFocus, vClickOutside } from '@/directives'

function closeDropdown() {
  // close logic
}
</script>

<template>
  <input v-focus />
  <div v-click-outside="closeDropdown">
    Dropdown content
  </div>
</template>
```

### 10.3 Plugin Pattern

**Impact: LOW (app-wide features)**

Structure plugins with proper install function.

```typescript
// plugins/toast.ts
import type { App, InjectionKey } from 'vue'
import { ref, readonly } from 'vue'

interface Toast {
  id: number
  message: string
  type: 'success' | 'error' | 'info'
}

interface ToastPlugin {
  toasts: readonly Toast[]
  show: (message: string, type?: Toast['type']) => void
  dismiss: (id: number) => void
}

export const ToastKey: InjectionKey<ToastPlugin> = Symbol('toast')

export function createToastPlugin() {
  const toasts = ref<Toast[]>([])
  let id = 0
  
  function show(message: string, type: Toast['type'] = 'info') {
    const toast = { id: ++id, message, type }
    toasts.value.push(toast)
    
    setTimeout(() => dismiss(toast.id), 5000)
  }
  
  function dismiss(toastId: number) {
    const index = toasts.value.findIndex(t => t.id === toastId)
    if (index > -1) toasts.value.splice(index, 1)
  }
  
  return {
    install(app: App) {
      const plugin: ToastPlugin = {
        toasts: readonly(toasts.value),
        show,
        dismiss
      }
      
      app.provide(ToastKey, plugin)
      app.config.globalProperties.$toast = plugin
    }
  }
}

// Usage
const toast = inject(ToastKey)!
toast.show('Saved successfully', 'success')
```

---

## Anti-Patterns Summary

### ❌ DON'T:

- Use Options API in new Vue 3 projects
- Mutate props directly
- Use `this` in `<script setup>`
- Create `reactive()` with primitives
- Use v-if and v-for on same element
- Forget `:key` in v-for loops
- Use index as `:key` for dynamic lists
- Access refs without `.value` in script
- Nest Pinia stores unnecessarily
- Use `$fetch` in components (use `useFetch`)

### ✅ DO:

- Use Composition API with `<script setup>`
- Define props and emits with TypeScript
- Use computed for derived state
- Use watchEffect for side effects
- Leverage VueUse composables
- Use Pinia for global state
- Handle loading/error states
- Clean up effects in onUnmounted
- Use Suspense for async components
- Use shallowRef for large objects

---

## Decision Checklist

Before implementing:

- [ ] **Using `<script setup>`?**
- [ ] **Props and emits typed?**
- [ ] **Reactivity optimized?** (shallow refs where appropriate)
- [ ] **Components lazy loaded?** (routes, heavy components)
- [ ] **Data fetching correct?** (useFetch in Nuxt, not $fetch)
- [ ] **State management needed?** (Pinia for global state)
- [ ] **Effects cleaned up?** (onUnmounted handlers)
- [ ] **List rendering optimized?** (unique keys, v-memo, virtual scroll)

---

## References

1. [Vue 3 Documentation](https://vuejs.org/)
2. [Nuxt 3 Documentation](https://nuxt.com/)
3. [Pinia Documentation](https://pinia.vuejs.org/)
4. [VueUse](https://vueuse.org/)
5. [Vue Test Utils](https://test-utils.vuejs.org/)
6. [Vitest](https://vitest.dev/)
