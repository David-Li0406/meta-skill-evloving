---
name: dev-native-web-components
description: Build native web components for web apps using declarative Shadow DOM, CSS-first interactivity, responsive units, and baseline 2025->2024->2023 features. Trigger when creating custom elements, component styles, UI overlays, or choosing modern HTML/CSS platform features for the latest four stable browsers.
metadata:
  category: development
---

# Native Web Components Skill

## What is it?

A skill for building framework-free web components using only native HTML, CSS, and modern browser platform features. It prioritizes Declarative Shadow DOM (DSD), CSS-first interactivity, and the newest baseline features (2025 → 2024 → 2023) to ensure compatibility across the latest four stable browser versions.

## Why use it?

- **Zero dependencies**: No frameworks, bundlers, or build tools required
- **Maximum performance**: Native platform features are faster than JavaScript alternatives
- **Cross-browser stability**: Baseline features ensure support across Chrome, Edge, Firefox, Safari
- **Future-proof**: Uses the newest standards with graceful degradation
- **Minimal JavaScript**: CSS handles interactivity; JS only for progressive enhancement

## How to use it?

### Workflow (feature-first)

1. Select the newest baseline feature that fits (2025 → 2024 → 2023). Avoid non-baseline features.
2. Start with semantic HTML in light DOM, then add DSD via `<template shadowrootmode="open">`.
3. Use CSS-first interactivity and native UI primitives (`details`, `popover`, `dialog`, `:has()`).
4. Make layout responsive with container queries and responsive units; avoid px for layout.
5. Add JavaScript only for behavior HTML/CSS cannot express; register custom elements only when lifecycle hooks are required.
6. Validate with the checklist and test on Chrome, Edge, Firefox, Safari latest stable.

## Component skeleton (DSD-first)

```html
<my-card>
  <template shadowrootmode="open">
    <style>
      :host {
        display: block;
        container-type: inline-size;
        padding: 1rem;
      }
    </style>
    <slot></slot>
  </template>
  <h2>Card title</h2>
</my-card>
```

## Mandatory rules

- Use DSD only; never call `attachShadow()`.
- Avoid frameworks or component libraries (Lit, React, Vue).
- Avoid JavaScript by default; treat JS as progressive enhancement only.
- Use responsive units (rem, em, %, cqi, dvh, clamp()); avoid px for layout.
- Use container queries for component layout; media queries only for page layout.
- Use native overlays (`popover`, `dialog`) instead of custom modals.
- Use `@scope` and `@layer` to prevent style leakage.
- Follow the 2025 -> 2024 -> 2023 feature ladder.
- Follow the project class naming convention (TBD); do not invent one here.

## Feature ladder (summary)

- 2025: `@scope`, `::details-content`, `view-transition-class`, `scrollend`, `content-visibility`
- 2024: DSD, Popover, `@starting-style`, `transition-behavior`, `light-dark()`, `text-wrap: balance`, `@property`
- 2023: container queries/units, `:has()`, subgrid

<!-- NOTE: Anchor positioning is NOT yet Baseline (limited status) -->

Use the full matrix in `references/baseline-features.md`.

## Minimal JavaScript policy

- Allow: custom element registration, event bridging, attribute reflection, optional dialog helpers.
- Avoid: rendering UI, templating, state machines, or framework APIs.
- Prefer: HTML primitives and CSS features.

## Folder structure (skill layout)

```
instructions/skills/dev-native-web-components/
  SKILL.md
  references/
    baseline-features.md
    declarative-shadow-dom.md
    slot-patterns.md
    forms.md
    responsive-design.md
    css-first-patterns.md
    popover-dialog.md
    view-transitions.md
    accessibility.md
    performance.md
    debugging.md
    validation-checklist.md
    css.md
    html.md
  examples/
    card-component/
    popover-menu/
    responsive-grid/
    accordion/
    scope-details/
    view-transitions/
    has-subgrid/
```

## Examples

- `card-component/` - DSD card with container queries
- `popover-menu/` - Popover navigation menu
- `responsive-grid/` - Container query grid layout
- `accordion/` - Details/summary accordion
- `scope-details/` - `@scope` and `::details-content` FAQ
- `view-transitions/` - Minimal view transition toggle
- `has-subgrid/` - `:has()` + subgrid spec table

## Testing & Debugging

- **E2E Testing**: Use the `playwright-testing` skill for component testing. See [debugging.md](references/debugging.md).
- **Debugging**: Use Playwright MCP Server or native browser DevTools. See [debugging.md](references/debugging.md).

## Supporting References

| Reference | Description |
|-----------|-------------|
| [dev-web-app](../dev-web-app/SKILL.md) | PWA, SEO, accessibility, i18n, performance, security |
| [baseline-features.md](references/baseline-features.md) | Baseline feature matrix (2025/2024/2023) |
| [declarative-shadow-dom.md](references/declarative-shadow-dom.md) | DSD patterns and SSR hydration |
| [slot-patterns.md](references/slot-patterns.md) | Slot deep dive, slotchange, nested slots |
| [forms.md](references/forms.md) | Forms in Shadow DOM, ElementInternals |
| [css-first-patterns.md](references/css-first-patterns.md) | CSS-only interactivity patterns |
| [responsive-design.md](references/responsive-design.md) | Container queries, responsive units |
| [popover-dialog.md](references/popover-dialog.md) | Native overlays decision tree |
| [view-transitions.md](references/view-transitions.md) | SPA and MPA view transitions |
| [accessibility.md](references/accessibility.md) | Component accessibility patterns |
| [performance.md](references/performance.md) | Component performance optimization |
| [debugging.md](references/debugging.md) | Debugging with Playwright MCP and DevTools |
| [validation-checklist.md](references/validation-checklist.md) | Pre-commit validation checklist |
| [css.md](references/css.md) | Deep CSS research sources |
| [html.md](references/html.md) | Deep HTML research sources |

## Limitations

- JavaScript patterns (minimal-javascript.md) will be added later
- Design tokens strategy will be added later
- Multi-component communication requires JS — on hold
- Fallback patterns for non-baseline features require JS — on hold
