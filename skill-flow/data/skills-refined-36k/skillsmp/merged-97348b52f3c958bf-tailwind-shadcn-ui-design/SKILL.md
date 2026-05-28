---
name: tailwind-shadcn-ui-design
description: Use this skill when creating or refactoring web interfaces, React components, or any visual UI work with Tailwind CSS and shadcn/ui, applying professional design principles for polished results.
---

# Tailwind + shadcn/ui Design Principles

## Folder Structure

```zsh
src/
├── components/
│   ├── ui/           # shadcn primitives (Button, Card, Dialog, etc.)
│   │   └── index.js  # barrel exports
│   └── [feature]/    # Domain components composed from ui/ primitives
├── pages/            # Page components, compose from components/
└── index.css         # Global styles, Tailwind imports, theme variables
```

Keep styles in a single `index.css` until it exceeds ~300 lines. Light/dark themes belong together as CSS variable swaps — no need for separate theme files.

## Core Principles

1. **Start with functionality, not chrome** - Design the feature first, not the shell.
2. **Work in grayscale first** - Add color only after hierarchy is established.
3. **Use existing systems** - Tailwind scale + shadcn components, don't reinvent.
4. **Hierarchy is everything** - Not all elements deserve equal emphasis.

## Component Hierarchy

### Layer 1: `src/components/ui/` — Design System Primitives

- Install via `npx shadcn@latest add <component>`
- **Modify directly** for project-wide design decisions (colors, spacing, cursor, sizing).
- **No unit tests** — primitives are tested upstream by shadcn/Base UI.
- **No Storybook stories** — document usage in domain components instead.

### Layer 2: `src/components/` — Domain Components

- Compose ui/ primitives into domain-specific components.
- Create wrappers only when adding **behavior or composition**, not just styling.
- Group by feature when >3 related components exist.

### Layer 3: `src/pages/` — Page Components

- Compose custom components into full pages.
- Minimal direct Tailwind; prefer component composition.
- Handle layout concerns (grid, spacing between sections).

## When to Modify ui/ vs. Create Wrapper

**Modify `ui/` directly when:**

- Changing project-wide defaults (padding, cursor, border-radius).
- Adding new variants that apply globally.
- Adjusting base styles for consistency.

**Create wrapper in `components/` when:**

- Adding domain-specific behavior (onClick handlers, state).
- Composing multiple primitives together.
- Creating contextual variations (MenuButton, SubmitButton with loading state).

## Barrel Exports

Use an index file to consolidate ui/ imports. Export only components, not CVA variants (keep variants as internal implementation details):

```js
// src/components/ui/index.js
export { Button } from './button' // not buttonVariants
export { Badge } from './badge' // not badgeVariants
export { Input } from './input' // not inputVariants
export { Card, CardHeader, CardTitle, CardContent, CardFooter } from './card'
// ... add as you install components
```

Then import from a single path:

```jsx
import { Button, Badge, Card } from '@/components/ui'
```

## Tailwind Best Practices

### Class Organization

Order classes consistently: layout → sizing → spacing → typography → colors → effects.

### Avoid Inline Style Bloat

Extract repeated **behavioral** patterns into wrapper components.

### Adding Variants to ui/ Components

Extend variants via `cva` when the variant applies project-wide.

### Design Tokens via CSS Variables

Define project tokens in `src/index.css` alongside shadcn variables.

## Common Patterns

### Button Hierarchy (shadcn)

```tsx
<Button>Save Changes</Button> // Primary
<Button variant="secondary">Cancel</Button> // Secondary
<Button variant="outline">Edit</Button> // Outline
<Button variant="ghost">Settings</Button> // Ghost
<Button variant="destructive">Delete</Button> // Destructive
<Button variant="link">Learn more</Button> // Link
```

### Card with Hierarchy

```tsx
<Card>
  <CardHeader>
    <CardTitle>Account Settings</CardTitle>
    <CardDescription>Manage your account preferences.</CardDescription>
  </CardHeader>
  <CardContent className="space-y-4">
    {/* Form fields */}
  </CardContent>
  <CardFooter className="flex justify-end gap-2">
    <Button variant="outline">Cancel</Button>
    <Button>Save</Button>
  </CardFooter>
</Card>
```

### Form with Labels

```tsx
<div className="space-y-4">
  <div className="space-y-2">
    <Label htmlFor="email">Email</Label>
    <Input id="email" type="email" placeholder="you@example.com" />
  </div>
  <div className="space-y-2">
    <Label htmlFor="password">Password</Label>
    <Input id="password" type="password" />
  </div>
</div>
```

### Alert Messages

```tsx
<Alert>
  <InfoIcon className="h-4 w-4" />
  <AlertTitle>Note</AlertTitle>
  <AlertDescription>Your session will expire in 5 minutes.</AlertDescription>
</Alert>

<Alert variant="destructive">
  <AlertCircle className="h-4 w-4" />
  <AlertTitle>Error</AlertTitle>
  <AlertDescription>Failed to save changes.</AlertDescription>
</Alert>
```

## Anti-Patterns

- ❌ Multiple primary buttons in one view.
- ❌ `variant="destructive"` for non-destructive actions.
- ❌ Skipping `Label` components (accessibility).
- ❌ Overriding shadcn styles instead of using variants.
- ❌ Not using `space-y-*` or `gap-*` for consistent spacing.
- ❌ Arbitrary Tailwind values like `w-[423px]` (use scale).
- ❌ Grey text on colored backgrounds (use same-hue shades).

## Topic References

- **[shadcn.md](references/shadcn.md)** - Component patterns, composition, customization.
- **[hierarchy.md](references/hierarchy.md)** - Visual hierarchy, emphasis, contrast.
- **[spacing.md](references/spacing.md)** - Layout, whitespace, sizing.
- **[typography.md](references/typography.md)** - Type scales, fonts, line-height.
- **[color.md](references/color.md)** - Palettes, shades, accessibility.
- **[depth.md](references/depth.md)** - Shadows, elevation, layering.
- **[polish.md](references/polish.md)** - Finishing touches, borders, backgrounds.