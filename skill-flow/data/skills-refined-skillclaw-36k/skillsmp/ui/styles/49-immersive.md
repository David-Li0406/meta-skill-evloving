---
name: VR/AR 風格
description: Immersive - 沉浸式體驗的視覺風格
---

# 49. VR/AR 風 Immersive

## 概述
展現沉浸式體驗、虛擬實境的科技視覺風格。

## 特徵
- 空間感
- 沉浸體驗
- 3D 元素
- 互動導向

## 配色
```css
:root {
  --vr-dark: #0a0a0f;
  --vr-primary: #8b5cf6;
  --vr-secondary: #06b6d4;
  --vr-glow: rgba(139, 92, 246, 0.5);
}
```

## 元件

### 光暈效果
```css
.vr-glow {
  box-shadow:
    0 0 20px var(--vr-glow),
    0 0 40px var(--vr-glow),
    0 0 60px var(--vr-glow);
}
```

### 漸層邊框
```css
.vr-border {
  position: relative;
  background: var(--vr-dark);
  border-radius: 16px;
  padding: 2px;
}

.vr-border::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 16px;
  padding: 2px;
  background: linear-gradient(135deg, var(--vr-primary), var(--vr-secondary));
  -webkit-mask: 
    linear-gradient(#fff 0 0) content-box, 
    linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
}
```

### 動態背景
```css
.vr-bg {
  background: radial-gradient(
    ellipse at center,
    var(--vr-primary) 0%,
    var(--vr-dark) 70%
  );
  animation: pulse-bg 4s ease-in-out infinite;
}

@keyframes pulse-bg {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}
```

### 按鈕
```css
.vr-button {
  background: linear-gradient(135deg, var(--vr-primary), var(--vr-secondary));
  color: white;
  padding: 16px 40px;
  border-radius: 100px;
  font-weight: 600;
  box-shadow: 0 0 20px var(--vr-glow);
}
```

### 3D 卡片
```css
.vr-card {
  transform-style: preserve-3d;
  perspective: 1000px;
}

.vr-card:hover {
  transform: rotateY(5deg) rotateX(5deg);
}
```

## 適用場景
- VR/AR 產品
- 遊戲
- 元宇宙
- 互動體驗
