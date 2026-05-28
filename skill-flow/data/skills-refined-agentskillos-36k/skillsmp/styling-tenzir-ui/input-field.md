# Input Field

Text input component with optional title, description, and various states.

## Contents

- [Props](#props)
- [Size Specifications](#size-specifications)
- [Base Styling](#base-styling)
- [State Specifications](#state-specifications)
- [Title Specifications](#title-specifications)
- [CSS Implementation](#css-implementation)
- [Usage Guidelines](#usage-guidelines)

## Props

| Prop          | Values                                                      |
| ------------- | ----------------------------------------------------------- |
| `state`       | `default`, `filled`, `hover`, `active`, `error`, `disabled` |
| `size`        | `m` (32px), `l` (36px)                                      |
| `title`       | `none`, `m`, `s`                                            |
| `description` | `true`, `false`                                             |
| `itemRight`   | `true`, `false` (icon on right side)                        |
| `type`        | `input`, `dropdown`                                         |

## Size Specifications

| Size | Height | Padding X | Padding Y | With Right Item PR |
| ---- | ------ | --------- | --------- | ------------------ |
| M    | 32px   | 12px      | 6px       | 8px                |
| L    | 36px   | 12px      | 8px       | 8px                |

## Base Styling

| Property      | Value                   |
| ------------- | ----------------------- |
| Background    | `neutral-100` (#f7f8fa) |
| Border radius | 5px                     |
| Font family   | Inter                   |
| Font size     | 14px                    |
| Font weight   | Regular (400)           |
| Line height   | 20px                    |
| Gap (items)   | 4px                     |

## State Specifications

| State    | Border Color            | Text Color              | Ring                        |
| -------- | ----------------------- | ----------------------- | --------------------------- |
| Default  | `neutral-200` (#f0f1f5) | `neutral-500` (#68738d) | none                        |
| Filled   | `neutral-200` (#f0f1f5) | `neutral-800` (#0e1017) | none                        |
| Hover    | `neutral-250` (#e3e6ed) | `neutral-500` (#68738d) | none                        |
| Active   | `primary-500` (#0a54ff) | `neutral-800` (#0e1017) | 3px `primary-200` (#e0eaff) |
| Error    | `red-500` (#ff0a33)     | `neutral-800` (#0e1017) | none                        |
| Disabled | `neutral-200` (#f0f1f5) | `neutral-300` (#ced3de) | none                        |

## Title Specifications

| Title Size | Font Size | Font Weight  | Line Height | Color                   |
| ---------- | --------- | ------------ | ----------- | ----------------------- |
| M          | 14px      | Medium (500) | 20px        | `neutral-800` (#0e1017) |
| S          | 10px      | Medium (500) | 14px        | `neutral-500` (#68738d) |

## Description Specifications

| Property    | Value                   |
| ----------- | ----------------------- |
| Font size   | 12px                    |
| Font weight | Regular (400)           |
| Line height | 18px                    |
| Color       | `neutral-600` (#414b62) |

## Error Message Specifications

| Property    | Value                   |
| ----------- | ----------------------- |
| Font size   | 12px                    |
| Font weight | Regular (400)           |
| Line height | 18px                    |
| Color       | `red-600` (#e00025)     |
| Icon size   | 16px                    |
| Icon color  | `red-600` (#e00025)     |
| Gap         | 4px (between icon/text) |
| Margin top  | 2px                     |

## CSS Implementation

```css
/* Input Field Container */
.input-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

/* Title + Description wrapper */
.input-field__header {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

/* Title - Size M */
.input-field__title--m {
  font-family: "Inter", sans-serif;
  font-size: 14px;
  font-weight: 500;
  line-height: 20px;
  color: var(--neutral-800);
}

/* Title - Size S */
.input-field__title--s {
  font-family: "Inter", sans-serif;
  font-size: 10px;
  font-weight: 500;
  line-height: 14px;
  color: var(--neutral-500);
}

/* Description */
.input-field__description {
  font-family: "Inter", sans-serif;
  font-size: 12px;
  font-weight: 400;
  line-height: 18px;
  color: var(--neutral-600);
}

/* Input Base */
.input-field__input {
  display: flex;
  align-items: center;
  gap: 4px;
  width: 100%;
  background: var(--neutral-100);
  border: 1px solid var(--neutral-200);
  border-radius: 5px;
  font-family: "Inter", sans-serif;
  font-size: 14px;
  font-weight: 400;
  line-height: 20px;
  color: var(--neutral-800);
  overflow: hidden;
}

/* Size M */
.input-field__input--m {
  height: 32px;
  padding: 6px 12px;
}

.input-field__input--m.input-field__input--has-right {
  padding-right: 8px;
}

/* Size L */
.input-field__input--l {
  height: 36px;
  padding: 8px 12px;
}

.input-field__input--l.input-field__input--has-right {
  padding-right: 8px;
}

/* Placeholder */
.input-field__input::placeholder {
  color: var(--neutral-500);
}

/* Hover */
.input-field__input:hover {
  border-color: var(--neutral-250);
}

/* Active/Focus */
.input-field__input:focus {
  border-color: var(--primary-500);
  box-shadow: 0 0 0 3px var(--primary-200);
  outline: none;
}

/* Error */
.input-field__input--error {
  border-color: var(--red-500);
}

.input-field__input--error:focus {
  border-color: var(--red-500);
  box-shadow: none;
}

/* Disabled */
.input-field__input:disabled {
  border-color: var(--neutral-200);
  color: var(--neutral-300);
  cursor: not-allowed;
}

.input-field__input:disabled::placeholder {
  color: var(--neutral-300);
}

/* Right icon */
.input-field__icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  color: var(--neutral-800);
}

/* Error message */
.input-field__error {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 2px;
}

.input-field__error-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  color: var(--red-600);
}

.input-field__error-text {
  font-family: "Inter", sans-serif;
  font-size: 12px;
  font-weight: 400;
  line-height: 18px;
  color: var(--red-600);
}
```

## CSS Custom Properties

```css
:root {
  /* Input field sizes */
  --input-height-m: 32px;
  --input-height-l: 36px;
  --input-padding-x: 12px;
  --input-padding-y-m: 6px;
  --input-padding-y-l: 8px;
  --input-radius: 5px;

  /* Input field colors */
  --input-bg: var(--neutral-100);
  --input-border: var(--neutral-200);
  --input-border-hover: var(--neutral-250);
  --input-border-focus: var(--primary-500);
  --input-border-error: var(--red-500);
  --input-focus-ring: var(--primary-200);

  /* Input field text */
  --input-text: var(--neutral-800);
  --input-placeholder: var(--neutral-500);
  --input-disabled: var(--neutral-300);

  /* Title */
  --input-title-m-size: 14px;
  --input-title-m-lh: 20px;
  --input-title-s-size: 10px;
  --input-title-s-lh: 14px;

  /* Error */
  --input-error-color: var(--red-600);
}
```

## Usage Guidelines

1. **Title selection**:
   - **Size M** - Default for most form fields
   - **Size S** - Compact forms, inline editing

2. **Description**:
   - Use for additional context or instructions
   - Keep concise (one line preferred)

3. **Size selection**:
   - **M (32px)** - Default for most use cases
   - **L (36px)** - Forms with more breathing room

4. **Right icons**:
   - Calendar icon for date inputs
   - Chevron for dropdown triggers
   - Keep icon size at 20px

5. **Error handling**:
   - Show error message below input
   - Include error icon for visibility
   - Error border takes precedence over focus ring

6. **Accessibility**:
   - Always include labels (title)
   - Use `aria-describedby` to link description/error
   - Use `aria-invalid="true"` for error state
