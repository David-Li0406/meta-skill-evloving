---
name: Vue Expert
description: Expert Vue 3 - Composition API, Pinia, Vue patterns et bonnes pratiques
workflows:
  - id: vue-creation
    template: wf-creation
    phase: Production
    name: Développement Vue.js
    duration: ongoing
  - id: vue-migration
    template: wf-refonte
    phase: Migration
    name: Migration Vue 2 → Vue 3
    duration: 5-15 jours
---

# Agent Vue Expert

## Responsabilité

Maîtriser Vue 3 avec la Composition API pour créer des applications réactives et maintenables.

## Tu NE fais PAS

- ❌ Implémenter Nuxt.js spécifiquement (SSR, modules) → Déléguer à un expert Nuxt si disponible
- ❌ Gérer le state Pinia avancé (patterns complexes, persistence) → `state-management/`
- ❌ Tester les composants Vue → `testing/component-testing.md`
- ❌ Optimiser les performances avancées → `performance/`

## Composants avec Script Setup

### Structure de base

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import type { User } from '@/types';

// Props avec valeurs par défaut
interface Props {
  userId: string;
  showAvatar?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  showAvatar: true
});

// Emits typés
const emit = defineEmits<{
  select: [id: string];
  update: [user: User];
}>();

// State réactif
const user = ref<User | null>(null);
const isLoading = ref(true);

// Computed
const fullName = computed(() => {
  if (!user.value) return '';
  return `${user.value.firstName} ${user.value.lastName}`;
});

// Methods
function handleSelect() {
  if (user.value) {
    emit('select', user.value.id);
  }
}

// Lifecycle
onMounted(async () => {
  user.value = await fetchUser(props.userId);
  isLoading.value = false;
});
</script>

<template>
  <div v-if="isLoading" class="skeleton" />
  <article v-else-if="user" class="user-card" @click="handleSelect">
    <img v-if="showAvatar" :src="user.avatar" :alt="fullName" />
    <h2>{{ fullName }}</h2>
    <p>{{ user.email }}</p>
  </article>
</template>

<style scoped>
.user-card {
  padding: 1rem;
  border-radius: 8px;
  cursor: pointer;
}
</style>
```

## Réactivité

### ref vs reactive

```vue
<script setup lang="ts">
import { ref, reactive, toRefs } from 'vue';

// ref - pour primitives et valeurs simples
const count = ref(0);
const message = ref('Hello');
count.value++; // Accès avec .value en JS

// reactive - pour objets
const state = reactive({
  count: 0,
  items: [] as string[]
});
state.count++; // Accès direct

// Destructuration avec toRefs
const { count: countRef, items } = toRefs(state);

// ref pour objets (recommandé pour la cohérence)
const user = ref<User | null>(null);
user.value = { name: 'John' };
</script>

<template>
  <!-- Dans le template, pas besoin de .value -->
  <p>Count: {{ count }}</p>
  <p>State count: {{ state.count }}</p>
</template>
```

### Computed et Watch

```vue
<script setup lang="ts">
import { ref, computed, watch, watchEffect } from 'vue';

const firstName = ref('John');
const lastName = ref('Doe');

// Computed - réactif, mémorisé
const fullName = computed(() => `${firstName.value} ${lastName.value}`);

// Computed writable
const fullNameWritable = computed({
  get: () => `${firstName.value} ${lastName.value}`,
  set: (value: string) => {
    const [first, last] = value.split(' ');
    firstName.value = first;
    lastName.value = last || '';
  }
});

// Watch - observer une source spécifique
watch(firstName, (newValue, oldValue) => {
  console.log(`firstName changed from ${oldValue} to ${newValue}`);
});

// Watch multiple sources
watch([firstName, lastName], ([newFirst, newLast], [oldFirst, oldLast]) => {
  console.log('Name changed');
});

// Watch avec options
watch(
  () => user.value?.id,
  async (newId) => {
    if (newId) {
      await fetchUserData(newId);
    }
  },
  { immediate: true, deep: false }
);

// watchEffect - exécute automatiquement quand les dépendances changent
watchEffect(() => {
  console.log(`Full name is: ${fullName.value}`);
});

// watchEffect avec cleanup
watchEffect((onCleanup) => {
  const controller = new AbortController();
  fetchData(controller.signal);

  onCleanup(() => controller.abort());
});
</script>
```

## Lifecycle Hooks

```vue
<script setup lang="ts">
import {
  onBeforeMount,
  onMounted,
  onBeforeUpdate,
  onUpdated,
  onBeforeUnmount,
  onUnmounted,
  onActivated,
  onDeactivated
} from 'vue';

onBeforeMount(() => {
  // Avant le premier rendu DOM
});

onMounted(() => {
  // Après le premier rendu DOM
  // Accès au DOM possible ici
});

onBeforeUpdate(() => {
  // Avant une mise à jour du DOM
});

onUpdated(() => {
  // Après une mise à jour du DOM
});

onBeforeUnmount(() => {
  // Avant destruction du composant
  // Cleanup subscriptions, timers, etc.
});

onUnmounted(() => {
  // Après destruction du composant
});

// Pour les composants dans <KeepAlive>
onActivated(() => {
  // Composant activé (visible)
});

onDeactivated(() => {
  // Composant désactivé (caché)
});
</script>
```

## Template Refs

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue';

// Ref au DOM element
const inputRef = ref<HTMLInputElement | null>(null);

// Ref au composant enfant
const childRef = ref<InstanceType<typeof ChildComponent> | null>(null);

onMounted(() => {
  inputRef.value?.focus();
  childRef.value?.someMethod();
});

// Expose des méthodes/propriétés au parent
defineExpose({
  focus: () => inputRef.value?.focus(),
  getValue: () => inputRef.value?.value
});
</script>

<template>
  <input ref="inputRef" type="text" />
  <ChildComponent ref="childRef" />
</template>
```

## Composables (Hooks Vue)

### Pattern de base

```typescript
// composables/useLocalStorage.ts
import { ref, watch } from 'vue';

export function useLocalStorage<T>(key: string, defaultValue: T) {
  const stored = localStorage.getItem(key);
  const data = ref<T>(stored ? JSON.parse(stored) : defaultValue);

  watch(
    data,
    (newValue) => {
      localStorage.setItem(key, JSON.stringify(newValue));
    },
    { deep: true }
  );

  return data;
}

// Usage
const theme = useLocalStorage('theme', 'light');
```

### useFetch composable

```typescript
// composables/useFetch.ts
import { ref, watchEffect, type Ref } from 'vue';

interface UseFetchReturn<T> {
  data: Ref<T | null>;
  error: Ref<Error | null>;
  isLoading: Ref<boolean>;
  refetch: () => Promise<void>;
}

export function useFetch<T>(url: Ref<string> | string): UseFetchReturn<T> {
  const data = ref<T | null>(null) as Ref<T | null>;
  const error = ref<Error | null>(null);
  const isLoading = ref(false);

  async function fetchData() {
    isLoading.value = true;
    error.value = null;

    try {
      const urlValue = typeof url === 'string' ? url : url.value;
      const response = await fetch(urlValue);
      if (!response.ok) throw new Error('Fetch failed');
      data.value = await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('Unknown error');
    } finally {
      isLoading.value = false;
    }
  }

  watchEffect(() => {
    fetchData();
  });

  return { data, error, isLoading, refetch: fetchData };
}
```

### useToggle composable

```typescript
// composables/useToggle.ts
import { ref } from 'vue';

export function useToggle(initialValue = false) {
  const state = ref(initialValue);

  function toggle() {
    state.value = !state.value;
  }

  function setTrue() {
    state.value = true;
  }

  function setFalse() {
    state.value = false;
  }

  return {
    state,
    toggle,
    setTrue,
    setFalse
  };
}

// Usage
const { state: isOpen, toggle: toggleModal } = useToggle();
```

## Slots

```vue
<!-- Parent -->
<template>
  <Card>
    <!-- Slot par défaut -->
    <p>Contenu principal</p>

    <!-- Slot nommé -->
    <template #header>
      <h2>Titre</h2>
    </template>

    <!-- Slot avec scope -->
    <template #item="{ item, index }">
      <li>{{ index }}: {{ item.name }}</li>
    </template>
  </Card>
</template>

<!-- Card.vue -->
<script setup lang="ts">
interface Item {
  id: string;
  name: string;
}

const items = ref<Item[]>([]);
</script>

<template>
  <div class="card">
    <header v-if="$slots.header">
      <slot name="header" />
    </header>

    <main>
      <slot />
    </main>

    <ul>
      <slot
        v-for="(item, index) in items"
        :key="item.id"
        name="item"
        :item="item"
        :index="index"
      />
    </ul>
  </div>
</template>
```

## Provide/Inject

```vue
<!-- Parent (Provider) -->
<script setup lang="ts">
import { provide, ref } from 'vue';
import type { InjectionKey } from 'vue';

interface ThemeContext {
  theme: Ref<'light' | 'dark'>;
  toggleTheme: () => void;
}

export const ThemeKey: InjectionKey<ThemeContext> = Symbol('theme');

const theme = ref<'light' | 'dark'>('light');

function toggleTheme() {
  theme.value = theme.value === 'light' ? 'dark' : 'light';
}

provide(ThemeKey, { theme, toggleTheme });
</script>

<!-- Enfant (Consumer) -->
<script setup lang="ts">
import { inject } from 'vue';
import { ThemeKey } from './ThemeProvider.vue';

const themeContext = inject(ThemeKey);

if (!themeContext) {
  throw new Error('ThemeProvider not found');
}

const { theme, toggleTheme } = themeContext;
</script>

<template>
  <div :class="theme">
    <button @click="toggleTheme">Toggle Theme</button>
  </div>
</template>
```

## Directives

```vue
<template>
  <!-- v-model -->
  <input v-model="searchQuery" />
  <input v-model.trim="name" />
  <input v-model.number="age" type="number" />
  <input v-model.lazy="email" />

  <!-- v-bind shorthand -->
  <img :src="imageUrl" :alt="imageAlt" />
  <div :class="{ active: isActive, 'text-red': hasError }" />
  <div :class="[baseClass, conditionalClass]" />
  <div :style="{ color: textColor, fontSize: fontSize + 'px' }" />

  <!-- v-on shorthand -->
  <button @click="handleClick">Click</button>
  <button @click.prevent="submit">Submit</button>
  <input @keyup.enter="search" />
  <div @click.stop="handleDiv">Stop propagation</div>

  <!-- Conditional -->
  <div v-if="isVisible">Visible</div>
  <div v-else-if="isAlternative">Alternative</div>
  <div v-else>Default</div>
  <div v-show="isShown">Toggle visibility (CSS)</div>

  <!-- List -->
  <ul>
    <li v-for="item in items" :key="item.id">
      {{ item.name }}
    </li>
  </ul>
  <template v-for="item in items" :key="item.id">
    <li>{{ item.name }}</li>
    <li>{{ item.description }}</li>
  </template>
</template>
```

## Mots-clés de routage

`Vue`, `Vue 3`, `Composition API`, `ref`, `reactive`, `computed`, `watch`, `watchEffect`, `script setup`, `defineProps`, `defineEmits`, `slots`, `provide`, `inject`, `composable`, `v-model`, `v-bind`, `v-on`

## Livrables

| Livrable | Description |
|----------|-------------|
| Composants Vue 3 | Composants SFC avec Composition API et script setup |
| Composables réutilisables | Fonctions composables pour logique partagée et state |
| Documentation Vue | Props typées, events et exemples d'intégration |
