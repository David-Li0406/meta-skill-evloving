---
name: stitch-to-shadcn
description: Convert Google Stitch HTML exports into reusable shadcn/ui React components. Use when user provides HTML file paths exported from stitch.withgoogle.com and needs TypeScript React components with CVA variants, proper props interfaces, and atomic design organization.
---

# Stitch HTML to shadcn/ui Component Converter

Convert Google Stitch design exports into production-ready, reusable React components using shadcn/ui as the foundation.

## Prerequisites

Before starting conversion:
1. **shadcn MCP must be available** - Query it before implementing ANY shadcn component.
2. **Project has shadcn/ui installed** - Components will import from `@/components/ui`.
3. **cn() utility exists** - From `@/lib/utils` (tailwind-merge + clsx).

## Quick Start

```
User: Convert this Stitch HTML at <input_path> to shadcn components
```

1. Read the HTML file at the provided path.
2. Run the 4-phase workflow below.
3. Output organized TypeScript components.

## Workflow Overview

| Phase | Focus | Output |
|-------|-------|--------|
| 0. Extract | Theme tokens, icons, custom CSS | `globals.css`, icon inventory |
| 1. Audit | Analyze HTML, identify patterns | Component inventory |
| 2. Atoms | Smallest units (buttons, inputs) | `@/components/ui/*` |
| 3. Molecules | Composed atoms (cards, form fields) | `@/components/*` |
| 4. Organisms | Complex sections (sidebars, tables) | `@/components/*` |

---

## Phase 0: Theme & Asset Extraction

**Objective:** Extract design tokens before component work.

### Steps

1. **Parse Tailwind config** - Find `<script id="tailwind-config">` block, extract custom colors.
2. **Map to CSS variables** - Convert Stitch colors to shadcn theme tokens in `globals.css`.
3. **Inventory icons** - List all `material-symbols-outlined` icons, map to Lucide equivalents.
4. **Extract custom CSS** - Move `<style>` block utilities to `globals.css` or Tailwind config.

### Theme Token Mapping

```css
/* globals.css - map Stitch colors to shadcn tokens */
:root {
  --background: 222.2 84% 4.9%;      /* Stitch: background-main */
  --foreground: 210 40% 98%;         /* Stitch: text-main */
  --primary: 142 71% 45%;            /* Stitch: primary */
  --muted-foreground: 215 20% 65%;   /* Stitch: text-dim */
  --border: 217 33% 17%;             /* Stitch: border-dim */
}
```

### Icon Conversion

Stitch uses Material Symbols; shadcn uses Lucide. See [component-mapping.md](references/component-mapping.md#icon-mapping) for full mapping table.

---

## Phase 1: Component Audit

**Objective:** Analyze HTML structure, identify all repeating UI patterns.

### Steps

1. **Read the HTML file** at the user-provided path.
2. **Scan for repeating patterns** - Elements that appear multiple times with similar structure.
3. **Categorize each pattern** using atomic design rules (see [atomic-design.md](references/atomic-design.md)).
4. **Create component inventory** listing:
   - Pattern name
   - Where it appears (line numbers/sections)
   - Suggested shadcn component mapping
   - Classification (atom/molecule/organism).

### Output Format

```markdown
## Component Inventory

### Atoms
| Pattern | Occurrences | shadcn Mapping | Notes |
|---------|-------------|----------------|-------|
| Primary Button | 12 | Button (variant="default") | Has loading state |
| Icon Button | 8 | Button (variant="ghost", size="icon") | - |

### Molecules
| Pattern | Occurrences | Composition | Notes |
|---------|-------------|-------------|-------|
| Stat Card | 4 | Card + heading + number | Has trend indicator |

### Organisms
| Pattern | Occurrences | Composition | Notes |
|---------|-------------|-------------|-------|
| Sidebar Nav | 1 | Logo + NavItems + UserMenu | Collapsible sections |
```

---

## Phase 2: Build Atoms

**Objective:** Create smallest UI units using shadcn primitives.

### Before Implementing ANY Component

**ALWAYS query shadcn MCP first:**
```
Use mcp__shadcn__getComponent to check: button, input, badge, etc.
```

### Implementation Pattern

For each atom identified in the audit:

1. **Check if shadcn provides it** → Use shadcn's version, customize variants.
2. **If not provided** → Create custom component following shadcn patterns.

### CVA Variant Structure (Required)

All variant-based components MUST use CVA:

```typescript
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  // Base styles (apply to ALL variants)
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
```

### Atom Requirements Checklist

- [ ] Uses CVA for variants (if has visual variations).
- [ ] Exports `VariantProps<typeof variants>` type.
- [ ] Forwards `className` prop via `cn()`.
- [ ] Has TypeScript interface with explicit props.
- [ ] Uses `React.forwardRef` for DOM element access.
- [ ] Extracts colors/styles from original HTML.
- [ ] "use client" directive ONLY if needs interactivity.

---

## Phase 3: Build Molecules

**Objective:** Compose atoms into functional units.

### Implementation Pattern

For each molecule identified:

1. Import atoms from `@/components/ui`.
2. Create TypeScript interface with all props.
3. Keep generic/reusable (not page-specific).

### Common Molecules

- Stat cards (icon + number + label + trend).
- Navigation items (icon + label + badge).
- Search bars (input + button + icon).
- Form field wrappers (label + input + error).
- Tab groups.
- Pagination controls.
- Log/activity entries.
- Action bars.

---

## Phase 4: Build Organisms & Layouts

**Objective:** Create major UI sections and page structures.

### Organism Implementation

For each organism:

1. Compose from molecules and atoms.
2. Handle internal UI state (selection, scroll, open/closed).
3. Accept data via props (NO hardcoded data).
4. Create flexible generic interfaces.

### Layout Components

Create layouts for page structures:

```typescript
interface SidebarLayoutProps {
  sidebar: React.ReactNode
  children: React.ReactNode
  sidebarWidth?: "sm" | "md" | "lg"
}

const SidebarLayout = ({ sidebar, children, sidebarWidth = "md" }: SidebarLayoutProps) => (
  <div className="flex min-h-screen">
    <aside className={cn(
      "border-r bg-background",
      sidebarWidth === "sm" && "w-64",
      sidebarWidth === "md" && "w-72",
      sidebarWidth === "lg" && "w-80"
    )}>
      {sidebar}
    </aside>
    <main className="flex-1">{children}</main>
  </div>
)
```

---

## Output Structure

After conversion, components should be organized:

```
src/components/
├── ui/                    # Atoms (shadcn primitives)
│   ├── button.tsx
│   ├── input.tsx
│   ├── badge.tsx
│   └── ...
├── stat-card.tsx          # Molecules
├── nav-item.tsx
├── search-bar.tsx
├── sidebar.tsx            # Organisms
├── data-table.tsx
├── terminal-log.tsx
└── layouts/
    ├── sidebar-layout.tsx
    └── dashboard-layout.tsx
```

---

## Best Practices Summary

| Practice | Reason |
|----------|--------|
| Query shadcn MCP first | Get accurate props/variants. |
| CVA for all variants | Type-safe, consistent styling. |
| Forward className | Consumer customization. |
| Generic interfaces `<T>` | Reusable across data types. |
| Server Components default | Better performance. |
| "use client" only when needed | useState, useEffect, handlers. |
| No hardcoded data | Components receive via props. |

---

## Troubleshooting

### "Component doesn't match design"
- Re-check HTML for exact colors/spacing.
- Extract CSS custom properties from Stitch export.
- Map to Tailwind equivalents or add to theme.

### "Too many variants"
- Split into multiple components.
- Use compound component pattern.
- Check if variants are actually distinct states.

### "Unclear classification"
- See [atomic-design.md](references/atomic-design.md) for decision rules.
- When in doubt: if it has child components → molecule/organism.

### "shadcn doesn't have this component"
- Check extended shadcn libraries (shadcn/ui has 100+ components).
- Build custom following shadcn patterns.
- Use Radix UI primitives as base.