---
name: tailwind-shadcn-ui
description: Use this skill when creating or styling web interfaces, React components, or layouts with Tailwind CSS and shadcn/ui, applying professional design principles for polished results.
---

# Tailwind + shadcn/ui Styling Structure

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

## Component Hierarchy

### Layer 1: `src/components/ui/` — Design System Primitives

- Install via `npx shadcn@latest add <component>`
- **Modify directly** for project-wide design decisions (colors, spacing, cursor, sizing)
- You own this code — it's your design system, not an external dependency
- **No unit tests** — primitives are tested upstream by shadcn/Base UI
- **No Storybook stories** — document usage in domain components instead

### Layer 2: `src/components/` — Domain Components

- Compose ui/ primitives into domain-specific components
- Create wrappers only when adding **behavior or composition**, not just styling
- Group by feature when >3 related components exist

### Layer 3: `src/pages/` — Page Components

- Compose custom components into full pages
- Minimal direct Tailwind; prefer component composition
- Handle layout concerns (grid, spacing between sections)

## Core Principles for UI Design

1. **Start with functionality, not chrome** - Design the feature first, not the shell.
2. **Work in grayscale first** - Add color only after hierarchy is established.
3. **Use existing systems** - Tailwind scale + shadcn components, don't reinvent.
4. **Hierarchy is everything** - Not all elements deserve equal emphasis.

## When to Modify ui/ vs. Create Wrapper

**Modify `ui/` directly when:**

- Changing project-wide defaults (padding, cursor, border-radius)
- Adding new variants that apply globally
- Adjusting base styles for consistency

```jsx
// src/components/ui/button.jsx — modify directly
const buttonVariants = cva(
  'cursor-pointer active:cursor-grabbing ...', // project cursor rules
  {
    variants: {
      size: {
        default: 'h-10 px-5 py-2.5' // project sizing
      }
    }
  }
)
```

**Create wrapper in `components/` when:**

- Adding domain-specific behavior (onClick handlers, state)
- Composing multiple primitives together
- Creating contextual variations 

## Quick Start with shadcn/ui

### Installation (Next.js)
```bash
npx shadcn@latest init
npx shadcn@latest add button card input label
```

### Core Components to Know

| Component | Use for |
|-----------|---------|
| `Button` | Actions with built-in variants (default, secondary, outline, ghost, destructive) |
| `Card` | Content containers with header, content, footer |
| `Input` + `Label` | Form fields with consistent styling |
| `Dialog` | Modals with accessible focus management |
| `DropdownMenu` | Actions menus with keyboard navigation |
| `Select` | Styled native-like selects |
| `Tabs` | Content organization |
| `Badge` | Status indicators, counts |
| `Alert` | Feedback messages |
| `Skeleton` | Loading states |

## Button Hierarchy (shadcn)

```tsx
// Primary: one per section max
<Button>Save Changes</Button>

// Secondary: clear but not dominant
<Button variant="secondary">Cancel</Button>

// Outline: lighter touch
```