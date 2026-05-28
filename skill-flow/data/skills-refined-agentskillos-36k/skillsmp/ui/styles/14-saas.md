---
name: SaaS 風格
description: SaaS - 軟體服務產品的現代風格
---

# 14. SaaS 風格

## 概述
現代軟體服務產品的標準設計風格。

## 特徵
- 功能展示區塊
- 定價表
- 客戶證言
- 清晰 CTA

## 配色
```css
:root {
  --saas-primary: #6366f1;
  --saas-secondary: #8b5cf6;
  --saas-dark: #1e1b4b;
  --saas-light: #f8fafc;
  --saas-success: #22c55e;
}
```

## 元件

### Hero 區塊
```css
.saas-hero {
  text-align: center;
  padding: 120px 20px;
  background: linear-gradient(135deg, var(--saas-primary), var(--saas-secondary));
  color: white;
}

.saas-hero h1 {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 24px;
}
```

### 定價卡片
```css
.pricing-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  text-align: center;
  border: 1px solid #e5e7eb;
}

.pricing-card.popular {
  border: 2px solid var(--saas-primary);
  transform: scale(1.05);
}

.pricing-price {
  font-size: 3rem;
  font-weight: 700;
}
```

### 功能列表
```css
.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 24px;
}

.feature-icon {
  width: 48px;
  height: 48px;
  background: rgba(99, 102, 241, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

## 適用場景
- 軟體產品
- API 服務
- 雲端平台
- 生產力工具
