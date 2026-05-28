---
name: 科技極簡風格
description: Tech Minimal - 科技感的極簡設計
---

# 45. 科技極簡 Tech Minimal

## 概述
結合科技感與極簡主義的現代設計。

## 特徵
- 幾何圖形
- 精準網格
- 科技元素
- 簡潔介面

## 配色
```css
:root {
  --tech-black: #0a0a0a;
  --tech-white: #fafafa;
  --tech-gray: #71717a;
  --tech-accent: #3b82f6;
  --tech-glow: rgba(59, 130, 246, 0.5);
}
```

## 元件

### 卡片
```css
.tech-card {
  background: var(--tech-white);
  border: 1px solid #e4e4e7;
  border-radius: 12px;
  padding: 32px;
}

.tech-card-dark {
  background: #18181b;
  border-color: #27272a;
  color: var(--tech-white);
}
```

### 線條裝飾
```css
.tech-lines {
  background-image: 
    linear-gradient(rgba(59, 130, 246, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(59, 130, 246, 0.1) 1px, transparent 1px);
  background-size: 40px 40px;
}
```

### 發光效果
```css
.tech-glow {
  box-shadow: 
    0 0 20px var(--tech-glow),
    0 0 40px var(--tech-glow);
}
```

### 按鈕
```css
.tech-button {
  background: var(--tech-black);
  color: var(--tech-white);
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 500;
  font-size: 14px;
}

.tech-button:hover {
  background: var(--tech-accent);
}
```

### 數據顯示
```css
.tech-metric {
  font-family: 'JetBrains Mono', monospace;
  font-size: 3rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--tech-accent), #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

## 適用場景
- 科技公司
- 開發工具
- API 服務
- 資料平台
