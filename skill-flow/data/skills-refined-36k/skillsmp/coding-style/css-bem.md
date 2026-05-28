---
name: CSS BEM 規範
description: Block Element Modifier 命名規範
---

# BEM 命名規範

## 基本結構

```
.block {}
.block__element {}
.block--modifier {}
.block__element--modifier {}
```

## 範例

### Block (區塊)
獨立的元件

```css
.card {}
.nav {}
.button {}
```

### Element (元素)
屬於區塊的一部分，用 `__` 連接

```css
.card__title {}
.card__body {}
.card__image {}
.nav__item {}
.nav__link {}
```

### Modifier (修飾符)
改變外觀或狀態，用 `--` 連接

```css
.card--featured {}
.card--horizontal {}
.button--primary {}
.button--large {}
.button--disabled {}
```

---

## 實際範例

### HTML
```html
<article class="card card--featured">
  <img class="card__image" src="..." alt="">
  <div class="card__body">
    <h3 class="card__title">標題</h3>
    <p class="card__text">內容...</p>
    <button class="button button--primary">按鈕</button>
  </div>
</article>
```

### CSS
```css
/* Block */
.card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

/* Modifier */
.card--featured {
  border: 2px solid gold;
}

/* Element */
.card__image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.card__body {
  padding: 16px;
}

.card__title {
  font-size: 1.25rem;
  margin-bottom: 8px;
}

.card__text {
  color: #666;
}
```

---

## 最佳實踐

1. **Block 獨立**：不依賴其他元素
2. **避免過深巢狀**：最多 Block > Element
3. **Element 只有一層**：不要 `.block__el1__el2`
4. **有意義的命名**：描述功能而非外觀
