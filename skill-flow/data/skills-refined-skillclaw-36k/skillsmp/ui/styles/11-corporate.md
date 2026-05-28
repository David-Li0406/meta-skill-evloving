---
name: 企業風
description: Corporate - 專業穩重的企業網站風格
---

# 11. 企業風 Corporate

## 概述
專業、穩重、值得信賴的企業形象設計。

## 特徵
- 藍色系為主
- 清晰的結構
- 專業攝影
- 標準化元件

## 配色
```css
:root {
  --corp-primary: #1e40af;
  --corp-secondary: #64748b;
  --corp-text: #1e293b;
  --corp-bg: #ffffff;
  --corp-light: #f8fafc;
}
```

## 字型
```css
body {
  font-family: 'Inter', 'Noto Sans TC', sans-serif;
}

h1, h2, h3 {
  font-weight: 600;
  color: var(--corp-text);
}
```

## 元件
```css
/* 專業按鈕 */
.corp-button {
  background: var(--corp-primary);
  color: white;
  padding: 12px 28px;
  border-radius: 6px;
  font-weight: 500;
}

/* 信任徽章 */
.trust-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--corp-secondary);
  font-size: 14px;
}

/* 統計數字 */
.stat-number {
  font-size: 3rem;
  font-weight: 700;
  color: var(--corp-primary);
}
```

## 適用場景
- 企業官網
- B2B 服務
- 金融機構
- 諮詢公司
