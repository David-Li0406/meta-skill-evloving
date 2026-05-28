---
name: 漸層風格
description: Gradient - 多彩漸層的視覺衝擊風格
---

# 07. 漸層風 Gradient

## 概述
使用豐富漸層色創造視覺衝擊力。

## 特徵
- 多彩漸層
- 鮮豔配色
- 現代感
- 動態變化

## 常用漸層
```css
:root {
  --grad-sunset: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  --grad-ocean: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --grad-mint: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  --grad-fire: linear-gradient(135deg, #f12711 0%, #f5af19 100%);
  --grad-night: linear-gradient(135deg, #0c3483 0%, #a2b6df 100%);
  --grad-candy: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
}
```

## 元件

### 漸層背景
```css
.gradient-bg {
  background: var(--grad-ocean);
  min-height: 100vh;
}
```

### 漸層文字
```css
.gradient-text {
  background: var(--grad-sunset);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

### 漸層按鈕
```css
.gradient-button {
  background: var(--grad-ocean);
  color: white;
  border: none;
  padding: 14px 32px;
  border-radius: 50px;
  font-weight: 600;
}

.gradient-button:hover {
  background: var(--grad-sunset);
}
```

### 漸層邊框
```css
.gradient-border {
  position: relative;
  background: white;
  padding: 24px;
}

.gradient-border::before {
  content: '';
  position: absolute;
  inset: -2px;
  background: var(--grad-ocean);
  border-radius: inherit;
  z-index: -1;
}
```

## 動態漸層
```css
.animated-gradient {
  background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
  background-size: 400% 400%;
  animation: gradientMove 15s ease infinite;
}

@keyframes gradientMove {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
```

## 適用場景
- 音樂/娛樂
- 創意產品
- 年輕品牌
- 行銷活動
