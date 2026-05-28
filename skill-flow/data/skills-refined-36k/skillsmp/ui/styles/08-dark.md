---
name: 暗黑模式
description: Dark Mode - 深色主題設計
---

# 08. 暗黑模式 Dark Mode

## 概述
使用深色背景的設計主題，護眼且現代感十足。

## 特徵
- 深色背景
- 降低飽和度
- 柔和對比
- 發光效果

## 配色
```css
:root {
  /* 背景層次 */
  --dark-bg-primary: #0f0f0f;
  --dark-bg-secondary: #1a1a1a;
  --dark-bg-tertiary: #262626;
  
  /* 文字 */
  --dark-text-primary: #f5f5f5;
  --dark-text-secondary: #a3a3a3;
  --dark-text-muted: #737373;
  
  /* 邊框 */
  --dark-border: #333333;
  
  /* 強調色 */
  --dark-accent: #3b82f6;
}
```

## 卡片
```css
.dark-card {
  background: var(--dark-bg-secondary);
  border: 1px solid var(--dark-border);
  border-radius: 12px;
  padding: 24px;
}
```

## 按鈕
```css
.dark-button {
  background: var(--dark-accent);
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
}

.dark-button-outline {
  background: transparent;
  color: var(--dark-text-primary);
  border: 1px solid var(--dark-border);
}
```

## 發光效果
```css
.glow {
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
}
```

## 實作切換
```css
@media (prefers-color-scheme: dark) {
  :root { /* 深色變數 */ }
}

[data-theme="dark"] {
  /* 深色變數 */
}
```

## 適用場景
- 科技產品
- 開發工具
- 影音平台
- 遊戲
