# Pinia State Management

**Check if installed:** Look for `pinia` or `@pinia/nuxt` in package.json before using.

## Overview

Pinia is the official state management library for Vue. In Nuxt, it integrates seamlessly with auto-imports and SSR.

## Store Definition

Use the Composition API style with the setup function pattern.

```typescript
// stores/user.ts
export const useUserStore = defineStore("user", () => {
  // State
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)

  // Getters (computed)
  const isAuthenticated = computed(() => !!user.value)
  const fullName = computed(() => {
    if (!user.value) return ""
    return `${user.value.firstName} ${user.value.lastName}`
  })

  // Actions (functions)
  async function login(credentials: LoginCredentials) {
    const response = await $fetch("/api/auth/login", {
      method: "POST",
      body: credentials,
    })
    user.value = response.user
    token.value = response.token
  }

  function logout() {
    user.value = null
    token.value = null
  }

  return {
    // State
    user,
    token,
    // Getters
    isAuthenticated,
    fullName,
    // Actions
    login,
    logout,
  }
})
```

## Usage in Components

### Accessing Store

```typescript
<script setup lang="ts">
const userStore = useUserStore()

// Direct access (not reactive)
console.log(userStore.user)

// Reactive access using storeToRefs
const { user, isAuthenticated } = storeToRefs(userStore)

// Actions don't need storeToRefs
const { login, logout } = userStore
</script>
```

### Important: storeToRefs

Use `storeToRefs()` to maintain reactivity when destructuring state and getters:

```typescript
// ✅ Correct: Reactive
const { user, isAuthenticated } = storeToRefs(userStore)

// ❌ Wrong: Loses reactivity
const { user, isAuthenticated } = userStore

// ✅ Correct: Actions don't need storeToRefs
const { login, logout } = userStore
```

## SSR Considerations

Pinia stores are automatically hydrated in Nuxt. No special configuration needed for SSR.

### Server-side initialization

```typescript
// stores/config.ts
export const useConfigStore = defineStore('config', () => {
  const config = ref<AppConfig | null>(null)

  async function fetchConfig() {
    // This runs on server during SSR
    config.value = await $fetch('/api/config')
  }

  return { config, fetchConfig }
})

// Usage in page
<script setup lang="ts">
const configStore = useConfigStore()

// Fetch on server, hydrate on client
await configStore.fetchConfig()
</script>
```

## Persisting State

For client-side persistence, use `@pinia-plugin-persistedstate/nuxt`:

```typescript
// stores/preferences.ts
export const usePreferencesStore = defineStore(
  "preferences",
  () => {
    const theme = ref<"light" | "dark">("light")
    const language = ref("en")

    return { theme, language }
  },
  {
    persist: true, // Persists to localStorage
  },
)
```

## Multiple Stores Pattern

Organize stores by domain:

```
stores/
├── user.ts          # Authentication & user data
├── cart.ts          # Shopping cart
├── products.ts      # Product catalog
└── ui.ts            # UI state (modals, sidebars, etc.)
```

## Testing Stores

```typescript
import { setActivePinia, createPinia } from "pinia"
import { useUserStore } from "~/stores/user"

describe("User Store", () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it("should authenticate user", async () => {
    const store = useUserStore()
    await store.login({ email: "test@example.com", password: "password" })
    expect(store.isAuthenticated).toBe(true)
  })
})
```
