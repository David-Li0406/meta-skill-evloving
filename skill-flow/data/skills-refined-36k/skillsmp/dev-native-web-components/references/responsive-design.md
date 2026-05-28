# Responsive Design Reference

> Use responsive units for all layout. **Never use `px` for layout** (only for borders/shadows).

---

## Unit Hierarchy

| Priority | Unit         | Use Case                  |
| -------- | ------------ | ------------------------- |
| 1️⃣       | `cqi`, `cqw` | Container-relative        |
| 2️⃣       | `dvh`, `svh` | Viewport (dynamic)        |
| 3️⃣       | `rem`        | Root-relative spacing     |
| 4️⃣       | `em`         | Element-relative (icons)  |
| ⚠️       | `px`         | **ONLY** borders, shadows |

---

## Container Query Units

```css
.card-container {
  container-type: inline-size;
}

.card-title {
  font-size: clamp(1rem, 4cqi, 2.5rem);
  padding-inline: 2cqi;
}
```

| Unit  | Description                 |
| ----- | --------------------------- |
| `cqi` | 1% of container inline size |
| `cqw` | 1% of container width       |
| `cqb` | 1% of container block size  |

---

## Container Queries Example

```css
.product-grid {
  container-type: inline-size;
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 15rem), 1fr));
}

@container (width < 30rem) {
  .product-card {
    display: block;
    text-align: center;
  }
}

@container (width >= 30rem) {
  .product-card {
    display: grid;
    grid-template-columns: 8rem 1fr;
    gap: 1rem;
  }
}

@container (width >= 50rem) {
  .product-card {
    grid-template-columns: 12rem 1fr auto;
  }
}
```

---

## Dynamic Viewport Units

```css
/* ❌ WRONG: 100vh causes issues on mobile */
.hero {
  height: 100vh;
}

/* ✅ CORRECT: Dynamic viewport respects browser chrome */
.hero {
  min-height: 100dvh;
}
```

| Unit  | Description             |
| ----- | ----------------------- |
| `dvh` | Dynamic viewport height |
| `svh` | Small viewport height   |
| `lvh` | Large viewport height   |

---

## Fluid Typography with clamp()

```css
:root {
  --text-sm: clamp(0.875rem, 2cqi, 1rem);
  --text-base: clamp(1rem, 2.5cqi, 1.125rem);
  --text-lg: clamp(1.125rem, 3cqi, 1.5rem);
  --text-xl: clamp(1.5rem, 4cqi, 2.5rem);
  --text-2xl: clamp(2rem, 5cqi, 4rem);

  --space-sm: clamp(0.5rem, 1cqi, 0.75rem);
  --space-md: clamp(1rem, 2cqi, 1.5rem);
  --space-lg: clamp(1.5rem, 3cqi, 2.5rem);
}
```

---

## Container vs Media Queries

| Feature     | Container  | Media       |
| ----------- | ---------- | ----------- |
| Scope       | Component  | Page        |
| Responds to | Container  | Viewport    |
| Use for     | Components | Page layout |

```css
/* Media: Page layout only */
@media (width >= 64rem) {
  .page {
    grid-template-columns: 16rem 1fr;
  }
}

/* Container: All component layout */
@container (width >= 30rem) {
  .card {
    flex-direction: row;
  }
}
```

---

## Responsive Images

```html
<img
  src="product-400.jpg"
  srcset="product-400.jpg 400w, product-800.jpg 800w"
  sizes="(max-width: 400px) 100vw, 50vw"
  alt="Product"
  loading="lazy"
/>
```

---

## Checklist

- [ ] No `px` for layout
- [ ] `clamp()` for fluid typography
- [ ] Container queries for components
- [ ] `dvh` instead of `vh` for mobile
- [ ] `aspect-ratio` for media

_Reference: [web.dev/learn/css/sizing](https://web.dev/learn/css/sizing)_
