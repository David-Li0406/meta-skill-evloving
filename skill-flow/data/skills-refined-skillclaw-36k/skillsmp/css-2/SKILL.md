---
name: css
description:
  Writes CSS and CSS Modules with modern features. Use when writing stylesheets,
  CSS modules, or styling components.
---

# CSS Protocol

## Modern Features

Use nesting, `:has()`, `&`, `&:hover`, nested `@media`

```css
.button {
  color: blue;

  &:hover {
    color: darkblue;
  }

  @media (max-width: 600px) {
    width: 100%;
  }
}
```

## CSS Modules

- camelCase class names only (no dashes)
- No tag selectors at root level
- No nested class/id selectors
- Nest pseudo-classes, pseudo-elements, `@media` with `&`

```css
/* ✓ Good */
.container { ... }
.headerTitle { ... }
.submitButton { ... }
```
