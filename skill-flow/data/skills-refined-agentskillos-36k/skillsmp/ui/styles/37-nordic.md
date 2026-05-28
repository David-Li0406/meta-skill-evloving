---
name: 北歐風
description: Scandinavian - 自然、溫暖的功能美學
---

# 37. 北歐風 Scandinavian

## 概述
簡約、溫暖、功能性的北歐設計美學。

## 特徵
- 自然色調
- 大量留白
- 溫暖質感
- 功能優先

## 配色
```css
:root {
  --nordic-bg: #faf9f6;
  --nordic-sand: #e8e2d9;
  --nordic-wood: #c4a77d;
  --nordic-forest: #4a5c4e;
  --nordic-text: #2c2c2c;
  --nordic-accent: #8b7355;
}
```

## 元件

### 卡片
```css
.nordic-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  border: 1px solid var(--nordic-sand);
}
```

### 按鈕
```css
.nordic-button {
  background: var(--nordic-text);
  color: white;
  padding: 14px 28px;
  border: none;
  border-radius: 100px;
  font-weight: 500;
}

.nordic-button-outline {
  background: transparent;
  color: var(--nordic-text);
  border: 1.5px solid var(--nordic-text);
}
```

### 字型
```css
body {
  font-family: 'DM Sans', 'Noto Sans TC', sans-serif;
  color: var(--nordic-text);
  line-height: 1.7;
}

h1, h2, h3 {
  font-weight: 500;
  letter-spacing: -0.02em;
}
```

## 適用場景
- 生活風格品牌
- 傢俱/家居
- 咖啡廳
- 設計工作室
