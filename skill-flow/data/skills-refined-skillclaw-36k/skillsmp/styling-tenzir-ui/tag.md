# Tag

Colored label component for categorization, filtering, and metadata display.

## Contents

- [Props](#props)
- [Size Specifications](#size-specifications)
- [Typography](#typography)
- [Color Specifications](#color-specifications)
- [Special States](#special-states-no-color-variant-only)
- [CSS Implementation](#css-implementation)
- [Usage Guidelines](#usage-guidelines)

## Props

| Prop      | Values                                                                                    |
| --------- | ----------------------------------------------------------------------------------------- |
| `color`   | `blue`, `lightblue`, `purple`, `pink`, `orange`, `yellow`, `red`, `green`, `grey`, `none` |
| `variant` | `default`, `add`, `remove`                                                                |
| `state`   | `default`, `hover`, `included`, `excluded`                                                |

## Size Specifications

| Property        | Default Variant | Add/Remove Variant |
| --------------- | --------------- | ------------------ |
| Height          | 24px            | 24px               |
| Padding left    | 6px             | 6px                |
| Padding right   | 6px             | 2px                |
| Padding Y       | 3px             | 3px                |
| Border radius   | 5px             | 5px                |
| Border          | 1px             | 1px                |
| Icon size       | -               | 16px               |
| Wrapper padding | 1px             | 1px                |

## Typography

| Property    | Value        |
| ----------- | ------------ |
| Font family | Inter        |
| Font size   | 12px         |
| Font weight | Medium (500) |
| Line height | 16px         |

## Color Specifications

Each color has a 200-level background, transparent border (default), solid 300-level border (hover), and 600-level text.

| Color     | Background                | Border (default)         | Border (hover)            | Text                      |
| --------- | ------------------------- | ------------------------ | ------------------------- | ------------------------- |
| Blue      | `primary-200` (#e0eaff)   | rgba(0, 67, 224, 0.12)   | `primary-300` (#adc6ff)   | `primary-600` (#0043e0)   |
| Lightblue | `lightblue-200` (#e0f5ff) | rgba(0, 150, 224, 0.12)  | `lightblue-300` (#ade4ff) | `lightblue-600` (#0096e0) |
| Purple    | `purple-200` (#f9e0ff)    | rgba(180, 0, 224, 0.12)  | `purple-300` (#efadff)    | `purple-600` (#b400e0)    |
| Pink      | `pink-200` (#ffe0f4)      | rgba(224, 0, 142, 0.12)  | `pink-300` (#ffade1)      | `pink-600` (#e0008e)      |
| Orange    | `orange-200` (#ffebe0)    | rgba(224, 75, 0, 0.12)   | `orange-300` (#ffc9ad)    | `orange-600` (#e04b00)    |
| Yellow    | `yellow-200` (#fef6e1)    | rgba(208, 150, 17, 0.12) | `yellow-300` (#f9e4b4)    | `yellow-600` (#d09611)    |
| Red       | `red-200` (#ffe0e5)       | rgba(224, 0, 37, 0.12)   | `red-300` (#ffadbb)       | `red-600` (#e00025)       |
| Green     | `green-200` (#e4fbec)     | rgba(28, 196, 90, 0.12)  | `green-300` (#b8f5ce)     | `green-600` (#1ab252)     |
| Grey      | `neutral-200` (#f0f1f5)   | rgba(65, 75, 98, 0.12)   | `neutral-300` (#ced3de)   | `neutral-600` (#414b62)   |
| No color  | `neutral-100` (#f7f8fa)   | rgba(65, 75, 98, 0.12)   | `neutral-300` (#ced3de)   | `neutral-600` (#414b62)   |
| None      | `neutral-50` (#fdfdfe)    | `neutral-200` (#f0f1f5)  | -                         | `neutral-400` (#959db1)   |

## Special States (No Color variant only)

| State    | Background              | Border                 | Text                    |
| -------- | ----------------------- | ---------------------- | ----------------------- |
| Included | `primary-200` (#e0eaff) | rgba(0, 67, 224, 0.12) | `primary-500` (#0a54ff) |
| Excluded | `red-200` (#ffe0e5)     | rgba(224, 0, 37, 0.12) | `red-500` (#ff0a33)     |

## CSS Implementation

```css
/* Tag wrapper */
.tag {
  display: inline-flex;
  padding: 1px;
}

/* Tag container */
.tag__container {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3px 6px;
  border-radius: 5px;
  border: 1px solid;
  font-family: "Inter", sans-serif;
  font-size: 12px;
  font-weight: 500;
  line-height: 16px;
  white-space: nowrap;
}

/* With icon (add/remove variants) */
.tag__container--with-icon {
  padding-left: 6px;
  padding-right: 2px;
}

/* Tag icon */
.tag__icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

/* Blue tag */
.tag--blue {
  background: var(--primary-200);
  border-color: rgba(0, 67, 224, 0.12);
  color: var(--primary-600);
}

.tag--blue:hover {
  border-color: var(--primary-300);
}

/* Lightblue tag */
.tag--lightblue {
  background: var(--lightblue-200);
  border-color: rgba(0, 150, 224, 0.12);
  color: var(--lightblue-600);
}

.tag--lightblue:hover {
  border-color: var(--lightblue-300);
}

/* Purple tag */
.tag--purple {
  background: var(--purple-200);
  border-color: rgba(180, 0, 224, 0.12);
  color: var(--purple-600);
}

.tag--purple:hover {
  border-color: var(--purple-300);
}

/* Pink tag */
.tag--pink {
  background: var(--pink-200);
  border-color: rgba(224, 0, 142, 0.12);
  color: var(--pink-600);
}

.tag--pink:hover {
  border-color: var(--pink-300);
}

/* Orange tag */
.tag--orange {
  background: var(--orange-200);
  border-color: rgba(224, 75, 0, 0.12);
  color: var(--orange-600);
}

.tag--orange:hover {
  border-color: var(--orange-300);
}

/* Yellow tag */
.tag--yellow {
  background: var(--yellow-200);
  border-color: rgba(208, 150, 17, 0.12);
  color: var(--yellow-600);
}

.tag--yellow:hover {
  border-color: var(--yellow-300);
}

/* Red tag */
.tag--red {
  background: var(--red-200);
  border-color: rgba(224, 0, 37, 0.12);
  color: var(--red-600);
}

.tag--red:hover {
  border-color: var(--red-300);
}

/* Green tag */
.tag--green {
  background: var(--green-200);
  border-color: rgba(28, 196, 90, 0.12);
  color: var(--green-600);
}

.tag--green:hover {
  border-color: var(--green-300);
}

/* Grey tag */
.tag--grey {
  background: var(--neutral-200);
  border-color: rgba(65, 75, 98, 0.12);
  color: var(--neutral-600);
}

.tag--grey:hover {
  border-color: var(--neutral-300);
}

/* No color tag */
.tag--no-color {
  background: var(--neutral-100);
  border-color: rgba(65, 75, 98, 0.12);
  color: var(--neutral-600);
}

.tag--no-color:hover {
  border-color: var(--neutral-300);
}

/* None tag (placeholder) */
.tag--none {
  background: var(--neutral-50);
  border-color: var(--neutral-200);
  color: var(--neutral-400);
}

/* Included state */
.tag--included {
  background: var(--primary-200);
  border-color: rgba(0, 67, 224, 0.12);
  color: var(--primary-500);
}

/* Excluded state */
.tag--excluded {
  background: var(--red-200);
  border-color: rgba(224, 0, 37, 0.12);
  color: var(--red-500);
}
```

## CSS Custom Properties

```css
:root {
  /* Tag sizing */
  --tag-height: 24px;
  --tag-padding-x: 6px;
  --tag-padding-y: 3px;
  --tag-radius: 5px;
  --tag-icon-size: 16px;

  /* Tag typography */
  --tag-font-size: 12px;
  --tag-font-weight: 500;
  --tag-line-height: 16px;
}
```

## Usage Guidelines

1. **Color selection**:
   - Use colors consistently for categories (e.g., blue for types, green for status)
   - Grey for neutral/uncategorized items
   - None for placeholder "No tag" state

2. **Variant usage**:
   - **Default** - Display-only tag
   - **Add** - Shows + icon on hover for adding tags
   - **Remove** - Shows x icon on hover for removing tags

3. **State usage**:
   - **Default** - Normal display
   - **Hover** - More visible border on interaction
   - **Included** - Filter is active (blue highlight)
   - **Excluded** - Filter is negated (red highlight)

4. **Icon behavior**:
   - Icons only appear on hover for Add/Remove variants
   - Icon color matches text color

5. **Accessibility**:
   - Use `role="button"` for interactive tags
   - Include `aria-label` describing the action
   - For filter tags, use `aria-pressed` to indicate state
