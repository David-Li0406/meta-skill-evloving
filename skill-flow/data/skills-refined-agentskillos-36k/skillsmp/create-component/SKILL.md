---
name: create-component
description: Create new Preact components following project conventions with proper file structure, TypeScript types, and Tailwind styling. Use when adding UI components, sections, or interactive elements to the site.
---

# Create Component

Create Preact components for agentconfig.org following project conventions.

## File Structure

Every component lives in its own folder under `site/src/components/`:

```
site/src/components/
└── {ComponentName}/
    ├── index.ts              # Re-exports component and types
    └── {ComponentName}.tsx   # Main implementation
```

## Step-by-Step Process

1. **Create the component folder** in `site/src/components/{ComponentName}/`
2. **Copy the template** from `assets/component-template.tsx`
3. **Rename and customize** the component
4. **Create index.ts** with exports
5. **Import in App.tsx** or parent component

## Template Files

### index.ts

```typescript
export { ComponentName } from './ComponentName'
export type { ComponentNameProps } from './ComponentName'
```

### ComponentName.tsx

See [assets/component-template.tsx](assets/component-template.tsx) for the full template.

## TypeScript Rules

1. **No semicolons** - Omit semicolons at end of statements
2. **Explicit return types** - Always specify `: ReactNode`
3. **Interface over type** - Use `interface` for props
4. **JSDoc comments** - Document props with `/** */`
5. **No `any`** - Use proper types or `unknown`
6. **Readonly arrays** - Use `readonly` for array props

```tsx
// Good
interface ListProps {
  /** Items to display in the list */
  readonly items: readonly string[]
}

// Bad
type ListProps = {
  items: string[];
}
```

## Styling Rules

1. **Tailwind utilities** - Use Tailwind classes for all styling
2. **cn() helper** - Use `cn()` from `@/lib/utils` for conditional classes
3. **Mobile-first** - Start with mobile, add `md:` and `lg:` for larger screens
4. **Theme-aware** - Use CSS variables for theme colors

```tsx
// Good - mobile first, theme aware
<div className="p-4 md:p-6 lg:p-8 bg-background text-foreground">

// Bad - desktop first
<div className="p-8 sm:p-4">
```

## Component Guidelines

### Keep Components Focused
- One component = one responsibility
- Under 150 lines (split if longer)
- Extract complex logic into custom hooks in `site/src/hooks/`

### Props Design
- Always include `className` prop for style overrides
- Use `children` for flexible content
- Use discriminated unions for variants

```tsx
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'ghost'
  className?: string
  children?: ReactNode
}
```

### Event Handlers
- Prefix with `on`: `onClick`, `onToggle`, `onSelect`
- Use specific types, not generic `Function`

```tsx
interface Props {
  // Good
  onSelect: (id: string) => void

  // Bad
  onSelect: Function
}
```

## Accessibility

1. **Semantic HTML** - Use `button` for buttons, `nav` for navigation
2. **ARIA attributes** - Add `aria-label`, `aria-expanded` for interactive elements
3. **Keyboard navigation** - Ensure focusable and keyboard-usable
4. **Focus visible** - Use `focus-visible:` for focus rings

```tsx
<button
  aria-expanded={isOpen}
  aria-controls="menu-content"
  className="focus-visible:ring-2 focus-visible:ring-primary"
>
```

## Checklist

Before considering the component complete:

- [ ] Component is in its own folder with `index.ts`
- [ ] All props have TypeScript types with JSDoc comments
- [ ] Uses `cn()` for className merging
- [ ] Mobile-first responsive design
- [ ] Theme-aware colors (CSS variables)
- [ ] Accessible (semantic HTML, ARIA, keyboard)
- [ ] Under 150 lines (or appropriately split)
- [ ] Named export (not default)
- [ ] No semicolons
