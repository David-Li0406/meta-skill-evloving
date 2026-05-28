---
name: Vanilla CSS 指南
description: 原生 CSS 開發最佳實踐
---

# 🎨 Vanilla CSS 指南

## CSS Variables

```css
:root {
  /* 色彩 */
  --color-primary: #3b82f6;
  --color-secondary: #64748b;
  --color-success: #22c55e;
  --color-error: #ef4444;
  
  /* 字型 */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  
  /* 間距 */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-4: 1rem;
  --space-8: 2rem;
  
  /* 圓角 */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  
  /* 陰影 */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
}

.button {
  background: var(--color-primary);
  border-radius: var(--radius-md);
  padding: var(--space-2) var(--space-4);
}
```

---

## 現代佈局

### Flexbox
```css
.flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
}

.flex-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

### Grid
```css
.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
}

.grid-auto {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-4);
}
```

---

## 響應式

```css
/* Mobile First */
.container {
  padding: var(--space-4);
}

@media (min-width: 768px) {
  .container {
    max-width: 768px;
    margin: 0 auto;
  }
}

@media (min-width: 1024px) {
  .container {
    max-width: 1024px;
  }
}
```

---

## 現代 CSS 功能

```css
/* clamp() 流體字型 */
h1 {
  font-size: clamp(2rem, 5vw, 4rem);
}

/* aspect-ratio */
.video {
  aspect-ratio: 16 / 9;
}

/* 容器查詢 */
@container (min-width: 400px) {
  .card {
    display: flex;
  }
}

/* :has() 選擇器 */
.card:has(img) {
  padding: 0;
}

/* 巢狀 (原生) */
.card {
  background: white;
  
  & .title {
    font-size: 1.25rem;
  }
  
  &:hover {
    box-shadow: var(--shadow-md);
  }
}
```

---

## Reset

```css
*, *::before, *::after {
  box-sizing: border-box;
}

* {
  margin: 0;
}

body {
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

img, picture, video, canvas, svg {
  display: block;
  max-width: 100%;
}

input, button, textarea, select {
  font: inherit;
}
```
