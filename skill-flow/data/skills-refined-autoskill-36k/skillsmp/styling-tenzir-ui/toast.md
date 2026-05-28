# Toast

Notification component for displaying transient messages, confirmations, and errors.

## Props

| Prop          | Values                             |
| ------------- | ---------------------------------- |
| `icon`        | `true`, `false`                    |
| `subtitle`    | `true`, `false`                    |
| `button`      | `true`, `false`                    |
| `progressbar` | `true`, `false`                    |
| `type`        | `Default`, `Error`, `Confirmation` |

## Size Specifications

### Toast Container

| Property      | Value                 |
| ------------- | --------------------- |
| Min height    | 48px                  |
| Padding X     | 16px                  |
| Padding Y     | 12px                  |
| Gap           | 16px                  |
| Border radius | 5px                   |
| Border        | 1px solid neutral-200 |
| Shadow        | shadow-s              |

### Icon

| Property | Value |
| -------- | ----- |
| Size     | 24px  |

### Button

| Property      | Value |
| ------------- | ----- |
| Padding X     | 8px   |
| Padding Y     | 3px   |
| Border radius | 5px   |

### Progress Bar

| Property | Value                   |
| -------- | ----------------------- |
| Height   | 2px                     |
| Position | Absolute, bottom-left   |
| Border   | 1px solid (color below) |

## Typography

### Title

| Property    | Value        |
| ----------- | ------------ |
| Font family | Inter        |
| Font size   | 14px         |
| Font weight | Medium (500) |
| Line height | 20px         |

### Subtitle

| Property    | Value         |
| ----------- | ------------- |
| Font family | Inter         |
| Font size   | 12px          |
| Font weight | Regular (400) |
| Line height | 18px          |

### Button Text

| Property    | Value           |
| ----------- | --------------- |
| Font family | Inter           |
| Font size   | 12px            |
| Font weight | Semi Bold (600) |
| Line height | 18px            |

## Color Specifications

### Container

| Element    | Color                   |
| ---------- | ----------------------- |
| Background | `neutral-50` (#fdfdfe)  |
| Border     | `neutral-200` (#f0f1f5) |

### Text

| Element  | Color                   |
| -------- | ----------------------- |
| Title    | `neutral-800` (#0e1017) |
| Subtitle | `neutral-500` (#68738d) |

### Icon by Type

| Type         | Icon Color            |
| ------------ | --------------------- |
| Default      | `green-600` (#1ab252) |
| Confirmation | (no icon)             |
| Error        | `red-600` (#e00025)   |

### Button

| Element    | Color                   |
| ---------- | ----------------------- |
| Background | `neutral-100` (#f7f8fa) |
| Text       | `neutral-800` (#0e1017) |

### Progress Bar Border

| Type         | Color                   |
| ------------ | ----------------------- |
| Default      | `primary-400` (#477eff) |
| Confirmation | `primary-400` (#477eff) |
| Error        | `red-400` (#ff4766)     |

## CSS Implementation

```css
/* Toast Container */
.toast {
  display: flex;
  align-items: center;
  gap: 16px;
  min-height: 48px;
  padding: 12px 16px;
  background: var(--neutral-50);
  border: 1px solid var(--neutral-200);
  border-radius: 5px;
  box-shadow: var(--shadow-s);
  position: relative;
  overflow: hidden;
}

/* Toast Icon */
.toast__icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.toast__icon--success {
  color: var(--green-600);
}

.toast__icon--error {
  color: var(--red-600);
}

/* Toast Text Container */
.toast__text {
  display: flex;
  flex-direction: column;
  gap: 0;
  max-width: 267px;
}

/* Toast Title */
.toast__title {
  font-family: "Inter", sans-serif;
  font-size: 14px;
  font-weight: 500;
  line-height: 20px;
  color: var(--neutral-800);
  white-space: nowrap;
}

/* Toast Subtitle */
.toast__subtitle {
  font-family: "Inter", sans-serif;
  font-size: 12px;
  font-weight: 400;
  line-height: 18px;
  color: var(--neutral-500);
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}

/* Toast Button */
.toast__button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3px 8px;
  background: var(--neutral-100);
  border: none;
  border-radius: 5px;
  font-family: "Inter", sans-serif;
  font-size: 12px;
  font-weight: 600;
  line-height: 18px;
  color: var(--neutral-800);
  cursor: pointer;
  flex-shrink: 0;
}

/* Toast Progress Bar */
.toast__progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 2px;
  background: #d9d9d9;
  border: 1px solid var(--primary-400);
}

.toast__progress--error {
  border-color: var(--red-400);
}
```

## CSS Custom Properties

```css
:root {
  /* Toast sizing */
  --toast-min-height: 48px;
  --toast-padding-x: 16px;
  --toast-padding-y: 12px;
  --toast-gap: 16px;
  --toast-radius: 5px;
  --toast-icon-size: 24px;

  /* Toast colors */
  --toast-bg: var(--neutral-50);
  --toast-border: var(--neutral-200);
  --toast-title-color: var(--neutral-800);
  --toast-subtitle-color: var(--neutral-500);

  /* Toast button */
  --toast-button-bg: var(--neutral-100);
  --toast-button-padding-x: 8px;
  --toast-button-padding-y: 3px;
  --toast-button-radius: 5px;

  /* Toast progress bar */
  --toast-progress-height: 2px;
  --toast-progress-default: var(--primary-400);
  --toast-progress-error: var(--red-400);
}
```

## Usage Guidelines

1. **Type selection**:
   - **Default** - Success messages, general notifications (green checkmark icon)
   - **Error** - Error messages, failures (red error icon)
   - **Confirmation** - Action confirmations with undo option (no icon)

2. **Content structure**:
   - **Title only** - Brief, single-line messages
   - **Title + Subtitle** - Additional context or details
   - Max subtitle width: ~267px (truncate with ellipsis)

3. **Button usage**:
   - Use for actionable toasts (e.g., "View", "Undo", "Revert")
   - Keep button text short (1-2 words)
   - Button appears after text content

4. **Progress bar**:
   - Use for auto-dismissing toasts
   - Shows remaining time before dismissal
   - Color matches toast type (blue for default/confirmation, red for error)

5. **Icon behavior**:
   - Default type: Green checkmark (state completed)
   - Error type: Red error icon
   - Confirmation type: No icon (relies on button for action)

6. **Positioning**:
   - Typically bottom-right or top-right of viewport
   - Stack multiple toasts vertically with gap
   - Apply shadow-s for elevation

7. **Accessibility**:
   - Use `role="alert"` for important messages
   - Use `role="status"` for non-critical updates
   - Ensure sufficient display time for reading
   - Support keyboard dismissal
