# Accessibility Guidelines

Component-specific accessibility prop guidance. Use this to determine which props to expose in component type definitions.

## Core Principle

**Only expose props users commonly need.** Other HTML attributes (data-*, aria-*, events) still work via `{...others}` spread but don't clutter TypeScript autocomplete.

---

## Always Include (All Components)

These props should be in **every** component type definition:

```tsx
{
  children?: JSX.Element;
  class?: string;
}
```

---

## Badge

**Purpose:** Labels for status, counts, or categories

### Recommended Props

```tsx
{
  /** Semantic role for the badge. Use "status" for live updates, "note" for static labels. */
  role?: "status" | "note" | "mark";

  /** Accessible label for screen readers when badge content isn't descriptive */
  "aria-label"?: string;

  /** Hide badge from screen readers when purely decorative */
  "aria-hidden"?: boolean;
}
```

### When to Use Each

- **`role="status"`** - Live updates (notification counts, online status)
  - Example: Badge showing "3" new messages
- **`role="note"`** - Static labels (categories, tags)
  - Example: Badge showing "Admin" user role
- **`role="mark"`** - Highlighting text
  - Example: Badge highlighting a search term

- **`aria-label`** - When badge content isn't self-explanatory
  - Example: Badge with "5" → `aria-label="5 unread messages"`
  - Example: Badge with icon → `aria-label="Premium user"`

- **`aria-hidden="true"`** - Purely decorative badges
  - Example: Visual-only indicator when text already explains the status

---

## Button

**Purpose:** Interactive button element

### Recommended Props

```tsx
{
  /** Button type - always specify to prevent accidental form submission */
  type?: "button" | "submit" | "reset";

  /** Accessible label for icon-only buttons (REQUIRED when no text content) */
  "aria-label"?: string;

  /** Indicates toggle button state (for buttons that can be pressed/unpressed) */
  "aria-pressed"?: boolean;

  /** Indicates if button controls expandable content (for menu buttons, accordions) */
  "aria-expanded"?: boolean;

  /** Disables button interaction (automatically sets aria-disabled) */
  disabled?: boolean;
}
```

### Common Events

Include in components that need them: `onClick`, `onFocus`, `onBlur`

### When to Use Each

- **`type`** - Always specify!
  - `"button"` - Default for most buttons (prevents form submission)
  - `"submit"` - Form submit buttons
  - `"reset"` - Form reset buttons

- **`aria-label`** - Icon-only buttons
  - Example: `<Button aria-label="Close">×</Button>`

- **`aria-pressed`** - Toggle buttons
  - Example: Bold button in editor (`aria-pressed={isBold}`)

- **`aria-expanded`** - Buttons that show/hide content
  - Example: Dropdown menu button

---

## Link

**Purpose:** Navigation link

### Recommended Props

```tsx
{
  /** Link destination (REQUIRED) */
  href?: string;

  /** Link target - use "_blank" for external links */
  target?: "_blank" | "_self" | "_parent" | "_top";

  /** Link relationship - use "noopener noreferrer" with target="_blank" */
  rel?: string;

  /** Accessible label when link text isn't descriptive */
  "aria-label"?: string;
}
```

### Common Events

`onClick`

### When to Use Each

- **`href`** - Always include for real links
- **`target="_blank"`** - External links, downloads
  - Always pair with `rel="noopener noreferrer"` for security
- **`aria-label`** - Non-descriptive link text
  - Example: "Read more" → Add `aria-label="Read more about pricing"`

---

## Input (Text Field)

**Purpose:** Text input field

### Recommended Props

```tsx
{
  /** Input type - choose appropriate type for validation */
  type?: "text" | "email" | "password" | "number" | "tel" | "url" | "search";

  /** Label when no visible label element (REQUIRED if no <label>) */
  "aria-label"?: string;

  /** Indicates required field (use with required attribute) */
  "aria-required"?: boolean;

  /** Indicates validation error (set to true when field has error) */
  "aria-invalid"?: boolean;

  /** ID of error/help text element */
  "aria-describedby"?: string;

  /** Disables input (use sparingly - prefer readonly) */
  disabled?: boolean;

  /** Makes input read-only (better than disabled for visible but unchangeable fields) */
  readonly?: boolean;
}
```

### Common Events

`onInput`, `onChange`, `onFocus`, `onBlur`

### When to Use Each

- **`type`** - Use semantic types (e.g., `"email"` for validation, `"tel"` for phone keyboard)

- **`aria-label`** vs `<label>` - Prefer visible `<label>`

- **`aria-required`** - Always pair with `required` attribute: `<input required aria-required={true} />`

- **`aria-invalid` + `aria-describedby`** - Link to error messages
  Example: `aria-invalid={hasError} aria-describedby="error-id"`

- **`readonly` vs `disabled`** - Use `readonly` for visible but unchangeable; `disabled` grays out completely

---

## Card

**Purpose:** Container for content

### Recommended Props

```tsx
{
  /** Semantic role for card */
  role?: "article" | "region" | "group";

  /** Label for card when role is "region" (REQUIRED with role="region") */
  "aria-label"?: string;
}
```

### When to Use Each

- **`role="article"`** - Standalone content (blog post preview, product card)
- **`role="region"`** - Major sections (dashboard sections, panels)
  - Must include `aria-label` to identify the region
- **`role="group"`** - Grouped items (list of related items)

---

## Alert

**Purpose:** Alert or notification message

### Recommended Props

```tsx
{
  /** Alert role - determines announcement behavior */
  role?: "alert" | "status";

  /** Screen reader announcement priority */
  "aria-live"?: "polite" | "assertive";
}
```

### When to Use Each

- **`role="alert"`** - Important messages (errors, warnings). Auto `aria-live="assertive"`

- **`role="status"`** - Informational updates (e.g., "Changes saved"). Auto `aria-live="polite"`

- **`aria-live`** - Custom timing: `"assertive"` interrupts, `"polite"` waits

---

## Modal (Dialog)

**Purpose:** Modal dialog

### Recommended Props

```tsx
{
  /** Modal role - determines behavior */
  role?: "dialog" | "alertdialog";

  /** Indicates modal behavior (should be true for modals) */
  "aria-modal"?: boolean;

  /** ID of modal title element */
  "aria-labelledby"?: string;

  /** ID of modal description element */
  "aria-describedby"?: string;
}
```

### When to Use Each

- **`role="dialog"`** - Standard modals (forms, details)
- **`role="alertdialog"`** - Confirmation modals (delete confirmations, destructive actions)

- **`aria-modal={true}`** - Required for proper modal behavior

- **`aria-labelledby`** - Link to modal heading ID

- **`aria-describedby`** - Link to modal description ID

---

## Icon

**Purpose:** Icon element

### Recommended Props

```tsx
{
  /** Hide decorative icons from screen readers (use for icons next to text) */
  "aria-hidden"?: boolean;

  /** Label for standalone icons (REQUIRED for icons without adjacent text) */
  "aria-label"?: string;

  /** Image role for semantic icons (use with aria-label) */
  role?: "img";
}
```

### When to Use Each

- **Decorative icon (next to text)** - Use `aria-hidden="true"`

- **Standalone icon (no text)** - Use `role="img"` + `aria-label`

---

## General Guidance

### Interactive Components

**Components:** Button, Link, Toggle Button, Menu Items

**Common Events:** `onClick`, `onFocus`, `onBlur`, `onKeyDown`

**Common Props:** `disabled`, `aria-label`

### Form Components

**Components:** TextField, Checkbox, Radio Group, Select, Switch, Slider

**Common Events:** `onInput`, `onChange`, `onFocus`, `onBlur`

**Common Props:**
- State: `disabled`, `readonly`, `required`
- Validation: `aria-required`, `aria-invalid`, `aria-describedby`

---

## Best Practices

### ✅ DO

1. **Expose commonly-used accessibility props** in type definitions
2. **Add JSDoc comments** explaining when/how to use each prop
3. **Provide examples** in comments for non-obvious props
4. **Use semantic HTML** when possible (button, not div with onClick)
5. **Test with keyboard navigation** - Tab, Enter, Escape, Arrow keys

### ❌ DON'T

1. **Don't expose every possible ARIA attribute** - keeps autocomplete clean
2. **Don't forget `{...others}` spread** - allows any HTML attribute
3. **Don't use `aria-label` when visible text works** - prefer visible labels
4. **Don't disable without good reason** - prefer readonly
5. **Don't forget focus indicators** - use `focus-visible:outline-*`

---

## Type Definition Pattern

```tsx
export type ComponentProps = {
  // ✅ Always include
  children?: JSX.Element;
  class?: string;

  // ✅ Expose common props with guidance
  /** Accessible label for screen readers when content isn't descriptive */
  "aria-label"?: string;

  /** Disables interaction */
  disabled?: boolean;

  // ✅ Component-specific props
  role?: "status" | "note";

  // ✅ Include variant types
} & VariantProps<typeof componentVariants>;

// ❌ DON'T extend JSX.HTMLAttributes - keeps autocomplete clean
// ✅ Props still work via {...others} spread!
```

---

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [Kobalte Documentation](https://kobalte.dev/)
