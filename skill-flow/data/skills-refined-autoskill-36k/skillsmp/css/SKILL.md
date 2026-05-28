---
name: CSS 架構技能
description: Tailwind、Bootstrap、SCSS 等 CSS 方案指南
---

# 🎨 CSS 架構技能

## CSS 方案選擇

| 方案 | 類型 | 適用場景 | 學習曲線 |
|-----|------|---------|---------|
| [Tailwind](tailwind.md) | 原子化 | 快速開發、客製化 | 中等 |
| [Bootstrap](bootstrap.md) | 元件庫 | 快速原型、標準 UI | 低 |
| [SCSS](scss.md) | 預處理器 | 複雜專案、設計系統 | 低 |
| [Vanilla](vanilla.md) | 原生 | 輕量、完全控制 | 低 |

---

## 快速選擇

| 需求 | 推薦 |
|-----|------|
| 快速開發 | Tailwind / Bootstrap |
| 客製化設計 | Tailwind / SCSS |
| 標準元件 | Bootstrap |
| 設計系統 | SCSS / CSS Variables |
| 輕量 | Vanilla CSS |

---

## CSS 架構方法論

### BEM (Block Element Modifier)

```css
/* Block */
.card { }

/* Element */
.card__title { }
.card__body { }

/* Modifier */
.card--featured { }
.card__title--large { }
```

### SMACSS (分類)

```
base/       基礎樣式
layout/     佈局
modules/    模組/元件
state/      狀態
theme/      主題
```

---

## CSS Variables 設計系統

```css
:root {
  /* 色彩 */
  --color-primary: #3b82f6;
  --color-secondary: #64748b;
  
  /* 字型 */
  --font-sans: 'Inter', sans-serif;
  --text-base: 1rem;
  
  /* 間距 */
  --space-4: 1rem;
  --space-8: 2rem;
  
  /* 圓角 */
  --radius-md: 8px;
  
  /* 陰影 */
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
}
```

---

## 響應式設計

```css
/* Mobile First */
.container {
  padding: 1rem;
}

@media (min-width: 768px) {
  .container {
    padding: 2rem;
  }
}

@media (min-width: 1024px) {
  .container {
    max-width: 1024px;
    margin: 0 auto;
  }
}
```

---

## 相關技能

- [UI 設計](../ui/SKILL.md)
- [響應式設計](../rwd/SKILL.md)
- [Coding Style - CSS](../code/css-bem.md)
