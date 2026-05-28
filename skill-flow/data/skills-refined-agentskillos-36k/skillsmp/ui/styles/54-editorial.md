---
name: 編輯風格
description: Editorial - 雜誌排版的視覺風格
---

# 54. 編輯風 Editorial

## 概述
借鑒雜誌排版的大膽視覺設計。

## 特徵
- 大標題
- 錯落排版
- 強烈對比
- 藝術圖片

## 配色
```css
:root {
  --edit-black: #000000;
  --edit-white: #ffffff;
  --edit-gray: #666666;
  --edit-accent: #ff3b3b;
}
```

## 字型
```css
h1 {
  font-family: 'Playfair Display', serif;
  font-size: clamp(3rem, 8vw, 8rem);
  font-weight: 700;
  line-height: 0.95;
  letter-spacing: -0.03em;
}

p {
  font-family: 'Inter', sans-serif;
  font-size: 1.125rem;
  line-height: 1.8;
}
```

## 排版
```css
.editorial-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 24px;
}

.featured-image {
  grid-column: span 8;
}

.article-text {
  grid-column: span 4;
}

/* 錯落效果 */
.offset-up {
  margin-top: -100px;
}
```

## 元件

### 大標題
```css
.mega-title {
  font-size: 12vw;
  font-weight: 900;
  line-height: 0.85;
  text-transform: uppercase;
}
```

### 下劃線連結
```css
.editorial-link {
  color: var(--edit-black);
  text-decoration: none;
  border-bottom: 2px solid var(--edit-accent);
  padding-bottom: 2px;
}
```

## 適用場景
- 時尚雜誌
- 攝影作品
- 創意機構
- 生活風格品牌
