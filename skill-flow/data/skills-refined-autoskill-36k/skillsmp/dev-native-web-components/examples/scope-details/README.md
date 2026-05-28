# Scoped FAQ Panel

FAQ panel using `@scope` for localized styles and `::details-content` for animation.

## Features Used

- **`@scope`** - Scoped styles without Shadow DOM leakage
- **`::details-content`** - Animate details content (Baseline 2025)
- **`<details>` / `<summary>`** - Native disclosure widget
- **Declarative Shadow DOM** - Component markup without JS

## Key Patterns

### Scoped Styles

```css
@scope (.faq) {
  summary {
    font-weight: 600;
  }
}
```

### Animated Details

```css
details::details-content {
  block-size: 0;
  overflow-y: clip;
  transition: block-size 0.25s ease, opacity 0.2s ease;
}

details[open]::details-content {
  block-size: auto;
  opacity: 1;
}
```

## Browser Support

- Chrome 131+
- Firefox 135+
- Safari 18.2+
