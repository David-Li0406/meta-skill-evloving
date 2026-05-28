---
name: 金融風格
description: Finance - 穩重安全的金融設計風格
---

# 21. 金融風 Finance

## 概述
傳達專業、安全、值得信賴的金融設計。

## 特徵
- 藍綠色調
- 數據圖表
- 專業嚴謹
- 安全信任

## 配色
```css
:root {
  --fin-primary: #0f766e;
  --fin-secondary: #1e40af;
  --fin-success: #16a34a;
  --fin-danger: #dc2626;
  --fin-dark: #0f172a;
  --fin-light: #f8fafc;
}
```

## 元件

### 數據卡片
```css
.finance-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  border: 1px solid #e2e8f0;
}

.finance-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--fin-dark);
}

.finance-change {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  font-weight: 500;
}

.finance-change.positive {
  color: var(--fin-success);
}

.finance-change.negative {
  color: var(--fin-danger);
}
```

### 信任標誌
```css
.trust-badges {
  display: flex;
  gap: 32px;
  justify-content: center;
  padding: 24px;
  background: var(--fin-light);
}

.trust-badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--fin-dark);
}
```

### 按鈕
```css
.finance-button {
  background: var(--fin-primary);
  color: white;
  padding: 14px 32px;
  border-radius: 8px;
  font-weight: 600;
}

.finance-button-secure {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.finance-button-secure::before {
  content: '🔒';
}
```

## 適用場景
- 銀行
- 投資平台
- 保險公司
- 金融科技
