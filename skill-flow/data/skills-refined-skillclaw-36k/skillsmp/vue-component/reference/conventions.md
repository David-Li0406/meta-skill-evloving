# Vue Component Conventions Reference

Detailed patterns and lessons learned. For core workflow and rules, see the main SKILL.md.

---

## Script Order (MANDATORY)

All Vue components MUST follow this exact order in `<script setup>`:

```vue
<script setup lang="ts">
// 1. TYPES & INTERFACES (local to this component)
type MyType = { ... };
interface MyInterface { ... }

// 2. COMPOSABLES (external stateful hooks)
const route = useRoute();
const userStore = useUserStore();
const { width, height } = useWindowSize();

// 3. CONSTANTS (static values, never change)
const TABLE_OFFSET = 400;
const DEFAULT_PAGE_SIZE = 50;

// 4. SERVICES (API service instances)
const invoiceService = new InvoiceService();
const shipmentService = new ShipmentService();

// 5. PROPS & EMITS (component interface)
const props = defineProps<{ ... }>();
const emit = defineEmits<{ ... }>();

// 6. MODELS (two-way bindings)
const open = defineModel<boolean>('open', { required: true });

// 7. REFS & REACTIVES (local mutable state)
const loading = ref<boolean>(false);
const data = ref<MyType>();
const formState = reactive({ ... });

// 8. COMPUTED (derived state)
const isValid = computed(() => ...);
const filteredItems = computed(() => ...);

// 9. FUNCTIONS (methods, handlers, helpers)
const fetchData = async () => { ... };
const handleClick = () => { ... };
const formatValue = (val: number) => { ... };

// 10. WATCHERS (reactive side effects)
watch(() => props.id, fetchData, { immediate: true });
watch(data, (newVal) => { ... });

// 11. LIFECYCLE HOOKS (always LAST)
onMounted(() => { ... });
onBeforeUnmount(() => { ... });
</script>
```

**Why this order matters:**
- Dependencies flow top-to-bottom (composables before refs that use them)
- Lifecycle hooks are always last because they may depend on anything above
- Watchers come before lifecycle hooks but after functions they may call
- Makes code predictable and easier to navigate

---

## Template Attribute Order

ESLint enforces specific attribute ordering in Vue templates:

1. `TWO_WAY_BINDING` (v-model)
2. `DEFINITION`
3. `LIST_RENDERING` (v-for)
4. `CONDITIONALS` (v-if, v-show)
5. `RENDER_MODIFIERS`
6. `GLOBAL`
7. `UNIQUE`, `SLOT`
8. `OTHER_DIRECTIVES`
9. `EVENTS` (@click, etc.)
10. `CONTENT`
11. `OTHER_ATTR` (:prop bindings)

```vue
<!-- Correct -->
<MyComponent :data="item" @click="handle" v-if="show" />

<!-- Wrong -->
<MyComponent v-if="show" :data="item" @click="handle" />
```

---

## Lessons Learned

### Focus Retention in Table Cells

When creating editable table cells with TanStack Table:
- **Problem**: Vue re-renders can cause input focus loss during typing
- **Solution**: Create a stable component with local state that syncs to table only on blur
- **Pattern**: Use a `focusTracker` module-level singleton to track active cell and cursor position
- **Key insight**: Extract complex cell components to separate `.vue` files, don't use `defineComponent` inline

### Component Extraction

When moving inline components to separate files:
- Create the `.vue` file using Composition API
- If the component needs module-level state (like `focusTracker`), put it in a separate `.ts` file
- Use absolute imports in the new file
- Test thoroughly after extraction - import resolution issues can crash the app

### Extracting Complex Dialog Logic

When a page component grows large due to dialog functionality:
- **Extract the dialog** to its own component (e.g., `ImportContractDialog.vue`)
- **Extract reusable UI patterns** (e.g., `FileUploadWithDragDrop.vue`, `DragDropZone.vue`)
- **Pass dependencies as props** (e.g., `existingReferences` for validation) rather than importing services
- **Emit events** for parent actions (e.g., `@imported` to trigger data refresh)
- **Reset state on dialog close** using a watcher on the `open` model

### Drag-and-Drop File Upload Pattern

For file upload with drag-and-drop support:
- Create a `DragDropZone` component handling drag events and format validation
- The zone emits `drop` (with FileList) and `formatError` events
- Wrap it in a `FileUploadWithDragDrop` component that:
  - Shows drop zone OR selected file info (never both)
  - Processes file content via FileReader
  - Emits `fileSelected` with content and File object
  - Exposes `clearSelectedFile()` for parent reset

### UI Component Availability

Not all expected components/icons exist in the warehouse library:
- **Dialogs**: Use `BaseDialog` from `@/components/utilities/BaseDialog.vue`, NOT `DialogComponent` from warehouse
- **Icons**: Check available icons - e.g., `PhFileJson` doesn't exist, use `PhFileText` instead
- **When in doubt**: Search codebase for existing usage patterns

### Vuelidate in Dialogs

When using Vuelidate for validation inside dialogs:
- Reset validation state when dialog closes: `v$.value.$reset()`
- Use `computed` for validation object to make it reactive
- Combine `required` with custom validators using `helpers.withMessage()`

### Finding API Endpoints

To find which endpoint is called for a feature:
1. Find the store that manages the data (e.g., `useCarrierSelectStore`)
2. Look at the actions that fetch data (e.g., `getRates`)
3. Trace to the service method (e.g., `shipmentService.getShipmentOptionsWithQuery`)
4. Find the actual endpoint in the service (e.g., `POST /shipping/v4/shipments/options`)

### Refactoring Large Files

When refactoring large files into multiple smaller files:
- **First verify existing tests pass** before making changes
- Make incremental changes and test after each
- If import resolution fails, revert and try a simpler approach
- Not every file needs to be split - readability > modularity

---

## Helper File Pattern

Extract reusable logic to co-located `-helpers.ts` files:

```typescript
// feature-helpers.ts
export const formatPrice = (value: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(value);
};

export const COLUMN_DEFINITIONS = [
  { key: 'name', label: 'Name', sortable: true },
  { key: 'status', label: 'Status', sortable: false },
] as const;
```

Keep components focused on reactive state and template rendering.

---

## Barrel Exports

Every component directory should have an `index.ts`:

```typescript
// src/components/feature-name/index.ts
export { default as FeatureComponent } from './FeatureComponent.vue';
export { default as FeatureSubComponent } from './FeatureSubComponent.vue';
export * from './feature-helpers';
```

---

## Defensive Rendering

Use `v-if` generously to prevent broken components:

```vue
<template>
  <div v-if="data">
    <h1>{{ data.title }}</h1>
    <p v-if="data.description">{{ data.description }}</p>
    <UserInfo v-if="data.user" :user="data.user" />
  </div>
  <LoadingSpinner v-else />
</template>
```

---

## Styling with Tailwind

**Always use Tailwind CSS classes instead of `<style>` blocks:**

```vue
<!-- Correct: Use Tailwind classes -->
<input class="text-sm font-medium text-white placeholder:text-white/70" />

<!-- Avoid: Scoped CSS -->
<style scoped>
input { font-size: 0.875rem; color: white; }
</style>
```

**For deep styling of library components, use Tailwind's arbitrary variants:**

```vue
<!-- Correct: Deep styling with Tailwind arbitrary variants -->
<InputComponent class="[&_input]:text-white [&_input::placeholder]:text-white/70" />

<!-- Avoid: Scoped CSS with :deep() -->
<style scoped>
.my-input :deep(input) { color: white; }
</style>
```

**Exceptions where CSS may be needed:**
- Complex animations that can't be expressed in Tailwind
- CSS variables for theming (rare)
- Third-party library overrides that don't work with classes
