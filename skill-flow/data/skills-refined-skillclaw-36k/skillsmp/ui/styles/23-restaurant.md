---
name: 餐飲風格
description: Restaurant - 溫暖美味的餐飲風格
---

# 23. 餐飲風 Restaurant

## 概述
溫暖、美味、有氛圍感的餐飲設計。

## 特徵
- 美食攝影
- 溫暖色調
- 氛圍營造
- 預約導向

## 配色
```css
:root {
  --resto-primary: #b45309;
  --resto-secondary: #78350f;
  --resto-cream: #fef3c7;
  --resto-dark: #1c1917;
  --resto-warm: #dc2626;
}
```

## 字型
```css
h1, h2 {
  font-family: 'Playfair Display', serif;
}

body {
  font-family: 'Lato', sans-serif;
}
```

## 元件

### Hero
```css
.resto-hero {
  min-height: 100vh;
  background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
              url('hero.jpg') center/cover;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
}

.resto-hero h1 {
  font-size: 4rem;
  font-weight: 400;
  letter-spacing: 0.1em;
}
```

### 菜單項目
```css
.menu-item {
  display: flex;
  justify-content: space-between;
  padding: 20px 0;
  border-bottom: 1px dashed #d4d4d4;
}

.menu-name {
  font-size: 1.125rem;
  font-weight: 500;
}

.menu-desc {
  color: #737373;
  font-size: 14px;
  margin-top: 4px;
}

.menu-price {
  font-weight: 600;
  color: var(--resto-primary);
}
```

### 預約按鈕
```css
.book-button {
  background: var(--resto-primary);
  color: white;
  padding: 16px 40px;
  font-size: 14px;
  letter-spacing: 2px;
  text-transform: uppercase;
}
```

## 適用場景
- 餐廳
- 咖啡廳
- 酒吧
- 烘焙坊
