# Component Naming Conventions

This guide establishes naming conventions and organizational patterns for Vue components in the Poche project, following the Atomic Design methodology with Nuxt UI.

## Table of Contents
- [Overview](#overview)
- [Atomic Design Structure](#atomic-design-structure)
- [Naming Conventions](#naming-conventions)
- [File Organization](#file-organization)
- [Component Props](#component-props)
- [Storybook Stories](#storybook-stories)
- [Examples](#examples)

## Overview

Poche follows the **Atomic Design** methodology to organize UI components into a clear hierarchy:

```
Atoms → Molecules → Organisms → Templates → Pages
```

This structure promotes:
- **Reusability**: Smaller components compose into larger ones
- **Consistency**: Shared design language across the application
- **Maintainability**: Clear component responsibilities and boundaries
- **Scalability**: Predictable structure as the codebase grows

## Atomic Design Structure

### Atoms (`components/atoms/`)

**Definition**: The smallest, indivisible UI elements. Cannot be broken down further without losing meaning.

**Characteristics**:
- Single, focused responsibility
- Highly reusable across the application
- Typically wrap Nuxt UI base components (UButton, UInput, etc.)
- Minimal to no internal state
- Pure presentational components

**Examples**:
- `Button.vue` - Wraps `UButton` with project-specific defaults
- `Input.vue` - Wraps `UInput` with consistent styling
- `Label.vue` - Wraps `UFormField` for form labels
- `Icon.vue` - Wraps `UIcon` for iconography
- `Link.vue` - Wraps `ULink` for navigation

**Naming Pattern**: `{Element}.vue`
- Use singular, descriptive nouns
- PascalCase for file names
- Match HTML element names when applicable

### Molecules (`components/molecules/`)

**Definition**: Simple groups of atoms functioning together as a unit.

**Characteristics**:
- Composed of 2-3 atoms
- Represent a single, cohesive UI pattern
- May have simple internal state
- Reusable across multiple contexts
- Focused on a specific interaction pattern

**Examples**:
- `FormField.vue` - Combines Label + Input for form fields
- `SearchBar.vue` - Input with search icon and specialized behavior
- `ArticleCard.vue` - Image + Title + Excerpt combination
- `ButtonGroup.vue` - Multiple buttons working together
- `TagList.vue` - Collection of tag atoms

**Naming Pattern**: `{Concept}{Type}.vue`
- Use descriptive compound nouns
- Suffix with component type when helpful (e.g., Bar, Card, Group)
- PascalCase for file names

### Organisms (`components/organisms/`)

**Definition**: Complex UI components composed of molecules and/or atoms.

**Characteristics**:
- Represent distinct sections of an interface
- May contain business logic and state management
- Less reusable than molecules (often context-specific)
- Form the major building blocks of pages
- Handle data fetching or complex interactions

**Examples**:
- `ArticleList.vue` - List of ArticleCard molecules with filtering
- `Navigation.vue` - Complete navigation system with menu items
- `ReaderView.vue` - Full article reading interface
- `UserProfile.vue` - Complete user profile section
- `SettingsPanel.vue` - Settings form with multiple FormFields

**Naming Pattern**: `{Feature}{Component}.vue`
- Use feature-based naming
- Descriptive enough to understand purpose
- PascalCase for file names

### Templates (`components/templates/`)

**Definition**: Page-level layouts that define content structure.

**Characteristics**:
- Define the page skeleton/layout
- Use slots for content injection
- No business logic or data fetching
- Highly reusable across similar pages
- Focus on structure, not content

**Examples**:
- `DefaultLayout.vue` - Standard page layout with header/footer
- `AuthLayout.vue` - Layout for authentication pages
- `SettingsLayout.vue` - Layout for settings pages with sidebar
- `ArticleLayout.vue` - Layout optimized for reading articles

**Naming Pattern**: `{Purpose}Layout.vue`
- Always suffix with "Layout"
- Describe the layout purpose
- PascalCase for file names

### Pages (`pages/`)

**Definition**: Actual routable pages that use templates and components.

**Note**: Pages are handled by Nuxt's file-based routing system and follow [Nuxt conventions](https://nuxt.com/docs/guide/directory-structure/pages).

## Naming Conventions

### Component Files

**Format**: `PascalCase.vue`

```
✅ Button.vue
✅ FormField.vue
✅ ArticleList.vue
✅ DefaultLayout.vue

❌ button.vue (lowercase)
❌ form-field.vue (kebab-case)
❌ article_list.vue (snake_case)
```

### Component Names (in `<script>`)

Components automatically use their filename as the component name in Vue 3's `<script setup>`.

```vue
<!-- Button.vue -->
<script setup lang="ts">
// Component name is automatically "Button"
defineProps<ButtonProps>();
</script>
```

### Props Interfaces

**Format**: `{ComponentName}Props`

```typescript
// Button.vue
export interface ButtonProps {
  label?: string;
  variant?: 'solid' | 'outline' | 'soft';
  size?: 'sm' | 'md' | 'lg';
}

// FormField.vue
export interface FormFieldProps {
  label?: string;
  name?: string;
  error?: string | boolean;
}
```

### Composables

**Format**: `use{Feature}.ts`

```
✅ useArticles.ts
✅ useAuth.ts
✅ useTheme.ts

❌ articles.ts
❌ authComposable.ts
```

## File Organization

### Directory Structure

```
apps/web/components/
├── atoms/
│   ├── Button.vue
│   ├── Button.stories.ts
│   ├── Input.vue
│   ├── Input.stories.ts
│   └── NAMING_CONVENTIONS.md
├── molecules/
│   ├── FormField.vue
│   ├── FormField.stories.ts
│   ├── SearchBar.vue
│   └── SearchBar.stories.ts
├── organisms/
│   ├── ArticleList.vue
│   ├── ArticleList.stories.ts
│   ├── Navigation.vue
│   └── Navigation.stories.ts
└── templates/
    ├── DefaultLayout.vue
    └── AuthLayout.vue
```

### Co-location

Each component should have its Storybook stories file co-located:

```
Button.vue          # Component implementation
Button.stories.ts   # Storybook documentation and tests
```

## Component Props

### Prop Naming

Use camelCase for prop names:

```typescript
✅ leadingIcon
✅ modelValue
✅ placeholder

❌ leading-icon (kebab-case)
❌ LeadingIcon (PascalCase)
```

### Prop Documentation

Always include JSDoc comments for props:

```typescript
export interface ButtonProps {
  /** Button label text */
  label?: string;

  /** Button visual style variant */
  variant?: 'solid' | 'outline' | 'soft';

  /** Button size */
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';

  /** Show loading spinner */
  loading?: boolean;
}
```

### Boolean Props

Use positive naming for boolean props:

```typescript
✅ disabled: boolean
✅ loading: boolean
✅ required: boolean

❌ notEnabled: boolean
❌ isNotLoading: boolean
```

## Storybook Stories

### Story File Naming

**Format**: `{ComponentName}.stories.ts`

```
Button.stories.ts
FormField.stories.ts
ArticleList.stories.ts
```

### Story Titles

**Format**: `{Category}/{ComponentName}`

```typescript
const meta = {
  title: 'Atoms/Button',        // ✅
  title: 'Molecules/FormField',  // ✅
  title: 'Organisms/ArticleList', // ✅
} satisfies Meta<typeof Component>;
```

### Story Names

Use PascalCase, descriptive names:

```typescript
export const Default: Story = { ... };
export const WithIcon: Story = { ... };
export const Loading: Story = { ... };
export const DisabledState: Story = { ... };
```

## Examples

### Atom Example: Button

```vue
<!-- apps/web/components/atoms/Button.vue -->
<script setup lang="ts">
/**
 * Button component - A wrapper around Nuxt UI's UButton
 * Provides a consistent button interface with support for variants, sizes, and icons
 */

export interface ButtonProps {
  /** Button label text */
  label?: string;
  /** Button color scheme */
  color?: 'primary' | 'secondary' | 'success' | 'error';
  /** Button visual style variant */
  variant?: 'solid' | 'outline' | 'soft' | 'ghost';
  /** Button size */
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  /** Show loading spinner */
  loading?: boolean;
  /** Disable the button */
  disabled?: boolean;
}

const props = withDefaults(defineProps<ButtonProps>(), {
  color: 'primary',
  variant: 'solid',
  size: 'md',
});

defineEmits<{
  click: [event: MouseEvent];
}>();
</script>

<template>
  <UButton
    :label="label"
    :color="color"
    :variant="variant"
    :size="size"
    :loading="loading"
    :disabled="disabled"
    @click="$emit('click', $event)"
  >
    <slot />
  </UButton>
</template>
```

### Molecule Example: FormField

```vue
<!-- apps/web/components/molecules/FormField.vue -->
<script setup lang="ts">
/**
 * FormField molecule component - Combines UFormField with UInput
 * Provides a complete form field pattern with label, input, validation, and help text
 */

export interface FormFieldProps {
  /** Label text for the form field */
  label?: string;
  /** Name attribute for the input field */
  name?: string;
  /** Input placeholder text */
  placeholder?: string;
  /** Error message to display */
  error?: string | boolean;
  /** Mark field as required */
  required?: boolean;
}

defineProps<FormFieldProps>();
</script>

<template>
  <UFormField :label="label" :name="name" :error="error" :required="required">
    <UInput :placeholder="placeholder" :name="name" :required="required" />
  </UFormField>
</template>
```

### Organism Example: ArticleList

```vue
<!-- apps/web/components/organisms/ArticleList.vue -->
<script setup lang="ts">
/**
 * ArticleList organism - Displays a filterable, paginated list of articles
 * Combines SearchBar, ArticleCard molecules with list management logic
 */

import type { Article } from '@poche/types';

export interface ArticleListProps {
  /** Array of articles to display */
  articles: Article[];
  /** Show loading state */
  loading?: boolean;
}

defineProps<ArticleListProps>();

const emit = defineEmits<{
  'article:select': [article: Article];
  'search': [query: string];
}>();
</script>

<template>
  <div class="space-y-4">
    <SearchBar @update:model-value="emit('search', $event)" />

    <div v-if="loading" class="text-center py-8">
      Loading articles...
    </div>

    <div v-else class="grid gap-4">
      <ArticleCard
        v-for="article in articles"
        :key="article.id"
        :article="article"
        @click="emit('article:select', article)"
      />
    </div>
  </div>
</template>
```

## Best Practices

### 1. Single Responsibility

Each component should have one clear purpose:

```
✅ FormField - Combines label + input
✅ SearchBar - Search-specific input
✅ ArticleCard - Display article summary

❌ SuperForm - Does everything (validation, submission, state management)
```

### 2. Composition Over Complexity

Build complex components from simpler ones:

```vue
<!-- Good: Compose from existing atoms -->
<FormField>
  <Input type="email" />
</FormField>

<!-- Avoid: Reimplementing everything -->
<div class="custom-field">
  <label>...</label>
  <input />
</div>
```

### 3. Consistent Prop Patterns

Follow Nuxt UI's prop conventions:

```typescript
// Size prop
size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'

// Color prop
color?: 'primary' | 'secondary' | 'success' | 'error' | 'warning' | 'info'

// Variant prop
variant?: 'solid' | 'outline' | 'soft' | 'subtle' | 'ghost'
```

### 4. Accessibility First

Always include proper ARIA attributes and semantic HTML:

```vue
<template>
  <button
    type="button"
    :aria-label="label"
    :aria-disabled="disabled"
    :aria-busy="loading"
  >
    {{ label }}
  </button>
</template>
```

### 5. TypeScript Everywhere

Use TypeScript for all props, emits, and composables:

```typescript
// Props interface
export interface ComponentProps {
  prop1: string;
  prop2?: number;
}

// Emits type
defineEmits<{
  update: [value: string];
  submit: [data: FormData];
}>();
```

## Migration Guide

When creating new components or refactoring existing ones:

1. **Identify the atomic level**: Determine if it's an atom, molecule, organism, or template
2. **Check existing components**: Reuse atoms/molecules before creating new ones
3. **Follow naming conventions**: Use the patterns defined in this guide
4. **Add Storybook stories**: Document usage with interactive examples
5. **Write tests**: Use Storybook interaction tests for critical user flows
6. **Document props**: Add JSDoc comments to all public APIs

## Resources

- [Atomic Design by Brad Frost](https://atomicdesign.bradfrost.com/)
- [Nuxt UI Documentation](https://ui.nuxt.com/)
- [Vue 3 Style Guide](https://vuejs.org/style-guide/)
- [Storybook Best Practices](https://storybook.js.org/docs/vue/writing-stories/introduction)
