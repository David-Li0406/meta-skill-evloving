---
name: 波希米亞風格
description: Bohemian - 民族圖騰的自由風格
---

# 41. 波希米亞 Bohemian

## 概述
充滿民族風情、自由不羈的波希米亞設計。

## 特徵
- 民族圖騰
- 豐富色彩
- 手工質感
- 自由奔放

## 配色
```css
:root {
  --boho-terracotta: #c4a77d;
  --boho-rust: #a0522d;
  --boho-teal: #3d7068;
  --boho-gold: #b8860b;
  --boho-cream: #f5f0e6;
  --boho-purple: #6b4d57;
}
```

## 圖騰背景
```css
.boho-pattern {
  background-image: url('data:image/svg+xml,...');
  background-size: 60px 60px;
}
```

## 元件

### 卡片
```css
.boho-card {
  background: var(--boho-cream);
  border-radius: 0;
  padding: 32px;
  border-top: 4px solid var(--boho-terracotta);
  border-bottom: 4px solid var(--boho-terracotta);
}
```

### 分隔線
```css
.boho-divider {
  height: 20px;
  background: repeating-linear-gradient(
    90deg,
    var(--boho-terracotta) 0px,
    var(--boho-terracotta) 10px,
    var(--boho-teal) 10px,
    var(--boho-teal) 20px
  );
}
```

### 按鈕
```css
.boho-button {
  background: var(--boho-terracotta);
  color: var(--boho-cream);
  padding: 14px 32px;
  border: none;
  font-family: 'Cormorant Garamond', serif;
  letter-spacing: 0.15em;
}
```

### 標題
```css
.boho-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 3rem;
  font-weight: 400;
  color: var(--boho-rust);
}
```

## 適用場景
- 家居裝飾
- 手工藝品
- 旅遊冒險
- 生活風格
