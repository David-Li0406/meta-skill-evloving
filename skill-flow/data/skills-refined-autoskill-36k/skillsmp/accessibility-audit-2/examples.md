# Accessibility Audit - Examples

## Example 1: Button Component Audit

**Scenario:** User wants to ensure a custom Button component meets WCAG 2.1 AA standards.

**Component Code:**
```tsx
// components/Button.tsx
export function Button({ onClick, children }) {
  return (
    <div onClick={onClick} className="button">
      {children}
    </div>
  );
}
```

**Audit Findings:**

❌ **Critical Issues:**
1. Using `<div>` instead of `<button>` - not keyboard accessible
2. No focus indicator
3. Missing accessible name for icon-only buttons
4. No disabled state handling

**Fixed Code:**
```tsx
// components/Button.tsx
import { cn } from "~/utils/cn";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: "primary" | "secondary";
  isLoading?: boolean;
}

export function Button({
  children,
  variant = "primary",
  isLoading = false,
  disabled,
  className,
  ...props
}: ButtonProps) {
  return (
    <button
      {...props}
      disabled={disabled || isLoading}
      aria-busy={isLoading}
      className={cn(
        "px-4 py-2 rounded",
        "focus:outline-none focus:ring-2 focus:ring-blue-500",
        "disabled:opacity-50 disabled:cursor-not-allowed",
        variant === "primary" && "bg-blue-600 text-white",
        variant === "secondary" && "bg-gray-200 text-gray-900",
        className
      )}
    >
      {isLoading && (
        <span className="sr-only">Loading...</span>
      )}
      {children}
    </button>
  );
}
```

**WCAG Compliance Checklist:**
- ✅ Semantic HTML (`<button>`)
- ✅ Keyboard accessible (native button behavior)
- ✅ Visible focus indicator (ring)
- ✅ Color contrast ratio ≥ 4.5:1
- ✅ Disabled state with `disabled` attribute
- ✅ Loading state with `aria-busy`
- ✅ Screen reader text for loading state

---

## Example 2: Form Accessibility

**Scenario:** LoginForm component needs accessibility improvements.

**Before:**
```tsx
export function LoginForm() {
  return (
    <form>
      <input type="email" placeholder="Email" />
      <input type="password" placeholder="Password" />
      <button>Login</button>
    </form>
  );
}
```

**Issues Found:**
❌ No labels for inputs (only placeholders)
❌ No error announcements
❌ No form validation feedback
❌ Missing autocomplete attributes

**After:**
```tsx
export function LoginForm() {
  const [errors, setErrors] = useState<Record<string, string>>({});

  return (
    <form aria-label="Login form">
      {/* Email field */}
      <div>
        <label htmlFor="email" className="block mb-1">
          Email address
        </label>
        <input
          id="email"
          type="email"
          name="email"
          autoComplete="email"
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? "email-error" : undefined}
          className="w-full px-3 py-2 border rounded"
        />
        {errors.email && (
          <span id="email-error" role="alert" className="text-red-600 text-sm">
            {errors.email}
          </span>
        )}
      </div>

      {/* Password field */}
      <div>
        <label htmlFor="password" className="block mb-1">
          Password
        </label>
        <input
          id="password"
          type="password"
          name="password"
          autoComplete="current-password"
          aria-invalid={!!errors.password}
          aria-describedby={errors.password ? "password-error" : undefined}
          className="w-full px-3 py-2 border rounded"
        />
        {errors.password && (
          <span id="password-error" role="alert" className="text-red-600 text-sm">
            {errors.password}
          </span>
        )}
      </div>

      <button type="submit" className="w-full py-2 bg-blue-600 text-white rounded">
        Log in
      </button>
    </form>
  );
}
```

**Improvements:**
- ✅ Explicit `<label>` elements with `htmlFor`
- ✅ `aria-invalid` for invalid fields
- ✅ `aria-describedby` linking errors to inputs
- ✅ `role="alert"` for error messages (screen reader announcement)
- ✅ `autocomplete` attributes for password managers
- ✅ Form label with `aria-label`

---

## Example 3: Image Accessibility

**Scenario:** Product card with images needs proper alt text.

**Before:**
```tsx
<div className="product-card">
  <img src="/product.jpg" />
  <h3>Product Name</h3>
</div>
```

**Issues:**
❌ Missing alt attribute
❌ Decorative vs informative not distinguished

**After:**
```tsx
<div className="product-card">
  {/* Informative image - describe what's shown */}
  <img
    src="/product.jpg"
    alt="Blue cotton t-shirt with logo on chest"
    loading="lazy"
  />
  <h3>Product Name</h3>

  {/* Decorative background pattern - empty alt */}
  <img
    src="/pattern.svg"
    alt=""
    role="presentation"
  />
</div>
```

**Guidelines:**
- ✅ Informative images: Descriptive alt text
- ✅ Decorative images: Empty alt (`alt=""`) + `role="presentation"`
- ✅ Complex images: Consider `aria-describedby` for longer descriptions
- ✅ Lazy loading for performance

---

## Example 4: Dynamic Content Updates

**Scenario:** Toast notifications need to announce to screen readers.

**Before:**
```tsx
export function Toast({ message }: { message: string }) {
  return (
    <div className="toast">
      {message}
    </div>
  );
}
```

**Issue:**
❌ Screen readers don't announce dynamic updates

**After:**
```tsx
export function Toast({
  message,
  type = "info"
}: {
  message: string;
  type?: "success" | "error" | "warning" | "info";
}) {
  return (
    <div
      role="status"
      aria-live="polite"
      aria-atomic="true"
      className={cn(
        "toast p-4 rounded shadow-lg",
        type === "error" && "bg-red-100 text-red-900",
        type === "success" && "bg-green-100 text-green-900"
      )}
    >
      {/* Visual icon for sighted users */}
      {type === "error" && <ErrorIcon aria-hidden="true" />}
      {type === "success" && <CheckIcon aria-hidden="true" />}

      {message}
    </div>
  );
}
```

**Key ARIA attributes:**
- ✅ `role="status"` - Identifies as status message
- ✅ `aria-live="polite"` - Announces when user is idle
- ✅ `aria-atomic="true"` - Reads entire message on update
- ✅ `aria-hidden="true"` on decorative icons

**For errors, use assertive:**
```tsx
<div
  role="alert"
  aria-live="assertive"  // Interrupts screen reader
  className="error-toast"
>
  {errorMessage}
</div>
```

---

## Example 5: Keyboard Navigation in Modal

**Scenario:** Modal dialog needs proper focus management.

**Before:**
```tsx
export function Modal({ isOpen, onClose, children }) {
  if (!isOpen) return null;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-content">
        {children}
      </div>
    </div>
  );
}
```

**Issues:**
❌ Focus not trapped in modal
❌ Can't close with Escape key
❌ Focus not returned after close
❌ No accessible name

**After:**
```tsx
import { useEffect, useRef } from "react";

export function Modal({
  isOpen,
  onClose,
  title,
  children
}: {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}) {
  const modalRef = useRef<HTMLDivElement>(null);
  const previousFocus = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (isOpen) {
      // Save previous focus
      previousFocus.current = document.activeElement as HTMLElement;

      // Focus modal
      modalRef.current?.focus();

      // Trap focus in modal
      const handleTab = (e: KeyboardEvent) => {
        if (e.key === "Tab" && modalRef.current) {
          const focusableElements = modalRef.current.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
          );
          const first = focusableElements[0] as HTMLElement;
          const last = focusableElements[focusableElements.length - 1] as HTMLElement;

          if (e.shiftKey && document.activeElement === first) {
            e.preventDefault();
            last.focus();
          } else if (!e.shiftKey && document.activeElement === last) {
            e.preventDefault();
            first.focus();
          }
        }
      };

      document.addEventListener("keydown", handleTab);
      return () => document.removeEventListener("keydown", handleTab);
    } else {
      // Restore focus when closed
      previousFocus.current?.focus();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div
      className="modal-backdrop fixed inset-0 bg-black/50 flex items-center justify-center"
      onClick={onClose}
    >
      <div
        ref={modalRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        tabIndex={-1}
        className="modal-content bg-white rounded-lg p-6 max-w-md"
        onClick={(e) => e.stopPropagation()}
        onKeyDown={(e) => {
          if (e.key === "Escape") {
            onClose();
          }
        }}
      >
        <h2 id="modal-title" className="text-xl font-bold mb-4">
          {title}
        </h2>

        {children}

        <button
          onClick={onClose}
          aria-label="Close dialog"
          className="mt-4 px-4 py-2 bg-gray-200 rounded"
        >
          Close
        </button>
      </div>
    </div>
  );
}
```

**Accessibility features:**
- ✅ `role="dialog"` and `aria-modal="true"`
- ✅ `aria-labelledby` points to title
- ✅ Focus trap (Tab cycles within modal)
- ✅ Escape key closes modal
- ✅ Focus returns to trigger after close
- ✅ Click outside closes (optional pattern)

---

## Common Accessibility Patterns

### Skip Links
```tsx
<a href="#main-content" className="sr-only focus:not-sr-only">
  Skip to main content
</a>
```

### Screen Reader Only Text
```tsx
<span className="sr-only">Loading...</span>

/* CSS */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

.sr-only:focus {
  position: static;
  width: auto;
  height: auto;
  padding: inherit;
  margin: inherit;
  overflow: visible;
  clip: auto;
  white-space: normal;
}
```

### Accessible Icon Buttons
```tsx
<button aria-label="Delete item">
  <TrashIcon aria-hidden="true" />
</button>
```

### Loading States
```tsx
<button disabled aria-busy="true">
  <span className="sr-only">Loading...</span>
  <Spinner aria-hidden="true" />
</button>
```

---

## Testing Checklist

### Automated Tests
- [ ] Run axe-core via Playwright
- [ ] Check Storybook a11y addon
- [ ] Validate with WAVE browser extension

### Manual Tests
- [ ] Keyboard navigation (Tab, Enter, Space, Arrow keys)
- [ ] Screen reader (NVDA/JAWS on Windows, VoiceOver on Mac)
- [ ] High contrast mode
- [ ] Zoom to 200%
- [ ] Color contrast (use contrast checker)

### WCAG 2.1 AA Quick Check
- [ ] 1.1.1 - All non-text content has alt text
- [ ] 2.1.1 - All functionality via keyboard
- [ ] 2.4.7 - Focus indicator visible
- [ ] 3.3.2 - Labels or instructions for input
- [ ] 4.1.2 - Name, role, value for UI components
