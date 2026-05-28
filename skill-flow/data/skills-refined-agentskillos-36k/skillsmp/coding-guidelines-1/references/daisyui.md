# daisyUI Patterns

Principles and research guidance for projects using daisyUI component library.

## Core Principles

### Component Class System
daisyUI provides semantic component classes that abstract Tailwind utilities. Components follow a base class + modifier pattern.

### Research Before Implementation
daisyUI components and class names evolve between versions. Always verify current syntax:
- Use context7 to query daisyUI documentation for specific components
- Search for: component name, available variants, size modifiers, color modifiers

## Common Patterns

### Base + Modifier Pattern
Components typically follow this structure:

```tsx
// Pattern: {component} {component}-{variant} {component}-{size}
<button class="btn btn-primary btn-lg">
<input class="input input-bordered input-error">
<div class="alert alert-warning">
```

Research available modifiers for each component.

### Semantic Colors
daisyUI uses semantic color names that adapt to themes. Research current color naming:
- Primary, secondary, accent colors
- State colors (info, success, warning, error)
- Base colors for backgrounds and content

### Native HTML Elements
daisyUI often enhances native elements. Research which HTML element to use:

```tsx
// Modal uses native <dialog>
<dialog class="modal">

// Progress uses native <progress>
<progress class="progress">
```

### Theming System
daisyUI has built-in themes and custom theme support. Research:
- Available built-in themes
- Custom theme configuration in tailwind.config.js
- Theme switching via `data-theme` attribute

## Research Checklist

Before implementing, query documentation for:
- [ ] Component's base class name
- [ ] Available variant modifiers (colors, sizes, styles)
- [ ] Required HTML structure (some components need specific nesting)
- [ ] Which native HTML element to use
- [ ] Theme color variables available
- [ ] Any deprecated components or renamed classes in current version

## Component Categories to Research

When building interfaces, research these component categories as needed:
- **Actions**: buttons, dropdowns, modals, swaps
- **Data Input**: inputs, selects, textareas, checkboxes, toggles
- **Data Display**: cards, tables, avatars, badges, stats
- **Navigation**: menus, tabs, breadcrumbs, pagination
- **Feedback**: alerts, toasts, loading, progress, tooltips
- **Layout**: drawers, footers, heroes, navbars
