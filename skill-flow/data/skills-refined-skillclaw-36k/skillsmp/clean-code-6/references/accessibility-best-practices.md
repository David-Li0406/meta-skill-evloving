# Accessibility Best Practices (WCAG 2.1 AA)

## Core Principles

- **WCAG 2.1 AA**: Apply across web and mobile with semantic elements and platform-native APIs
- **Perceivable**: Content must be perceivable by all users
- **Operable**: Interface must be operable by all users
- **Understandable**: Content must be understandable
- **Robust**: Content must work with assistive technologies

---

## Color & Contrast

### Contrast Ratios

| Element Type    | Minimum Ratio |
| --------------- | ------------- |
| Normal text     | 4.5:1         |
| Large text      | 3:1           |
| UI components   | 3:1           |
| Focus indicator | 3:1           |

### Don't Rely on Color Alone

Always provide additional indicators:

```tsx
// ❌ Color only
<span className="text-red-500">Error</span>

// ✅ Color + icon + text
<span className="text-red-500 flex items-center gap-1">
  <AlertIcon aria-hidden="true" />
  Error: Invalid email
</span>
```

---

## Semantic HTML

### Use Native Elements

| Instead of                 | Use             |
| -------------------------- | --------------- |
| `<div onClick>`            | `<button>`      |
| `<div role="heading">`     | `<h1>` - `<h6>` |
| `<div role="navigation">`  | `<nav>`         |
| `<div role="main">`        | `<main>`        |
| `<div role="contentinfo">` | `<footer>`      |

### Heading Hierarchy

Use h1-h6 in proper order, never skip levels:

```tsx
// ✅ Correct hierarchy
<h1>Page Title</h1>
  <h2>Section</h2>
    <h3>Subsection</h3>
  <h2>Another Section</h2>

// ❌ Skipped level
<h1>Page Title</h1>
  <h3>Subsection</h3>  // Missing h2
```

---

## ARIA

### When to Use

Use ARIA only when semantic HTML is insufficient:

```tsx
// ✅ Native element - no ARIA needed
<button>Submit</button>

// ✅ ARIA for custom component
<div
  role="button"
  tabIndex={0}
  aria-pressed={isPressed}
  onKeyDown={handleKeyDown}
>
  Toggle
</div>
```

### Common ARIA Patterns

```tsx
// Loading state
<button aria-busy={isLoading} disabled={isLoading}>
  {isLoading ? "Loading..." : "Submit"}
</button>

// Expanded state
<button
  aria-expanded={isOpen}
  aria-controls="menu"
>
  Menu
</button>
<div id="menu" hidden={!isOpen}>
  {/* Menu content */}
</div>

// Live region for dynamic content
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>
```

### Don't Duplicate Implicit Roles

```tsx
// ❌ Redundant
<button role="button">Click</button>
<nav role="navigation">...</nav>

// ✅ Correct
<button>Click</button>
<nav>...</nav>
```

---

## Keyboard Navigation

### All Interactive Elements Must Be Keyboard Accessible

```tsx
// ✅ Keyboard support
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === "Enter" || e.key === " ") {
      handleClick();
    }
  }}
>
  Custom Button
</div>
```

### Focus Indicators

Always show visible focus indicators:

```tsx
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      ringColor: {
        DEFAULT: "hsl(var(--ring))",
      },
    },
  },
};

// Component
<button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2">
  Button
</button>;
```

### Focus Management

Handle focus for modals, dynamic content, and SPAs:

```tsx
function Modal({ isOpen, onClose }) {
  const closeButtonRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      closeButtonRef.current?.focus();
    }
  }, [isOpen]);

  return (
    <dialog open={isOpen}>
      <button ref={closeButtonRef} onClick={onClose}>
        Close
      </button>
      {/* Modal content */}
    </dialog>
  );
}
```

---

## Images

### Alt Text

```tsx
// Meaningful image
<Image
  src="/hero.jpg"
  alt="Team collaborating in a modern office"
/>

// Decorative image
<Image
  src="/decorative-pattern.svg"
  alt=""
  aria-hidden="true"
/>

// React Native
<Image
  source={source}
  accessibilityLabel="Team collaborating"
/>

// Decorative in React Native
<Image
  source={source}
  accessible={false}
/>
```

---

## Forms

### Label Association

```tsx
// Web
<label htmlFor="email">Email</label>
<input id="email" type="email" />

// React Native
<Text nativeID="email-label">Email</Text>
<TextInput
  nativeID="email"
  aria-labelledby="email-label"
  accessibilityLabel="Email"
/>
```

### Required Fields

Mark in text, not just color:

```tsx
<label htmlFor="email">
  Email <span aria-hidden="true">*</span>
  <span className="sr-only">(required)</span>
</label>
```

### Validation Messages

```tsx
<input
  id="email"
  aria-invalid={!!error}
  aria-describedby={error ? "email-error" : undefined}
/>;
{
  error && (
    <p id="email-error" role="alert" className="text-red-500">
      {error}
    </p>
  );
}
```

### Input Hints

```tsx
<input
  type="email"
  inputMode="email"
  autoComplete="email"
  enterKeyHint="next"
/>
```

---

## Motion & Animation

### Respect Reduced Motion

```tsx
// CSS
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

// React
const prefersReducedMotion = window.matchMedia(
  "(prefers-reduced-motion: reduce)"
).matches;
```

### Avoid Flashing

Never flash content more than 3 times per second.

---

## Live Regions

### Web

```tsx
// Polite - waits for user to finish current task
<div aria-live="polite">
  {statusMessage}
</div>

// Assertive - interrupts immediately
<div aria-live="assertive" role="alert">
  {errorMessage}
</div>
```

### React Native

```typescript
import { AccessibilityInfo } from "react-native";

AccessibilityInfo.announceForAccessibility("Item added to cart");
```

---

## Platform-Specific

### Web

| Feature    | Implementation                |
| ---------- | ----------------------------- |
| Labels     | `htmlFor` + `id`              |
| State      | `aria-*` attributes           |
| Validation | `role="alert"` or `aria-live` |

### React Native

| Feature    | Implementation                               |
| ---------- | -------------------------------------------- |
| Labels     | `accessibilityLabel`                         |
| State      | `accessibilityState`                         |
| Validation | `AccessibilityInfo.announceForAccessibility` |
| Decorative | `accessible={false}`                         |

---

## Anti-Patterns

| Pattern                  | Problem            | Solution                |
| ------------------------ | ------------------ | ----------------------- |
| Color-only indicators    | Not perceivable    | Add icons/text          |
| Missing alt text         | Image content lost | Meaningful alt or empty |
| Skipped heading levels   | Navigation broken  | Maintain hierarchy      |
| No focus indicator       | Can't see focus    | Visible ring/outline    |
| Duplicate implicit roles | Verbose for AT     | Remove redundant roles  |
| No keyboard support      | Not operable       | Add tabIndex + handlers |
| Placeholder as label     | Label disappears   | Use visible label       |
| Auto-playing video       | Disruptive         | Require user action     |
| Flashing content         | Seizure risk       | Avoid >3 flashes/sec    |
