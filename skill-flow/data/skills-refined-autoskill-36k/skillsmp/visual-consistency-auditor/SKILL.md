---
name: visual-consistency-auditor
description: Skill for ensuring visual consistency and preventing layout shifts during responsive transitions.
---

# Visual Consistency Auditor (Design System & Brand)

This skill acts as a "Brand Guardian" to ensure that FlyerBoard maintains a unified look and feel across all features and development cycles.

## Design System Tokens

### Colors (Tailwind)
- **Primary**: `primary-500` (#ef4444) - Use for main actions/branding.
- **Neutral**: `neutral-800` (#242428) - Use for primary text.
- **Neutral Secondary**: `neutral-500` (#71717a) - Use for secondary text.
- **Borders**: `neutral-200` (#dbdbe4).

### Typography
- **Primary Font**: `Plus Jakarta Sans`.
- **Base Size**: 16px (ensure inputs don't zoom on iOS).

### Layout
- **Containers**: Always use the `.container-padding` and `.content-max-width` utility classes defined in `tailwind.config.js`.

### Iconography (Lucide)
- **Library**: Always use `lucide-react`.
- **Main Actions/Nav**: 24px (`w-6 h-6`).
- **Sub-actions/Buttons**: 20px (`w-5 h-5`).
- **Inline/Micro**: 16px (`w-4 h-4`).
- **Style**: Soft colors (e.g., `text-neutral-500`) unless active or primary.

### Minimal Aesthetic
- **Philosophy**: Divar-inspired "content-first" look.
- **Clutter**: Remove non-essential borders and shadow "chrome without compromising aesthetics"
- **White Space**: Prioritize medium breathing room over dense information.
- **Micro-interactions**: Use subtle transitions (200ms) for hovers and state changes.

## Consistency Rules

### 1. Component Reuse
Before creating a new UI component, check `src/components/ui/` to see if one already exists:
- `CircularProgress`: For determinate loading.
- `BottomSheet`: For mobile action menus.
- `ImageDisplay`: For all image rendering.
- `StarRating`: For reviews/ratings.

### 2. Interaction Patterns
- **Feedback**: Every successful non-trivial user action should trigger a `toast.success()`.
- **Loading**: Every async operation must show a loading state (Skeleton or Spinner).
- **Navigation**: Use the standard `Header` component with slot-based icons.

## Scripts

### `audit-design-system.sh`
Scans for hardcoded color hex values or absolute pixel spacings that should be replaced with design tokens.

**Command**:
```bash
./.agent/skills/visual-consistency-auditor/scripts/audit-design-system.sh <path-to-file>
```

## Tips
- Avoid using "arbitrary values" in Tailwind (`w-[123px]`) unless absolutely necessary.
- Refer to `tailwind.config.js` for the full list of available brand colors and spacing tokens.
