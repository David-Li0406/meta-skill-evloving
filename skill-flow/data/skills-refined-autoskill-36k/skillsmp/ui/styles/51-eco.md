---
name: 環保風格
description: Eco/Green - 自然環保的綠色風格
---

# 51. 環保風 Eco/Green

## 概述
傳達自然、永續、環保理念的設計風格。

## 特徵
- 綠色調
- 自然元素
- 有機形狀
- 永續訊息

## 配色
```css
:root {
  --eco-green: #22c55e;
  --eco-dark: #15803d;
  --eco-light: #f0fdf4;
  --eco-earth: #78716c;
  --eco-sand: #faf5f0;
  --eco-leaf: #4ade80;
}
```

## 元件

### 特色區塊
```css
.eco-feature {
  background: var(--eco-light);
  border-radius: 24px;
  padding: 40px;
  position: relative;
  overflow: hidden;
}

.eco-feature::before {
  content: '🌿';
  position: absolute;
  font-size: 100px;
  opacity: 0.1;
  right: -20px;
  bottom: -20px;
}
```

### 統計數字
```css
.eco-stat {
  text-align: center;
}

.eco-stat-number {
  font-size: 3rem;
  font-weight: 700;
  color: var(--eco-dark);
}

.eco-stat-label {
  color: var(--eco-earth);
}
```

### 按鈕
```css
.eco-button {
  background: var(--eco-green);
  color: white;
  padding: 14px 32px;
  border-radius: 50px;
  font-weight: 600;
}

.eco-button-outline {
  background: transparent;
  color: var(--eco-dark);
  border: 2px solid var(--eco-dark);
}
```

### 有機形狀
```css
.organic-shape {
  border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
}
```

## 適用場景
- 環保組織
- 有機食品
- 永續品牌
- 綠能科技
