---
name: 奢華風
description: Luxury - 黑金配色的高端精緻風格
---

# 52. 奢華風 Luxury

## 概述
精緻、高端、尊榮的奢侈品牌設計風格。

## 特徵
- 黑金配色
- 精緻細節
- 優雅動效
- 高品質圖片

## 配色
```css
:root {
  --lux-black: #0a0a0a;
  --lux-gold: #c9a962;
  --lux-gold-light: #e8d5a3;
  --lux-white: #fafafa;
  --lux-gray: #888888;
}
```

## 字型
```css
body {
  font-family: 'Playfair Display', 'Noto Serif TC', serif;
}

h1, h2 {
  font-weight: 400;
  letter-spacing: 0.15em;
  text-transform: uppercase;
}

.accent-text {
  font-family: 'Cormorant Garamond', serif;
  font-style: italic;
}
```

## 元件

### 按鈕
```css
.lux-button {
  background: transparent;
  color: var(--lux-gold);
  border: 1px solid var(--lux-gold);
  padding: 16px 40px;
  font-size: 12px;
  letter-spacing: 3px;
  text-transform: uppercase;
  transition: all 0.3s ease;
}

.lux-button:hover {
  background: var(--lux-gold);
  color: var(--lux-black);
}
```

### 分隔線
```css
.lux-divider {
  width: 60px;
  height: 1px;
  background: var(--lux-gold);
  margin: 40px auto;
}
```

### 金色漸層
```css
.gold-gradient {
  background: linear-gradient(
    135deg,
    #c9a962 0%,
    #e8d5a3 50%,
    #c9a962 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

## 適用場景
- 珠寶/手錶
- 高端時尚
- 酒店/度假村
- 烈酒/香水
