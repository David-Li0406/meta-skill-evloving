---
name: 日式禪風
description: Japanese Zen - 禪意留白的和風設計
---

# 36. 日式禪風 Japanese Zen

## 概述
融合日本美學與禪意的極簡設計風格。

## 特徵
- 大量留白（間）
- 自然材質感
- 非對稱平衡
- 細膩細節

## 配色
```css
:root {
  --zen-white: #faf8f5;
  --zen-black: #1a1a1a;
  --zen-gray: #8c8c8c;
  --zen-beige: #d4c5b5;
  --zen-red: #bc002d;  /* 日本紅 */
  --zen-gold: #c9a962;
}
```

## 字型
```css
body {
  font-family: 'Noto Serif TC', 'Hiragino Mincho ProN', serif;
  letter-spacing: 0.05em;
  line-height: 2;
}
```

## 元件

### 分隔線
```css
.zen-divider {
  width: 1px;
  height: 60px;
  background: var(--zen-black);
  margin: 60px auto;
}
```

### 直書文字
```css
.vertical-text {
  writing-mode: vertical-rl;
  text-orientation: mixed;
}
```

### 按鈕
```css
.zen-button {
  background: transparent;
  color: var(--zen-black);
  border: 1px solid var(--zen-black);
  padding: 12px 32px;
  font-size: 13px;
  letter-spacing: 0.2em;
}
```

## 適用場景
- 日本料理
- 溫泉旅館
- 茶道/花道
- 藝術展覽
