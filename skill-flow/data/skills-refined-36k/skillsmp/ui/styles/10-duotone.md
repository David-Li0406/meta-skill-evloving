---
name: 雙色調風格
description: Duotone - 雙色處理的藝術風格
---

# 10. 雙色調 Duotone

## 概述
使用兩種顏色處理的強烈藝術風格。

## 特徵
- 只有兩色
- 強烈對比
- 藝術感
- 統一調性

## 配色組合

```css
:root {
  /* 經典配色 */
  --duo-1-dark: #1a1a2e;
  --duo-1-light: #ff6b6b;
  
  /* 青橙 */
  --duo-2-dark: #0d7377;
  --duo-2-light: #ff9f1c;
  
  /* 紫粉 */
  --duo-3-dark: #5c2d91;
  --duo-3-light: #ff5e78;
  
  /* 藍橙 */
  --duo-4-dark: #1e3a8a;
  --duo-4-light: #f97316;
}
```

## CSS 濾鏡

```css
/* 雙色調圖片 */
.duotone-image {
  position: relative;
  isolation: isolate;
}

.duotone-image img {
  filter: grayscale(100%) contrast(1.2);
}

.duotone-image::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--duo-1-dark), var(--duo-1-light));
  mix-blend-mode: color;
}
```

## SVG 濾鏡

```html
<svg>
  <filter id="duotone">
    <feColorMatrix type="matrix" values="
      0.5 0.5 0.5 0 0
      0.5 0.5 0.5 0 0
      0.5 0.5 0.5 0 0
      0   0   0   1 0
    "/>
    <feComponentTransfer color-interpolation-filters="sRGB">
      <feFuncR type="table" tableValues="0.1 1"/>
      <feFuncG type="table" tableValues="0.1 0.4"/>
      <feFuncB type="table" tableValues="0.2 0.4"/>
    </feComponentTransfer>
  </filter>
</svg>

<img src="photo.jpg" style="filter: url(#duotone)">
```

## 元件

### 背景
```css
.duotone-bg {
  background: linear-gradient(135deg, var(--duo-1-dark) 0%, var(--duo-1-light) 100%);
}
```

### 文字
```css
.duotone-text {
  color: var(--duo-1-light);
}

.duotone-text-dark {
  color: var(--duo-1-dark);
}
```

## 適用場景
- Spotify 風格
- 音樂活動
- 藝術展覽
- 創意品牌
