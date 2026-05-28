---
name: 古典復古
description: Vintage - 舊紙張質感的懷舊風格
---

# 27. 古典復古 Vintage

## 概述
帶有歲月感和舊時代魅力的懷舊設計。

## 特徵
- 泛黃質感
- 舊照片風格
- 復古字型
- 懷舊氛圍

## 配色
```css
:root {
  --vintage-cream: #faf6e9;
  --vintage-brown: #8b7355;
  --vintage-sepia: #d4a574;
  --vintage-dark: #3d3027;
  --vintage-rust: #a0522d;
}
```

## 字型
```css
h1, h2 {
  font-family: 'Playfair Display', serif;
}

body {
  font-family: 'Crimson Text', Georgia, serif;
}
```

## 紙張質感
```css
.vintage-paper {
  background: var(--vintage-cream);
  background-image: url("data:image/svg+xml,..."); /* 紙張紋理 */
  box-shadow: 
    inset 0 0 50px rgba(139, 115, 85, 0.1),
    0 0 20px rgba(0,0,0,0.1);
}
```

## 元件

### 老照片效果
```css
.vintage-photo {
  filter: sepia(50%) contrast(90%) brightness(90%);
  border: 8px solid white;
  box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}
```

### 徽章
```css
.vintage-badge {
  border: 2px solid var(--vintage-brown);
  border-radius: 100px;
  padding: 8px 24px;
  font-family: 'Playfair Display', serif;
  font-style: italic;
  color: var(--vintage-brown);
}
```

### 按鈕
```css
.vintage-button {
  background: var(--vintage-brown);
  color: var(--vintage-cream);
  padding: 12px 28px;
  border: none;
  font-family: 'Playfair Display', serif;
  letter-spacing: 0.1em;
}
```

### 分隔線
```css
.vintage-rule {
  border: none;
  height: 1px;
  background: linear-gradient(
    90deg,
    transparent,
    var(--vintage-brown),
    transparent
  );
  margin: 40px 0;
}
```

## 適用場景
- 咖啡廳
- 古董店
- 歷史網站
- 傳統工藝
