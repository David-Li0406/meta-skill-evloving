---
name: ui-components
description: >
  Patterns and conventions for creating agnostic UI components in GeroCare.
  Trigger: When creating new UI components, reusable components, or building the component library.
license: Apache-2.0
metadata:
  author: gero-cloud
  version: "1.0"
  scope: [root]
  auto_invoke: "Creating new UI components"
---

## When to Use

Create agnostic UI components when:
- Building reusable primitives that don't depend on business logic
- Creating form inputs, buttons, cards, or other base UI elements
- Implementing design system components
- Building components used across multiple features

**Don't create agnostic components when:**
- Component contains business logic or domain-specific code
- Component is tightly coupled to a single feature
- Use feature-specific components instead (`src/business/{feature}/presentation/`)

---

## Component Categories

Components are organized by atomic design principles:

| Category | Location | Description | Examples |
|----------|----------|-------------|----------|
| **Atoms** | `src/business/common/presentation/atoms/` | Basic building blocks | Button, Input, Card, Badge |
| **Molecules** | `src/business/common/presentation/molecules/` | Simple compositions | StatCard, FormField, Tabs |
| **Organisms** | `src/business/common/presentation/organisms/` | Complex compositions | Table, Modal, Calendar |

---

## Critical Patterns

### 1. Component Structure

All components must follow this structure:

```vue
<script setup lang="ts">
import { computed } from 'vue'

defineOptions({
  name: 'App{ComponentName}',
})

interface Props {
  // Props with TypeScript types
}

const props = withDefaults(defineProps<Props>(), {
  // Default values
})

const emit = defineEmits<{
  'event-name': [value: Type]
}>()

// Computed properties for classes/styles
const classes = computed(() => ({
  'component': true,
  'component--modifier': props.condition,
}))
</script>

<template>
  <div :class="classes">
    <slot />
  </div>
</template>

<style scoped>
/* Use semantic CSS variables */
.component {
  /* Styles using tokens */
}
</style>
```

### 2. Naming Conventions

- **Component files**: PascalCase (e.g., `Button.vue`, `StatCard.vue`)
- **Component name**: `App{ComponentName}` (e.g., `AppButton`, `AppStatCard`)
- **CSS classes**: BEM-like pattern with component prefix (e.g., `.button`, `.button--primary`)
- **Props**: camelCase (e.g., `modelValue`, `isDisabled`)

### 3. TypeScript Patterns

**Props Interface:**
```typescript
interface Props {
  modelValue: string | number
  variant?: 'primary' | 'secondary' | 'danger'
  disabled?: boolean
  required?: boolean
  error?: string | boolean
}
```

**Emits:**
```typescript
const emit = defineEmits<{
  'update:modelValue': [value: string | number]
  'change': [value: string]
  'click': [event: MouseEvent]
}>()
```

### 4. CSS Variables and Tokens

Always use semantic design tokens from `src/assets/themes/semantic.css`:

| Use | Variable Pattern | Example |
|-----|------------------|---------|
| Colors | `--color-{type}-{variant}` | `--color-text-primary`, `--color-bg-hover` |
| Spacing | `--spacing-{size}` | `--spacing-md`, `--spacing-xl` |
| Typography | `--font-size-{size}`, `--font-weight-{weight}` | `--font-size-sm`, `--font-weight-semibold` |
| Borders | `--color-border-{state}` | `--color-border-default`, `--color-border-focus` |
| Radius | `--radius-{size}` | `--radius-md`, `--radius-lg` |
| Shadows | `--shadow-{size}` | `--shadow-md`, `--shadow-lg` |
| Transitions | `--transition-{speed}` | `--transition-base`, `--transition-slow` |

**Never use:**
- Hard-coded colors (e.g., `#000000`, `rgb(255, 0, 0)`)
- Pixel values for spacing (use `--spacing-*` variables)
- Fixed font sizes (use `--font-size-*` variables)

### 5. v-model Support

For form inputs, always support v-model:

```typescript
// Props
interface Props {
  modelValue: string | number
}

// Emit
const emit = defineEmits<{
  'update:modelValue': [value: string | number]
}>()

// Handler
const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}
```

### 6. Error Handling

Components should handle errors gracefully:

```typescript
interface Props {
  error?: string | boolean
}

const hasError = computed(() => {
  return props.error === true || (typeof props.error === 'string' && props.error.length > 0)
})

const classes = computed(() => ({
  'input': true,
  'input--error': hasError.value,
}))
```

### 7. Accessibility

Include accessibility attributes:

```vue
<button
  :aria-label="ariaLabel"
  :aria-disabled="disabled"
  :disabled="disabled"
  @click="handleClick"
>
  <slot />
</button>
```

---

## Component Examples

### Atom Example: Button

```vue
<script setup lang="ts">
import { computed } from 'vue'

defineOptions({
  name: 'AppButton',
})

interface Props {
  variant?: 'primary' | 'secondary' | 'danger' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  type?: 'button' | 'submit' | 'reset'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  disabled: false,
  type: 'button',
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const buttonClasses = computed(() => ({
  'button': true,
  [`button--${props.variant}`]: true,
  [`button--${props.size}`]: true,
  'button--disabled': props.disabled,
}))

const handleClick = (event: MouseEvent) => {
  if (!props.disabled) {
    emit('click', event)
  }
}
</script>

<template>
  <button :type="type" :class="buttonClasses" :disabled="disabled" @click="handleClick">
    <slot />
  </button>
</template>

<style scoped>
.button {
  padding: var(--spacing-md);
  border: none;
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
  transition: all var(--transition-base);
}

.button--primary {
  background: var(--color-button-primary-bg);
  color: var(--color-button-primary-text);
}

.button--disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
```

### Molecule Example: StatCard

```vue
<script setup lang="ts">
import { computed } from 'vue'
import Card from '../atoms/Card.vue'

defineOptions({
  name: 'AppStatCard',
})

interface Props {
  value: string | number
  label: string
  variant?: 'default' | 'primary' | 'success'
  clickable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  clickable: false,
})

const emit = defineEmits<{
  click: []
}>()
</script>

<template>
  <Card :clickable="clickable" variant="elevated" padding="lg" @click="emit('click')">
    <div class="stat-card">
      <div class="stat-card__value">{{ value }}</div>
      <div class="stat-card__label">{{ label }}</div>
    </div>
  </Card>
</template>

<style scoped>
.stat-card {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.stat-card__value {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
}
</style>
```

---

## Decision Trees

### Component Category Decision

```
Is it a basic UI primitive?
├─ Yes → Atoms (Button, Input, Badge)
└─ No → Does it compose 2+ atoms?
    ├─ Yes → Molecules (FormField, StatCard)
    └─ No → Organisms (Table, Modal, Calendar)
```

### Location Decision

```
Does it contain business logic?
├─ Yes → Feature component (src/business/{feature}/presentation/)
└─ No → Agnostic component
    ├─ Atom → atoms/
    ├─ Molecule → molecules/
    └─ Organism → organisms/
```

---

## File Organization

```
src/business/common/presentation/
├── atoms/          # Basic components
│   ├── Button.vue
│   ├── Input.vue
│   └── Card.vue
├── molecules/      # Composed components
│   ├── StatCard.vue
│   └── Tabs.vue
└── organisms/      # Complex components
    ├── Table.vue
    ├── Modal.vue
    └── Calendar.vue
```

---

## Testing Considerations

Components should be:
- Type-safe (TypeScript)
- Accessible (ARIA attributes)
- Responsive (mobile-first)
- Theme-aware (dark/light mode support via CSS variables)

---

## Resources

- **Design Tokens**: `src/assets/themes/semantic.css`
- **Base Tokens**: `src/assets/themes/tokens.css`
- **Existing Components**: `src/business/common/presentation/`
- **Component Examples**: See Button.vue, Card.vue, StatCard.vue
