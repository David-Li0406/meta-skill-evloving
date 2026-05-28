---
name: 裝飾藝術
description: Art Deco - 對稱幾何的 1920 年代奢華風格
---

# 28. 裝飾藝術 Art Deco

## 概述
源自 1920 年代的奢華裝飾主義設計風格。

## 特徵
- 對稱幾何
- 金色裝飾
- 奢華感
- 線條圖案

## 配色
```css
:root {
  --deco-gold: #d4af37;
  --deco-black: #0d0d0d;
  --deco-cream: #f5f0e6;
  --deco-navy: #1a1a2e;
  --deco-emerald: #2d5a27;
}
```

## 字型
```css
h1, h2, h3 {
  font-family: 'Playfair Display', serif;
  font-weight: 400;
  letter-spacing: 0.2em;
}
```

## 元件

### 邊框裝飾
```css
.deco-frame {
  border: 2px solid var(--deco-gold);
  padding: 40px;
  position: relative;
}

.deco-frame::before,
.deco-frame::after {
  content: '';
  position: absolute;
  width: 20px;
  height: 20px;
  border: 2px solid var(--deco-gold);
}

.deco-frame::before {
  top: 10px;
  left: 10px;
  border-right: none;
  border-bottom: none;
}

.deco-frame::after {
  bottom: 10px;
  right: 10px;
  border-left: none;
  border-top: none;
}
```

### 分隔線
```css
.deco-divider {
  display: flex;
  align-items: center;
  gap: 20px;
}

.deco-divider::before,
.deco-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--deco-gold);
}

.deco-divider-icon {
  color: var(--deco-gold);
}
```

### 按鈕
```css
.deco-button {
  background: transparent;
  color: var(--deco-gold);
  border: 2px solid var(--deco-gold);
  padding: 16px 40px;
  font-size: 12px;
  letter-spacing: 0.3em;
  text-transform: uppercase;
}

.deco-button:hover {
  background: var(--deco-gold);
  color: var(--deco-black);
}
```

## 適用場景
- 高端酒店
- 奢侈品牌
- 婚禮策劃
- 復古活動
