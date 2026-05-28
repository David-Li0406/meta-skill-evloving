# Segmented Control

A toggle component for switching between mutually exclusive options, available in icon and text variants.

## Contents

- [Props](#props)
- [Container Specifications](#container-specifications)
- [Size Specifications](#size-specifications)
- [Button States](#button-states)
- [CSS Implementation](#css-implementation)
- [Usage Guidelines](#usage-guidelines)

## Props

| Prop     | Values                              |
| -------- | ----------------------------------- |
| `type`   | `icon`, `text`                      |
| `amount` | `two`, `three`, `four`              |
| `size`   | `xs` (24px), `s` (28px), `m` (32px) |
| `active` | `1`, `2`, `3`, `4`                  |

## Container Specifications

| Property      | Value                       |
| ------------- | --------------------------- |
| Background    | `neutral-100` (#f7f8fa)     |
| Border        | 1px `neutral-200` (#f0f1f5) |
| Border radius | 5px                         |
| Padding       | 2px                         |
| Gap           | 2px (between buttons)       |

## Size Specifications

### Icon Type

| Size     | Container Height | Button Height | Button Width | Icon Size |
| -------- | ---------------- | ------------- | ------------ | --------- |
| M (32px) | 32px             | 28px          | 32px         | 24px      |

### Text Type

| Size      | Container Height | Button Height | Padding X | Font Size | Line Height |
| --------- | ---------------- | ------------- | --------- | --------- | ----------- |
| XS (24px) | 24px             | 20px          | 6px       | 12px      | 18px        |
| S (28px)  | 28px             | 24px          | 8px       | 14px      | 20px        |

## Button States

**Note:** Unlike other interactive components, segmented controls have only two states: Active and Inactive. There are no hover, pressed, or focus states.

### Active Button

| Property      | Value                                   |
| ------------- | --------------------------------------- |
| Background    | `neutral-50` (#fdfdfe)                  |
| Border radius | 3px                                     |
| Shadow        | `0px 1px 4px 0px rgba(14, 18, 23, 0.2)` |
| Text color    | `neutral-800` (#0e1017)                 |
| Icon color    | `neutral-800` (#0e1017)                 |

### Inactive Button

| Property      | Value                   |
| ------------- | ----------------------- |
| Background    | transparent             |
| Border radius | 4px                     |
| Shadow        | none                    |
| Text color    | `neutral-500` (#68738d) |
| Icon color    | `neutral-600` (#414b62) |

## Typography

- Font family: Inter
- Font weight: Medium (500)
- Text alignment: center
- Min width: 20px

## CSS Implementation

```css
/* Container */
.segmented-control {
  display: flex;
  align-items: center;
  gap: 0;
  padding: 2px;
  background: var(--neutral-100);
  border: 1px solid var(--neutral-200);
  border-radius: 5px;
}

/* Buttons wrapper */
.segmented-control__buttons {
  display: flex;
  align-items: center;
  gap: 2px;
}

/* Base button */
.segmented-control__button {
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition:
    background 0.15s ease,
    box-shadow 0.15s ease;
}

/* Active button */
.segmented-control__button--active {
  background: var(--neutral-50);
  border-radius: 3px;
  box-shadow: 0px 1px 4px 0px rgba(14, 18, 23, 0.2);
}

/* Icon button - M size */
.segmented-control__button--icon-m {
  width: 32px;
  height: 28px;
}

.segmented-control__button--icon-m svg {
  width: 24px;
  height: 24px;
}

/* Text button - XS size */
.segmented-control__button--text-xs {
  height: 20px;
  padding: 0 6px;
  min-width: 20px;
  font-family: "Inter", sans-serif;
  font-size: 12px;
  font-weight: 500;
  line-height: 18px;
}

/* Text button - S size */
.segmented-control__button--text-s {
  height: 24px;
  padding: 0 8px;
  min-width: 20px;
  font-family: "Inter", sans-serif;
  font-size: 14px;
  font-weight: 500;
  line-height: 20px;
}

/* Inactive text color */
.segmented-control__button:not(.segmented-control__button--active) {
  color: var(--neutral-500);
}

/* Inactive icon color */
.segmented-control__button:not(.segmented-control__button--active) svg {
  color: var(--neutral-600);
}

/* Active text/icon color */
.segmented-control__button--active {
  color: var(--neutral-800);
}

.segmented-control__button--active svg {
  color: var(--neutral-800);
}
```

## CSS Custom Properties

```css
:root {
  /* Segmented control container */
  --segmented-control-bg: var(--neutral-100);
  --segmented-control-border: var(--neutral-200);
  --segmented-control-radius: 5px;
  --segmented-control-padding: 2px;
  --segmented-control-gap: 2px;

  /* Active button */
  --segmented-control-active-bg: var(--neutral-50);
  --segmented-control-active-radius: 3px;
  --segmented-control-active-shadow: 0px 1px 4px 0px rgba(14, 18, 23, 0.2);
  --segmented-control-active-color: var(--neutral-800);

  /* Inactive button */
  --segmented-control-inactive-radius: 4px;
  --segmented-control-inactive-color: var(--neutral-500);
  --segmented-control-inactive-icon-color: var(--neutral-600);

  /* Sizes - Icon M */
  --segmented-control-icon-m-width: 32px;
  --segmented-control-icon-m-height: 28px;
  --segmented-control-icon-m-icon: 24px;

  /* Sizes - Text XS */
  --segmented-control-text-xs-height: 20px;
  --segmented-control-text-xs-px: 6px;
  --segmented-control-text-xs-font: 12px;
  --segmented-control-text-xs-lh: 18px;

  /* Sizes - Text S */
  --segmented-control-text-s-height: 24px;
  --segmented-control-text-s-px: 8px;
  --segmented-control-text-s-font: 14px;
  --segmented-control-text-s-lh: 20px;
}
```

## Usage Guidelines

1. **Type selection**:
   - **Icon** - Use for switching between view modes (e.g., grid/list, table/chart)
   - **Text** - Use for time ranges, categories, or labeled options

2. **Amount**:
   - **Two** - Binary choices (e.g., On/Off, Grid/List)
   - **Three** - Common for time ranges (e.g., 1D/1W/1M)
   - **Four** - Extended options (e.g., 1D/1W/1M/1Y)

3. **Size selection**:
   - **XS (24px)** - Compact UI, embedded in headers
   - **S (28px)** - Default for most use cases
   - **M (32px)** - Icon variants, more prominent controls

4. **Active state**:
   - Only one option can be active at a time
   - Active button has elevated appearance (shadow + white background)
   - Inactive buttons remain flat and muted
   - **No hover/focus states** - transition happens only on click/selection

5. **Accessibility**:
   - Use `role="group"` on container with `aria-label`
   - Use `role="radio"` on buttons with `aria-checked`
   - Ensure keyboard navigation (arrow keys to move, Enter/Space to select)

6. **Common patterns**:
   - View switchers: Grid | List | Table
   - Time filters: 1D | 1W | 1M | 1Y
   - Data views: Chart | Table | Raw
