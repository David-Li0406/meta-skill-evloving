---
name: 亮白模式
description: Light Mode - 純白清新的設計風格
---

# 09. 亮白模式 Light Mode

## 概述
以純白為主的清新專業設計風格。

## 特徵
- 純白背景
- 清新明亮
- 微妙陰影
- 專業感

## 配色
```css
:root {
  --light-bg: #ffffff;
  --light-surface: #f8fafc;
  --light-border: #e2e8f0;
  --light-text: #1e293b;
  --light-secondary: #64748b;
  --light-primary: #3b82f6;
}
```

## 元件

### 卡片
```css
.light-card {
  background: var(--light-bg);
  border: 1px solid var(--light-border);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.light-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
```

### 按鈕
```css
.light-button {
  background: var(--light-primary);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 500;
}

.light-button-secondary {
  background: var(--light-surface);
  color: var(--light-text);
  border: 1px solid var(--light-border);
}
```

### 輸入框
```css
.light-input {
  background: var(--light-bg);
  border: 1px solid var(--light-border);
  border-radius: 8px;
  padding: 12px 16px;
  color: var(--light-text);
}

.light-input:focus {
  border-color: var(--light-primary);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
```

### 導航
```css
.light-nav {
  background: var(--light-bg);
  border-bottom: 1px solid var(--light-border);
  padding: 16px 24px;
}
```

## 適用場景
- 企業官網
- SaaS 產品
- 文件網站
- 專業服務
