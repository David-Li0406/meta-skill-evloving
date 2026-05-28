---
name: Nuxt 4 Frontend Development
description: Expert guidance for Nuxt 4 projects with app/ directory structure, Vue 3 Composition API, TypeScript, Vitest, ESLint, and Tailwind CSS 4 with Vite plugin. Use when creating components, composables, tests, or any frontend code. Enforces Tailwind-only styling (no inline styles or custom CSS). Supports Nuxt layers.
version: 1.0.0
---

# Nuxt 4 Frontend Development Skill

## Overview

This skill guides development of modern, type-safe frontend applications using:
- **Nuxt 4** - Latest version with `app/` directory structure, improved TypeScript support and auto-imports
- **Vue 3** - Composition API with `<script setup>` syntax
- **TypeScript** - Strict mode enabled for maximum type safety
- **Vitest** - Fast unit testing with Vue Test Utils
- **ESLint** - Code quality and consistency
- **Tailwind CSS 4** - Utility-first styling with Vite plugin (NO inline styles or custom CSS allowed)

## When to Use This Skill

Use this skill when:
- Creating new Nuxt 4 components, composables, or utilities in the `app/` directory
- Writing tests for Vue components or composables
- Setting up or modifying project configuration
- Implementing new features following project conventions
- Styling components (MUST use Tailwind classes only, NO inline styles or custom CSS)
- Organizing code with Nuxt layers
- Setting up Tailwind 4 with the Vite plugin

## Project Structure

### Directory Organization

Nuxt 4 uses the `app/` directory as the primary source directory. All application code lives under `app/`:

```
project/
├── app/
│   ├── components/
│   │   ├── ui/              # Reusable UI components (buttons, inputs, etc.)
│   │   ├── features/        # Feature-specific components
│   │   └── layouts/         # Layout components
│   ├── composables/         # Reusable composition functions
│   ├── utils/               # Pure utility functions
│   ├── types/               # TypeScript type definitions
│   ├── pages/               # File-based routing
│   ├── layouts/             # Application layouts
│   ├── middleware/          # Route middleware
│   ├── plugins/             # Vue plugins
│   ├── assets/              # Assets to be processed (CSS, images)
│   │   └── css/
│   │       └── main.css     # Tailwind imports
│   └── app.vue              # Root application component
├── server/                  # Server API routes and middleware (stays at root)
│   ├── api/
│   ├── middleware/
│   └── utils/
├── layers/                  # Nuxt layers for code organization
│   └── base/                # Example: shared base layer
├── tests/                   # Test utilities and fixtures
│   ├── unit/
│   └── integration/
├── public/                  # Static assets (not processed)
└── nuxt.config.ts           # Nuxt configuration
```

**Key Points:**
- **All application code goes in `app/`** - components, composables, pages, layouts, etc.
- **Server code stays at root level** in `server/` directory
- **Use `app/assets/`** for assets that need processing (Tailwind CSS, images)
- **Use `public/`** for static files served as-is

### Naming Conventions

- **Components**: PascalCase (e.g., `app/components/UserProfile.vue`, `app/components/ui/BaseButton.vue`)
- **Composables**: camelCase with `use` prefix (e.g., `app/composables/useAuth.ts`, `app/composables/useFetchData.ts`)
- **Utils**: camelCase (e.g., `app/utils/formatDate.ts`, `app/utils/validateEmail.ts`)
- **Types**: PascalCase for interfaces/types (e.g., `User`, `ApiResponse`)
- **Pages**: kebab-case (e.g., `app/pages/user-profile.vue`, `app/pages/about-us.vue`)
- **Layouts**: kebab-case (e.g., `app/layouts/default.vue`, `app/layouts/admin.vue`)
- **Test files**: Match source file with `.test.ts` or `.spec.ts` suffix

### Nuxt Layers

Nuxt layers allow you to organize and share code across projects. Use layers for:
- Shared UI components and composables
- Base configuration and setup
- Theme systems
- Multi-tenant applications

**Layer Structure:**
```
layers/
├── base/                    # Shared base layer
│   ├── app/
│   │   ├── components/
│   │   ├── composables/
│   │   └── utils/
│   └── nuxt.config.ts       # Layer-specific config
└── admin/                   # Admin-specific layer
    ├── app/
    │   ├── components/
    │   └── pages/
    └── nuxt.config.ts
```

**Using Layers in nuxt.config.ts:**
```typescript
export default defineNuxtConfig({
  extends: [
    './layers/base',
    './layers/admin'
  ]
})
```

**Layer Best Practices:**
- Each layer should have its own `nuxt.config.ts`
- Layers can extend other layers
- Components, composables, and utils from layers are auto-imported
- Layer order matters - later layers override earlier ones
- Keep layers focused on specific domains or features
- Document layer dependencies clearly

**Example Base Layer Config:**
```typescript
// layers/base/nuxt.config.ts
export default defineNuxtConfig({
  components: {
    dirs: [
      {
        path: '~/components',
        global: true
      }
    ]
  }
})
```

## Code Standards

### TypeScript Configuration

Always use strict TypeScript settings:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  typescript: {
    strict: true,
    typeCheck: true,
  }
})
```

**Type Definition Best Practices:**
- Define interfaces in `types/` directory for shared types
- Use `type` for unions, intersections, and simple aliases
- Use `interface` for object shapes that may be extended
- Export types from a central `types/index.ts` for easy imports
- Always type function parameters and return values

### Vue 3 Component Patterns

**Preferred Component Structure:**

```vue
<script setup lang="ts">
// 1. Imports
import { ref, computed, onMounted } from 'vue'
import type { User } from '~/types'

// 2. Props and Emits
interface Props {
  userId: string
  isActive?: boolean
}

interface Emits {
  update: [user: User]
  close: []
}

const props = withDefaults(defineProps<Props>(), {
  isActive: true
})

const emit = defineEmits<Emits>()

// 3. Composables
const { data: user, pending } = await useFetch(`/api/users/${props.userId}`)

// 4. Reactive State
const isEditing = ref(false)

// 5. Computed Properties
const displayName = computed(() => 
  user.value ? `${user.value.firstName} ${user.value.lastName}` : ''
)

// 6. Methods
const handleUpdate = () => {
  if (user.value) {
    emit('update', user.value)
  }
}

// 7. Lifecycle
onMounted(() => {
  console.log('Component mounted')
})
</script>

<template>
  <div class="container">
    <!-- Template content -->
  </div>
</template>
```

**Key Principles:**
- Always use `<script setup>` for Composition API
- Use `lang="ts"` on script tags
- Destructure props carefully (use `.value` when needed)
- Prefer `computed` over methods for derived state
- Use `defineProps` with TypeScript interfaces, not runtime props

### Composables Patterns

**Structure for Reusable Composables:**

```typescript
// composables/useAuth.ts
import { ref, computed } from 'vue'
import type { User } from '~/types'

export const useAuth = () => {
  // State
  const user = ref<User | null>(null)
  const isLoading = ref(false)
  const error = ref<Error | null>(null)

  // Computed
  const isAuthenticated = computed(() => !!user.value)

  // Methods
  const login = async (email: string, password: string) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await $fetch<User>('/api/auth/login', {
        method: 'POST',
        body: { email, password }
      })
      user.value = response
    } catch (e) {
      error.value = e as Error
      throw e
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    await $fetch('/api/auth/logout', { method: 'POST' })
    user.value = null
  }

  // Return public API
  return {
    user: readonly(user),
    isAuthenticated,
    isLoading: readonly(isLoading),
    error: readonly(error),
    login,
    logout
  }
}
```

**Composable Best Practices:**
- Always return an object with named properties
- Use `readonly()` for state that shouldn't be mutated externally
- Include loading and error states for async operations
- Provide TypeScript types for all parameters and return values
- Keep composables focused on a single responsibility

### Data Fetching Patterns

**Preferred Nuxt 4 Data Fetching:**

```typescript
// Good: Using useFetch with auto-typed response
const { data, pending, error, refresh } = await useFetch('/api/users', {
  query: { limit: 10 }
})

// Good: Using useAsyncData for more control
const { data: users } = await useAsyncData(
  'users-list',
  () => $fetch<User[]>('/api/users')
)

// Good: Lazy loading with explicit type
const { data, pending } = useLazyFetch<Product>(`/api/products/${id}`)
```

**Data Fetching Rules:**
- Use `useFetch` for simple API calls
- Use `useAsyncData` when you need custom async logic
- Add unique keys to `useAsyncData` to manage cache
- Always await in `<script setup>` to enable SSR
- Use `useLazyFetch` for client-side only or lazy loading
- Type the response explicitly when TypeScript can't infer

### Tailwind CSS Guidelines

**CRITICAL: We use Tailwind 4 with the Vite plugin. ALWAYS use Tailwind utility classes. NEVER use inline styles or custom CSS that could be achieved with Tailwind classes.**

**Tailwind 4 Setup:**
```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  vite: {
    plugins: [
      // Tailwind 4 uses Vite plugin instead of PostCSS
    ]
  },
  css: ['~/assets/css/main.css']
})
```

```css
/* app/assets/css/main.css */
@import "tailwindcss";

/* Custom design tokens (if needed) */
@theme {
  --color-primary: #3b82f6;
  --color-secondary: #8b5cf6;
  --font-display: 'Inter', sans-serif;
}
```

**Mandatory Class Usage Rules:**

❌ **NEVER do this:**
```vue
<!-- BAD: Inline styles -->
<div style="padding: 16px; background-color: blue;">

<!-- BAD: Custom CSS that could be Tailwind -->
<style scoped>
.my-button {
  padding: 1rem;
  background-color: #3b82f6;
  border-radius: 0.5rem;
}
</style>

<!-- BAD: Arbitrary CSS properties -->
<div class="[background:linear-gradient(to-right,#fff,#000)]">
```

✅ **ALWAYS do this:**
```vue
<!-- GOOD: Pure Tailwind classes -->
<div class="p-4 bg-blue-500">

<button class="px-4 py-2 bg-blue-600 rounded-lg">

<!-- GOOD: Use Tailwind's gradient utilities -->
<div class="bg-gradient-to-r from-white to-black">
```

**Class Organization:**
Order classes by category for better readability:
1. **Layout**: `flex`, `grid`, `block`, `inline-flex`
2. **Positioning**: `relative`, `absolute`, `top-0`, `left-0`
3. **Spacing**: `p-4`, `m-2`, `space-x-4`, `gap-4`
4. **Sizing**: `w-full`, `h-screen`, `max-w-lg`
5. **Typography**: `text-sm`, `font-bold`, `leading-tight`
6. **Colors**: `text-gray-900`, `bg-blue-600`
7. **Borders**: `border`, `border-gray-300`, `rounded-lg`
8. **Effects**: `shadow-lg`, `opacity-50`
9. **Transitions**: `transition-all`, `duration-300`
10. **States**: `hover:bg-blue-700`, `focus:ring-2`, `disabled:opacity-50`

**Example:**
```vue
<template>
  <button
    class="
      flex items-center justify-center
      px-6 py-3 
      w-full max-w-xs
      text-base font-semibold text-white 
      bg-blue-600 rounded-xl
      shadow-md
      transition-all duration-200
      hover:bg-blue-700 hover:shadow-lg
      focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
      active:scale-95
      disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-blue-600
    "
    :disabled="isLoading"
  >
    <LoadingSpinner v-if="isLoading" class="mr-2 h-4 w-4" />
    {{ isLoading ? 'Processing...' : 'Submit' }}
  </button>
</template>
```

**Responsive Design:**
```vue
<template>
  <div class="
    grid grid-cols-1 
    sm:grid-cols-2 
    md:grid-cols-3 
    lg:grid-cols-4 
    gap-4
    p-4 
    sm:p-6 
    lg:p-8
  ">
    <!-- Content -->
  </div>
</template>
```

**When to Extract Components:**
If you're repeating the same class combinations across multiple components, extract them into a reusable component:

```vue
<!-- app/components/ui/PrimaryButton.vue -->
<template>
  <button
    class="
      px-6 py-3 
      text-base font-semibold text-white 
      bg-blue-600 rounded-xl
      hover:bg-blue-700
      focus:outline-none focus:ring-2 focus:ring-blue-500
      disabled:opacity-50 disabled:cursor-not-allowed
    "
    v-bind="$attrs"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
defineOptions({
  inheritAttrs: false
})
</script>
```

**DO NOT use `@apply` or custom CSS:**
```css
/* ❌ BAD - Don't do this */
<style scoped>
.btn-primary {
  @apply px-6 py-3 bg-blue-600 text-white rounded-xl;
}
</style>

/* ✅ GOOD - Use Tailwind classes directly in template */
```

**Tailwind 4 Configuration:**
```typescript
// tailwind.config.ts (if needed for custom values)
export default {
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eff6ff',
          500: '#3b82f6',
          900: '#1e3a8a',
        }
      },
      spacing: {
        '128': '32rem',
      }
    }
  }
}
```

**Custom Properties with Tailwind 4:**
Use CSS custom properties in `@theme` for dynamic theming:
```css
/* app/assets/css/main.css */
@import "tailwindcss";

@theme {
  --color-brand-primary: oklch(0.5 0.2 240);
  --color-brand-secondary: oklch(0.6 0.15 280);
  --radius-default: 0.5rem;
}
```

Then use in templates:
```vue
<div class="bg-brand-primary text-white rounded-[--radius-default]">
```

**Key Principles:**
- NEVER write custom CSS that could be Tailwind utilities
- NEVER use inline `style` attributes
- Extract repeated patterns to reusable components, NOT CSS
- Use Tailwind's spacing scale (don't use arbitrary values unless absolutely necessary)
- Leverage Tailwind's color palette - only extend when brand requires specific colors
- Always use responsive prefixes for mobile-first design

### ESLint Configuration

**Expected ESLint Setup:**
```javascript
// .eslintrc.cjs or eslint.config.js
module.exports = {
  extends: [
    '@nuxt/eslint-config',
    'plugin:vue/vue3-recommended',
    'plugin:@typescript-eslint/recommended'
  ],
  rules: {
    'vue/multi-word-component-names': 'error',
    'vue/component-name-in-template-casing': ['error', 'PascalCase'],
    '@typescript-eslint/no-explicit-any': 'warn',
    '@typescript-eslint/explicit-function-return-type': 'off',
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off'
  }
}
```

## Testing with Vitest

### Test File Structure

```typescript
// components/UserCard.test.ts
import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import UserCard from './UserCard.vue'
import type { User } from '~/types'

describe('UserCard', () => {
  const mockUser: User = {
    id: '1',
    name: 'John Doe',
    email: 'john@example.com'
  }

  it('renders user information correctly', () => {
    const wrapper = mount(UserCard, {
      props: { user: mockUser }
    })

    expect(wrapper.text()).toContain('John Doe')
    expect(wrapper.text()).toContain('john@example.com')
  })

  it('emits delete event when delete button clicked', async () => {
    const wrapper = mount(UserCard, {
      props: { user: mockUser }
    })

    await wrapper.find('[data-test="delete-btn"]').trigger('click')
    
    expect(wrapper.emitted('delete')).toBeTruthy()
    expect(wrapper.emitted('delete')?.[0]).toEqual([mockUser.id])
  })
})
```

### Composable Testing

```typescript
// composables/useCounter.test.ts
import { describe, it, expect } from 'vitest'
import { useCounter } from './useCounter'

describe('useCounter', () => {
  it('increments counter', () => {
    const { count, increment } = useCounter()
    
    expect(count.value).toBe(0)
    increment()
    expect(count.value).toBe(1)
  })

  it('decrements counter', () => {
    const { count, decrement } = useCounter(5)
    
    expect(count.value).toBe(5)
    decrement()
    expect(count.value).toBe(4)
  })
})
```

### Testing Best Practices

- **Test user behavior, not implementation details**
- Use `data-test` attributes for reliable element selection
- Mock external dependencies (APIs, composables)
- Test edge cases and error states
- Keep tests isolated and independent
- Use `describe` blocks to organize related tests
- Write descriptive test names that explain the expected behavior

### Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./tests/setup.ts']
  },
  resolve: {
    alias: {
      '~': fileURLToPath(new URL('./', import.meta.url)),
      '@': fileURLToPath(new URL('./', import.meta.url))
    }
  }
})
```

## Common Patterns

### Form Handling

```vue
<script setup lang="ts">
import { ref, reactive } from 'vue'
import { z } from 'zod'

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8)
})

type FormData = z.infer<typeof schema>

const form = reactive<FormData>({
  email: '',
  password: ''
})

const errors = ref<Partial<Record<keyof FormData, string>>>({})
const isSubmitting = ref(false)

const handleSubmit = async () => {
  errors.value = {}
  
  const result = schema.safeParse(form)
  if (!result.success) {
    result.error.issues.forEach(issue => {
      if (issue.path[0]) {
        errors.value[issue.path[0] as keyof FormData] = issue.message
      }
    })
    return
  }

  isSubmitting.value = true
  try {
    await $fetch('/api/auth/login', {
      method: 'POST',
      body: form
    })
  } catch (e) {
    console.error(e)
  } finally {
    isSubmitting.value = false
  }
}
</script>
```

### Error Handling

```typescript
// utils/error-handler.ts
export class ApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public code?: string
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

export const handleApiError = (error: unknown): string => {
  if (error instanceof ApiError) {
    return error.message
  }
  
  if (error instanceof Error) {
    return error.message
  }
  
  return 'An unexpected error occurred'
}
```

### Loading States

```vue
<script setup lang="ts">
const { data, pending, error } = await useFetch('/api/data')
</script>

<template>
  <div>
    <div v-if="pending" class="flex justify-center p-8">
      <LoadingSpinner />
    </div>
    
    <div v-else-if="error" class="text-red-600">
      {{ error.message }}
    </div>
    
    <div v-else-if="data">
      <!-- Render data -->
    </div>
  </div>
</template>
```

## Anti-Patterns (Don't Do This)

### ❌ Avoid Options API

```vue
<!-- BAD -->
<script lang="ts">
export default {
  data() {
    return { count: 0 }
  },
  methods: {
    increment() { this.count++ }
  }
}
</script>

<!-- GOOD -->
<script setup lang="ts">
const count = ref(0)
const increment = () => count.value++
</script>
```

### ❌ Don't Use `any` Type

```typescript
// BAD
const fetchData = async (): Promise<any> => { ... }

// GOOD
const fetchData = async (): Promise<User[]> => { ... }
```

### ❌ Avoid Mutating Props

```vue
<script setup lang="ts">
const props = defineProps<{ count: number }>()

// BAD
const increment = () => props.count++

// GOOD
const emit = defineEmits<{ increment: [] }>()
const increment = () => emit('increment')
</script>
```

### ❌ NEVER Use Inline Styles

```vue
<!-- BAD - Inline styles are forbidden -->
<div style="padding: 16px; background-color: blue;">
<div :style="{ padding: '16px', backgroundColor: 'blue' }">
<div :style="computedStyles">

<!-- GOOD - Always use Tailwind classes -->
<div class="p-4 bg-blue-500">
```

### ❌ NEVER Write Custom CSS for Tailwind-Available Styles

```vue
<!-- BAD - Don't write CSS that Tailwind already provides -->
<style scoped>
.my-container {
  display: flex;
  align-items: center;
  padding: 1rem;
  background-color: #3b82f6;
  border-radius: 0.5rem;
}
</style>

<!-- GOOD - Use Tailwind utilities -->
<div class="flex items-center p-4 bg-blue-500 rounded-lg">
```

### ❌ Don't Use @apply Directive

```vue
<!-- BAD - Avoid @apply, use classes directly -->
<style scoped>
.btn {
  @apply px-4 py-2 bg-blue-600 text-white rounded-lg;
}
</style>

<!-- GOOD - Component extraction for reuse -->
<!-- app/components/ui/Button.vue -->
<template>
  <button class="px-4 py-2 bg-blue-600 text-white rounded-lg">
    <slot />
  </button>
</template>
```

### ❌ Don't Use Nuxt 2 Patterns

```typescript
// BAD (Nuxt 2)
export default {
  asyncData({ $axios }) {
    return $axios.get('/api/users')
  }
}

// GOOD (Nuxt 4)
const { data: users } = await useFetch('/api/users')
```

### ❌ Avoid Deep Prop Drilling

```typescript
// BAD - passing data through many layers
<ComponentA :user="user" />
  <ComponentB :user="user" />
    <ComponentC :user="user" />

// GOOD - use composables or provide/inject
// In parent
provide('user', user)

// In deep child
const user = inject<User>('user')
```

### ❌ Don't Use Old Folder Structure

```typescript
// BAD (Nuxt 3 and earlier)
components/MyComponent.vue
composables/useAuth.ts
pages/index.vue

// GOOD (Nuxt 4)
app/components/MyComponent.vue
app/composables/useAuth.ts
app/pages/index.vue
```

## Quick Reference Commands

```bash
# Development
npm run dev

# Type checking
npm run typecheck

# Linting
npm run lint
npm run lint:fix

# Testing
npm run test
npm run test:watch
npm run test:coverage

# Build
npm run build
npm run preview
```

## Additional Notes

- Always run `npm run typecheck` before committing
- Use `console.log` sparingly; prefer debugging tools
- Keep components under 200 lines; split if larger
- Write tests for all business logic and complex components
- Document complex logic with comments
- Use TypeScript's utility types (`Partial`, `Pick`, `Omit`, etc.)
- **CRITICAL**: NEVER use inline styles (`style` attribute or `:style` binding)
- **CRITICAL**: NEVER write custom CSS that could be Tailwind utility classes
- **CRITICAL**: All styling MUST use Tailwind utility classes directly in templates
- All application code goes in the `app/` directory (Nuxt 4 convention)
- Use Nuxt layers for shared code and multi-tenant applications
- Extract repeated Tailwind patterns into reusable components, not CSS classes

## Resources

- [Nuxt 4 Documentation](https://nuxt.com/docs)
- [Vue 3 Composition API](https://vuejs.org/api/composition-api-setup.html)
- [Vitest Documentation](https://vitest.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
