---
name: ui-design
description: instructions for OpenPromo's design principles when desigining user flows/product surfaces on OpenPromo dashboard or www.
---

# OpenPromo UI Design Principles

Decision-making framework for building UI on OpenPromo dashboard and www.

## Core Principles

1. **Plain, minimal, flat** - no heavy shadows, no clustered cards
2. **Progressive disclosure** - start simple, expand for complexity
3. **Usability over minimalism** - function wins when there's conflict

## Design Signature

What makes OpenPromo distinct from generic shadcn:

| Element | Approach |
|---------|----------|
| **Typography** | Tight tracking on headings (-0.02em), tighter on display (-0.03em) |
| **Focus rings** | Coral highlight color, not gray |
| **Accent** | Coral `--highlight` for CTAs, badges, active states |
| **Badges** | Use `variant="highlight"` for emphasis, not just default |
| **Buttons** | `variant="highlight"` for primary CTAs that need to pop |

## Component Selection

### Containers
- **Card**: standalone content blocks, stats, settings sections
- **Dialog**: confirmations, quick forms (< 5 fields), focused tasks
- **Drawer**: side panels, detail views, forms with context needed
- **Sheet**: mobile-first overlays, filters on small screens

### Data Display
- **Table**: structured data, sortable columns, bulk actions needed
- **Grid (DataGrid)**: visual content (images, cards), gallery views
- **List**: simple items, sequential data, timeline-like content

### Forms
- **Inline**: single field edits, toggles, quick settings
- **Modal (Dialog)**: short forms, confirmations, focused input
- **Page/Section**: complex forms, multi-step flows, settings pages

### Feedback
- **Toast (sonner)**: transient success/info messages
- **Alert**: persistent warnings, important info in context
- **ErrorState**: full component failure, with retry option

### icons 
- we have lucide icons and react-icons installed, react-icons is way more complete, so prefer to use them.

## Layout Patterns

### Page Structure
```
Header (fixed, blur on scroll)
  SidebarTrigger | Breadcrumb | Actions
Main
  PageHeader (title + actions)
  Content (max-w-7xl centered)
```

### Spacing Scale
- `gap-1` / `gap-1.5`: tight, related items
- `gap-2` / `gap-3`: form fields, list items
- `gap-4`: section content
- `gap-6`: major sections, page padding

### Responsive
- Mobile-first approach
- Breakpoints: `sm:` (640), `md:` (768), `lg:` (1024), `xl:` (1280)
- Grid columns: 1 -> 2 (sm) -> 3 (lg) -> 4 (xl)

## State Handling

### Loading
- Use skeleton components from `@/components/common`
- Match skeleton shape to expected content
- `TableSkeleton`, `GridSkeleton`, `CardSkeleton`

### Error
- Use `ErrorState` component
- Always provide retry action when possible
- Use `variant="minimal"` for inline contexts

### Empty
- Center in container
- Icon + heading + description
- Primary CTA to resolve (e.g., "Create first item")

## Common Patterns

### Filter Bar
```tsx
<FilterBar hasActiveFilters={hasFilters} onClearFilters={clear}>
  <FilterSelect ... />
  <FilterDateRange ... />
  <FilterSearch ... />
</FilterBar>
```

### Data Table with Selection
```tsx
<DataTableHeader table={table} searchValue={search} onSearchChange={setSearch} />
<BatchActionBar selectedCount={n} actions={[...]} />
<Table>...</Table>
<DataTableFooter table={table} />
```

### Stats Display
```tsx
<StatCardGroup columns="auto">
  <StatCard label="..." value={n} trend={{...}} />
</StatCardGroup>
```

## Avoid

- `shadow-md` or larger (flat design - no shadows except `shadow-sm` in rare cases)
- Hardcoded colors (`bg-gray-*`, `text-gray-*`, `bg-white`, `border-gray-*`)
- Manual dark mode classes (`dark:bg-*`) - use theme tokens instead
- Nested cards within cards
- Multiple CTAs competing for attention
- Custom components when primitives exist in `@/components/common`
- Inline styles or arbitrary Tailwind values

## Design Tokens (OKLCH Color System)

We use OKLCH color space for perceptual uniformity. All colors are defined in `packages/ui/src/styles/theme.css`.

### Design Direction: "Warm Minimal"
- Warm stone-based neutrals (not cool grays)
- Near-black primary in light mode, near-white in dark mode
- Coral accent (`--highlight`) for special emphasis
- Flat design - minimal shadows

### Core Token Usage

| Token | Tailwind Class | Use Case |
|-------|---------------|----------|
| `--background` | `bg-background` | Page background |
| `--foreground` | `text-foreground` | Primary text |
| `--card` | `bg-card` | Card/container backgrounds |
| `--muted` | `bg-muted` | Subtle backgrounds, disabled states, skeletons |
| `--muted-foreground` | `text-muted-foreground` | Secondary text, placeholders, icons |
| `--border` | `border-border` | All borders (use `border-border/40` for subtle) |
| `--primary` | `bg-primary` | Primary buttons, active states |
| `--destructive` | `text-destructive` | Error states, delete actions |
| `--success` | `text-success`, `bg-success` | Success states, confirmations |
| `--warning` | `text-warning`, `bg-warning` | Warning states, cautions |
| `--info` | `text-info`, `bg-info` | Informational states |
| `--highlight` | `bg-highlight` | Special emphasis (coral accent) |

### Migration Patterns

When updating legacy code, use these replacements:

```
bg-white              → bg-card or bg-background
bg-gray-50            → bg-muted/50
bg-gray-100           → bg-muted
bg-gray-200           → bg-muted (or border-border for dividers)
text-gray-500         → text-muted-foreground
text-gray-600         → text-muted-foreground
text-gray-700         → text-foreground
text-gray-800         → text-foreground
text-gray-900         → text-foreground
border-gray-200       → border-border
border-gray-300       → border-border
shadow-md, shadow-lg  → REMOVE (flat design)
hover:shadow-md       → hover:border-foreground/50

text-emerald-600 dark:text-emerald-400  → text-success
text-amber-600 dark:text-amber-400      → text-warning
text-sky-600 dark:text-sky-400          → text-info
bg-emerald-*/10                         → bg-success/10
bg-amber-*/10                           → bg-warning/10
bg-sky-*/10                             → bg-info/10
```

### Semantic State Colors

Use these tokens for state indicators (they auto-adapt to dark mode):

```tsx
// Success state
<div className="bg-success/10 text-success border-success/30">Success!</div>
<Text tone="success">Operation completed</Text>

// Warning state
<div className="bg-warning/10 text-warning border-warning/30">Warning</div>
<Text tone="warning">Please review</Text>

// Info state
<div className="bg-info/10 text-info border-info/30">Info</div>
<Text tone="info">Did you know?</Text>
```

### Brand Colors (Keep As-Is)

These colors should NOT be converted to theme tokens:

- **Platform brand colors**: FB blue, IG pink, TikTok black/white
- **Chart colors**: Use `--chart-1` through `--chart-5`

### Error/Destructive States

```tsx
// Error container
<div className="border border-destructive/30 bg-destructive/10 text-destructive">
  Error message
</div>

// Destructive button/action
<Button variant="destructive">Delete</Button>

// Error text
<span className="text-destructive">Field is required</span>
```

### Dark Mode

Theme tokens automatically adapt. Never use explicit dark mode classes for theme colors:

```tsx
// GOOD - auto-adapts
className="bg-card text-foreground border-border"

// BAD - manual dark mode
className="bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
```

### Skeleton/Loading States

```tsx
// Skeleton placeholder
<div className="bg-muted animate-pulse rounded-lg" />

// Gradient skeleton (for avatars)
<div className="bg-gradient-to-r from-muted to-muted-foreground/20" />
```

## Decision Checklist

Before building new UI:
1. Does a primitive exist in `packages/ui` or `dash/ui/components/common`?
2. Does similar UI exist elsewhere in the app? Follow that pattern.
3. Is this the simplest solution that meets the requirement?
4. Would a user understand this without explanation?
5. Are you using theme tokens instead of hardcoded colors?
