---
name: 醫療風格
description: Medical - 乾淨專業的醫療健康風格
---

# 19. 醫療風 Medical

## 概述
傳達專業、信任、乾淨的醫療健康設計。

## 特徵
- 藍綠色調
- 乾淨留白
- 專業圖片
- 無障礙優先

## 配色
```css
:root {
  --med-primary: #0891b2;
  --med-secondary: #14b8a6;
  --med-light: #f0fdfa;
  --med-dark: #134e4a;
  --med-white: #ffffff;
  --med-text: #1e293b;
}
```

## 元件

### 服務卡片
```css
.service-card {
  background: white;
  border-radius: 12px;
  padding: 32px;
  text-align: center;
  border: 1px solid #e2e8f0;
}

.service-icon {
  width: 64px;
  height: 64px;
  background: var(--med-light);
  border-radius: 50%;
  margin: 0 auto 16px;
}
```

### 醫師卡片
```css
.doctor-card {
  text-align: center;
}

.doctor-photo {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 16px;
}

.doctor-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--med-dark);
}

.doctor-specialty {
  color: var(--med-primary);
}
```

### CTA
```css
.med-button {
  background: var(--med-primary);
  color: white;
  padding: 14px 32px;
  border-radius: 8px;
  font-weight: 500;
}

.med-button-outline {
  background: transparent;
  color: var(--med-primary);
  border: 2px solid var(--med-primary);
}
```

## 適用場景
- 醫院/診所
- 健康服務
- 醫療設備
- 健康資訊平台
