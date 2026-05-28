# Search Input

Specialized input for search functionality with optional search icon and clear button.

## Props

| Prop    | Values                                 |
| ------- | -------------------------------------- |
| `state` | `default`, `filled`, `hover`, `active` |
| `icon`  | `true`, `false`                        |

## Size Specifications

| Property      | Value |
| ------------- | ----- |
| Height        | 32px  |
| Padding X     | 8px   |
| Padding Y     | 6px   |
| Border radius | 5px   |
| Icon size     | 20px  |
| Gap           | 8px   |

## State Specifications

| State   | Border Color            | Text Color              | Ring                        |
| ------- | ----------------------- | ----------------------- | --------------------------- |
| Default | `neutral-200` (#f0f1f5) | `neutral-500` (#68738d) | none                        |
| Filled  | `neutral-200` (#f0f1f5) | `neutral-800` (#0e1017) | none                        |
| Hover   | `neutral-300` (#ced3de) | `neutral-400` (#959db1) | none                        |
| Active  | `primary-500` (#0a54ff) | `neutral-800` (#0e1017) | 3px `primary-200` (#e0eaff) |

## Icon Behavior

| State   | Search Icon | Clear Icon |
| ------- | ----------- | ---------- |
| Default | Optional    | Hidden     |
| Filled  | Optional    | Visible    |
| Hover   | Optional    | Hidden     |
| Active  | Optional    | Visible    |

## CSS Implementation

```css
/* Search Input Base */
.search-input {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 32px;
  padding: 6px 8px;
  background: var(--neutral-100);
  border: 1px solid var(--neutral-200);
  border-radius: 5px;
  font-family: "Inter", sans-serif;
  font-size: 14px;
  font-weight: 400;
  line-height: 20px;
  color: var(--neutral-800);
}

/* Icons */
.search-input__icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  color: var(--neutral-800);
}

/* Input text */
.search-input__text {
  flex: 1;
  min-width: 0;
  background: transparent;
  border: none;
  outline: none;
  font: inherit;
  color: inherit;
}

.search-input__text::placeholder {
  color: var(--neutral-500);
}

/* Clear button */
.search-input__clear {
  display: none;
  width: 20px;
  height: 20px;
  padding: 0;
  background: transparent;
  border: none;
  cursor: pointer;
  color: var(--neutral-800);
}

.search-input--filled .search-input__clear,
.search-input--active .search-input__clear {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Hover */
.search-input:hover {
  border-color: var(--neutral-300);
}

.search-input:hover .search-input__text::placeholder {
  color: var(--neutral-400);
}

/* Active/Focus */
.search-input:focus-within {
  border-color: var(--primary-500);
  box-shadow: 0 0 0 3px var(--primary-200);
}
```

## CSS Custom Properties

```css
:root {
  /* Search input */
  --search-height: 32px;
  --search-padding: 8px;
  --search-radius: 5px;
  --search-gap: 8px;
  --search-icon-size: 20px;

  /* Search colors */
  --search-bg: var(--neutral-100);
  --search-border: var(--neutral-200);
  --search-border-hover: var(--neutral-300);
  --search-border-focus: var(--primary-500);
  --search-focus-ring: var(--primary-200);
}
```

## Usage Guidelines

1. **Icon placement**:
   - Search icon on left (optional) - helps users identify search field
   - Clear button on right - appears when input has value

2. **Search icon**:
   - Include when search field is not obviously identifiable
   - Can omit in search-focused contexts (e.g., search page)

3. **Clear button**:
   - Only show when input has content
   - Clears input and typically refocuses

4. **Placeholder text**:
   - Use "Search..." as default
   - Can be more specific: "Search users...", "Search files..."

5. **Accessibility**:
   - Include `role="search"` on containing element
   - Use `aria-label` if no visible label
   - Clear button needs accessible name
