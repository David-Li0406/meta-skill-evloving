---
name: vue
description: >
  Vue 3 Composition API patterns with TypeScript, Pinia, and Vee-Validate.
  Trigger: When working with .vue files, composables, Pinia stores, or form validation.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
metadata:
  author: cvix
  version: "1.0"
---

# Vue 3 Skill

Conventions for Vue 3 development with Composition API, TypeScript, and the cvix component
ecosystem.

## When to Use

- Creating or modifying `.vue` components
- Building composables for reusable logic
- Managing state with Pinia stores
- Implementing form validation with Vee-Validate + Zod
- Working with the `@cvix/ui` component library

## Critical Patterns

### 1. Component Structure

**ALWAYS use `<script setup lang="ts">`**:

```vue
<script setup lang="ts">
// 1. Imports
import { computed, ref } from 'vue';
import { useUserStore } from '@/stores/user';

// 2. Type definitions
type Props = {
  title: string;
  count?: number;
  isActive?: boolean;
};

// 3. Props with defaults
const props = withDefaults(defineProps<Props>(), {
  count: 0,
  isActive: false,
});

// 4. Emits with types
const emit = defineEmits<{
  (e: 'update', value: number): void;
  (e: 'close'): void;
}>();

// 5. Composables and stores
const userStore = useUserStore();

// 6. Reactive state
const localCount = ref(props.count);

// 7. Computed properties
const doubled = computed(() => localCount.value * 2);

// 8. Methods
const increment = () => {
  localCount.value++;
  emit('update', localCount.value);
};
</script>

<template>
  <div class="card">
    <h2>{{ title }}</h2>
    <p>Count: {{ localCount }} (Doubled: {{ doubled }})</p>
    <button @click="increment">Increment</button>
  </div>
</template>

<style scoped>
.card {
  padding: var(--space-4);
}
</style>
```

### 2. Pinia Stores

**ALWAYS type state, getters, and actions**:

```typescript
// stores/user.ts
import { defineStore } from 'pinia';
import { api, isAxiosError } from '@/api';
import { toast } from 'vue-sonner';

type User = {
  id: string;
  name: string;
  email: string;
};

type UserState = {
  currentUser: User | null;
  isLoading: boolean;
  error: string | null;
};

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    currentUser: null,
    isLoading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state): boolean => state.currentUser !== null,
    userInitials: (state): string => {
      if (!state.currentUser) return '';
      return state.currentUser.name
        .split(' ')
        .map(n => n[0])
        .join('');
    },
  },

  actions: {
    async fetchUser(id: string): Promise<void> {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await api.getUser(id);
        this.currentUser = response.data;
      } catch (e) {
        // Type-safe error handling
        const error = e instanceof Error ? e : new Error('Unknown error');
        const message = isAxiosError(e) && e.response?.data?.message
          ? e.response.data.message
          : error.message || 'Failed to fetch user';

        this.error = message;
        toast.error('Error', { description: message });
      } finally {
        this.isLoading = false;
      }
    },

    logout(): void {
      this.currentUser = null;
    },
  },
});
```

### 3. Composables

**Return reactive values, prefix with `use`**:

```typescript
// composables/useCounter.ts
import { ref, computed, type Ref, type ComputedRef } from 'vue';

type UseCounterReturn = {
  count: Ref<number>;
  doubled: ComputedRef<number>;
  increment: () => void;
  decrement: () => void;
  reset: () => void;
};

export const useCounter = (initial = 0): UseCounterReturn => {
  const count = ref(initial);
  const doubled = computed(() => count.value * 2);

  const increment = () => count.value++;
  const decrement = () => count.value--;
  const reset = () => count.value = initial;

  return { count, doubled, increment, decrement, reset };
};
```

### 4. Form Validation (Vee-Validate + Zod)

**CRITICAL: Manual validation on blur, NOT automatic**:

```vue
<script setup lang="ts">
import { useForm } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/zod';
import { z } from 'zod';
import {
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
  Input,
  Button,
} from '@cvix/ui';

const schema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string().min(8, 'Must be at least 8 characters'),
});

type FormData = z.infer<typeof schema>;

const { handleSubmit, validateField, resetForm } = useForm<FormData>({
  validationSchema: toTypedSchema(schema),
  validateOnMount: false, // ✅ CRITICAL: Don't validate on mount
});

const onSubmit = handleSubmit((values) => {
  console.log('Form submitted:', values);
});
</script>

<template>
  <form @submit="onSubmit">
    <FormField v-slot="{ componentField }" name="email">
      <FormItem>
        <FormLabel>Email</FormLabel>
        <FormControl>
          <!-- ✅ Manual validation on blur -->
          <Input
            type="email"
            v-bind="componentField"
            @blur="validateField('email')"
          />
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>

    <Button type="submit">Submit</Button>
  </form>
</template>
```

### 5. Component Communication

| Scenario        | Approach                  |
|-----------------|---------------------------|
| Parent → Child  | Props                     |
| Child → Parent  | `emit()`                  |
| Sibling/Distant | Pinia store               |
| Provide/Inject  | Rarely, for deeply nested |

**NEVER use global event buses**.

## UI Components (@cvix/ui)

Use Shadcn-Vue components from `@cvix/ui`:

```vue
<script setup lang="ts">
import { Button, Card, CardHeader, CardTitle, CardContent } from '@cvix/ui';
</script>

<template>
  <Card>
    <CardHeader>
      <CardTitle>Dashboard</CardTitle>
    </CardHeader>
    <CardContent>
      <Button variant="default" @click="handleAction">
        Take Action
      </Button>
    </CardContent>
  </Card>
</template>
```

## Performance Patterns

```vue
<script setup lang="ts">
import { onUnmounted, shallowRef } from 'vue';

// ✅ Use shallowRef for large objects that don't need deep reactivity
const largeData = shallowRef<LargeObject | null>(null);

// ✅ Clean up side effects
const intervalId = setInterval(() => {
  // polling logic
}, 5000);

onUnmounted(() => {
  clearInterval(intervalId);
});
</script>

<template>
  <!-- ✅ v-once for truly static content -->
  <footer v-once>
    <p>© 2024 CVIX</p>
  </footer>

  <!-- ✅ v-memo for expensive lists -->
  <div v-for="item in items" :key="item.id" v-memo="[item.id, item.updated]">
    {{ item.name }}
  </div>
</template>
```

## Anti-Patterns

❌ **Options API** - Always use Composition API with `<script setup>`
❌ **`any` type** - Always provide proper TypeScript types
❌ **Mutating props** - Props are read-only, emit events instead
❌ **Global event bus** - Use Pinia for cross-component state
❌ **`validate-on-blur` prop** - Use manual `validateField()` on `@blur`
❌ **Field injection** - Use constructor pattern in stores

## i18n Pattern

```vue
<script setup lang="ts">
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
</script>

<template>
  <h1>{{ t('dashboard.title') }}</h1>
  <p>{{ t('dashboard.welcome', { name: user.name }) }}</p>
</template>
```

## Commands

```bash
# Development
pnpm --filter @cvix/webapp dev

# Testing
pnpm --filter @cvix/webapp vitest run
pnpm --filter @cvix/webapp vitest --watch

# Type checking
pnpm --filter @cvix/webapp vue-tsc --noEmit

# Linting
pnpm --filter @cvix/webapp lint
```

## Resources

- [Vue 3 Documentation](https://vuejs.org/guide/)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [Vee-Validate + Zod](https://vee-validate.logaretm.com/v4/integrations/zod-schema-validation/)
- [Shadcn-Vue](https://www.shadcn-vue.com/)
