---
name: 旅遊風格
description: Travel - 冒險大圖的旅遊觀光風格
---

# 24. 旅遊風 Travel

## 概述
冒險感、大圖背景的旅遊觀光設計。

## 特徵
- 大圖背景
- 目的地導向
- 搜尋優先
- 體驗展示

## 配色
```css
:root {
  --travel-primary: #0ea5e9;
  --travel-secondary: #14b8a6;
  --travel-accent: #f97316;
  --travel-dark: #0c4a6e;
  --travel-light: #f0f9ff;
}
```

## 元件

### Hero 搜尋
```css
.travel-hero {
  min-height: 70vh;
  background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.5)),
              url('destination.jpg') center/cover;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
}

.search-box {
  background: white;
  border-radius: 100px;
  padding: 8px;
  display: flex;
  gap: 8px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.search-input {
  border: none;
  padding: 16px 24px;
  font-size: 1rem;
  min-width: 200px;
}

.search-button {
  background: var(--travel-primary);
  color: white;
  padding: 16px 32px;
  border-radius: 100px;
  font-weight: 600;
}
```

### 目的地卡片
```css
.destination-card {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  aspect-ratio: 4/5;
}

.destination-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.destination-card:hover .destination-image {
  transform: scale(1.1);
}

.destination-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 24px;
  background: linear-gradient(transparent, rgba(0,0,0,0.8));
  color: white;
}
```

### 價格標籤
```css
.price-tag {
  background: var(--travel-accent);
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 700;
}
```

## 適用場景
- 旅行社
- 訂房平台
- 旅遊部落格
- 目的地行銷
