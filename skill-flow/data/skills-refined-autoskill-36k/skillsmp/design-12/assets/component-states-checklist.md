# Component States Checklist

## Overview

Every interactive component MUST implement all five states. Missing states create confusion, accessibility issues, and poor user experience.

---

## The Five Required States

### 1. Default State

The component's normal, resting appearance.

**Requirements:**
- Clear visual identity
- Readable text with sufficient contrast
- Distinguishable from surrounding elements

```css
.button {
  background: var(--color-primary);
  color: var(--color-text-on-primary);
  padding: var(--space-sm) var(--space-md);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
}
```

---

### 2. Hover State

Visual feedback when the cursor is over the element (pointer devices only).

**Requirements:**
- Noticeable but subtle change
- Indicates interactivity
- Should NOT trigger on touch devices

```css
/* Only apply on devices that support hover */
@media (hover: hover) {
  .button:hover {
    background: var(--color-primary-hover);
    transform: translateY(-1px);
    box-shadow: var(--shadow-sm);
  }
}
```

**Common hover effects:**
- Background color shift (darker/lighter)
- Subtle shadow increase
- Slight transform (lift, scale)
- Border color change
- Underline (for links)

---

### 3. Active State

Visual feedback when the element is being clicked/pressed.

**Requirements:**
- Immediate response to press
- Feels "pressed in" or "activated"
- Shorter/no transition for instant feedback

```css
.button:active {
  background: var(--color-primary-active);
  transform: translateY(1px);
  box-shadow: none;
}
```

**Common active effects:**
- Darker background
- Inward transform (scale down, move down)
- Shadow removal
- Border inset effect

---

### 4. Focus State

Visual indicator showing which element has keyboard focus.

**Requirements:**
- MUST be visible (never `outline: none` without alternative)
- High contrast against background
- Works in both light and dark modes
- Distinct from hover state

```css
.button:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

/* Remove default outline only when providing custom focus */
.button:focus {
  outline: none;
}

.button:focus-visible {
  box-shadow: 0 0 0 3px var(--color-focus-ring);
}
```

**Focus indicator options:**
- Outline (recommended - most accessible)
- Box shadow (ring effect)
- Border change
- Background change + outline

**Important:** Use `:focus-visible` instead of `:focus` to show focus rings only for keyboard navigation, not mouse clicks.

---

### 5. Disabled State

Indicates the element cannot be interacted with.

**Requirements:**
- Visually distinct from enabled state
- Lower contrast/opacity
- No hover/active effects
- Cursor indicates non-interactivity
- Include reason (if possible)

```css
.button:disabled,
.button[aria-disabled="true"] {
  background: var(--color-neutral-200);
  color: var(--color-neutral-400);
  cursor: not-allowed;
  opacity: 0.6;
  pointer-events: none;
}

/* Remove hover effect */
.button:disabled:hover {
  transform: none;
  box-shadow: none;
}
```

**Disabled state guidelines:**
- Reduce opacity OR use muted colors (not both heavily)
- Keep text readable (don't go below 3:1 contrast)
- Consider showing tooltip explaining why disabled

---

## Complete Button Example

```css
/* Base button */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-xs);
  padding: var(--space-sm) var(--space-md);
  font-size: var(--font-size-body);
  font-weight: var(--font-weight-medium);
  line-height: 1;
  color: var(--color-text-on-primary);
  background: var(--color-primary);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--duration-fast) var(--easing-standard);
}

/* Hover - only on capable devices */
@media (hover: hover) {
  .btn:hover:not(:disabled) {
    background: var(--color-primary-600);
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
  }
}

/* Active/pressed */
.btn:active:not(:disabled) {
  background: var(--color-primary-700);
  transform: translateY(0);
  box-shadow: var(--shadow-sm);
}

/* Focus - keyboard navigation */
.btn:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

/* Disabled */
.btn:disabled {
  background: var(--color-neutral-300);
  color: var(--color-neutral-500);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}
```

---

## State Checklist by Component

### Buttons

| State | Required Effect |
|-------|-----------------|
| Default | Brand color, readable text |
| Hover | Darker/lighter, slight lift |
| Active | Pressed effect, darker still |
| Focus | Visible outline/ring |
| Disabled | Muted, cursor: not-allowed |

### Links

| State | Required Effect |
|-------|-----------------|
| Default | Distinct color (usually blue), underline optional |
| Hover | Underline, color shift |
| Active | Darker color |
| Focus | Outline around text |
| Visited | Different color (optional but recommended) |

### Form Inputs

| State | Required Effect |
|-------|-----------------|
| Default | Clear border, proper contrast |
| Hover | Border color change |
| Focus | Strong border or ring, cursor in field |
| Disabled | Muted background, readonly appearance |
| Error | Red border, error icon/message |
| Success | Green border, checkmark (optional) |

### Checkboxes/Radios

| State | Required Effect |
|-------|-----------------|
| Default | Empty, visible boundary |
| Hover | Boundary highlight |
| Focus | Outline around control |
| Checked | Fill/checkmark visible |
| Disabled | Muted, non-interactive |

### Cards (Clickable)

| State | Required Effect |
|-------|-----------------|
| Default | Clear boundaries, readable |
| Hover | Lift effect, shadow increase |
| Active | Pressed/selected effect |
| Focus | Outline around entire card |
| Selected | Distinct background or border (if selectable) |

---

## Testing States

### Manual Checklist

For each interactive component:

- [ ] **Default:** Does it look correct without interaction?
- [ ] **Hover:** Mouse over - does it respond? (desktop only)
- [ ] **Active:** Click and hold - does it show pressed state?
- [ ] **Focus:** Tab to element - is focus ring visible?
- [ ] **Disabled:** Add disabled attribute - is it visually distinct?

### Keyboard Testing

1. Tab through the page
2. Every interactive element should receive visible focus
3. Enter/Space should activate buttons
4. Arrow keys should work in menus/dropdowns
5. Escape should close modals/menus

### Screen Reader Testing

1. Focus each element
2. Screen reader should announce element type
3. State should be announced ("button, disabled")
4. Changes should be announced (aria-live regions)

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `outline: none` without replacement | No visible focus | Add `:focus-visible` style |
| Same hover and active state | No press feedback | Make active state darker |
| Disabled via JS only | Still focusable | Add `disabled` attribute |
| Low contrast disabled state | Unreadable | Keep 3:1 minimum |
| Hover effect on touch devices | Sticky hover | Use `@media (hover: hover)` |
| Missing focus state | Keyboard users lost | Always style `:focus-visible` |

---

## Quick Reference

```css
/* Complete state pattern */
.interactive-element {
  /* Default */
  background: var(--default);
  cursor: pointer;
}

@media (hover: hover) {
  .interactive-element:hover:not(:disabled) {
    /* Hover */
    background: var(--hover);
  }
}

.interactive-element:active:not(:disabled) {
  /* Active */
  background: var(--active);
}

.interactive-element:focus-visible {
  /* Focus */
  outline: 2px solid var(--focus);
  outline-offset: 2px;
}

.interactive-element:disabled {
  /* Disabled */
  opacity: 0.6;
  cursor: not-allowed;
}
```
