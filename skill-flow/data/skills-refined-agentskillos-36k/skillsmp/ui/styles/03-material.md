---
name: 質感設計
description: Material Design - Google 風格的卡片式設計
---

# 03. 質感設計 Material Design

## 概述
Google 開發的設計語言，強調卡片、陰影層次和動效。

## 特徵
- 卡片式設計
- 層次陰影
- 漣漪動效
- 大膽用色

## 配色
```css
:root {
  --md-primary: #6200ee;
  --md-primary-variant: #3700b3;
  --md-secondary: #03dac6;
  --md-background: #ffffff;
  --md-surface: #ffffff;
  --md-error: #b00020;
  --md-on-primary: #ffffff;
  --md-on-secondary: #000000;
}
```

## 陰影系統
```css
.elevation-1 { box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); }
.elevation-2 { box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23); }
.elevation-3 { box-shadow: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23); }
.elevation-4 { box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22); }
```

## 卡片
```css
.md-card {
  background: var(--md-surface);
  border-radius: 4px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
}
```

## 按鈕
```css
.md-button {
  background: var(--md-primary);
  color: var(--md-on-primary);
  padding: 0 16px;
  height: 36px;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
```

## 適用場景
- Android 應用
- Google 風格產品
- Dashboard
