# Tab Bar

Horizontal navigation component for switching between content sections.

## Props

### Tab Bar

| Prop   | Values                                |
| ------ | ------------------------------------- |
| `tabs` | `two`, `three`, `four`, `five`, `six` |

### Tab Bar Tab

| Prop           | Values                                    |
| -------------- | ----------------------------------------- |
| `state`        | `active`, `inactive`, `hover`, `disabled` |
| `notification` | `true`, `false`                           |

### Tab Bar Counter

| Prop    | Values                        |
| ------- | ----------------------------- |
| `state` | `default`, `warning`, `error` |

## Size Specifications

### Tab Bar

| Property | Value |
| -------- | ----- |
| Height   | 48px  |
| Gap      | 4px   |

### Tab Bar Tab

| Property           | Value             |
| ------------------ | ----------------- |
| Height             | 48px              |
| Padding Y          | 8px               |
| Text Padding X     | 8px               |
| Text Padding Y     | 6px               |
| Text Border Radius | 5px               |
| Active Indicator   | 2px bottom border |

### Tab Bar Counter

| Property      | Value |
| ------------- | ----- |
| Min Width     | 14px  |
| Padding       | 2px   |
| Border Radius | 5px   |
| Gap from text | 4px   |

## Typography

### Tab Text

| Property    | Value        |
| ----------- | ------------ |
| Font family | Inter        |
| Font size   | 14px         |
| Font weight | Medium (500) |
| Line height | 20px         |

### Counter Text

| Property    | Value           |
| ----------- | --------------- |
| Font family | Inter           |
| Font size   | 10px            |
| Font weight | Semi Bold (600) |
| Line height | 14px            |
| Alignment   | center          |

## State Specifications

### Tab States

| State    | Text Color              | Background              | Border                             |
| -------- | ----------------------- | ----------------------- | ---------------------------------- |
| Active   | `neutral-800` (#0e1017) | transparent             | 2px bottom `primary-500` (#0a54ff) |
| Inactive | `neutral-500` (#68738d) | transparent             | none                               |
| Hover    | `neutral-700` (#262e40) | `neutral-100` (#f7f8fa) | none                               |
| Disabled | `neutral-300` (#ced3de) | transparent             | none                               |

### Counter States

| State   | Background              | Text Color              |
| ------- | ----------------------- | ----------------------- |
| Default | `neutral-200` (#f0f1f5) | `neutral-500` (#68738d) |
| Hover   | `neutral-250` (#e3e6ed) | `neutral-600` (#414b62) |

## CSS Implementation

```css
/* Tab Bar Container */
.tab-bar {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* Tab Bar Tab */
.tab-bar__tab {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-start;
  height: 48px;
  padding: 8px 0;
}

/* Tab text container */
.tab-bar__text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  padding: 6px 8px;
  border-radius: 5px;
  font-family: "Inter", sans-serif;
  font-size: 14px;
  font-weight: 500;
  line-height: 20px;
  white-space: nowrap;
  cursor: pointer;
}

/* With notification counter */
.tab-bar__text--with-counter {
  gap: 4px;
}

/* Active state */
.tab-bar__tab--active {
  border-bottom: 2px solid var(--primary-500);
}

.tab-bar__tab--active .tab-bar__text {
  color: var(--neutral-800);
}

/* Inactive state */
.tab-bar__tab--inactive .tab-bar__text {
  color: var(--neutral-500);
}

/* Hover state */
.tab-bar__tab--hover .tab-bar__text,
.tab-bar__tab:hover .tab-bar__text {
  background: var(--neutral-100);
  color: var(--neutral-700);
}

/* Disabled state */
.tab-bar__tab--disabled .tab-bar__text {
  color: var(--neutral-300);
  cursor: not-allowed;
}

/* Counter */
.tab-bar__counter {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2px;
  min-width: 14px;
  border-radius: 5px;
  background: var(--neutral-200);
  font-family: "Inter", sans-serif;
  font-size: 10px;
  font-weight: 600;
  line-height: 14px;
  text-align: center;
  color: var(--neutral-500);
}

/* Counter hover state */
.tab-bar__tab:hover .tab-bar__counter {
  background: var(--neutral-250);
  color: var(--neutral-600);
}
```

## CSS Custom Properties

```css
:root {
  /* Tab bar */
  --tab-bar-gap: 4px;
  --tab-bar-height: 48px;

  /* Tab */
  --tab-padding-y: 8px;
  --tab-text-padding-x: 8px;
  --tab-text-padding-y: 6px;
  --tab-text-radius: 5px;

  /* Tab colors */
  --tab-active-color: var(--neutral-800);
  --tab-active-indicator: var(--primary-500);
  --tab-inactive-color: var(--neutral-500);
  --tab-hover-color: var(--neutral-700);
  --tab-hover-bg: var(--neutral-100);
  --tab-disabled-color: var(--neutral-300);

  /* Counter */
  --tab-counter-padding: 2px;
  --tab-counter-radius: 5px;
  --tab-counter-min-width: 14px;
  --tab-counter-bg: var(--neutral-200);
  --tab-counter-bg-hover: var(--neutral-250);
  --tab-counter-color: var(--neutral-500);
  --tab-counter-color-hover: var(--neutral-600);
}
```

## Usage Guidelines

1. **Tab count**:
   - **Two** - Binary choices (e.g., Input/Output)
   - **Three-Four** - Common for main navigation sections
   - **Five-Six** - Use sparingly; consider overflow handling

2. **Active indicator**:
   - 2px bottom border in primary-500 (blue)
   - Only one tab can be active at a time

3. **Notification counter**:
   - Use to show counts (e.g., unread items, results)
   - Keep numbers concise (use abbreviations for large numbers)
   - Counter inherits hover state from parent tab

4. **Behavior**:
   - Tabs should be clickable across their full height
   - Hover state applies to text container only
   - Active state overrides hover styling

5. **Accessibility**:
   - Use `role="tablist"` on container
   - Use `role="tab"` on each tab
   - Use `aria-selected` for active state
   - Use `aria-disabled` for disabled tabs
   - Support keyboard navigation (arrow keys)
