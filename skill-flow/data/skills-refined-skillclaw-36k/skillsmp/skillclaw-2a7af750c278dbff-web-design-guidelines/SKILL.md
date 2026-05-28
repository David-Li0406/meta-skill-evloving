---
name: web-design-guidelines
description: Use this skill when you need to review UI code for compliance with Web Interface Guidelines, particularly for accessibility, design audits, or UX evaluations.
---

# Web Interface Guidelines

Review files for compliance with Web Interface Guidelines.

## When to use

Use this skill when a user asks to:
- Review UI/UX for accessibility or design issues.
- Audit a site against best practices.
- Check a specific feature or flow for UI guidelines.

## Philosophy

Aim for accessible, predictable interfaces that reduce user error and cognitive load. Prefer clarity over novelty, and fix issues in order of user impact (accessibility → usability → visual polish). Use evidence from the UI and user flows, not personal taste. The guiding principle is to reduce friction in the primary user journey.

## How It Works

1. Fetch the latest guidelines from the source URL below.
2. Read the specified files (or prompt user for files/pattern).
3. Check against all rules in the fetched guidelines.
4. Output findings in the terse `file:line` format.

## Guidelines Source

Fetch fresh guidelines before each review:

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

Use WebFetch to retrieve the latest rules. The fetched content contains all the rules and output format instructions.

## Rules

### Accessibility

- Icon-only buttons need `aria-label`.
- Form controls need `<label>` or `aria-label`.
- Interactive elements need keyboard handlers (`onKeyDown`/`onKeyUp`).
- Use `<button>` for actions, `<a>`/`<Link>` for navigation (not `<div onClick>`).
- Images need `alt` (or `alt=""` if decorative).
- Decorative icons need `aria-hidden="true"`.
- Async updates (toasts, validation) need `aria-live="polite"`.
- Use semantic HTML (`<button>`, `<a>`, `<label>`, `<table>`) before ARIA.
- Headings should be hierarchical `<h1>`–`<h6>`; include skip link for main content.
- Use `scroll-margin-top` on heading anchors.

### Focus States

- Interactive elements need visible focus: `focus-visible:ring-*` or equivalent.
- Never `outline-none` / `outline: none` without focus replacement.
- Use `:focus-visible` over `:focus` (avoid focus ring on click).
- Group focus with `:focus-within` for compound controls.

### Forms

- Inputs need `autocomplete` and meaningful `name`.
- Use correct `type` (`email`, `tel`, `url`, `number`) and `inputmode`.
- Never block paste (`onPaste` + `preventDefault`).
- Labels should be clickable (`htmlFor` or wrapping control).
- Disable spellcheck on emails, codes, usernames (`spellCheck={false}`).
- Checkboxes/radios: label + control share single hit target (no dead zones).
- Submit button stays enabled until request starts; show spinner during request.
- Errors should be inline next to fields; focus first error on submit.
- Placeholders should end with `…` and show example pattern.
- Use `autocomplete="off"` on non-auth fields to avoid password manager triggers.
- Warn before navigation with unsaved changes (`beforeunload` or router guard).

### Animation

- Honor `prefers-reduced-motion` (provide reduced variant or disable).
- Animate `transform`/`opacity` only (compositor-friendly).
- Never `transition: all`—list properties explicitly.
- Set correct `transform-origin`.
- For SVG, apply transforms on `<g>` wrapper with `transform-box: fill-box; transform-origin: center`.
- Ensure animations are interruptible—respond to user interactions.