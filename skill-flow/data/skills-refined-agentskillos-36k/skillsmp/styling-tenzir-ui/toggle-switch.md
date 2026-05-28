# Toggle Switch

Binary switch control for on/off states.

## Props

| Prop     | Values                                  |
| -------- | --------------------------------------- |
| `state`  | `default`, `hover`, `focus`, `disabled` |
| `active` | `true`, `false`                         |

## Size Specifications

| Property      | Value |
| ------------- | ----- |
| Width         | 32px  |
| Height        | 20px  |
| Border radius | 35px  |
| Knob size     | 16px  |
| Knob inset    | 2px   |

## Inactive State Specifications

| State    | Background              | Ring                        |
| -------- | ----------------------- | --------------------------- |
| Default  | `neutral-300` (#ced3de) | none                        |
| Hover    | `neutral-400` (#959db1) | none                        |
| Focus    | `neutral-300` (#ced3de) | 2px `primary-200` (#e0eaff) |
| Disabled | `neutral-200` (#f0f1f5) | none                        |

## Active State Specifications

| State    | Background              | Border                      | Ring |
| -------- | ----------------------- | --------------------------- | ---- |
| Default  | `primary-500` (#0a54ff) | none                        | none |
| Hover    | `primary-600` (#0043e0) | none                        | none |
| Focus    | `primary-500` (#0a54ff) | 2px `primary-300` (#adc6ff) | none |
| Disabled | `neutral-300` (#ced3de) | none                        | none |

## Knob Specifications

| Property | Value                  |
| -------- | ---------------------- |
| Size     | 16px                   |
| Color    | `neutral-50` (#fdfdfe) |
| Shape    | Circle                 |
| Position | 2px from edge          |

## Knob Position

| State    | Left Position |
| -------- | ------------- |
| Inactive | 2px           |
| Active   | 14px (right)  |

## CSS Implementation

```css
/* Toggle Switch Base */
.toggle {
  position: relative;
  width: 32px;
  height: 20px;
  border-radius: 35px;
  cursor: pointer;
  transition: background 0.2s ease;
}

/* Inactive - Default */
.toggle--inactive {
  background: var(--neutral-300);
}

/* Inactive - Hover */
.toggle--inactive:hover {
  background: var(--neutral-400);
}

/* Inactive - Focus */
.toggle--inactive:focus-visible {
  background: var(--neutral-300);
  border-radius: 45px;
  box-shadow: 0 0 0 2px var(--primary-200);
  outline: none;
}

/* Inactive - Disabled */
.toggle--inactive:disabled {
  background: var(--neutral-200);
  cursor: not-allowed;
}

/* Active - Default */
.toggle--active {
  background: var(--primary-500);
}

/* Active - Hover */
.toggle--active:hover {
  background: var(--primary-600);
}

/* Active - Focus */
.toggle--active:focus-visible {
  background: var(--primary-500);
  border: 2px solid var(--primary-300);
  outline: none;
}

/* Active - Disabled */
.toggle--active:disabled {
  background: var(--neutral-300);
  cursor: not-allowed;
}

/* Knob */
.toggle__knob {
  position: absolute;
  top: 2px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--neutral-50);
  transition: left 0.2s ease;
}

/* Knob positions */
.toggle--inactive .toggle__knob {
  left: 2px;
}

.toggle--active .toggle__knob {
  left: 14px;
}
```

## CSS Custom Properties

```css
:root {
  /* Toggle switch */
  --toggle-width: 32px;
  --toggle-height: 20px;
  --toggle-radius: 35px;
  --toggle-knob-size: 16px;
  --toggle-knob-inset: 2px;

  /* Toggle inactive */
  --toggle-inactive-bg: var(--neutral-300);
  --toggle-inactive-bg-hover: var(--neutral-400);
  --toggle-inactive-bg-disabled: var(--neutral-200);

  /* Toggle active */
  --toggle-active-bg: var(--primary-500);
  --toggle-active-bg-hover: var(--primary-600);
  --toggle-active-bg-disabled: var(--neutral-300);
  --toggle-active-focus-border: var(--primary-300);

  /* Knob */
  --toggle-knob-color: var(--neutral-50);

  /* Focus ring */
  --toggle-focus-ring: var(--primary-200);
}
```

## Usage Guidelines

1. **When to use toggles**:
   - Immediate on/off settings
   - Binary choices that take effect immediately
   - Settings that don't require form submission

2. **When to use checkbox instead**:
   - Form fields that require submission
   - Multiple selections
   - Yes/no questions in forms

3. **Labeling**:
   - Place label to the left or right of toggle
   - Label should describe the "on" state
   - Consider showing current state text (On/Off)

4. **Behavior**:
   - Changes should take effect immediately
   - Consider showing loading state for async changes
   - Animate the knob transition (0.2s)

5. **Accessibility**:
   - Use `role="switch"` and `aria-checked`
   - Support keyboard activation (Space)
   - Ensure visible focus state
   - Consider announcing state changes to screen readers
