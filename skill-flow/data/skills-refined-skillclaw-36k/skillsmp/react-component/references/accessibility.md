# Accessibility (a11y) Guide

Accessibility is a non-negotiable requirement for building professional, inclusive, and compliant web applications. It is not a feature to be added later; it is a fundamental aspect of component design.

This guide provides the core principles and practices to follow.

## Table of Contents

1. [Core Principles (POUR)](#core-principles-pour)
2. [The Golden Rule: Use Semantic HTML](#the-golden-rule-use-semantic-html)
3. [ARIA: Use Sparingly](#aria-use-sparingly)
4. [Focus Management](#focus-management)
5. [Forms & Labels](#forms--labels)
6. [Testing for Accessibility](#testing-for-accessibility)

---

## Core Principles (POUR)

All UIs must adhere to the four principles of the Web Content Accessibility Guidelines (WCAG).

| Principle          | Description                                                                                                                           | Key Takeaway                                                                                   |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| **Perceivable**    | Users must be able to perceive the information being presented. It can't be invisible to all of their senses.                         | Provide text alternatives for non-text content (`alt` tags). Ensure sufficient color contrast. |
| **Operable**       | Users must be able to operate the interface. The interface cannot require interaction that a user cannot perform.                     | All functionality must be available from a keyboard. No keyboard traps.                        |
| **Understandable** | Users must be able to understand the information as well as the operation of the user interface.                                      | Make content readable and predictable. Help users avoid and correct mistakes.                  |
| **Robust**         | Content must be robust enough that it can be interpreted reliably by a wide variety of user agents, including assistive technologies. | Use valid HTML. Ensure ARIA attributes are used correctly.                                     |

---

## The Golden Rule: Use Semantic HTML

The most important step toward accessibility is to use native HTML elements for their intended purpose. Browsers provide built-in keyboard support, roles, and states for semantic elements.

- **Use `<button>` for actions.** It's focusable, can be activated with `Enter` and `Space`, and is announced as a "button" by screen readers.
- **Use `<a>` for navigation.** It's focusable and handles standard keyboard and mouse events for navigating to a new URL.
- **Use `<nav>`, `<main>`, `<header>`, `<footer>`** to define page landmarks, allowing screen reader users to navigate your application efficiently.
- **Use `<h1>` through `<h6>`** to create a logical document outline. Never skip heading levels.
- **Use `<label>` for all form inputs.** See the [Forms & Labels](#forms--labels) section for details.
- **Use `<ul>` or `<ol>` for lists.**

**Do not create a `div` that tries to act like a `button`.**

```tsx
// BAD: Un-semantic, inaccessible, and requires manual event handling
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') handleClick();
  }}
>
  Submit
</div>

// GOOD: Semantic, accessible out-of-the-box
<button onClick={handleClick}>
  Submit
</button>
```

---

## ARIA: Use Sparingly

ARIA (`Accessible Rich Internet Applications`) attributes should only be used when semantic HTML is not sufficient. This is common in complex, dynamic components like custom dropdowns, tabs, or modals provided by libraries like Radix UI.

**Rule: No ARIA is better than bad ARIA.** Incorrect ARIA can make an application less accessible than having none at all.

| Attribute          | Purpose                                                                                          | Example                                                                                           |
| ------------------ | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| `role`             | Overrides the native role of an element. Use with extreme caution.                               | `<div role="alert">...</div>`                                                                     |
| `aria-label`       | Provides an accessible name when no visible text label exists (e.g., an icon-only button).       | `<button aria-label="Close">X</button>`                                                           |
| `aria-labelledby`  | Associates an element with the ID of another element that serves as its label.                   | `<div id="dialog-title">Confirm</div><div role="dialog" aria-labelledby="dialog-title">...</div>` |
| `aria-describedby` | Associates an element with supplementary descriptive text.                                       | `<input aria-describedby="password-hint">`                                                        |
| `aria-hidden`      | Hides an element from assistive technologies. Useful for decorative icons or off-screen content. | `<svg aria-hidden="true">...</svg>`                                                               |
| `aria-expanded`    | Indicates whether a collapsible element is currently expanded or collapsed.                      | `<button aria-expanded={isOpen}>...</button>`                                                     |
| `aria-haspopup`    | Indicates that an element triggers a popup menu or dialog.                                       | `<button aria-haspopup="true">...</button>`                                                       |

When using headless libraries like Radix UI, these attributes are typically handled for you. Your job is to ensure you are using their components correctly.

---

## Focus Management

Operable UI depends on predictable focus management.

1.  **Visible Focus States:** All interactive elements (`button`, `a`, `input`, etc.) **must** have a visible outline when focused. Use Tailwind's `focus-visible` utility to style focus rings that only appear during keyboard navigation. Never use `outline: none` without providing a clear alternative.

2.  **Logical Focus Order:** The focus order should follow the visual layout of the page. This is usually handled for free by writing logical, well-structured HTML.

3.  **No Keyboard Traps:** A user must be able to navigate into and out of any component using only the keyboard. Modals and dialogs are a common failure point; they must trap focus _inside_ while open and return focus to the trigger element when closed. Use Radix UI's `Dialog` or `Popover` components to handle this for you.

---

## Forms & Labels

Every form control **must** be associated with a visible `<label>` element. This is non-negotiable. It helps all users understand what the input is for and increases the clickable target area for the input.

Use the `htmlFor` attribute on the `label` and match it with the `id` of the `input`.

```tsx
// GOOD: Explicitly linked label and input
<div>
  <label htmlFor="user-email">Email Address</label>
  <input type="email" id="user-email" name="email" />
</div>

// BAD: No label, placeholder is not a substitute
<input type="email" placeholder="Email Address" />

// BAD: Label is not programmatically linked
<div>
  <span>Email Address</span>
  <input type="email" />
</div>
```

When using a component library like `shadcn/ui`, this is handled by their `Form` components. Ensure you use them as documented.

---

## Testing for Accessibility

Testing is a combination of automated checks and manual testing.

### Automated Testing

Use `axe-core` integrated into your Vitest setup to catch common violations during your normal test runs.

1.  **Install dev dependencies:**
    `pnpm add -D @axe-core/react vitest-axe`

2.  **Set up `vitest-axe`:** Extend your test expect assertions.

    ```ts
    // In a test setup file
    import { expect } from 'vitest'
    import { toHaveNoViolations } from 'vitest-axe'
    import 'vitest-axe/extend-expect'

    expect.extend(toHaveNoViolations)
    ```

3.  **Write tests:**

    ```tsx
    import { render } from '@testing-library/react'
    import { axe } from 'vitest-axe'
    import { MyFormComponent } from './MyFormComponent'

    it('should have no accessibility violations', async () => {
      const { container } = render(<MyFormComponent />)
      const results = await axe(container)
      expect(results).toHaveNoViolations()
    })
    ```

### Manual Testing

Automated tools only catch ~30% of a11y issues. Manual testing is essential.

1.  **Keyboard Navigation:** Can you navigate and operate every interactive element using only the `Tab`, `Shift+Tab`, `Enter`, `Space`, and arrow keys?
    - Is the focus indicator always visible?
    - Is the focus order logical?
    - Are there any keyboard traps?

2.  **Screen Reader Testing:**
    - Use a built-in screen reader (VoiceOver on macOS, Narrator on Windows) to navigate your component.
    - Are all interactive elements announced correctly (e.g., "Submit, button")?
    - Is all important information read aloud?
    - Are form inputs clearly labeled?
