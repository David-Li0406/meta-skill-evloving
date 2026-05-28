---
name: 健身風格
description: Fitness - 動感活力的健身運動風格
---

# 25. 健身風 Fitness

## 概述
動感、活力、激勵性的健身運動設計。

## 特徵
- 深色背景
- 鮮豔強調
- 動態效果
- 熱血氛圍

## 配色
```css
:root {
  --fit-dark: #0f0f0f;
  --fit-primary: #f97316;
  --fit-secondary: #22c55e;
  --fit-accent: #ef4444;
  --fit-white: #ffffff;
}
```

## 字型
```css
body {
  font-family: 'Oswald', 'Noto Sans TC', sans-serif;
}

h1, h2 {
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

## 元件

### Hero
```css
.fit-hero {
  min-height: 100vh;
  background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
              url('fitness.jpg') center/cover;
  display: flex;
  align-items: center;
  color: var(--fit-white);
}

.fit-hero h1 {
  font-size: 5rem;
  line-height: 1;
}

.fit-hero h1 span {
  color: var(--fit-primary);
}
```

### 課程卡片
```css
.class-card {
  background: #1a1a1a;
  border-radius: 16px;
  overflow: hidden;
  position: relative;
}

.class-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: var(--fit-primary);
}

.class-body {
  padding: 24px;
  color: var(--fit-white);
}

.class-time {
  color: var(--fit-primary);
  font-weight: 700;
}
```

### CTA 按鈕
```css
.fit-button {
  background: var(--fit-primary);
  color: var(--fit-white);
  padding: 18px 48px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  clip-path: polygon(0 0, 100% 0, 95% 100%, 5% 100%);
}
```

## 適用場景
- 健身房
- 運動品牌
- 健身教練
- 運動課程
