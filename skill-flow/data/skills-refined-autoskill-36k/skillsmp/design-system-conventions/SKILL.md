---
name: design-system-conventions
description: Guide for UI styling with semantic design system classes. Never use gray-* colors or arbitrary Tailwind utilities.
---

# Design System Conventions Skill

## Purpose

Enforce consistent styling using semantic design system classes. Prevent arbitrary Tailwind utilities and ensure visual consistency.

## ⚠️ CRITICAL: Never Use Generic Grays

**FORBIDDEN**: `text-gray-*`, `bg-gray-*`, `border-gray-*`

**USE INSTEAD**: Semantic tokens from the design system.

## Color Token Reference

| Purpose             | Token                      | Example         |
| ------------------- | -------------------------- | --------------- |
| Primary text        | `text-foreground`          | Main content    |
| Strong text         | `text-foreground-strong`   | Headings        |
| Muted text          | `text-foreground/80`       | Secondary       |
| Background          | `bg-background`            | Page background |
| Muted background    | `bg-muted`                 | Cards, sections |
| Border              | `border-border`            | All borders     |
| Primary button text | `text-primary-foreground`  | Button labels   |

### Opacity Variants

Use `/80`, `/70`, `/60` suffixes for opacity:

```tsx
// ✅ CORRECT
<p className="text-foreground/80">Secondary text</p>

// ❌ WRONG
<p className="text-gray-600">Secondary text</p>
```

## Typography Classes

**ALWAYS use semantic classes, NEVER arbitrary text-\* utilities for typography.**

| Class          | Usage                  |
| -------------- | ---------------------- |
| `.heading-1`   | Page titles (h1)       |
| `.heading-2`   | Section titles (h2)    |
| `.heading-3`   | Subsection titles (h3) |
| `.heading-4`   | Minor headings (h4)    |
| `.body-large`  | Large body text        |
| `.body-normal` | Default body text      |
| `.body-small`  | Small body text        |
| `.label`       | Form labels, captions  |

### Examples

```tsx
// ✅ CORRECT
<h1 className="heading-1">Page Title</h1>
<p className="body-normal">Content here</p>

// ❌ WRONG
<h1 className="text-3xl md:text-4xl font-bold">Page Title</h1>
<p className="text-base">Content here</p>
```

## Button Classes

Use semantic button classes (component coming in Week 4):

| Class          | Usage                |
| -------------- | -------------------- |
| `.btn-primary` | Primary actions      |
| `.btn-neutral` | Secondary actions    |
| `.btn-outline` | Tertiary actions     |
| `.btn-muted`   | Low-emphasis actions |

```tsx
// ✅ CORRECT
<button className="btn-primary">Submit</button>

// ❌ WRONG
<button className="bg-primary text-whiteCorp px-6 py-3 rounded-xl hover:bg-primarydark">
  Submit
</button>
```

## Card Classes

| Class            | Usage                      |
| ---------------- | -------------------------- |
| `.card-bordered` | Border + subtle shadow     |
| `.card-elevated` | Stronger shadow, no border |
| `.card-body`     | Inner padding              |
| `.card-header`   | Header section             |
| `.card-footer`   | Footer section             |

```tsx
// ✅ CORRECT
<div className="card-bordered">
  <div className="card-body">
    <h3 className="heading-3">Card Title</h3>
    <p className="body-normal">Content</p>
  </div>
</div>
```

## Badge Classes

| Class            | Usage                     |
| ---------------- | ------------------------- |
| `.badge-primary` | Red background (emphasis) |
| `.badge-default` | Gray background (neutral) |

## Layout Utilities

Replace repetitive flex patterns:

| Semantic Class  | Replaces                            |
| --------------- | ----------------------------------- |
| `.flex-center`  | `flex justify-center items-center`  |
| `.flex-between` | `flex justify-between items-center` |
| `.flex-start`   | `flex justify-start items-center`   |
| `.stack`        | `flex flex-col gap-element-gap`     |

```tsx
// ✅ CORRECT
<div className="flex-center gap-element-gap">
  <Icon />
  <span>Text</span>
</div>

// ❌ WRONG
<div className="flex justify-center items-center gap-4">
  <Icon />
  <span>Text</span>
</div>
```

## Spacing Tokens

| Token                          | Usage              |
| ------------------------------ | ------------------ |
| `py-section-y`, `px-section-x` | Section spacing    |
| `p-card-padding`               | Card inner padding |
| `gap-element-gap`              | Default gaps       |

### Tailwind Spacing Exception

**Allowed**: One-off micro-spacing inside leaf components (`gap-1`, `gap-2`, `p-1`, `p-2`)

**Not allowed**:

- Section/page/layout spacing
- Card/button/input paddings
- Shared components

**Rule**: If repeated → create/extend a semantic token instead.

## Border Radius Tokens

| Token            | Usage        | Value |
| ---------------- | ------------ | ----- |
| `rounded-button` | Buttons      | 8px   |
| `rounded-card`   | Cards        | 12px  |
| `rounded-input`  | Form inputs  | 8px   |
| `rounded-badge`  | Pills/badges | full  |

## Deprecated Aliases - DO NOT USE

❌ `primarydark`, `primarySoft`, `whiteCorp`, `darkCorp`, `blackCorp`, `fullBlackCorp`, `bColor`

Use semantic tokens instead.

## Migration Context

**Current Phase**: Week 0 - Foundation

When modifying existing components:

1. Prefer semantic classes over inline utilities
2. Keep changes incremental
3. Consult `/docs/reference-data.md` for priority
4. Use new semantic color tokens

## Checklist Before Styling

- [ ] Using semantic typography classes? (not `text-xl font-bold`)
- [ ] Using semantic color tokens? (not `gray-*`)
- [ ] Using button classes? (not inline utilities)
- [ ] Using card classes? (not custom shadows/borders)
- [ ] Using layout utilities? (`flex-center` vs manual flex)
- [ ] Using spacing tokens? (for consistent spacing)

## Files to Reference

- [styles/globals.css](../../../styles/globals.css) - Design system classes
- [tailwind.config.js](../../../tailwind.config.js) - Theme tokens
- [docs/design-system-overview.md](../../../docs/design-system-overview.md) - Full documentation
- [docs/implementation-reference.md](../../../docs/implementation-reference.md) - Code examples
