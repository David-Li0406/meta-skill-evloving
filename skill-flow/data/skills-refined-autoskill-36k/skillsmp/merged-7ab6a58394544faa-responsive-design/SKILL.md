---
name: responsive-design
description: Use this skill to create responsive web designs that work across all devices and screen sizes, focusing on mobile-first layouts, breakpoints, and optimizing for different viewports.
---

# Responsive Design

## When to use this skill

- When designing layouts for new websites/apps that need to work on mobile, tablet, and desktop.
- When converting legacy fixed layouts to responsive designs.
- When optimizing images and assets for different devices.
- When ensuring compatibility across various screen sizes, including tablets and large displays.

## Instructions

### Step 1: Mobile-First Approach

Design for small screens first and progressively enhance for larger screens.

**Example**:
```css
/* Base: Mobile (320px~) */
.container {
  padding: 1rem;
  font-size: 14px;
}

.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

/* Tablet (768px~) */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
    font-size: 16px;
  }

  .grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }
}

/* Desktop (1024px~) */
@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 3rem;
  }

  .grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
  }
}

/* Large screens (1440px~) */
@media (min-width: 1440px) {
  .grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

### Step 2: Flexbox/Grid Layouts

Utilize modern CSS layout systems.

**Flexbox** (1D layout):
```css
/* Navigation bar */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

/* Card list */
.card-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

@media (min-width: 768px) {
  .card-list {
    flex-direction: row;
    flex-wrap: wrap;
  }

  .card {
    flex: 1 1 calc(50% - 0.5rem);  /* 2 columns */
  }
}

@media (min-width: 1024px) {
  .card {
    flex: 1 1 calc(33.333% - 0.667rem);  /* 3 columns */
  }
}
```

**CSS Grid** (2D layout):
```css
/* Dashboard layout */
.dashboard {
  display: grid;
  grid-template-areas:
    "header"
    "sidebar"
    "main"
    "footer";
  gap: 1rem;
}

@media (min-width: 768px) {
  .dashboard {
    grid-template-areas:
      "header header"
      "sidebar main"
      "footer footer";
    grid-template-columns: 250px 1fr;
  }
}

@media (min-width: 1024px) {
  .dashboard {
    grid-template-columns: 300px 1fr;
  }
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }
```

### Step 3: Responsive Images

Serve appropriate images for different devices.

**Using srcset**:
```html
<img
  src="image-800.jpg"
  srcset="
    image-400.jpg 400w,
    image-800.jpg 800w,
    image-1200.jpg 1200w,
    image-1600.jpg 1600w
  "
  sizes="
    (max-width: 600px) 100vw,
    (max-width: 900px) 50vw,
    33vw
  "
  alt="Responsive image"
/>
```

**Using picture element** (Art Direction):
```html
<picture>
  <source media="(max-width: 767px)" srcset="portrait.jpg">
  <source media="(max-width: 1023px)" srcset="square.jpg">
  <img src="landscape.jpg" alt="Art direction example">
</picture>
```

### Step 4: Responsive Typography

Adjust text sizes based on screen size.

**Using clamp() function** (fluid sizing):
```css
:root {
  --font-size-body: clamp(14px, 2.5vw, 18px);
  --font-size-h1: clamp(24px, 5vw, 48px);
  --font-size-h2: clamp(20px, 4vw, 36px);
}

body {
  font-size: var(--font-size-body);
}

h1 {
  font-size: var(--font-size-h1);
  line-height: 1.2;
}

h2 {
  font-size: var(--font-size-h2);
  line-height: 1.3;
}
```

### Step 5: Container Queries (New Feature)

Apply styles based on the size of the parent container.

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

.card {
  padding: 1rem;
}

.card h2 {
  font-size: 1.2rem;
}

/* When container is at least 400px */
@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
    padding: 1.5rem;
  }

  .card h2 {
    font-size: 1.5rem;
  }
}

/* When container is at least 600px */
@container card (min-width: 600px) {
  .card {
    grid-template-columns: 300px 1fr;
    padding: 2rem;
  }
}
```

## Verification Checklist

Before completing responsive work:

- [ ] Started with mobile layout.
- [ ] Used project's standard breakpoints.
- [ ] Implemented fluid layouts (no fixed widths).
- [ ] Used relative units (rem/em) for sizing.
- [ ] Ensured touch targets are a minimum of 44x44px.
- [ ] Maintained readable typography without zoom (16px+ body).
- [ ] Prioritized content on mobile.
- [ ] Optimized images for different sizes.
- [ ] Tested at all key breakpoints.
- [ ] No horizontal scrolling on mobile.
- [ ] No overlapping or truncated content.

## Best Practices

1. **Container Queries First**: Prefer container queries over media queries when possible.
2. **Flexbox vs Grid**: Use Flexbox for 1D layouts and Grid for 2D layouts.
3. **Performance**: Implement lazy loading for images and use modern formats like WebP.
4. **Testing**: Utilize Chrome DevTools Device Mode and BrowserStack for testing.

## References

- [MDN Responsive Design](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design)
- [CSS Grid Guide](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [Flexbox Guide](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- [Container Queries](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Container_Queries)

## Metadata

### Version
- **Current Version**: 1.0.0
- **Last Updated**: 2025-01-01
- **Compatible Platforms**: Claude, ChatGPT, Gemini

### Tags
`#responsive` `#mobile-first` `#CSS` `#Flexbox` `#Grid` `#media-query` `#frontend`