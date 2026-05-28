---
name: 復古風格
description: Retro - 80/90 年代懷舊設計
---

# 26. 復古風 Retro

## 概述
80/90 年代風格的懷舊設計。

## 特徵
- 霓虹色調
- 漸層效果
- 幾何圖案
- 復古字型

## 配色
```css
:root {
  --retro-pink: #ff71ce;
  --retro-blue: #01cdfe;
  --retro-green: #05ffa1;
  --retro-yellow: #fffb96;
  --retro-purple: #b967ff;
  --retro-dark: #1a1a2e;
}
```

## 字型
```css
h1, h2 {
  font-family: 'Monoton', cursive;
  /* 或 'Bungee', 'Press Start 2P' */
}
```

## 元件

### 霓虹文字
```css
.neon-text {
  color: var(--retro-pink);
  text-shadow:
    0 0 5px var(--retro-pink),
    0 0 10px var(--retro-pink),
    0 0 20px var(--retro-pink),
    0 0 40px var(--retro-pink);
}
```

### 漸層背景
```css
.retro-gradient {
  background: linear-gradient(
    180deg,
    var(--retro-dark) 0%,
    #16213e 50%,
    var(--retro-purple) 100%
  );
}
```

### 網格線
```css
.retro-grid {
  background-image: 
    linear-gradient(var(--retro-pink) 1px, transparent 1px),
    linear-gradient(90deg, var(--retro-pink) 1px, transparent 1px);
  background-size: 40px 40px;
  background-position: center center;
  perspective: 500px;
  transform: rotateX(60deg);
}
```

### 按鈕
```css
.retro-button {
  background: linear-gradient(var(--retro-pink), var(--retro-purple));
  color: white;
  padding: 14px 32px;
  border: 3px solid white;
  font-weight: 700;
  text-transform: uppercase;
}
```

## 適用場景
- 復古活動
- 音樂/演唱會
- 獨立遊戲
- 時尚品牌
