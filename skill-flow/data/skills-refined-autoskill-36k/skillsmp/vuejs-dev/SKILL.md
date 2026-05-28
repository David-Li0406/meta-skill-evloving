---
name: vuejs-dev
description: |
  Vue 3 development: Composition API, reactivity, components, props/emits, Vue Router, Pinia.
  WHEN: Creating .vue components, using Composition API (ref, reactive, computed), props/emits, slots, composables, Vue Router navigation, Pinia state management.
  WHEN NOT: React development, plain HTML/JS (use html-dev, js-dev), ApexCharts (use vuejs-apex-charts), Shadcn components (use vuejs-shadcn).
---

# Vue.js Development

Core patterns and best practices for Vue.js development.

## Component Structure

Standard Single File Component (SFC) order:

```vue
<script setup lang="ts">
// 1. Imports
// 2. Props & Emits
// 3. Composables
// 4. Reactive state
// 5. Computed
// 6. Methods
// 7. Watchers
// 8. Lifecycle hooks
// 9. Expose (if needed)
</script>

<template>
  <!-- Template content -->
</template>

<style scoped>
/* Scoped styles */
</style>
```

## Props & Emits

### Vue 3 TypeScript

```typescript
// Props with types
const props = defineProps<{
  title: string
  count?: number
  items: string[]
}>()

// Props with defaults
const props = withDefaults(defineProps<{
  title: string
  count?: number
}>(), {
  count: 0
})

// Emits with types
const emit = defineEmits<{
  (e: 'update', id: number): void
  (e: 'delete'): void
}>()

// v-model (Vue 3.4+)
const modelValue = defineModel<string>()
const count = defineModel<number>('count', { default: 0 })
```

### Vue 3 JavaScript

```javascript
const props = defineProps({
  title: { type: String, required: true },
  count: { type: Number, default: 0 },
  items: { type: Array, default: () => [] }
})

const emit = defineEmits(['update', 'delete'])
```

## Reactivity

```typescript
import { ref, reactive, computed, watch, watchEffect } from 'vue'

// Primitives → ref
const count = ref(0)
const name = ref('')

// Objects → reactive (or ref)
const state = reactive({ loading: false, items: [] })

// Computed
const doubled = computed(() => count.value * 2)
const fullName = computed(() => `${first.value} ${last.value}`)

// Watch single source
watch(count, (newVal, oldVal) => {
  console.log(`Changed: ${oldVal} → ${newVal}`)
})

// Watch multiple sources
watch([firstName, lastName], ([newFirst, newLast]) => {
  // handle changes
})

// Watch with options
watch(source, callback, { immediate: true, deep: true })

// Auto-track dependencies
watchEffect(() => {
  console.log(`Count is ${count.value}`)
})
```

## Lifecycle Hooks

```typescript
import { 
  onMounted, 
  onUnmounted, 
  onBeforeMount,
  onBeforeUnmount,
  onUpdated 
} from 'vue'

onMounted(() => {
  // DOM is ready, fetch data, add listeners
})

onUnmounted(() => {
  // Cleanup: remove listeners, cancel requests
})
```

## Composables

Extract reusable logic into `composables/use*.ts`:

```typescript
// composables/useFetch.ts
import { ref, type Ref } from 'vue'

export function useFetch<T>(url: string) {
  const data: Ref<T | null> = ref(null)
  const error = ref<Error | null>(null)
  const loading = ref(false)

  async function execute() {
    loading.value = true
    error.value = null
    try {
      const res = await fetch(url)
      data.value = await res.json()
    } catch (e) {
      error.value = e as Error
    } finally {
      loading.value = false
    }
  }

  return { data, error, loading, execute }
}
```

## Template Patterns

### Conditional Rendering

```vue
<template>
  <!-- v-if: removes from DOM -->
  <div v-if="loading">Loading...</div>
  <div v-else-if="error">Error: {{ error }}</div>
  <div v-else>{{ data }}</div>

  <!-- v-show: toggles display CSS -->
  <div v-show="isVisible">Always in DOM</div>
</template>
```

### List Rendering

```vue
<template>
  <!-- Always use :key with unique identifier -->
  <ul>
    <li v-for="item in items" :key="item.id">
      {{ item.name }}
    </li>
  </ul>

  <!-- With index (use only if no unique id) -->
  <div v-for="(item, index) in items" :key="index">
    {{ item }}
  </div>
</template>
```

### Event Handling

```vue
<template>
  <button @click="handleClick">Click</button>
  <button @click="handleClick($event)">With event</button>
  <input @keyup.enter="submit" />
  <form @submit.prevent="onSubmit">...</form>
</template>
```

### Slots

```vue
<!-- Parent -->
<MyComponent>
  <template #header>Header content</template>
  <template #default>Default slot</template>
  <template #footer="{ count }">Footer: {{ count }}</template>
</MyComponent>

<!-- Child (MyComponent.vue) -->
<template>
  <header><slot name="header" /></header>
  <main><slot /></main>
  <footer><slot name="footer" :count="itemCount" /></footer>
</template>
```

## Provide/Inject

```typescript
// Parent component
import { provide, ref } from 'vue'

const theme = ref('dark')
provide('theme', theme)

// Child/descendant component
import { inject } from 'vue'

const theme = inject('theme', 'light') // with default
```

## Common Patterns

### Async Components

```typescript
import { defineAsyncComponent } from 'vue'

const AsyncModal = defineAsyncComponent(() => 
  import('./components/Modal.vue')
)
```

### Template Refs

```vue
<script setup>
import { ref, onMounted } from 'vue'

const inputRef = ref<HTMLInputElement | null>(null)

onMounted(() => {
  inputRef.value?.focus()
})
</script>

<template>
  <input ref="inputRef" />
</template>
```

### Expose

```typescript
// Expose methods/refs for parent access
defineExpose({
  focus: () => inputRef.value?.focus(),
  reset: () => { /* ... */ }
})
```

## Anti-Patterns to Avoid

1. **Direct prop mutation** → Emit event instead
2. **Reactive destructuring** → Use `toRefs()` or access via object
3. **Missing :key in v-for** → Always provide unique key
4. **Watchers without cleanup** → Return cleanup function
5. **Over-using reactive()** → Prefer ref() for simplicity
