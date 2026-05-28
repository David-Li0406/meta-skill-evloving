---
name: web-accessibility
description: Use this skill when building accessible web applications that comply with WCAG guidelines, ensuring usability for all users, including those with disabilities.
---

# Web Accessibility (WCAG 2.1)

Build accessible web applications that work for everyone by following WCAG 2.1 AA standards. This skill covers ARIA patterns, keyboard navigation, screen reader support, focus management, and semantic HTML.

## Quick Start

### ARIA Patterns

#### Button
```tsx
<button
  type="button"
  aria-pressed={isPressed}
  aria-disabled={isDisabled}
  onClick={handleClick}
>
  Toggle Feature
</button>
```

#### Modal Dialog
```tsx
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  aria-describedby="modal-description"
>
  <h2 id="modal-title">Confirm Action</h2>
  <p id="modal-description">Are you sure you want to proceed?</p>
  <button onClick={onConfirm}>Confirm</button>
  <button onClick={onCancel}>Cancel</button>
</div>
```

#### Navigation Menu
```tsx
<nav aria-label="Main navigation">
  <ul role="menubar">
    <li role="none">
      <a role="menuitem" href="/home">Home</a>
    </li>
    <li role="none">
      <button
        role="menuitem"
        aria-haspopup="true"
        aria-expanded={isOpen}
      >
        Products
      </button>
      {isOpen && (
        <ul role="menu" aria-label="Products submenu">
          <li role="none">
            <a role="menuitem" href="/products/new">New</a>
          </li>
        </ul>
      )}
    </li>
  </ul>
</nav>
```

## Keyboard Navigation

### Focus Management
```tsx
import { useEffect, useRef } from 'react';

function Modal({ isOpen, onClose, children }) {
  const modalRef = useRef<HTMLDivElement>(null);
  const previousFocus = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (isOpen) {
      previousFocus.current = document.activeElement as HTMLElement;
      modalRef.current?.focus();
    } else {
      previousFocus.current?.focus();
    }
  }, [isOpen]);

  // Trap focus within modal
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      onClose();
    }
    
    if (e.key === 'Tab') {
      const focusable = modalRef.current?.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      
      if (focusable && focusable.length > 0) {
        const first = focusable[0] as HTMLElement;
        const last = focusable[focusable.length - 1] as HTMLElement;
        
        if (e.shiftKey && document.activeElement === first) {
          last.focus();
          e.preventDefault();
        } else if (!e.shiftKey && document.activeElement === last) {
          first.focus();
          e.preventDefault();
        }
      }
    }
  };

  return (
    <div ref={modalRef} onKeyDown={handleKeyDown}>
      {children}
    </div>
  );
}
```

## WCAG 2.1 AA Requirements

### Key Principles

1. **Perceivable**: Information must be presentable to users in ways they can perceive.
2. **Operable**: Interface must be operable by all users.
3. **Understandable**: Information and operation must be understandable.
4. **Robust**: Content must be robust enough to work with current and future user agents.

### Compliance Checklist

- All images have alt text.
- All functionality is available from the keyboard.
- Focus indicators are visible.
- Color contrast ratios meet minimum requirements.

## Testing

- Test with assistive technologies like screen readers.
- Ensure all interactive elements are keyboard accessible.
- Regularly audit for compliance with WCAG standards.