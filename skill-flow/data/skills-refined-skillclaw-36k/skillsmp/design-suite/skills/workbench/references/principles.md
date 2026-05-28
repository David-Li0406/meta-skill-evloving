# Core Craft Principles

These apply regardless of design direction. This is the quality floor.

---

## Surface & Token Architecture

Professional interfaces don't pick colors randomly — they build systems. Understanding this architecture is the difference between "looks okay" and "feels like a real product."

### The Primitive Foundation

Every color in your interface should trace back to a small set of primitives in your Tailwind config:

- **ink** — text colors (primary, secondary, muted)
- **surface** — surface colors (base, elevated, overlay)
- **edge** — edge colors (default, subtle)
- **accent** — your primary action color
- **semantic** — functional colors (destructive, warning, success)

Don't invent new colors. Map everything to these primitives.

### Surface Elevation Hierarchy

Surfaces stack. A dropdown sits above a card which sits above the page. Build a numbered system in your CSS variables:

```css
:root {
  --surface: #ffffff;           /* Level 1: Cards, panels */
  --surface-elevated: #ffffff;  /* Level 2: Dropdowns, popovers */
  --surface-overlay: #ffffff;   /* Level 3: Modals, stacked overlays */
}

.dark {
  --surface: #141414;           /* Level 1 */
  --surface-elevated: #1a1a1a;  /* Level 2: slightly lighter */
  --surface-overlay: #1f1f1f;   /* Level 3: even lighter */
}
```

In dark mode, higher elevation = slightly lighter. In light mode, higher elevation = shadow or barely lighter. The principle: **elevated surfaces need visual distinction from what's beneath them.**

### The Subtlety Principle

This is where most interfaces fail. Study Airwallex and Stripe — their surfaces are **barely different** but still distinguishable. Their borders are **light but not invisible**.

**For surfaces:** The difference between elevation levels should be subtle — a few percentage points of lightness, not dramatic jumps. In dark mode, surface might be 8% lighter than canvas, elevated might be 10%, overlay might be 12%. You can barely see it, but you feel it.

**For borders:** Borders should define regions without demanding attention. Use low opacity:

```jsx
// Tailwind with CSS variable
className="border border-edge"  // where --edge: rgba(0, 0, 0, 0.08)

// Or with Tailwind opacity
className="border border-black/[0.08] dark:border-white/[0.08]"
```

The border should disappear when you're not looking for it, but be findable when you need to understand the structure.

**The test:** Squint at your interface. You should still perceive the hierarchy — what's above what, where regions begin and end. But no single border or surface should jump out at you. If borders are the first thing you notice, they're too strong. If you can't find where one region ends and another begins, they're too subtle.

**Common AI mistakes to avoid:**
- Borders that are too visible (`border-gray-300` instead of subtle rgba)
- Surface jumps that are too dramatic (going from dark to light instead of dark to slightly-less-dark)
- Using different hues for different surfaces (gray card on blue background)
- Harsh dividers where subtle borders would do

### Text Hierarchy via Tokens

Build four levels in your Tailwind config:

```jsx
// Primary — default text, highest contrast
className="text-ink"

// Secondary — supporting text, slightly muted
className="text-ink-secondary"

// Tertiary — metadata, timestamps, less important
className="text-ink-muted"

// Faint — disabled, placeholder, lowest contrast
className="text-ink-muted/60"
```

Use all four consistently. If you're only using two, your hierarchy is too flat.

### Border Progression

Borders aren't binary. Build a scale:

```jsx
// Default — standard borders
className="border border-edge"

// Subtle — softer separation
className="border border-edge-subtle"

// Strong — emphasis, hover states
className="border border-edge hover:border-edge dark:hover:border-white/20"

// Focus — clear focus indication
className="ring-2 ring-accent/20"
```

Match border intensity to the importance of the boundary.

### Dedicated Control Tokens

Form controls (inputs, checkboxes, selects) have specific needs. Create dedicated patterns:

```jsx
// Input base
className="
  bg-canvas
  border border-edge
  rounded-control
  px-3 py-2
  text-ink placeholder:text-ink-muted
  focus:outline-none focus:ring-2 focus:ring-accent/20 focus:border-accent
  transition-colors
"

// Checkbox/Radio container
className="
  h-4 w-4
  rounded
  border border-edge
  bg-canvas
  data-[state=checked]:bg-accent data-[state=checked]:border-accent
"
```

This separation lets you tune controls independently from layout surfaces.

### Context-Aware Bases

Different areas of your app might need different base surfaces:

```jsx
// Main canvas
className="bg-canvas"

// Sidebar — could match or contrast
className="bg-canvas border-r border-edge"

// Inset/recessed areas
className="bg-canvas/50"  // or a dedicated --canvas-inset
```

The surface hierarchy works the same way — it just starts from a different base.

### Alternative Backgrounds for Depth

Beyond shadows, use contrasting backgrounds to create depth. An "alternative" or "inset" background makes content feel recessed:

```jsx
// Empty states in data grids
className="bg-canvas rounded-lg"

// Code blocks
className="bg-canvas font-mono text-sm p-4 rounded-lg"

// Inset panels
className="bg-canvas/50 rounded-lg p-4"
```

---

## Spacing System

Use Tailwind's spacing scale consistently. Map semantic meanings to the scale:

```
Micro (icon gaps, tight pairs):     gap-1, gap-1.5, gap-2   (4-8px)
Element (within buttons, inputs):   p-2, p-3, p-4           (8-16px)
Card (card internals):              p-4, p-5, p-6           (16-24px)
Section (between related groups):   gap-6, gap-8            (24-32px)
Region (major separations):         gap-8, gap-12, gap-16   (32-64px)
```

**The rule:** Every spacing value should be on the scale. `gap-[13px]` or `p-[22px]` signals no system.

## Symmetrical Padding

TLBR must match unless there's a clear reason. Tailwind makes this natural:

```jsx
// Good
className="p-4"
className="px-4 py-3"  // Only when horizontal needs more room

// Bad — asymmetric without reason
className="pt-6 pr-4 pb-3 pl-4"
```

## Border Radius Consistency

Sharper corners feel technical, rounder corners feel friendly. Pick a scale that fits your product's personality:

```jsx
// Sharp (utility tools, data apps)
className="rounded"      // 4px — inputs, small buttons
className="rounded-md"   // 6px — cards
className="rounded-lg"   // 8px — modals

// Soft (friendly, consumer-facing)
className="rounded-lg"   // 8px — inputs, buttons
className="rounded-xl"   // 12px — cards
className="rounded-2xl"  // 16px — modals
```

Don't mix sharp and soft randomly — inconsistent radius is as jarring as inconsistent spacing.

## Depth & Elevation Strategy

Match your depth approach to your design direction. Choose ONE and commit:

**Borders-only (flat)** — Clean, technical, dense. Works for utility-focused tools where information density matters more than visual lift. Stripe and many developer tools use almost no shadows.

```jsx
className="border border-edge rounded-card"
```

**Subtle single shadows** — Soft lift without complexity. Works for approachable products that want gentle depth.

```jsx
className="shadow-sm rounded-card"
// Or custom: shadow-[0_1px_3px_rgba(0,0,0,0.08)]
```

**Layered shadows** — Rich, premium, dimensional. Multiple shadow layers create realistic depth. Stripe uses this for some card types.

```jsx
// In tailwind.config.js
boxShadow: {
  'layered': `
    0 0 0 0.5px rgba(0, 0, 0, 0.05),
    0 1px 2px rgba(0, 0, 0, 0.04),
    0 2px 4px rgba(0, 0, 0, 0.03),
    0 4px 8px rgba(0, 0, 0, 0.02)
  `
}

// Usage
className="shadow-layered rounded-card"
```

**Surface color shifts** — Background tints establish hierarchy without any shadows.

```jsx
className="bg-surface"  // Card slightly different from canvas
```

## Card Layouts

Monotonous card layouts are lazy design. A metric card doesn't have to look like a plan card doesn't have to look like a settings card.

Design each card's internal structure for its specific content — but keep the surface treatment consistent:

```jsx
// Consistent surface treatment
const cardBase = "bg-surface border border-edge rounded-card"

// Metric card — number-focused
<div className={`${cardBase} p-4`}>
  <span className="text-xs text-ink-muted uppercase tracking-wide">Revenue</span>
  <span className="text-2xl font-semibold tabular-nums">$24,500</span>
  <span className="text-xs text-green-600">+12.5%</span>
</div>

// Action card — interaction-focused
<div className={`${cardBase} p-4 hover:border-edge-strong transition-colors cursor-pointer`}>
  ...
</div>
```

## Isolated Controls

UI controls deserve container treatment. Date pickers, filters, dropdowns — these should feel like crafted objects.

**Never use native form elements for styled UI.** Native `<select>`, `<input type="date">`, and similar elements render OS-native dropdowns that cannot be styled. Use MUI or build custom components:

```jsx
// Custom select with MUI + Tailwind
import { Select, MenuItem } from '@mui/material';

<Select
  className="min-w-[120px]"
  sx={{
    '& .MuiSelect-select': {
      padding: '8px 12px',
    },
    '& .MuiOutlinedInput-notchedOutline': {
      borderColor: 'var(--edge)',
    },
  }}
>
  <MenuItem value="option1">Option 1</MenuItem>
</Select>
```

## Typography Hierarchy

Build distinct levels that are visually distinguishable at a glance:

```jsx
// Headlines — heavier weight, tighter tracking
className="text-2xl font-semibold tracking-tight text-ink"

// Section titles
className="text-lg font-medium text-ink"

// Body — comfortable for reading
className="text-sm text-ink-secondary leading-relaxed"

// Labels/UI — works at smaller sizes
className="text-xs font-medium uppercase tracking-wide text-ink-muted"

// Data — monospace for alignment
className="font-mono text-sm tabular-nums text-ink"
```

Don't rely on size alone. Combine size, weight, and letter-spacing to create clear hierarchy.

## Monospace for Data

Numbers, IDs, codes, timestamps belong in monospace:

```jsx
className="font-mono tabular-nums"
```

`tabular-nums` ensures columnar alignment. Mono signals "this is data."

## Iconography

Icons clarify, not decorate — if removing an icon loses no meaning, remove it.

```jsx
// Icon with subtle container
<div className="p-2 rounded-lg bg-accent/10">
  <Icon className="h-4 w-4 text-accent" />
</div>

// Icon next to text — optical alignment
<div className="flex items-center gap-2">
  <Icon className="h-4 w-4 text-ink-muted" />
  <span className="text-sm">Label</span>
</div>
```

## Animation

Keep it fast and functional. Use Tailwind's transition utilities:

```jsx
// Micro-interactions (hover, focus) — instant feel
className="transition-colors duration-150"

// Larger transitions (panels, modals) — slightly longer
className="transition-all duration-200 ease-out"

// Transform-based animations
className="transition-transform duration-200 ease-out"
```

Avoid spring/bounce effects in professional interfaces — they feel playful, not serious.

## Contrast Hierarchy

Build a four-level system using your ink tokens:

```jsx
text-ink          // Primary — highest contrast
text-ink-secondary // Secondary — slightly muted
text-ink-muted    // Tertiary — metadata, less important
text-ink-muted/60 // Faint — disabled, lowest contrast
```

Use all four consistently throughout.

## Color Carries Meaning

Gray builds structure. Color communicates:

```jsx
// Status
className="text-green-600"  // Success
className="text-amber-600"  // Warning
className="text-red-600"    // Error

// Action
className="bg-accent text-white"  // Primary action

// Identity
className="text-accent"  // Brand, links
```

Unmotivated color is noise. Color that reinforces the product's world is character.

## Navigation Context

Screens need grounding. A data table floating in space feels like a component demo, not a product.

```jsx
// Sidebar with navigation
<aside className="w-64 border-r border-edge bg-canvas">
  <nav className="p-4 space-y-1">
    <a className="flex items-center gap-2 px-3 py-2 rounded-md bg-surface text-ink text-sm">
      <Icon /> Dashboard
    </a>
    <a className="flex items-center gap-2 px-3 py-2 rounded-md text-ink-secondary text-sm hover:bg-surface">
      <Icon /> Transactions
    </a>
  </nav>
</aside>
```

Consider using the same background as the main content area. Rely on a subtle border for separation rather than different background colors.

## Dark Mode

Dark interfaces have different needs:

**Borders over shadows** — Shadows are less visible on dark backgrounds. Lean more on borders for definition.

```jsx
// Dark mode might need slightly stronger borders
className="border border-edge dark:border-white/10"
```

**Adjust semantic colors** — Status colors often need adjustment for dark backgrounds:

```jsx
// Success — slightly desaturated for dark
className="text-green-600 dark:text-green-500"

// Error — adjusted for dark
className="text-red-600 dark:text-red-500"
```

**Same structure, different values** — The hierarchy system still applies, just with inverted values. Define all variants in your CSS variables:

```css
:root {
  --ink: #0f172a;
  --ink-secondary: #475569;
  --edge: rgba(0, 0, 0, 0.08);
}

.dark {
  --ink: #fafafa;
  --ink-secondary: #a1a1aa;
  --edge: rgba(255, 255, 255, 0.08);
}
```

---

## MUI + Tailwind Patterns

When using MUI components with Tailwind:

### Buttons

```jsx
import { Button } from '@mui/material';

// Primary action
<Button
  variant="contained"
  className="bg-accent hover:bg-accent/90 text-white normal-case font-medium px-4 py-2 rounded-control shadow-none"
  disableElevation
>
  Save Changes
</Button>

// Secondary action
<Button
  variant="outlined"
  className="border-edge text-ink hover:bg-surface normal-case font-medium px-4 py-2 rounded-control"
>
  Cancel
</Button>
```

### Form Fields

```jsx
import { TextField } from '@mui/material';

<TextField
  variant="outlined"
  size="small"
  className="w-full"
  sx={{
    '& .MuiOutlinedInput-root': {
      borderRadius: 'var(--radius-control)',
      '& fieldset': {
        borderColor: 'var(--edge)',
      },
      '&:hover fieldset': {
        borderColor: 'var(--edge)',
      },
      '&.Mui-focused fieldset': {
        borderColor: 'var(--accent)',
        borderWidth: '1px',
      },
    },
  }}
/>
```

### Data Tables

```jsx
import { DataGrid } from '@mui/x-data-grid';

<DataGrid
  className="border-none"
  sx={{
    '& .MuiDataGrid-cell': {
      borderColor: 'var(--edge-subtle)',
    },
    '& .MuiDataGrid-columnHeaders': {
      backgroundColor: 'var(--canvas)',
      borderColor: 'var(--edge)',
    },
    '& .MuiDataGrid-row:hover': {
      backgroundColor: 'var(--surface)',
    },
  }}
/>
```

See `references/tailwind-mui-integration.md` for complete setup patterns.
