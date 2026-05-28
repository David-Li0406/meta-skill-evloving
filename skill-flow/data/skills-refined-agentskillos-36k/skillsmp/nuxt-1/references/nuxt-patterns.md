# Nuxt Common Patterns

## Data Fetching

### useFetch for API Calls

Use `useFetch` for API endpoints. It runs on both server and client, with automatic hydration.

```typescript
const { data, status, error, refresh } = await useFetch("/api/users")

// With query parameters
const { data, status } = await useFetch("/api/users", {
  query: { limit: 10, page: 1 },
})

// With type safety
interface User {
  id: number
  name: string
}
const { data, status, error } = await useFetch<User[]>("/api/users")
```

**Status values:** `'idle'` | `'pending'` | `'success'` | `'error'`

**Handle all states in templates:**

```vue
<template>
  <div v-if="status === 'pending'">Loading...</div>
  <div v-else-if="status === 'error'">
    <p>Error: {{ error?.message }}</p>
  </div>
  <div v-else-if="data">
    <!-- Success state -->
    <ul>
      <li v-for="user of data" :key="user.id">{{ user.name }}</li>
    </ul>
  </div>
</template>
```

### useAsyncData for Complex Data

Use `useAsyncData` when you need more control or complex transformations.

```typescript
const { data, status, error } = await useAsyncData("users", async () => {
  const users = await $fetch("/api/users")
  const stats = await $fetch("/api/stats")
  return { users, stats }
})

// With caching key
const { data, status, error } = await useAsyncData(`user-${id}`, () =>
  $fetch(`/api/users/${id}`),
)
```

### Lazy Fetching

Use lazy variants when you don't want to block navigation:

```typescript
// Non-blocking
const { status, data } = await useLazyFetch('/api/users')

// Show loading state
<div v-if="status === 'pending'">Loading...</div>
<div v-else>{{ data }}</div>
```

### Client-Only Fetching

```typescript
const { data } = await useFetch("/api/users", {
  server: false, // Only fetch on client
})
```

### Refresh and Refetch

```typescript
const { data, status, refresh } = await useFetch("/api/users")

// Manually refetch
await refresh()

// Refetch on event
watch(searchQuery, () => refresh())
```

## SEO and Meta Tags

### useHead

```typescript
useHead({
  title: "My Page",
  meta: [
    { name: "description", content: "Page description" },
    { property: "og:title", content: "My Page" },
  ],
  link: [{ rel: "canonical", href: "https://example.com/page" }],
})
```

### useSeoMeta (Type-Safe)

```typescript
useSeoMeta({
  title: "My Page",
  description: "Page description",
  ogTitle: "My Page",
  ogDescription: "Page description",
  ogImage: "https://example.com/image.jpg",
  twitterCard: "summary_large_image",
})
```

### definePageMeta

```typescript
definePageMeta({
  title: "User Profile",
  description: "View user profile",
  middleware: ["auth"],
})
```

## Error Handling

### Show Error Page

```typescript
showError({
  statusCode: 404,
  message: "Page not found",
})

// With custom error
showError({
  statusCode: 403,
  message: "Access denied",
  fatal: true,
})
```

### Clear Error

```typescript
clearError({ redirect: "/" })
```

### Handle Errors in Data Fetching

```typescript
const { data, status, error } = await useFetch("/api/users")

if (error.value) {
  showError({
    statusCode: error.value.statusCode,
    message: error.value.message,
  })
}
```

### Error Component

```vue
<!-- error.vue -->
<template>
  <div>
    <h1>{{ error.statusCode }}</h1>
    <p>{{ error.message }}</p>
    <button @click="handleError">Go Home</button>
  </div>
</template>

<script setup lang="ts">
const { error } = defineProps<{
  error: { statusCode: number; message: string }
}>()

function handleError() {
  clearError({ redirect: "/" })
}
</script>
```

## Environment Variables and Config

### Runtime Config

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  runtimeConfig: {
    // Private (server-only)
    apiSecret: process.env.API_SECRET,
    databaseUrl: process.env.DATABASE_URL,

    // Public (exposed to client)
    public: {
      apiBase: process.env.API_BASE_URL || "http://localhost:3000",
      environment: process.env.NODE_ENV,
    },
  },
})

// Usage
const config = useRuntimeConfig()
console.log(config.public.apiBase) // Available everywhere
console.log(config.apiSecret) // Server-only
```

### App Config

For non-sensitive configuration that can be updated at runtime:

```typescript
// app.config.ts
export default defineAppConfig({
  theme: {
    primaryColor: "#3b82f6",
  },
})

// Usage
const appConfig = useAppConfig()
console.log(appConfig.theme.primaryColor)
```

## Server API Routes

### GET Request

```typescript
// server/api/users.get.ts
export default defineEventHandler(async (event) => {
  const query = getQuery(event)

  return {
    users: [
      { id: 1, name: "Alice" },
      { id: 2, name: "Bob" },
    ],
  }
})
```

### POST Request

```typescript
// server/api/users.post.ts
export default defineEventHandler(async (event) => {
  const body = await readBody(event)

  // Validate and save user
  return { success: true, user: body }
})
```

### Dynamic Routes

```typescript
// server/api/users/[id].get.ts
export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, "id")

  // Fetch user by id
  return { id, name: "User" }
})
```

### Error Handling in API Routes

```typescript
export default defineEventHandler(async (event) => {
  try {
    const data = await fetchData()
    return data
  } catch (error) {
    throw createError({
      statusCode: 500,
      message: "Internal server error",
    })
  }
})
```

### Protected API Routes

Requires `nuxt-auth-utils` module for session management.

```typescript
// server/api/admin/users.get.ts
export default defineEventHandler(async (event) => {
  const session = await requireUserSession(event) // from nuxt-auth-utils

  if (!session.user.isAdmin) {
    throw createError({
      statusCode: 403,
      message: "Forbidden",
    })
  }

  return { users: [] }
})
```

## Middleware

### Route Middleware

```typescript
// middleware/auth.ts
export default defineNuxtRouteMiddleware((to, from) => {
  const user = useState("user")

  if (!user.value) {
    return navigateTo("/login")
  }
})

// Usage in page
definePageMeta({
  middleware: "auth",
})
```

### Global Middleware

```typescript
// middleware/analytics.global.ts
export default defineNuxtRouteMiddleware((to, from) => {
  // Track page view
  console.log("Navigating to:", to.path)
})
```

## State Management

### useState

For shared state across components:

```typescript
// composables/useAuth.ts
export const useAuth = () => {
  const user = useState<User | null>("user", () => null)
  const isAuthenticated = computed(() => !!user.value)

  async function login(credentials: LoginCredentials) {
    const response = await $fetch("/api/auth/login", {
      method: "POST",
      body: credentials,
    })
    user.value = response.user
  }

  function logout() {
    user.value = null
  }

  return {
    user,
    isAuthenticated,
    login,
    logout,
  }
}

// Usage in component
const { user, login, logout } = useAuth()
```

## Composables

### Auto-Import from composables/

```typescript
// composables/useCounter.ts
export const useCounter = () => {
  const count = ref(0)

  function increment() {
    count.value++
  }

  function decrement() {
    count.value--
  }

  return {
    count,
    increment,
    decrement,
  }
}

// Usage (auto-imported)
const { count, increment } = useCounter()
```

## Layouts

### Default Layout

```vue
<!-- layouts/default.vue -->
<template>
  <div>
    <header>
      <nav>Navigation</nav>
    </header>
    <main>
      <slot />
    </main>
    <footer>Footer</footer>
  </div>
</template>
```

### Custom Layout

```vue
<!-- layouts/admin.vue -->
<template>
  <div class="admin-layout">
    <aside>Sidebar</aside>
    <main>
      <slot />
    </main>
  </div>
</template>

<!-- Usage in page -->
<script setup lang="ts">
definePageMeta({
  layout: "admin",
})
</script>
```

### Dynamic Layout

```typescript
setPageLayout("admin")
```

## Plugins

### Client-Only Plugin

```typescript
// plugins/analytics.client.ts
export default defineNuxtPlugin(() => {
  // Only runs on client
  console.log("Client-side analytics initialized")
})
```

### Server-Only Plugin

```typescript
// plugins/database.server.ts
export default defineNuxtPlugin(() => {
  // Only runs on server
  return {
    provide: {
      db: createDatabaseConnection(),
    },
  }
})
```

### Universal Plugin

```typescript
// plugins/api.ts
export default defineNuxtPlugin(() => {
  const api = $fetch.create({
    baseURL: "/api",
    onResponseError({ response }) {
      if (response.status === 401) {
        navigateTo("/login")
      }
    },
  })

  return {
    provide: {
      api,
    },
  }
})

// Usage
const { $api } = useNuxtApp()
const data = await $api("/users")
```
