# Card Component Example

A responsive product card built with native web platform features.

## Features Used

- **Declarative Shadow DOM** (`<template shadowrootmode="open">`)
- **Container Queries** (`@container card (width >= 25rem)`)
- **CSS Nesting** (native `&` syntax)
- **light-dark()** color function
- **clamp()** for fluid typography
- **Container query units** (`cqi`)

## How It Works

1. **DSD Template**: Card renders immediately from HTML, no JS required
2. **Slots**: Content passed from light DOM (`<span slot="title">`)
3. **Container Queries**: Layout adapts to container width, not viewport
4. **CSS Variables**: All styling uses design tokens

## Responsive Behavior

| Container Width | Layout                          |
| --------------- | ------------------------------- |
| < 25rem         | Stacked (image on top)          |
| 25rem - 35rem   | Side-by-side (image left)       |
| ≥ 35rem         | Full horizontal (actions right) |

## Usage

```html
<div class="card-container">
  <product-card>
    <template shadowrootmode="open">
      <!-- Shadow DOM styles and structure -->
    </template>

    <!-- Light DOM content -->
    <img slot="image" src="product.jpg" alt="Product" />
    <span slot="title">Product Name</span>
    <span slot="description">Description text</span>
    <span slot="price">$99.00</span>
    <button slot="actions">Buy</button>
  </product-card>
</div>
```

## Browser Support

- Chrome 120+
- Edge 120+
- Firefox 121+
- Safari 17.2+
