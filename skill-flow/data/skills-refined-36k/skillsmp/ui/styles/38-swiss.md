---
name: 瑞士風格
description: Swiss/International - 網格系統的精準設計
---

# 38. 瑞士風 Swiss/International

## 概述
源自瑞士的國際平面設計風格，強調網格和無襯線字體。

## 特徵
- 嚴謹網格
- 無襯線字型
- 客觀清晰
- 數學比例

## 配色
```css
:root {
  --swiss-black: #000000;
  --swiss-white: #ffffff;
  --swiss-red: #ff0000;
  --swiss-gray: #666666;
}
```

## 字型
```css
body {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

h1, h2, h3 {
  font-weight: 700;
  letter-spacing: -0.02em;
}
```

## 網格系統
```css
.swiss-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 20px;
}

.swiss-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 40px;
}
```

## 元件

### 標題
```css
.swiss-headline {
  font-size: 6rem;
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.03em;
}

.swiss-subhead {
  font-size: 1.25rem;
  font-weight: 400;
  color: var(--swiss-gray);
  max-width: 50ch;
}
```

### 分隔線
```css
.swiss-rule {
  height: 2px;
  background: var(--swiss-black);
  margin: 40px 0;
}
```

### 按鈕
```css
.swiss-button {
  background: var(--swiss-black);
  color: var(--swiss-white);
  padding: 16px 32px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-size: 14px;
}
```

### 編號列表
```css
.swiss-list-item {
  display: grid;
  grid-template-columns: 60px 1fr;
  gap: 20px;
  padding: 20px 0;
  border-top: 1px solid var(--swiss-black);
}

.swiss-number {
  font-size: 1.5rem;
  font-weight: 700;
}
```

## 適用場景
- 建築事務所
- 設計公司
- 博物館
- 企業報告
