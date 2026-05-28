---
name: 極簡風
description: Minimal - 少即是多的設計哲學
---

# 01. 極簡風 Minimal

## 概述

極簡主義設計遵循「少即是多」(Less is More) 的哲學，透過移除不必要的元素，讓重要內容脫穎而出。這種風格強調功能性、清晰度和大量留白。

### 核心特徵

- **大量留白**：空間本身就是設計元素
- **簡潔線條**：清晰、俐落的視覺邊界
- **有限配色**：通常只有 2-3 種顏色
- **功能優先**：每個元素都有存在的理由
- **隱藏複雜性**：簡化介面但不簡化功能

---

## 視覺特徵

### 形狀與線條
- 幾何形狀：矩形、圓形
- 細線條分隔
- 無過多裝飾

### 陰影與層次
- 極少或無陰影
- 平面設計
- 透過留白區分層次

### 材質與紋理
- 純色背景
- 無紋理
- 偶爾使用細微漸層

---

## 配色方案

### 經典配色

```css
:root {
  /* 主色調 - 黑白灰 */
  --color-primary: #000000;
  --color-secondary: #ffffff;
  --color-accent: #1a1a1a;
  
  /* 灰階 */
  --color-gray-100: #f7f7f7;
  --color-gray-200: #e5e5e5;
  --color-gray-300: #d4d4d4;
  --color-gray-500: #737373;
  --color-gray-700: #404040;
  --color-gray-900: #171717;
  
  /* 可選強調色 */
  --color-highlight: #0066cc; /* 藍色 */
}
```

### 替代配色

| 方案 | 主色 | 背景 | 強調 |
|-----|------|-----|------|
| 純黑白 | #000 | #fff | - |
| 暖極簡 | #333 | #faf9f6 | #b8860b |
| 冷極簡 | #1a1a2e | #f8f9fa | #0066cc |
| 綠極簡 | #1a1a1a | #f5f7f5 | #2d5a27 |

---

## 字型建議

### 推薦字型

**西文：**
- Helvetica Neue / Helvetica
- Inter
- SF Pro
- Roboto
- Arial

**中文：**
- 思源黑體 (Noto Sans TC)
- 蘋方 (PingFang)
- 微軟雅黑

### 字型設定

```css
:root {
  --font-family: 'Inter', 'Noto Sans TC', -apple-system, sans-serif;
  
  /* 字型大小 */
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.25rem;
  --text-xl: 1.5rem;
  --text-2xl: 2rem;
  --text-3xl: 3rem;
  
  /* 字重 */
  --font-light: 300;
  --font-normal: 400;
  --font-medium: 500;
  --font-bold: 700;
}

h1 {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  letter-spacing: -0.02em;
  line-height: 1.2;
}

p {
  font-size: var(--text-base);
  font-weight: var(--font-normal);
  line-height: 1.7;
  color: var(--color-gray-700);
}
```

---

## 元件樣式

### 按鈕

```css
/* 主要按鈕 */
.btn-primary {
  background: var(--color-primary);
  color: var(--color-secondary);
  padding: 0.875rem 2rem;
  border: none;
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  letter-spacing: 0.05em;
  text-transform: uppercase;
  cursor: pointer;
  transition: opacity 0.2s ease;
}

.btn-primary:hover {
  opacity: 0.85;
}

/* 次要按鈕 */
.btn-secondary {
  background: transparent;
  color: var(--color-primary);
  padding: 0.875rem 2rem;
  border: 1px solid var(--color-primary);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  letter-spacing: 0.05em;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: var(--color-primary);
  color: var(--color-secondary);
}
```

### 卡片

```css
.card {
  background: var(--color-secondary);
  padding: 2rem;
  border: 1px solid var(--color-gray-200);
}

.card-title {
  font-size: var(--text-lg);
  font-weight: var(--font-medium);
  margin-bottom: 0.75rem;
}

.card-text {
  font-size: var(--text-sm);
  color: var(--color-gray-500);
  line-height: 1.6;
}
```

### 導航

```css
.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid var(--color-gray-200);
}

.nav-logo {
  font-size: var(--text-lg);
  font-weight: var(--font-bold);
  letter-spacing: -0.02em;
}

.nav-links {
  display: flex;
  gap: 2.5rem;
}

.nav-link {
  font-size: var(--text-sm);
  color: var(--color-gray-700);
  text-decoration: none;
  transition: color 0.2s ease;
}

.nav-link:hover {
  color: var(--color-primary);
}
```

### 表單輸入

```css
.input {
  width: 100%;
  padding: 0.875rem 1rem;
  font-size: var(--text-base);
  border: 1px solid var(--color-gray-300);
  background: transparent;
  transition: border-color 0.2s ease;
}

.input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.input::placeholder {
  color: var(--color-gray-500);
}
```

---

## 動態效果

### 建議

- **少量動畫**：僅用於必要的回饋
- **簡單過渡**：fade、slide
- **速度適中**：200-300ms
- **避免**：彈跳、旋轉、過多動態

### CSS 過渡

```css
/* 基本過渡 */
.transition-base {
  transition: all 0.2s ease;
}

/* 滑入效果 */
.fade-in {
  animation: fadeIn 0.3s ease forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

---

## 佈局特點

### 網格系統

```css
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 2rem;
}

/* 大量留白 */
section {
  padding: 6rem 0;
}
```

### 留白比例

- 區塊間距：至少 80-120px
- 元件間距：24-48px
- 文字與邊界：適當的呼吸空間

---

## 適用場景

### 推薦產業
- 設計/創意工作室
- 高端品牌
- 建築事務所
- 藝廊/美術館
- 科技公司
- 個人作品集

### 品牌調性
- 專業、高端
- 現代、簡潔
- 優雅、克制

### 目標受眾
- 設計敏感者
- 追求品質者
- 專業人士

---

## 注意事項

### 優點
✅ 永不過時
✅ 載入速度快
✅ 專注於內容
✅ 高端質感

### 挑戰
⚠️ 需要高品質內容支撐
⚠️ 可能顯得「空洞」若無好內容
⚠️ 不適合資訊量大的網站
⚠️ 需要精確的細節處理

---

## 完整 CSS 範本

```css
/* 極簡風基礎樣式 */
:root {
  --color-primary: #000000;
  --color-secondary: #ffffff;
  --color-gray-200: #e5e5e5;
  --color-gray-500: #737373;
  --color-gray-700: #404040;
  
  --font-family: 'Inter', 'Noto Sans TC', sans-serif;
  --space-unit: 1rem;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-family);
  font-size: 1rem;
  line-height: 1.7;
  color: var(--color-gray-700);
  background: var(--color-secondary);
}

h1, h2, h3, h4, h5, h6 {
  color: var(--color-primary);
  font-weight: 500;
  line-height: 1.3;
  margin-bottom: 1rem;
}

a {
  color: inherit;
  text-decoration: none;
}

img {
  max-width: 100%;
  height: auto;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

section {
  padding: 6rem 0;
}

section + section {
  border-top: 1px solid var(--color-gray-200);
}
```
