# Affordance Patterns

Universal patterns for making interactions obvious and intuitive.

## Visual Affordance Signals

### Interactive vs Static

| Signal | Means Interactive | Means Static |
|--------|-------------------|--------------|
| Cursor | Pointer | Default |
| Shadow | Elevated, clickable | Flat |
| Border | Editable or clickable | None or decorative |
| Color | Saturated accent | Muted/gray |
| Hover | State change | No change |

### Button Affordances

| Button Type | Visual Treatment | Expected Behavior |
|-------------|------------------|-------------------|
| Primary | Filled, accent color | Main action, one per screen |
| Secondary | Outlined or muted | Alternative action |
| Tertiary | Text only | Low-priority action |
| Destructive | Red accent | Dangerous, confirm first |
| Disabled | Grayed, 50% opacity | Can't click, explain why |

### Input Affordances

| Input Type | Visual Signal | Interaction |
|------------|---------------|-------------|
| Text input | Border, white bg | Tap to type |
| Dropdown | Chevron icon | Tap to select |
| Checkbox | Square, checkmark | Tap to toggle |
| Radio | Circle, dot | Tap to select (exclusive) |
| Slider | Track + handle | Drag to adjust |
| Toggle | Pill, on/off | Tap to switch |

### Card Affordances

| Card Type | Visual Cues | Behavior |
|-----------|-------------|----------|
| Clickable | Hover lift, cursor pointer | Entire card is tap target |
| Expandable | Chevron, "Read more" | Tap to expand in place |
| Actionable | Visible buttons | Specific actions on card |
| Read-only | No hover effect | Display only |

## Touch Target Guidelines

### Minimum Sizes

| Platform | Minimum | Recommended | Spacing |
|----------|---------|-------------|---------|
| iOS | 44x44pt | 48x48pt | 8pt between |
| Android | 48x48dp | 56x56dp | 8dp between |
| Web (touch) | 44x44px | 48x48px | 8px between |
| Web (mouse) | 24x24px | 32x32px | 4px between |

### Touch Target Expansion

When visual element is smaller than touch target:
```css
.small-icon-button {
  /* Visual size */
  width: 24px;
  height: 24px;

  /* Touch target expansion */
  position: relative;
}

.small-icon-button::before {
  content: '';
  position: absolute;
  inset: -12px; /* Expands to 48x48 */
}
```

## Z-Index Hierarchy

### Standard Layer System

| Layer | Z-Index Range | Contents |
|-------|---------------|----------|
| Base | 0 | Page content |
| Sticky | 10-20 | Sticky headers, footers |
| Dropdown | 30-40 | Menus, popovers |
| Overlay | 45-49 | Background dims |
| Modal | 50 | Dialogs, sheets |
| Toast | 60 | Notifications |
| Tooltip | 70 | Contextual hints |
| Critical | 9999 | Debug, system alerts |

### Mobile Nav Pattern

```css
:root {
  --z-header: 50;
  --z-overlay: 55;
  --z-mobile-nav: 60;
}
```

## Component Consolidation Patterns

### When to Consolidate

**Consolidate when:**
- Same data structure, different layout
- Same behavior, different styling
- Same component, different sizes
- Same purpose, different contexts

**Keep separate when:**
- Behavior differs fundamentally
- Logic complexity increases significantly
- Testing becomes harder
- Props become confusing

### Variant Pattern

```tsx
interface CardProps {
  variant: 'default' | 'compact' | 'featured';
  // ... other props
}

function Card({ variant = 'default', ...props }: CardProps) {
  const styles = {
    default: 'aspect-[4/3] p-4',
    compact: 'aspect-square p-2',
    featured: 'aspect-[16/9] p-6',
  };

  return <div className={styles[variant]}>...</div>;
}
```

### Consolidation Checklist

1. **Audit usage**: Grep for all instances of similar components
2. **Compare props**: Map out all props, find commonalities
3. **Design variants**: Define variant names that make sense
4. **Migrate incrementally**: Update one usage at a time
5. **Delete originals**: Remove old components, update exports
6. **Test**: Verify all usages work correctly

## Positioning Patterns

### Sticky Elements

```css
/* Sticky header that respects safe areas */
.sticky-header {
  position: sticky;
  top: 0;
  top: env(safe-area-inset-top, 0);
  z-index: var(--z-sticky);
}

/* Sticky bottom bar */
.sticky-footer {
  position: sticky;
  bottom: 0;
  bottom: env(safe-area-inset-bottom, 0);
}
```

### Dynamic Height Reference

```css
/* Set header height variable */
.header {
  height: var(--header-height, 56px);
}

/* Reference in other elements */
.content {
  padding-top: var(--header-height, 56px);
}

/* With offset */
.sticky-below-header {
  top: var(--header-height, 56px);
}
```

### Fixed + Scrollable Content

```css
/* Fixed shell, scrollable content */
.app-shell {
  display: flex;
  flex-direction: column;
  height: 100vh;
  height: 100dvh; /* Dynamic viewport height */
}

.fixed-header {
  flex-shrink: 0;
}

.scrollable-content {
  flex: 1;
  overflow-y: auto;
}

.fixed-footer {
  flex-shrink: 0;
}
```

## Gesture Affordances

### Swipe Patterns

| Gesture | Affordance Signal | Common Use |
|---------|-------------------|------------|
| Swipe left | Visible delete/action hint | Delete item |
| Swipe right | Visible complete hint | Mark done |
| Swipe down | Pull indicator | Refresh |
| Swipe horizontal | Pagination dots | Navigate cards |

### Long Press

- Show after 500ms hold
- Subtle haptic feedback
- Visual indicator (scale, highlight)
- Context menu or drag mode

### Drag Affordances

| Drag Type | Visual Signal |
|-----------|---------------|
| Reorderable | Drag handle (⋮⋮) |
| Resizable | Resize corner |
| Moveable | Move cursor on grab |
| Draggable | Elevation on drag |

## Hover State Design

### Hover Effect Types

| Element | Hover Effect | Purpose |
|---------|--------------|---------|
| Link | Underline/color change | Confirm clickable |
| Button | Background darken/lighten | Show active |
| Card | Subtle lift + shadow | Show interactive |
| Icon | Color/scale change | Confirm clickable |
| Row | Background highlight | Show focused |

### Hover State Guidelines

**Do:**
- Keep hover effects subtle (5-10% opacity shift)
- Make transitions smooth (150-200ms)
- Ensure sufficient contrast change
- Consider touch users (no hover)

**Don't:**
- Make critical info hover-only
- Use jarring transitions
- Rely on hover for essential actions
- Forget keyboard focus states

### Focus States

Always pair hover with focus for accessibility:
```css
.interactive-element:hover,
.interactive-element:focus-visible {
  /* Same or similar treatment */
  background: var(--hover-bg);
  outline: 2px solid var(--focus-ring);
  outline-offset: 2px;
}
```

## Progressive Disclosure Patterns

### Disclosure Triggers

| Trigger | Pattern | Use When |
|---------|---------|----------|
| Click/tap | Show/hide section | Related content |
| Hover | Tooltip | Brief hints |
| Scroll | Load more | Long lists |
| Time | Reveal after delay | Onboarding |
| Completion | Unlock next | Guided flows |

### Expand/Collapse

```
[Section Header]          [▼]
└── Hidden content appears when clicked

[Section Header]          [▲]
    Visible content
    that was hidden
```

### Tooltip vs Popover

| Tooltip | Popover |
|---------|---------|
| Hover triggered | Click triggered |
| Text only | Rich content |
| Disappears on leave | Persists until dismiss |
| Small (max 250px) | Can be larger |
| No interaction | May have actions |
