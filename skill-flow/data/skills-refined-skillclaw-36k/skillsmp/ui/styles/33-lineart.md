---
name: 線條藝術
description: Line Art - 細線條簡筆畫的優雅風格
---

# 33. 線條藝術 Line Art

## 概述
使用細線條繪製的簡約優雅設計。

## 特徵
- 細緻線條
- 簡筆風格
- 優雅留白
- 極簡美學

## 配色
```css
:root {
  --line-black: #1a1a1a;
  --line-white: #ffffff;
  --line-gray: #f5f5f5;
  --line-accent: #d4a574;
}
```

## 線條效果

### 基本線條
```css
.line-border {
  border: 1px solid var(--line-black);
}

.line-border-thin {
  border: 0.5px solid var(--line-black);
}
```

### 描邊動畫
```css
.line-draw {
  stroke-dasharray: 1000;
  stroke-dashoffset: 1000;
  animation: draw 2s ease forwards;
}

@keyframes draw {
  to {
    stroke-dashoffset: 0;
  }
}
```

## 元件

### 卡片
```css
.line-card {
  background: var(--line-white);
  border: 1px solid var(--line-black);
  padding: 32px;
}

.line-card-title {
  font-size: 1.5rem;
  font-weight: 300;
  letter-spacing: 0.1em;
}
```

### 按鈕
```css
.line-button {
  background: transparent;
  color: var(--line-black);
  border: 1px solid var(--line-black);
  padding: 12px 28px;
  font-weight: 400;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  transition: all 0.3s ease;
}

.line-button:hover {
  background: var(--line-black);
  color: var(--line-white);
}
```

### 分隔線
```css
.line-separator {
  display: flex;
  align-items: center;
  gap: 24px;
}

.line-separator::before,
.line-separator::after {
  content: '';
  flex: 1;
  height: 0.5px;
  background: var(--line-black);
}
```

### 圖標風格
```css
.line-icon {
  width: 48px;
  height: 48px;
  stroke: var(--line-black);
  stroke-width: 1;
  fill: none;
}
```

## 適用場景
- 設計師作品集
- 建築事務所
- 高端品牌
- 藝術畫廊
