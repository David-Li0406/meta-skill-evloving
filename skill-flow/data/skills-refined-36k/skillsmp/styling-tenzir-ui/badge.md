# Badge

Small uppercase label for status indicators and feature flags.

## Contents

- [Props](#props)
- [Size Specifications](#size-specifications)
- [Typography](#typography)
- [Color Specifications](#color-specifications)
- [CSS Implementation](#css-implementation)
- [CSS Custom Properties](#css-custom-properties)
- [Usage Guidelines](#usage-guidelines)

## Props

| Prop           | Values                                                                            |
| -------------- | --------------------------------------------------------------------------------- |
| `color`        | `blue`, `lightblue`, `purple`, `pink`, `orange`, `yellow`, `red`, `green`, `grey` |
| `transparency` | `true`, `false`                                                                   |

## Size Specifications

| Property      | Value |
| ------------- | ----- |
| Height        | 16px  |
| Padding X     | 4px   |
| Padding Y     | 1px   |
| Border radius | 3px   |
| Border        | 1px   |

## Typography

| Property       | Value           |
| -------------- | --------------- |
| Font family    | Inter           |
| Font size      | 8px             |
| Font weight    | Semi Bold (600) |
| Line height    | 14px            |
| Text transform | uppercase       |
| Letter spacing | 0.4px           |

## Color Specifications

Each color has a solid variant (300-level border) and transparent variant (12% opacity border).

| Color     | Border (solid)            | Border (transparent)     | Text (solid)              | Text (transparent)        |
| --------- | ------------------------- | ------------------------ | ------------------------- | ------------------------- |
| Blue      | `primary-300` (#adc6ff)   | rgba(0, 67, 224, 0.12)   | `primary-500` (#0a54ff)   | `primary-400` (#477eff)   |
| Lightblue | `lightblue-300` (#ade4ff) | rgba(0, 150, 224, 0.12)  | `lightblue-500` (#0aadff) | `lightblue-400` (#47c2ff) |
| Purple    | `purple-300` (#efadff)    | rgba(180, 0, 224, 0.12)  | `purple-500` (#cf0aff)    | `purple-400` (#db47ff)    |
| Pink      | `pink-300` (#ffade1)      | rgba(224, 0, 142, 0.12)  | `pink-500` (#ff0aa5)      | `pink-400` (#ff47bc)      |
| Orange    | `orange-300` (#ffc9ad)    | rgba(224, 75, 0, 0.12)   | `orange-500` (#ff5c0a)    | `orange-400` (#ff8547)    |
| Yellow    | `yellow-300` (#f9e4b4)    | rgba(208, 150, 17, 0.12) | `yellow-500` (#edae1d)    | `yellow-400` (#f1c255)    |
| Red       | `red-300` (#ffadbb)       | rgba(224, 0, 37, 0.12)   | `red-500` (#ff0a33)       | `red-400` (#ff4766)       |
| Green     | `green-300` (#b8f5ce)     | rgba(28, 196, 90, 0.12)  | `green-500` (#29e06c)     | `green-400` (#5ee891)     |
| Grey      | `neutral-300` (#ced3de)   | rgba(65, 75, 98, 0.12)   | `neutral-500` (#68738d)   | `neutral-400` (#959db1)   |

## CSS Implementation

```css
/* Badge Base */
.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 1px 4px;
  border-radius: 3px;
  border: 1px solid;
  font-family: "Inter", sans-serif;
  font-size: 8px;
  font-weight: 600;
  line-height: 14px;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Blue badge */
.badge--blue {
  border-color: var(--primary-300);
  color: var(--primary-500);
}

.badge--blue-transparent {
  border-color: rgba(0, 67, 224, 0.12);
  color: var(--primary-400);
}

/* Lightblue badge */
.badge--lightblue {
  border-color: var(--lightblue-300);
  color: var(--lightblue-500);
}

.badge--lightblue-transparent {
  border-color: rgba(0, 150, 224, 0.12);
  color: var(--lightblue-400);
}

/* Purple badge */
.badge--purple {
  border-color: var(--purple-300);
  color: var(--purple-500);
}

.badge--purple-transparent {
  border-color: rgba(180, 0, 224, 0.12);
  color: var(--purple-400);
}

/* Pink badge */
.badge--pink {
  border-color: var(--pink-300);
  color: var(--pink-500);
}

.badge--pink-transparent {
  border-color: rgba(224, 0, 142, 0.12);
  color: var(--pink-400);
}

/* Orange badge */
.badge--orange {
  border-color: var(--orange-300);
  color: var(--orange-500);
}

.badge--orange-transparent {
  border-color: rgba(224, 75, 0, 0.12);
  color: var(--orange-400);
}

/* Yellow badge */
.badge--yellow {
  border-color: var(--yellow-300);
  color: var(--yellow-500);
}

.badge--yellow-transparent {
  border-color: rgba(208, 150, 17, 0.12);
  color: var(--yellow-400);
}

/* Red badge */
.badge--red {
  border-color: var(--red-300);
  color: var(--red-500);
}

.badge--red-transparent {
  border-color: rgba(224, 0, 37, 0.12);
  color: var(--red-400);
}

/* Green badge */
.badge--green {
  border-color: var(--green-300);
  color: var(--green-500);
}

.badge--green-transparent {
  border-color: rgba(28, 196, 90, 0.12);
  color: var(--green-400);
}

/* Grey badge */
.badge--grey {
  border-color: var(--neutral-300);
  color: var(--neutral-500);
}

.badge--grey-transparent {
  border-color: rgba(65, 75, 98, 0.12);
  color: var(--neutral-400);
}
```

## CSS Custom Properties

```css
:root {
  /* Badge sizing */
  --badge-height: 16px;
  --badge-padding-x: 4px;
  --badge-padding-y: 1px;
  --badge-radius: 3px;

  /* Badge typography */
  --badge-font-size: 8px;
  --badge-font-weight: 600;
  --badge-line-height: 14px;
  --badge-letter-spacing: 0.4px;
}
```

## Usage Guidelines

1. **Common use cases**:
   - **NEW** - Highlight new features
   - **BETA** - Mark experimental features
   - **OR** - Boolean operator indicator
   - **OFF** - Disabled state indicator

2. **Transparency selection**:
   - **Solid border** - More prominent, use for important badges
   - **Transparent border** - Subtle, use inline with other elements

3. **Color selection** (same palette as tags):
   - **Blue** - Primary/informational badges
   - **Lightblue** - Secondary informational
   - **Purple** - Special/unique items
   - **Pink** - Accent/highlight
   - **Orange** - Caution/attention
   - **Yellow** - Warning/pending
   - **Red** - Error/disabled states
   - **Green** - Success/active states
   - **Grey** - Neutral/inactive

4. **Placement**:
   - Typically next to feature names or in headers
   - Keep badges short (1-4 characters ideal)

5. **Accessibility**:
   - Badges are decorative; ensure meaning is also conveyed in context
   - Don't rely solely on color to convey meaning
