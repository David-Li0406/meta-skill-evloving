---
name: viya-ui-warehouse-structure
description: Understanding the viya-ui-warehouse Storybook component library structure, coding standards, and component patterns. Use when creating or modifying shared UI components.
license: MIT
metadata:
  author: shipitsmarter
  version: "1.0"
---

# Viya UI Warehouse Structure

The `viya-ui-warehouse` repository is the shared Vue.js component library with Storybook documentation. Components here are published to `@shipitsmarter/viya-ui-warehouse`.

---

## Key Paths

| Path | Purpose |
|------|---------|
| `src/components/` | All shared UI components |
| `src/components/{component-name}/` | Individual component folder |
| `src/components/index.ts` | Main export file |

---

## Common Commands

```bash
# Storybook development server
npm run storybook

# Build library for distribution
npm run build

# Watch mode for local development
npm run library:watch

# Lint and type checking
npm run lint
npm run lint -- --fix
npm run lint -- --fix <file>
```

---

## Component Folder Structure

Each component in the warehouse follows this structure:

```
src/components/{component-name}/
├── {ComponentName}.vue          # Main component
├── {ComponentName}.stories.ts   # Storybook stories
├── {ComponentName}.mdx          # Documentation
├── index.ts                     # Exports
├── helpers.ts                   # Helper methods/types (optional)
├── types.d.ts                   # TypeScript types (optional)
└── {SubComponent}.vue           # Subcomponents (optional)
```

---

## Component File Structure

Components must follow this section-based structure:

```vue
<script setup lang="ts">
// ============================================================================
// Imports
// ============================================================================

import { computed, ref } from "vue";

import { someHelper } from "@/components/component-name/helpers";

// ============================================================================
// Types & Interfaces
// ============================================================================

interface Props {
  label: string;
  variant?: "primary" | "secondary";
  disabled?: boolean;
}

// ============================================================================
// Props & Emits
// ============================================================================

const props = withDefaults(defineProps<Props>(), {
  variant: "primary",
  disabled: false,
});

const emit = defineEmits<{
  click: [event: MouseEvent];
  change: [value: string];
}>();

// ============================================================================
// State
// ============================================================================

const isActive = ref(false);

// ============================================================================
// Computed
// ============================================================================

const computedClasses = computed(() => ({
  "is-active": isActive.value,
  "is-disabled": props.disabled,
}));

// ============================================================================
// Functions
// ============================================================================

const handleClick = (event: MouseEvent) => {
  if (!props.disabled) {
    emit("click", event);
  }
};
</script>

<template>
  <div :class="computedClasses" @click="handleClick">
    <slot>{{ label }}</slot>
  </div>
</template>
```

---

## Stories File Structure (`.stories.ts`)

```typescript
import type { Meta, StoryFn } from "@storybook/vue3-vite";

import { ComponentName, componentVariants, componentSizes } from "@/components";

const meta: Meta<typeof ComponentName> = {
  component: ComponentName,
  title: "Components/ComponentName", // or 'Form/ComponentName' for form elements
  tags: ["autodocs"],
  render: (args) => ({
    components: { ComponentName },
    data: () => ({ args }),
    template: `<ComponentName v-bind="args" />`,
  }),
  argTypes: {
    variant: {
      options: componentVariants,
      control: { type: "select" },
    },
    size: {
      options: componentSizes,
      control: { type: "select" },
    },
  },
};

export default meta;

// Basic story template
const Template: StoryFn<typeof ComponentName> = (args) => ({
  components: { ComponentName },
  setup() {
    return { args };
  },
  template: `<ComponentName v-bind="args" />`,
});

// Default story
export const Default = Template.bind({});
Default.args = {
  label: "Default Label",
};

// Variant showcase
const VariantsTemplate: StoryFn<typeof ComponentName> = (args) => ({
  components: { ComponentName },
  setup() {
    return { args, componentVariants };
  },
  template: `
    <div class="flex gap-2">
      <ComponentName 
        v-for="variant in componentVariants" 
        :key="variant" 
        v-bind="args" 
        :variant="variant" 
        :label="variant" 
      />
    </div>
  `,
});
export const Variants = VariantsTemplate.bind({});

// State stories
export const Disabled = Template.bind({});
Disabled.args = {
  label: "Disabled",
  disabled: true,
};
```

---

## MDX Documentation Structure (`.mdx`)

```mdx
import { Meta, Primary, Controls, Story } from "@storybook/addon-docs/blocks";

import * as Stories from "./ComponentName.stories";

<Meta of={Stories} />

# Component Name

Brief description of what the component does and when to use it.

<Primary />

## Designs

You can find the designs at [Figma](https://figma.com/design/...).

## Variants

Description of available variants:

<Story of={Stories.Variants} />

- `primary`: Main style variant
- `secondary`: Alternative style variant

## Props

<Controls />

## Usage

\`\`\`vue
<script setup lang="ts">
import { ComponentName } from "@shipitsmarter/viya-ui-warehouse";
</script>

<template>
  <ComponentName label="Click me" variant="primary" />
</template>
\`\`\`
```

---

## Index Export File (`index.ts`)

```typescript
export { default as ComponentName } from '@/components/component-name/ComponentName.vue';
export * from '@/components/component-name/helpers';
// Export types if separate file exists
export * from '@/components/component-name/types.d';
```

---

## Helpers File (`helpers.ts`)

```typescript
// Types
export type ComponentVariant = "primary" | "secondary" | "danger";
export type ComponentSize = "xs" | "sm" | "md";

// Constants (for stories argTypes)
export const componentVariants: ComponentVariant[] = [
  "primary",
  "secondary",
  "danger",
];
export const componentSizes: ComponentSize[] = ["xs", "sm", "md"];

// Style mappings
export const variantStyles: Record<ComponentVariant, string> = {
  primary: "bg-primary text-white",
  secondary: "bg-secondary text-gray-800",
  danger: "bg-danger text-white",
};

// Helper functions
export const getVariantClass = (variant: ComponentVariant): string => {
  return variantStyles[variant] || variantStyles.primary;
};
```

---

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Component names | `PascalCase` | `ButtonComponent`, `SelectComponent` |
| Folder names | `kebab-case` | `button-component`, `select-component` |
| File names | Match component/folder | `ButtonComponent.vue`, `helpers.ts` |

---

## Storybook URL Patterns

When navigating to components in Storybook:

**URL Pattern:** `http://localhost:6006/?path=/docs/{story-path}--docs`

**Building `{story-path}` from stories `title`:**
1. Take the `title` (e.g., `'Date Time/Date Input'`)
2. Convert to lowercase
3. Replace spaces with hyphens
4. Replace forward slashes with hyphens
5. Append `--docs` for docs page

| Stories `title` | URL Path |
|-----------------|----------|
| `'Date Time/Date Input'` | `?path=/docs/date-time-date-input--docs` |
| `'Components/Button'` | `?path=/docs/components-button--docs` |
| `'Layout/Sliding Drawer'` | `?path=/docs/layout-sliding-drawer--docs` |

---

## Best Practices

### Stories
- Include a `Default` story with minimal props
- Create `Variants` story showing all variant options
- Create `Sizes` story showing all size options
- Include `Disabled` and `Loading` states if applicable

### Documentation
- Start with a clear description of component purpose
- Link to Figma designs when available
- Show all variants and states with stories
- Include complete usage examples

### Code Organization
- Keep helpers in separate `helpers.ts` file
- Export types separately if complex
- Use consistent section comments
- Always run `npm run lint -- --fix` after changes

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| **vue-component** | Vue component patterns and conventions |
| **viya-app-structure** | Working with the main application |
