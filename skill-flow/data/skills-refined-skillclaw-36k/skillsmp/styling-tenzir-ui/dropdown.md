# Dropdown

Dropdown trigger button that shows a chevron indicator and supports optional leading icon.

## Props

| Prop     | Values                                                              |
| -------- | ------------------------------------------------------------------- |
| `icon`   | `true`, `false`                                                     |
| `state`  | `default`, `hover`, `active`, `pressed`, `focus`, `hover-on-active` |
| `size`   | `s`, `m`, `l`                                                       |
| `border` | `true`, `false`                                                     |

## Size Specifications

| Size | Height | Padding (no border) | Padding (with border) | Icon Size |
| ---- | ------ | ------------------- | --------------------- | --------- |
| `s`  | 28px   | 4px / 2px           | 8px / 2px             | 24px      |
| `m`  | 32px   | 4px / 4px           | 8px / 4px             | 24px      |
| `l`  | 36px   | 4px / 6px           | 8px / 6px             | 24px      |

All dropdowns use:

- Border radius: 5px
- Gap between icon and text: 8px
- Chevron icon: 20px
- Font size: 14px
- Line height: 20px

## Font Weight

| Border | Font Weight     |
| ------ | --------------- |
| No     | Semi Bold (600) |
| Yes    | Medium (500)    |

## State Specifications (No Border)

| State           | Background    | Text Color    | Border                                     |
| --------------- | ------------- | ------------- | ------------------------------------------ |
| Default         | transparent   | `neutral-800` | none                                       |
| Hover           | `neutral-100` | `neutral-800` | none                                       |
| Active          | `neutral-100` | `neutral-800` | none                                       |
| Hover on Active | `neutral-200` | `neutral-800` | none                                       |
| Pressed         | `neutral-200` | `neutral-800` | none                                       |
| Focus           | `neutral-100` | `neutral-800` | 1px `neutral-200` + 3px `neutral-250` ring |

## State Specifications (With Border)

| State           | Background    | Text Color    | Border                                     |
| --------------- | ------------- | ------------- | ------------------------------------------ |
| Default         | transparent   | `neutral-800` | 1px `neutral-250`                          |
| Hover           | `neutral-100` | `neutral-800` | 1px `neutral-250`                          |
| Active          | `neutral-100` | `neutral-800` | 1px `neutral-250`                          |
| Hover on Active | `neutral-200` | `neutral-800` | 1px `neutral-250`                          |
| Pressed         | `neutral-200` | `neutral-800` | 1px `neutral-250`                          |
| Focus           | `neutral-100` | `neutral-800` | 1px `neutral-200` + 3px `neutral-250` ring |

## Active State (Open)

When the dropdown is open (active state):

- Chevron icon rotates 180 degrees (points up)
- Background changes to `neutral-100`

## CSS Implementation

```css
/* Dropdown Base */
.dropdown {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px;
  border-radius: 5px;
  background: transparent;
  color: var(--neutral-800);
  font-family: "Inter", sans-serif;
  font-size: 14px;
  font-weight: 600;
  line-height: 20px;
  cursor: pointer;
}

/* With border variant */
.dropdown--border {
  border: 1px solid var(--neutral-250);
  padding: 2px 8px;
  font-weight: 500;
}

/* Size variants */
.dropdown--s {
  height: 28px;
  padding-top: 2px;
  padding-bottom: 2px;
}
.dropdown--m {
  height: 32px;
  padding-top: 4px;
  padding-bottom: 4px;
}
.dropdown--l {
  height: 36px;
  padding-top: 6px;
  padding-bottom: 6px;
}

/* Hover */
.dropdown:hover {
  background: var(--neutral-100);
}

/* Active (open) */
.dropdown--active {
  background: var(--neutral-100);
}

.dropdown--active:hover {
  background: var(--neutral-200);
}

/* Pressed */
.dropdown:active {
  background: var(--neutral-200);
}

/* Focus */
.dropdown:focus-visible {
  background: var(--neutral-100);
  border: 1px solid var(--neutral-200);
  box-shadow: 0 0 0 3px var(--neutral-250);
  outline: none;
}

/* Chevron */
.dropdown__chevron {
  width: 20px;
  height: 20px;
  transition: transform 0.2s ease;
}

.dropdown--active .dropdown__chevron {
  transform: rotate(180deg);
}

/* Leading icon */
.dropdown__icon {
  width: 24px;
  height: 24px;
}

/* Text */
.dropdown__text {
  flex-shrink: 0;
}
```

## CSS Custom Properties

```css
:root {
  /* Dropdown sizes */
  --dropdown-height-s: 28px;
  --dropdown-height-m: 32px;
  --dropdown-height-l: 36px;

  /* Dropdown styling */
  --dropdown-radius: 5px;
  --dropdown-gap: 8px;
  --dropdown-icon-size: 24px;
  --dropdown-chevron-size: 20px;

  /* Dropdown colors */
  --dropdown-bg: transparent;
  --dropdown-bg-hover: var(--neutral-100);
  --dropdown-bg-active: var(--neutral-100);
  --dropdown-bg-pressed: var(--neutral-200);
  --dropdown-border: var(--neutral-250);
  --dropdown-focus-ring: var(--neutral-250);
}
```

## Usage Guidelines

1. **Border vs. no border**:
   - **With border** - Use in form contexts or when dropdown needs clear boundaries
   - **Without border** - Use in navigation or when dropdown is part of a larger interactive element

2. **Icon usage**:
   - Include leading icon when it helps identify the dropdown's purpose
   - Use consistent icon size (24px)

3. **Size selection**:
   - **S (28px)** - Compact UI, toolbars
   - **M (32px)** - Default choice, most common
   - **L (36px)** - Forms, prominent selections

4. **State management**:
   - Toggle `--active` class when dropdown menu is open
   - Use chevron rotation to indicate open state
   - Ensure hover states work correctly on both closed and open states

5. **Accessibility**:
   - Use `aria-expanded` to indicate open/closed state
   - Use `aria-haspopup="listbox"` or `aria-haspopup="menu"` as appropriate
   - Ensure keyboard navigation works (Enter/Space to toggle, Escape to close)
