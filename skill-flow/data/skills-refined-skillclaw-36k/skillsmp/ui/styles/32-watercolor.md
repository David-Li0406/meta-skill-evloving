---
name: 水彩風格
description: Watercolor - 柔和暈染的手繪風格
---

# 32. 水彩風 Watercolor

## 概述
柔和、藝術感的手繪水彩風格設計。

## 特徵
- 柔和暈染
- 手繪感
- 自然色調
- 藝術氣息

## 配色
```css
:root {
  --wc-pink: #fce7f3;
  --wc-blue: #dbeafe;
  --wc-green: #dcfce7;
  --wc-yellow: #fef9c3;
  --wc-purple: #f3e8ff;
  --wc-text: #374151;
}
```

## 水彩效果

### 暈染背景
```css
.watercolor-bg {
  background: 
    radial-gradient(ellipse at 20% 30%, var(--wc-pink) 0%, transparent 50%),
    radial-gradient(ellipse at 70% 60%, var(--wc-blue) 0%, transparent 40%),
    radial-gradient(ellipse at 40% 80%, var(--wc-green) 0%, transparent 45%),
    #ffffff;
}
```

### 水彩邊框
```css
.watercolor-border {
  position: relative;
  padding: 2rem;
}

.watercolor-border::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--wc-pink), var(--wc-blue), var(--wc-green));
  border-radius: 20px;
  filter: blur(20px);
  opacity: 0.6;
  z-index: -1;
}
```

## 元件

### 卡片
```css
.wc-card {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 24px;
  padding: 32px;
  position: relative;
}

.wc-card::before {
  content: '';
  position: absolute;
  top: -10px;
  left: -10px;
  right: -10px;
  bottom: -10px;
  background: linear-gradient(45deg, var(--wc-pink), var(--wc-blue));
  border-radius: 34px;
  filter: blur(15px);
  opacity: 0.5;
  z-index: -1;
}
```

### 按鈕
```css
.wc-button {
  background: linear-gradient(135deg, #f472b6, #a78bfa);
  color: white;
  padding: 14px 32px;
  border-radius: 100px;
  font-weight: 500;
  box-shadow: 0 4px 15px rgba(244, 114, 182, 0.4);
}
```

## 適用場景
- 婚禮網站
- 藝術展覽
- 化妝品
- 花藝/園藝
