# Vue & Nuxt

## Patterns


---
  #### **Name**
Composable Extraction
  #### **Description**
Extract reactive logic into reusable functions
  #### **When**
Logic is used in multiple components or is complex enough to test alone
  #### **Example**
    # COMPOSABLE PATTERN:
    
    """
    Composables are the primary way to share stateful logic in Vue 3.
    They're just functions that use Vue's reactivity system.
    """
    
    // composables/useCounter.ts
    import { ref, computed } from 'vue'
    
    export function useCounter(initial = 0) {
      const count = ref(initial)
    
      const doubled = computed(() => count.value * 2)
    
      function increment() {
        count.value++
      }
    
      function decrement() {
        count.value--
      }
    
      function reset() {
        count.value = initial
      }
    
      return {
        count,       // readonly ref
        doubled,     // computed
        increment,   // function
        decrement,
        reset
      }
    }
    
    // Usage in component
    <script setup>
    import { useCounter } from '@/composables/useCounter'
    
    const { count, increment, decrement } = useCounter(10)
    </script>
    
    <template>
      <button @click="decrement">-</button>
      <span>{{ count }}</span>
      <button @click="increment">+</button>
    </template>
    

---
  #### **Name**
Async Data Fetching (Nuxt)
  #### **Description**
Server-side data fetching with useFetch or useAsyncData
  #### **When**
Loading data in Nuxt pages or components
  #### **Example**
    # NUXT DATA FETCHING:
    
    """
    Nuxt provides useFetch and useAsyncData for SSR-compatible data fetching.
    Data is fetched on server, serialized, and hydrated on client.
    """
    
    // Using useFetch (simpler, includes $fetch)
    <script setup>
    const { data: posts, pending, error, refresh } = await useFetch('/api/posts')
    </script>
    
    // Using useAsyncData (more control)
    <script setup>
    const { data: user } = await useAsyncData('user', () =>
      $fetch(`/api/users/${route.params.id}`)
    )
    </script>
    
    // With error handling and loading states
    <template>
      <div v-if="pending">Loading...</div>
      <div v-else-if="error">Error: {{ error.message }}</div>
      <div v-else>
        <article v-for="post in posts" :key="post.id">
          {{ post.title }}
        </article>
      </div>
    </template>
    
    // Lazy loading (don't block navigation)
    <script setup>
    const { data } = useLazyFetch('/api/slow-data')
    </script>
    
    // Transform data
    <script setup>
    const { data: userNames } = await useFetch('/api/users', {
      transform: (users) => users.map(u => u.name)
    })
    </script>
    

---
  #### **Name**
Pinia Store Pattern
  #### **Description**
Centralized state management with Pinia
  #### **When**
State needs to be shared across multiple components
  #### **Example**
    # PINIA STORES:
    
    """
    Pinia replaced Vuex as the official state management solution.
    Simpler API, full TypeScript support, composition API friendly.
    """
    
    // stores/user.ts
    import { defineStore } from 'pinia'
    
    export const useUserStore = defineStore('user', () => {
      // State (refs)
      const user = ref<User | null>(null)
      const loading = ref(false)
    
      // Getters (computed)
      const isLoggedIn = computed(() => !!user.value)
      const displayName = computed(() =>
        user.value?.name ?? 'Anonymous'
      )
    
      // Actions (functions)
      async function login(email: string, password: string) {
        loading.value = true
        try {
          user.value = await authService.login(email, password)
        } finally {
          loading.value = false
        }
      }
    
      function logout() {
        user.value = null
      }
    
      return {
        user,
        loading,
        isLoggedIn,
        displayName,
        login,
        logout
      }
    })
    
    // Usage in component
    <script setup>
    const userStore = useUserStore()
    
    // Direct access
    console.log(userStore.displayName)
    
    // Destructure with storeToRefs for reactivity
    const { user, isLoggedIn } = storeToRefs(userStore)
    const { login, logout } = userStore  // Actions don't need storeToRefs
    </script>
    

---
  #### **Name**
Provide/Inject for DI
  #### **Description**
Dependency injection without prop drilling
  #### **When**
Deep component trees need access to shared values
  #### **Example**
    # PROVIDE/INJECT:
    
    """
    Provide/Inject allows ancestor components to serve as a dependency
    injector for all descendants, regardless of depth.
    """
    
    // Parent component (provider)
    <script setup>
    import { provide, ref } from 'vue'
    
    const theme = ref('dark')
    const toggleTheme = () => {
      theme.value = theme.value === 'dark' ? 'light' : 'dark'
    }
    
    // Provide with symbol key for type safety
    provide('theme', {
      theme,
      toggleTheme
    })
    </script>
    
    // Any descendant component (consumer)
    <script setup>
    import { inject } from 'vue'
    
    const { theme, toggleTheme } = inject('theme')!
    </script>
    
    <template>
      <div :class="theme">
        <button @click="toggleTheme">Toggle Theme</button>
      </div>
    </template>
    
    // Type-safe provide/inject
    import type { InjectionKey, Ref } from 'vue'
    
    interface ThemeContext {
      theme: Ref<'dark' | 'light'>
      toggleTheme: () => void
    }
    
    export const ThemeKey: InjectionKey<ThemeContext> = Symbol('theme')
    
    // Usage
    provide(ThemeKey, { theme, toggleTheme })
    const themeContext = inject(ThemeKey)!
    

---
  #### **Name**
v-model with Composables
  #### **Description**
Custom v-model bindings for form handling
  #### **When**
Building form components with two-way binding
  #### **Example**
    # V-MODEL PATTERN:
    
    """
    Vue 3 allows multiple v-model bindings per component and
    simplifies the event naming convention.
    """
    
    // Custom input component
    <script setup>
    const model = defineModel<string>()
    // Equivalent to:
    // const props = defineProps(['modelValue'])
    // const emit = defineEmits(['update:modelValue'])
    </script>
    
    <template>
      <input
        :value="model"
        @input="model = $event.target.value"
      />
    </template>
    
    // Multiple v-models
    <script setup>
    const firstName = defineModel<string>('firstName')
    const lastName = defineModel<string>('lastName')
    </script>
    
    // Usage
    <UserForm v-model:first-name="first" v-model:last-name="last" />
    
    // Form composable
    function useForm<T extends Record<string, any>>(initial: T) {
      const form = reactive({ ...initial })
      const errors = reactive<Partial<Record<keyof T, string>>>({})
    
      function reset() {
        Object.assign(form, initial)
        Object.keys(errors).forEach(k => delete errors[k as keyof T])
      }
    
      function validate(rules: Partial<Record<keyof T, (v: any) => string | null>>) {
        let valid = true
        for (const [key, rule] of Object.entries(rules)) {
          const error = rule(form[key as keyof T])
          if (error) {
            errors[key as keyof T] = error
            valid = false
          }
        }
        return valid
      }
    
      return { form, errors, reset, validate }
    }
    

## Anti-Patterns


---
  #### **Name**
Options API in New Code
  #### **Description**
Using Options API for new Vue 3 components
  #### **Why**
    Composition API offers better TypeScript support, code organization,
    and reusability through composables. Options API fragments related
    logic across data, methods, computed, and watch sections.
    
  #### **Instead**
    Use <script setup> with Composition API:
    
    // WRONG: Options API
    export default {
      data() { return { count: 0 } },
      methods: { increment() { this.count++ } },
      computed: { doubled() { return this.count * 2 } }
    }
    
    // RIGHT: Composition API
    <script setup>
    const count = ref(0)
    const doubled = computed(() => count.value * 2)
    const increment = () => count.value++
    </script>
    

---
  #### **Name**
Mutating Props
  #### **Description**
Directly modifying props instead of emitting events
  #### **Why**
    Props are read-only for a reason - it breaks one-way data flow and
    makes debugging impossible. The parent doesn't know its data changed.
    
  #### **Instead**
    Emit events for the parent to handle:
    
    // WRONG
    props.items.push(newItem)
    
    // RIGHT
    emit('add-item', newItem)
    
    // For v-model pattern
    <script setup>
    const model = defineModel()
    </script>
    

---
  #### **Name**
Overusing Watchers
  #### **Description**
Using watch when computed would work
  #### **Why**
    Watchers are imperative and side-effectful. Computed properties are
    declarative and cached. Most "watch" usage can be replaced with
    computed properties, which are easier to test and reason about.
    
  #### **Instead**
    // WRONG: Watch for derived state
    const items = ref([])
    const total = ref(0)
    watch(items, (newItems) => {
      total.value = newItems.reduce((sum, item) => sum + item.price, 0)
    })
    
    // RIGHT: Computed for derived state
    const items = ref([])
    const total = computed(() =>
      items.value.reduce((sum, item) => sum + item.price, 0)
    )
    

---
  #### **Name**
Prop Drilling Through Many Levels
  #### **Description**
Passing props through 4+ component levels
  #### **Why**
    Each intermediate component becomes coupled to props it doesn't use.
    Adding a new prop requires editing many files. Logic becomes hard
    to follow.
    
  #### **Instead**
    Use provide/inject for deep trees:
    
    // Provider (any ancestor)
    provide('user', user)
    
    // Consumer (any descendant)
    const user = inject('user')
    
    // Or Pinia for truly global state
    

---
  #### **Name**
Giant Components
  #### **Description**
Components with 300+ lines doing too much
  #### **Why**
    Large components are hard to test, hard to understand, and often
    hide reusable logic. If your template needs a comment to explain
    a section, that section is a component.
    
  #### **Instead**
    Extract smaller components and composables:
    
    - Each component should do one thing
    - If logic is reused, extract a composable
    - If UI is reused, extract a component
    - If template section needs a comment, it's a component
    