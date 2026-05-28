# Popover Menu Example

Navigation menus using the native Popover API with CSS animations.

## Features Used

- **Popover API** (`popover`, `popovertarget`)
- **Anchor Positioning** (`position-anchor`, `inset-area`)
- **Entry Animations** (`@starting-style`)
- **light-dark()** for color scheme
- **ARIA attributes** for accessibility

## Key Patterns

### Declarative Trigger

```html
<button popovertarget="menu">Open</button>
<nav id="menu" popover>...</nav>
```

### Anchor Positioning

```css
.trigger {
  anchor-name: --menu;
}

.menu {
  position: absolute;
  position-anchor: --menu;
  inset-area: bottom;
}
```

### Entry Animation

```css
.menu {
  opacity: 0;
  transition: opacity 0.2s, display 0.2s allow-discrete;
}

.menu:popover-open {
  opacity: 1;
}

@starting-style {
  .menu:popover-open {
    opacity: 0;
  }
}
```

## Browser Support

- Chrome 114+
- Edge 114+
- Firefox 125+
- Safari 17.0+
