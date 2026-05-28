---
name: 作品集風格
description: Portfolio - 視覺主導的展示型風格
---

# 16. 作品集 Portfolio

## 概述
以視覺展示為主的個人或機構作品集設計。

## 特徵
- 大圖展示
- 極簡導航
- 作品優先
- 微妙動效

## 配色
```css
:root {
  --port-bg: #0a0a0a;
  --port-white: #ffffff;
  --port-gray: #888888;
  --port-accent: #ff4444;
}
```

## 佈局
```css
.portfolio-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2px;
}

.portfolio-item {
  aspect-ratio: 16/10;
  overflow: hidden;
  position: relative;
}

.portfolio-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.portfolio-item:hover img {
  transform: scale(1.05);
}

.portfolio-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.portfolio-item:hover .portfolio-overlay {
  opacity: 1;
}
```

## 導航
```css
.portfolio-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  padding: 24px 40px;
  display: flex;
  justify-content: space-between;
  z-index: 100;
  mix-blend-mode: difference;
}

.portfolio-nav a {
  color: white;
  text-decoration: none;
}
```

## 適用場景
- 設計師
- 攝影師
- 創意機構
- 藝術家
