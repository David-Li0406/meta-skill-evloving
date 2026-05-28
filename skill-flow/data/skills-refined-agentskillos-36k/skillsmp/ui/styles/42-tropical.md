---
name: 熱帶風格
description: Tropical - 熱帶植物的度假風格
---

# 42. 熱帶風 Tropical

## 概述
充滿熱帶植物、鮮豔色彩的度假風格。

## 特徵
- 熱帶植物
- 鮮豔色彩
- 度假氛圍
- 夏日活力

## 配色
```css
:root {
  --trop-green: #228b22;
  --trop-pink: #ff69b4;
  --trop-yellow: #ffd700;
  --trop-orange: #ff6347;
  --trop-blue: #40e0d0;
  --trop-cream: #fffaf0;
}
```

## 元件

### 植物邊框
```css
.tropical-frame {
  padding: 60px;
  background: var(--trop-cream);
  position: relative;
}

.tropical-frame::before,
.tropical-frame::after {
  content: '🌿';
  position: absolute;
  font-size: 80px;
}

.tropical-frame::before {
  top: 20px;
  left: 20px;
}

.tropical-frame::after {
  bottom: 20px;
  right: 20px;
  transform: rotate(180deg);
}
```

### 卡片
```css
.tropical-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0,0,0,0.1);
}

.tropical-card-header {
  background: linear-gradient(135deg, var(--trop-pink), var(--trop-orange));
  padding: 24px;
  color: white;
}
```

### 按鈕
```css
.tropical-button {
  background: linear-gradient(135deg, var(--trop-pink), var(--trop-yellow));
  color: white;
  padding: 16px 36px;
  border-radius: 100px;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(255, 105, 180, 0.4);
}
```

### 標籤
```css
.tropical-tag {
  background: var(--trop-green);
  color: white;
  padding: 6px 16px;
  border-radius: 100px;
  font-size: 14px;
  font-weight: 600;
}
```

## 適用場景
- 度假村
- 熱帶飲品
- 夏季活動
- 旅遊目的地
