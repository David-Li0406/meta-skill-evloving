# Buttons

Tenzir's button system provides standard, destructive, and floating button variants across multiple sizes with consistent styling for all interactive states.

## Contents

- [Standard Buttons](#standard-buttons)
- [Delete Buttons](#delete-buttons-destructive)
- [Floating Buttons](#floating-buttons)
- [CSS Custom Properties](#css-custom-properties)
- [Usage Guidelines](#usage-guidelines)

## Standard Buttons

### Props

| Prop       | Values                                             |
| ---------- | -------------------------------------------------- |
| `variant`  | `primary`, `secondary`, `tertiary`                 |
| `size`     | `xs`, `s`, `m`, `l`                                |
| `state`    | `default`, `hover`, `pressed`, `focus`, `disabled` |
| `icon`     | `none`, `leading`, `only`                          |
| `shortcut` | `boolean` - shows keyboard shortcut badge          |

### Size Specifications

All buttons use `border-radius: 5px` and `font-weight: 600` (Semi Bold).

| Size | Height | Padding X | Padding Y | Font Size | Line Height | Icon Size |
| ---- | ------ | --------- | --------- | --------- | ----------- | --------- |
| `xs` | 24px   | 8px       | 3px       | 12px      | 18px        | 16px      |
| `s`  | 28px   | 12px      | 4px       | 14px      | 20px        | 16px      |
| `m`  | 32px   | 12px      | 6px       | 14px      | 20px        | 20px      |
| `l`  | 36px   | 16px      | 8px       | 14px      | 20px        | 20px      |

### Primary Button

Solid blue background for primary actions.

| State    | Background       | Text         | Border         |
| -------- | ---------------- | ------------ | -------------- |
| Default  | `blue-500`       | `neutral-50` | none           |
| Hover    | `blue-600`       | `neutral-50` | none           |
| Pressed  | `blue-600` + dim | `neutral-50` | none           |
| Focus    | `blue-600`       | `neutral-50` | 3px `blue-300` |
| Disabled | `neutral-300`    | `neutral-50` | none           |

```css
.btn-primary {
  background: var(--blue-500);
  color: var(--neutral-50);
  border: none;
  border-radius: 5px;
}

.btn-primary:hover {
  background: var(--blue-600);
}

.btn-primary:focus-visible {
  background: var(--blue-600);
  outline: 3px solid var(--blue-300);
  outline-offset: 0;
}

.btn-primary:disabled {
  background: var(--neutral-300);
  cursor: not-allowed;
}
```

### Secondary Button

Outlined button for secondary actions.

| State    | Background       | Text          | Border            |
| -------- | ---------------- | ------------- | ----------------- |
| Default  | transparent      | `neutral-800` | 1px `neutral-250` |
| Hover    | `blue-100`       | `blue-500`    | 1px `blue-300`    |
| Pressed  | `blue-100` + dim | `blue-500`    | 1px `blue-300`    |
| Focus    | `blue-100`       | `blue-500`    | 3px `blue-300`    |
| Disabled | transparent      | `neutral-400` | 1px `neutral-250` |

```css
.btn-secondary {
  background: transparent;
  color: var(--neutral-800);
  border: 1px solid var(--neutral-250);
  border-radius: 5px;
}

.btn-secondary:hover {
  background: var(--blue-100);
  color: var(--blue-500);
  border-color: var(--blue-300);
}

.btn-secondary:focus-visible {
  background: var(--blue-100);
  color: var(--blue-500);
  outline: 3px solid var(--blue-300);
  outline-offset: 0;
}

.btn-secondary:disabled {
  color: var(--neutral-400);
  cursor: not-allowed;
}
```

### Tertiary Button

Text-only button for low-emphasis actions.

| State    | Background    | Text          | Border         |
| -------- | ------------- | ------------- | -------------- |
| Default  | transparent   | `neutral-800` | none           |
| Hover    | `neutral-100` | `neutral-800` | none           |
| Pressed  | `neutral-200` | `neutral-800` | none           |
| Focus    | transparent   | `neutral-800` | 3px `blue-300` |
| Disabled | transparent   | `neutral-400` | none           |

```css
.btn-tertiary {
  background: transparent;
  color: var(--neutral-800);
  border: none;
  border-radius: 5px;
}

.btn-tertiary:hover {
  background: var(--neutral-100);
}

.btn-tertiary:focus-visible {
  outline: 3px solid var(--blue-300);
  outline-offset: 0;
}

.btn-tertiary:disabled {
  color: var(--neutral-400);
  cursor: not-allowed;
}
```

### Icon Buttons

Icon-only buttons use square dimensions based on size.

| Size | Dimensions | Icon Size | Padding |
| ---- | ---------- | --------- | ------- |
| `xs` | 24×24px    | 16px      | 4px     |
| `s`  | 28×28px    | 16px      | 6px     |
| `m`  | 32×32px    | 20px      | 6px     |
| `l`  | 36×36px    | 20px      | 8px     |

### Shortcut Badge

Buttons can display a keyboard shortcut badge (e.g., `⌘↵`).

- Font: Inter Medium (500), 10px
- Background: `neutral-50` at 8% opacity (lighten overlay)
- Border radius: 3px
- Padding: 2px 4px
- Gap from button text: 8px

---

## Delete Buttons (Destructive)

Destructive button variants using red colors for dangerous actions like deletion.

### Primary Delete Button

Solid red background for primary destructive actions.

| State    | Background          | Text         | Border          |
| -------- | ------------------- | ------------ | --------------- |
| Default  | `red-500` (#ff0a33) | `neutral-50` | none            |
| Hover    | `red-600` (#e00025) | `neutral-50` | none            |
| Pressed  | `red-600` + 20% dim | `neutral-50` | none            |
| Focus    | `red-600`           | `neutral-50` | 2-3px `red-200` |
| Disabled | `neutral-300`       | `neutral-50` | none            |

```css
.btn-delete-primary {
  background: var(--red-500);
  color: var(--neutral-50);
  border: none;
  border-radius: 5px;
}

.btn-delete-primary:hover {
  background: var(--red-600);
}

.btn-delete-primary:active {
  background:
    linear-gradient(rgba(14, 16, 23, 0.2), rgba(14, 16, 23, 0.2)),
    var(--red-600);
}

.btn-delete-primary:focus-visible {
  background: var(--red-600);
  outline: 3px solid var(--red-200);
  outline-offset: 0;
}

.btn-delete-primary:disabled {
  background: var(--neutral-300);
  cursor: not-allowed;
}
```

### Secondary Delete Button

Outlined button with red border for secondary destructive actions.

| State    | Background          | Text                | Border             |
| -------- | ------------------- | ------------------- | ------------------ |
| Default  | transparent         | `red-500` (#ff0a33) | 1px `red-200`      |
| Hover    | `red-100` (#fff0f2) | `red-500`           | 1px `red-300`      |
| Pressed  | `red-200` (#ffe0e5) | `red-600` (#e00025) | 1px `red-400`      |
| Focus    | `red-100`           | `red-500`           | 3px `red-200` ring |
| Disabled | transparent         | `neutral-300`       | 1px `neutral-200`  |

```css
.btn-delete-secondary {
  background: transparent;
  color: var(--red-500);
  border: 1px solid var(--red-200);
  border-radius: 5px;
}

.btn-delete-secondary:hover {
  background: var(--red-100);
  border-color: var(--red-300);
}

.btn-delete-secondary:active {
  background: var(--red-200);
  color: var(--red-600);
  border-color: var(--red-400);
}

.btn-delete-secondary:focus-visible {
  background: var(--red-100);
  box-shadow: 0 0 0 2px var(--red-200);
}

.btn-delete-secondary:disabled {
  color: var(--neutral-300);
  border-color: var(--neutral-200);
  cursor: not-allowed;
}
```

### Tertiary Delete Button

Text-only button for low-emphasis destructive actions.

| State    | Background          | Text                | Border        |
| -------- | ------------------- | ------------------- | ------------- |
| Default  | transparent         | `red-500` (#ff0a33) | none          |
| Hover    | `red-100` (#fff0f2) | `red-500`           | none          |
| Pressed  | `red-200` (#ffe0e5) | `red-600` (#e00025) | none          |
| Focus    | `red-100`           | `red-500`           | 2px `red-200` |
| Disabled | transparent         | `neutral-300`       | none          |

```css
.btn-delete-tertiary {
  background: transparent;
  color: var(--red-500);
  border: none;
  border-radius: 5px;
}

.btn-delete-tertiary:hover {
  background: var(--red-100);
}

.btn-delete-tertiary:active {
  background: var(--red-200);
  color: var(--red-600);
}

.btn-delete-tertiary:focus-visible {
  background: var(--red-100);
  outline: 2px solid var(--red-200);
  outline-offset: 0;
}

.btn-delete-tertiary:disabled {
  color: var(--neutral-300);
  cursor: not-allowed;
}
```

### Delete Shortcut Badge

For delete buttons, the shortcut badge uses red-tinted colors.

| Variant   | Background                   | Icon Color    |
| --------- | ---------------------------- | ------------- |
| Primary   | `lighten-20%` (white at 20%) | white         |
| Secondary | `red-400` at 12% opacity     | `red-500`     |
| Tertiary  | `red-400` at 12% opacity     | `red-500`     |
| Disabled  | `neutral-100`                | `neutral-300` |

---

## Floating Buttons

Icon button groups that float over content with elevated shadow styling.

### Props

| Prop        | Values                                    |
| ----------- | ----------------------------------------- |
| `amount`    | `single`, `double`, `triple`              |
| `state`     | `default`, `hover`, `pressed`, `disabled` |
| `placement` | `outside`, `inside`                       |

### Size Specifications

| Property       | Value             |
| -------------- | ----------------- |
| Height         | 28px              |
| Width (single) | 32px              |
| Width (double) | 65px              |
| Width (triple) | 98px              |
| Icon size      | 24px              |
| Padding X      | 4px               |
| Padding Y      | 2px               |
| Border radius  | 5px               |
| Border         | 1px `neutral-200` |

### Shadow Specifications

| Placement | Shadow             | Opacity |
| --------- | ------------------ | ------- |
| Outside   | `shadow-s`         | 20%     |
| Inside    | `shadow-s` (light) | 10%     |

```css
/* Outside placement */
box-shadow:
  0px 3px 6px -3px rgba(14, 18, 23, 0.2),
  0px 8px 16px -8px rgba(14, 18, 23, 0.2);

/* Inside placement */
box-shadow:
  0px 3px 6px -3px rgba(14, 18, 23, 0.1),
  0px 8px 16px -8px rgba(14, 18, 23, 0.1);
```

### State Specifications

| State    | Icon Background | Icon Color    |
| -------- | --------------- | ------------- |
| Default  | `neutral-50`    | `neutral-800` |
| Hover    | `neutral-100`   | `neutral-800` |
| Pressed  | `neutral-200`   | `neutral-800` |
| Disabled | `neutral-50`    | `neutral-300` |

```css
.floating-button {
  display: flex;
  align-items: center;
  height: 28px;
  background: var(--neutral-50);
  border: 1px solid var(--neutral-200);
  border-radius: 5px;
  box-shadow: var(--shadow-s);
}

.floating-button--inside {
  box-shadow:
    0px 3px 6px -3px rgba(14, 18, 23, 0.1),
    0px 8px 16px -8px rgba(14, 18, 23, 0.1);
}

.floating-button__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2px 4px;
  background: var(--neutral-50);
  border-radius: 5px;
}

.floating-button__icon:hover {
  background: var(--neutral-100);
}

.floating-button__icon:active {
  background: var(--neutral-200);
}

.floating-button__icon--disabled {
  background: var(--neutral-50);
  color: var(--neutral-300);
  cursor: not-allowed;
}

.floating-button__icon svg {
  width: 24px;
  height: 24px;
}

.floating-button__divider {
  width: 1px;
  height: 100%;
  background: var(--neutral-200);
}
```

---

## CSS Custom Properties

```css
:root {
  /* Button sizes */
  --btn-height-xs: 24px;
  --btn-height-s: 28px;
  --btn-height-m: 32px;
  --btn-height-l: 36px;

  --btn-px-xs: 8px;
  --btn-px-s: 12px;
  --btn-px-m: 12px;
  --btn-px-l: 16px;

  --btn-py-xs: 3px;
  --btn-py-s: 4px;
  --btn-py-m: 6px;
  --btn-py-l: 8px;

  /* Button radius */
  --btn-radius: 5px;

  /* Focus ring */
  --btn-focus-ring-width: 3px;
  --btn-focus-ring-color: var(--blue-300);

  /* Delete button colors */
  --btn-delete-bg: var(--red-500);
  --btn-delete-bg-hover: var(--red-600);
  --btn-delete-text: var(--neutral-50);
  --btn-delete-focus-ring: var(--red-200);

  /* Floating button */
  --floating-btn-height: 28px;
  --floating-btn-icon-size: 24px;
  --floating-btn-padding-x: 4px;
  --floating-btn-padding-y: 2px;
  --floating-btn-radius: 5px;
  --floating-btn-border: var(--neutral-200);
  --floating-btn-bg: var(--neutral-50);
  --floating-btn-bg-hover: var(--neutral-100);
  --floating-btn-bg-pressed: var(--neutral-200);
}
```

---

## Usage Guidelines

### Choosing a Variant

1. **Standard buttons:**
   - **Primary** - Main action, one per section (e.g., "Save", "Submit")
   - **Secondary** - Alternative actions (e.g., "Cancel", "Export")
   - **Tertiary** - Low-emphasis actions (e.g., "Learn more", "Skip")

2. **Delete buttons:**
   - Use sparingly for truly destructive actions
   - Require confirmation for irreversible actions
   - Use clear, specific labels (e.g., "Delete project" not just "Delete")
   - Prefer secondary/tertiary for less critical destructive actions

3. **Floating buttons:**
   - **Outside** - Buttons floating over content areas (cards, images)
   - **Inside** - Buttons within containers that already have elevation
   - **Single** - Copy button, action button
   - **Double** - Common pairs like Copy + Run
   - **Triple** - Related action sets

### Choosing a Size

- **XS (24px)** - Inline actions, compact UI
- **S (28px)** - Secondary UI, toolbars
- **M (32px)** - Default size, most common
- **L (36px)** - Hero sections, prominent CTAs

### Icon Usage

- Leading icons clarify the action (e.g., download, add, delete)
- Icon-only buttons need accessible labels (`aria-label`)
- Use 16px icons for XS/S sizes, 20px for M/L sizes

### Accessibility

- Always include `aria-label` for icon-only buttons
- Avoid disabling without explanation
- Consider showing tooltips explaining why an action is unavailable
