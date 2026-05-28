---
name: 電商風
description: E-commerce - 商品導向的電商網站風格
---

# 13. 電商風 E-commerce

## 概述
以轉換率為導向，強調商品展示和購買流程。

## 特徵
- 商品圖片主導
- 明確 CTA
- 價格突出
- 信任標誌

## 配色
```css
:root {
  --ecom-primary: #ff6b00;    /* CTA 色 */
  --ecom-secondary: #1a1a1a;
  --ecom-success: #22c55e;    /* 促銷色 */
  --ecom-text: #333333;
  --ecom-bg: #f5f5f5;
  --ecom-sale: #ef4444;       /* 特價色 */
}
```

## 元件

### 商品卡片
```css
.product-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.product-image {
  aspect-ratio: 1;
  object-fit: cover;
}

.product-title {
  font-weight: 500;
  margin: 12px 0 8px;
}

.product-price {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--ecom-primary);
}

.product-original-price {
  text-decoration: line-through;
  color: #999;
  font-size: 0.875rem;
}
```

### CTA 按鈕
```css
.btn-add-cart {
  background: var(--ecom-primary);
  color: white;
  width: 100%;
  padding: 14px;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  font-size: 1rem;
}

.btn-buy-now {
  background: var(--ecom-secondary);
  color: white;
}
```

### 促銷標籤
```css
.sale-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  background: var(--ecom-sale);
  color: white;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}
```

## 適用場景
- 購物網站
- 品牌商城
- 市集平台
