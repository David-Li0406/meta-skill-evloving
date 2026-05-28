---
name: 科幻風格
description: Sci-Fi - 太空與未來科技的設計風格
---

# 44. 科幻風 Sci-Fi

## 概述
太空探索、未來科技的科幻設計風格。

## 特徵
- 太空元素
- 金屬質感
- 未來科技
- 星際氛圍

## 配色
```css
:root {
  --scifi-dark: #0a0a0f;
  --scifi-blue: #60a5fa;
  --scifi-silver: #94a3b8;
  --scifi-accent: #22d3ee;
  --scifi-glow: rgba(96, 165, 250, 0.3);
}
```

## 元件

### 星空背景
```css
.starfield {
  background: var(--scifi-dark);
  background-image: 
    radial-gradient(white 1px, transparent 1px),
    radial-gradient(white 1px, transparent 1px);
  background-size: 100px 100px, 50px 50px;
  background-position: 0 0, 25px 25px;
}
```

### 金屬質感
```css
.metallic {
  background: linear-gradient(
    135deg,
    #1a1a2e 0%,
    #3d3d5c 50%,
    #1a1a2e 100%
  );
  border: 1px solid var(--scifi-silver);
}
```

### HUD 風格
```css
.hud-frame {
  border: 1px solid var(--scifi-blue);
  position: relative;
  padding: 24px;
}

.hud-frame::before {
  content: '';
  position: absolute;
  top: -1px;
  left: 20px;
  right: 20px;
  height: 3px;
  background: var(--scifi-blue);
}

.hud-frame::after {
  content: 'SYSTEM ONLINE';
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--scifi-dark);
  padding: 0 12px;
  font-size: 10px;
  color: var(--scifi-blue);
  letter-spacing: 2px;
}
```

### 按鈕
```css
.scifi-button {
  background: transparent;
  color: var(--scifi-blue);
  border: 1px solid var(--scifi-blue);
  padding: 12px 32px;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-size: 12px;
  clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
}
```

## 適用場景
- 太空主題
- 科幻遊戲
- 科技展覽
- 未來概念
