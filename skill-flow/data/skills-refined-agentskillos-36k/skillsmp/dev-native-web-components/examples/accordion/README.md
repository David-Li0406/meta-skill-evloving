# Accordion Example

Native details/summary accordion with smooth CSS animations.

## Features Used

- **`<details>` element** - Native disclosure widget
- **`name` attribute** - Exclusive accordion (one open at a time)
- **`::details-content`** - Style and animate content (Baseline 2025)
- **CSS-only animation** - No JavaScript for expand/collapse

## Key Patterns

### Basic Accordion

```html
<details name="faq">
  <summary>Question</summary>
  <div class="content">Answer</div>
</details>
```

### Animated Content

```css
details::details-content {
  block-size: 0;
  overflow-y: clip;
  transition: block-size 0.3s ease;
}

details[open]::details-content {
  block-size: auto;
}
```

### Exclusive Accordion

```html
<!-- Same name = only one open at a time -->
<details name="faq">...</details>
<details name="faq">...</details>
```

### Multi-Open Accordion

```html
<!-- No name attribute = multiple can be open -->
<details>...</details>
<details>...</details>
```

## Browser Support

- Chrome 131+ (`::details-content`)
- Firefox 135+ (`::details-content`)
- Safari 18.2+ (`::details-content`)
- Exclusive accordion (name): Baseline 2024
