---
name: 賽博龐克
description: Cyberpunk - 霓虹、高對比的未來都市風格
---

# 43. 賽博龐克 Cyberpunk

## 概述
霓虹色、高對比的未來都市科幻風格。

## 特徵
- 深黑背景
- 霓虹發光色
- 高對比
- 科技 UI 元素
- 故障效果

## 配色
```css
:root {
  --cyber-bg: #0a0a0a;
  --cyber-surface: #1a1a2e;
  --cyber-cyan: #00fff5;
  --cyber-pink: #ff00ff;
  --cyber-yellow: #ffff00;
  --cyber-blue: #00d4ff;
}
```

## 霓虹發光
```css
.neon-cyan {
  color: var(--cyber-cyan);
  text-shadow: 
    0 0 5px var(--cyber-cyan),
    0 0 10px var(--cyber-cyan),
    0 0 20px var(--cyber-cyan);
}

.neon-pink {
  color: var(--cyber-pink);
  text-shadow: 
    0 0 5px var(--cyber-pink),
    0 0 10px var(--cyber-pink),
    0 0 20px var(--cyber-pink);
}
```

## 邊框發光
```css
.cyber-border {
  border: 1px solid var(--cyber-cyan);
  box-shadow: 
    0 0 10px var(--cyber-cyan),
    inset 0 0 10px rgba(0, 255, 245, 0.1);
}
```

## 故障效果
```css
.glitch {
  animation: glitch 1s infinite;
}

@keyframes glitch {
  0%, 90%, 100% { transform: translate(0); }
  92% { transform: translate(-2px, 2px); }
  94% { transform: translate(2px, -2px); }
  96% { transform: translate(-2px, -2px); }
  98% { transform: translate(2px, 2px); }
}
```

## 按鈕
```css
.cyber-button {
  background: transparent;
  color: var(--cyber-cyan);
  border: 2px solid var(--cyber-cyan);
  padding: 12px 32px;
  text-transform: uppercase;
  letter-spacing: 2px;
  position: relative;
  clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 10px, 100% 100%, 10px 100%, 0 calc(100% - 10px));
}
```

## 適用場景
- 遊戲網站
- 音樂活動
- 科技產品
- 娛樂產業
