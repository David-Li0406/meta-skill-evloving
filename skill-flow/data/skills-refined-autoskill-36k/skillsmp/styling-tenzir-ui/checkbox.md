# Checkbox

Square selection control for multiple choice options.

## Props

| Prop      | Values                                  |
| --------- | --------------------------------------- |
| `state`   | `default`, `hover`, `focus`, `disabled` |
| `checked` | `true`, `false`                         |

## Size Specifications

| Property      | Value |
| ------------- | ----- |
| Size          | 16px  |
| Border radius | 5px   |
| Border width  | 1px   |
| Checkmark     | ~7px  |

## Unchecked State Specifications

| State    | Background              | Border                  | Ring                        |
| -------- | ----------------------- | ----------------------- | --------------------------- |
| Default  | `neutral-50` (#fdfdfe)  | `neutral-300` (#ced3de) | none                        |
| Hover    | `neutral-100` (#f7f8fa) | `neutral-300` (#ced3de) | none                        |
| Focus    | `neutral-50` (#fdfdfe)  | `neutral-300` (#ced3de) | 2px `primary-200` (#e0eaff) |
| Disabled | `neutral-100` (#f7f8fa) | `neutral-250` (#e3e6ed) | none                        |

## Checked State Specifications

| State    | Background              | Border                      | Ring | Checkmark              |
| -------- | ----------------------- | --------------------------- | ---- | ---------------------- |
| Default  | `primary-500` (#0a54ff) | none                        | none | `neutral-50` (#fdfdfe) |
| Hover    | `primary-600` (#0043e0) | none                        | none | `neutral-50` (#fdfdfe) |
| Focus    | `primary-500` (#0a54ff) | 2px `primary-300` (#adc6ff) | none | `neutral-50` (#fdfdfe) |
| Disabled | `neutral-300` (#ced3de) | none                        | none | `neutral-50` (#fdfdfe) |

## CSS Implementation

```css
/* Checkbox Base */
.checkbox {
  position: relative;
  width: 16px;
  height: 16px;
  border-radius: 5px;
  cursor: pointer;
}

/* Unchecked - Default */
.checkbox--unchecked {
  background: var(--neutral-50);
  border: 1px solid var(--neutral-300);
}

/* Unchecked - Hover */
.checkbox--unchecked:hover {
  background: var(--neutral-100);
}

/* Unchecked - Focus */
.checkbox--unchecked:focus-visible {
  background: var(--neutral-50);
  box-shadow: 0 0 0 2px var(--primary-200);
  outline: none;
}

/* Unchecked - Disabled */
.checkbox--unchecked:disabled {
  background: var(--neutral-100);
  border-color: var(--neutral-250);
  cursor: not-allowed;
}

/* Checked - Default */
.checkbox--checked {
  background: var(--primary-500);
  border: none;
}

/* Checked - Hover */
.checkbox--checked:hover {
  background: var(--primary-600);
}

/* Checked - Focus */
.checkbox--checked:focus-visible {
  background: var(--primary-500);
  border: 2px solid var(--primary-300);
  outline: none;
}

/* Checked - Disabled */
.checkbox--checked:disabled {
  background: var(--neutral-300);
  cursor: not-allowed;
}

/* Checkmark icon */
.checkbox__checkmark {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--neutral-50);
}

.checkbox__checkmark svg {
  width: 100%;
  height: 100%;
}
```

## CSS Custom Properties

```css
:root {
  /* Checkbox */
  --checkbox-size: 16px;
  --checkbox-radius: 5px;

  /* Checkbox unchecked */
  --checkbox-unchecked-bg: var(--neutral-50);
  --checkbox-unchecked-bg-hover: var(--neutral-100);
  --checkbox-unchecked-border: var(--neutral-300);
  --checkbox-unchecked-border-disabled: var(--neutral-250);

  /* Checkbox checked */
  --checkbox-checked-bg: var(--primary-500);
  --checkbox-checked-bg-hover: var(--primary-600);
  --checkbox-checked-bg-disabled: var(--neutral-300);
  --checkbox-checked-focus-border: var(--primary-300);
  --checkbox-checkmark: var(--neutral-50);

  /* Focus ring */
  --checkbox-focus-ring: var(--primary-200);
}
```

## Usage Guidelines

1. **When to use checkboxes**:
   - Multiple selections from a list
   - Binary yes/no choices
   - Terms and conditions acceptance

2. **Labeling**:
   - Always pair with a visible label
   - Label should be clickable to toggle state
   - Keep labels concise

3. **Grouping**:
   - Group related checkboxes vertically
   - Use fieldset and legend for groups
   - Consider "Select all" for long lists

4. **Accessibility**:
   - Use native `<input type="checkbox">` when possible
   - Include `aria-checked` for custom implementations
   - Ensure focus is visible (2px primary-200 ring)
   - Support keyboard activation (Space)
