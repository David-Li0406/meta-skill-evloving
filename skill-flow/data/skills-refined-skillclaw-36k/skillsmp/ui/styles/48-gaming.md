---
name: 遊戲風格
description: Gaming - 動態炫酷的遊戲網站風格
---

# 48. 遊戲風 Gaming

## 概述
動態、炫酷、沉浸式的遊戲產業設計。

## 特徵
- 深色背景
- 鮮豔強調色
- 動態效果
- 電競元素

## 配色
```css
:root {
  --game-bg: #0d0d0d;
  --game-surface: #1a1a1a;
  --game-red: #ff4655;
  --game-blue: #00d4ff;
  --game-yellow: #ffd700;
  --game-green: #00ff87;
}
```

## 字型
```css
body {
  font-family: 'Rajdhani', 'Noto Sans TC', sans-serif;
}

h1, h2 {
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}
```

## 元件

### 斜切邊角
```css
.game-card {
  background: var(--game-surface);
  clip-path: polygon(0 0, calc(100% - 20px) 0, 100% 20px, 100% 100%, 20px 100%, 0 calc(100% - 20px));
  padding: 24px;
}
```

### 發光邊框
```css
.game-border {
  border: 2px solid var(--game-red);
  box-shadow: 
    0 0 10px var(--game-red),
    inset 0 0 10px rgba(255, 70, 85, 0.1);
}
```

### 按鈕
```css
.game-button {
  background: linear-gradient(135deg, var(--game-red), #ff0040);
  color: white;
  padding: 16px 40px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
}
```

### 閃爍動畫
```css
.glitch-text {
  animation: glitch 2s infinite;
}

@keyframes glitch {
  0%, 90% { text-shadow: none; }
  91% { text-shadow: -2px 0 var(--game-red), 2px 0 var(--game-blue); }
  92% { text-shadow: 2px 0 var(--game-red), -2px 0 var(--game-blue); }
  93%, 100% { text-shadow: none; }
}
```

## 適用場景
- 遊戲官網
- 電競戰隊
- 遊戲直播
- 電競賽事
