---
name: 波普藝術
description: Pop Art - 漫畫風的鮮豔設計
---

# 30. 波普藝術 Pop Art

## 概述
受 Andy Warhol 等藝術家啟發的流行藝術風格。

## 特徵
- 漫畫風格
- 鮮豔飽和
- 網點效果
- 粗黑邊框

## 配色
```css
:root {
  --pop-red: #ff3b3b;
  --pop-yellow: #ffe135;
  --pop-blue: #0066ff;
  --pop-pink: #ff69b4;
  --pop-black: #000000;
  --pop-white: #ffffff;
}
```

## 網點效果
```css
.halftone {
  background: 
    radial-gradient(circle, var(--pop-black) 1px, transparent 1px);
  background-size: 4px 4px;
}

.halftone-large {
  background: 
    radial-gradient(circle, var(--pop-black) 2px, transparent 2px);
  background-size: 8px 8px;
}
```

## 元件

### 漫畫對話框
```css
.speech-bubble {
  background: var(--pop-white);
  border: 3px solid var(--pop-black);
  border-radius: 20px;
  padding: 20px;
  position: relative;
}

.speech-bubble::after {
  content: '';
  position: absolute;
  bottom: -20px;
  left: 30px;
  border: 10px solid transparent;
  border-top-color: var(--pop-black);
}
```

### 按鈕
```css
.pop-button {
  background: var(--pop-yellow);
  color: var(--pop-black);
  border: 3px solid var(--pop-black);
  padding: 16px 32px;
  font-weight: 900;
  font-size: 1.25rem;
  text-transform: uppercase;
  box-shadow: 4px 4px 0 var(--pop-black);
}

.pop-button:active {
  transform: translate(4px, 4px);
  box-shadow: none;
}
```

### 標題
```css
.pop-title {
  font-size: 4rem;
  font-weight: 900;
  text-transform: uppercase;
  color: var(--pop-red);
  -webkit-text-stroke: 3px var(--pop-black);
}
```

### 爆炸效果
```css
.pop-burst {
  background: var(--pop-yellow);
  clip-path: polygon(
    50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%,
    50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%
  );
  padding: 60px;
  text-align: center;
}
```

## 適用場景
- 藝術展覽
- 娛樂活動
- 時尚品牌
- 廣告行銷
