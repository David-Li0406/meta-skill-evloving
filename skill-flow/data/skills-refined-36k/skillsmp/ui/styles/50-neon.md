---
name: 霓虹風格
description: Neon - 發光霓虹管的視覺風格
---

# 50. 霓虹風 Neon

## 概述
霓虹燈管發光效果的視覺風格。

## 特徵
- 發光效果
- 深色背景
- 霓虹色彩
- 夜店氛圍

## 配色
```css
:root {
  --neon-bg: #0a0a0a;
  --neon-pink: #ff00ff;
  --neon-blue: #00ffff;
  --neon-green: #39ff14;
  --neon-yellow: #ffff00;
  --neon-orange: #ff6600;
}
```

## 發光效果

### 文字發光
```css
.neon-text-pink {
  color: var(--neon-pink);
  text-shadow:
    0 0 5px var(--neon-pink),
    0 0 10px var(--neon-pink),
    0 0 20px var(--neon-pink),
    0 0 40px var(--neon-pink),
    0 0 80px var(--neon-pink);
}

.neon-text-blue {
  color: var(--neon-blue);
  text-shadow:
    0 0 5px var(--neon-blue),
    0 0 10px var(--neon-blue),
    0 0 20px var(--neon-blue),
    0 0 40px var(--neon-blue);
}
```

### 閃爍動畫
```css
.neon-flicker {
  animation: neonFlicker 1.5s infinite alternate;
}

@keyframes neonFlicker {
  0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {
    text-shadow:
      0 0 5px var(--neon-pink),
      0 0 10px var(--neon-pink),
      0 0 20px var(--neon-pink),
      0 0 40px var(--neon-pink);
  }
  20%, 24%, 55% {
    text-shadow: none;
  }
}
```

### 邊框發光
```css
.neon-border {
  border: 2px solid var(--neon-blue);
  box-shadow:
    0 0 5px var(--neon-blue),
    0 0 10px var(--neon-blue),
    inset 0 0 5px var(--neon-blue);
}
```

### 按鈕
```css
.neon-button {
  background: transparent;
  color: var(--neon-pink);
  border: 2px solid var(--neon-pink);
  padding: 14px 32px;
  text-transform: uppercase;
  letter-spacing: 2px;
  box-shadow:
    0 0 5px var(--neon-pink),
    inset 0 0 5px var(--neon-pink);
  transition: all 0.3s ease;
}

.neon-button:hover {
  background: var(--neon-pink);
  color: var(--neon-bg);
  box-shadow:
    0 0 20px var(--neon-pink),
    0 0 40px var(--neon-pink);
}
```

## 適用場景
- 夜店/酒吧
- 音樂活動
- 遊戲
- 復古科幻
