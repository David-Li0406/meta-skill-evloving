---
name: 插畫風格
description: Illustration - 自訂插圖的品牌識別風格
---

# 34. 插畫風 Illustration

## 概述
使用自訂插圖建立獨特品牌識別的設計風格。

## 特徵
- 原創插圖
- 故事性
- 品牌一致性
- 人性化

## 配色
```css
:root {
  --illus-primary: #5b6cf9;
  --illus-secondary: #ff7eb3;
  --illus-accent: #ffc145;
  --illus-bg: #fef9f3;
  --illus-text: #2d2d2d;
}
```

## 插圖風格建議

### 扁平插畫
- 無陰影或極少
- 簡單幾何形狀
- 有限色彩數量

### 等距插畫
- 2.5D 視角
- 適合展示流程/架構
- 科技感

### 線條插畫
- 細線條輪廓
- 極簡風格
- 優雅

### 漸層插畫
- 柔和漸層
- 現代感
- 豐富色彩

## 元件

### 特色區塊
```css
.feature-with-illus {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  align-items: center;
}

.feature-illus {
  max-width: 100%;
  height: auto;
}
```

### Hero 區塊
```css
.hero-illus {
  display: flex;
  align-items: center;
  min-height: 80vh;
  background: var(--illus-bg);
}

.hero-illus-image {
  flex: 1;
  max-width: 50%;
}

.hero-illus-content {
  flex: 1;
  padding: 48px;
}
```

## 插圖資源
- unDraw (免費)
- Storyset (免費)
- Blush (免費/付費)
- Humaaans (免費)

## 適用場景
- 科技新創
- 教育平台
- SaaS 產品
- 生活服務
