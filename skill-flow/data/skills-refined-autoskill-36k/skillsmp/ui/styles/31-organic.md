---
name: 有機風格
description: Organic - 自然曲線的有機設計
---

# 31. 有機風 Organic

## 概述
使用自然流動形狀的有機設計風格。

## 特徵
- 自然曲線
- 流動形狀
- 柔和色調
- 生命感

## 配色
```css
:root {
  --org-green: #4ade80;
  --org-brown: #a3a095;
  --org-cream: #faf7f2;
  --org-sage: #9caf88;
  --org-terracotta: #c4a77d;
}
```

## 有機形狀

### Blob 形狀
```css
.blob {
  border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
}

.blob-alt {
  border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
}
```

### 波浪效果
```css
.wave {
  position: relative;
}

.wave::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100px;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 100'%3E%3Cpath fill='%23fff' d='M0,50 C360,100 720,0 1080,50 C1260,75 1440,50 1440,50 L1440,100 L0,100 Z'/%3E%3C/svg%3E");
}
```

## 元件

### 卡片
```css
.organic-card {
  background: var(--org-cream);
  border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
  padding: 48px;
}
```

### 按鈕
```css
.organic-button {
  background: var(--org-sage);
  color: white;
  padding: 16px 32px;
  border-radius: 100px;
  font-weight: 500;
}
```

### 圖片容器
```css
.organic-image {
  border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
  overflow: hidden;
}
```

### 分隔線
```css
.organic-divider {
  height: 60px;
  background: url("data:image/svg+xml,...");
  background-size: cover;
}
```

## 適用場景
- 有機食品
- 健康生活
- 美容保養
- 環保品牌
