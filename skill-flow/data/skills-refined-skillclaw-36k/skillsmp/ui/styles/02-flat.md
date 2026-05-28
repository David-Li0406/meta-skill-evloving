---
name: 扁平化設計
description: Flat Design - 無陰影、純色塊的簡潔風格
---

# 02. 扁平化 Flat Design

## 概述
移除所有 3D 效果，使用純色塊、簡潔圖標的設計風格。

## 特徵
- 無陰影、無漸層
- 純色塊
- 簡潔圖標
- 明確的幾何形狀

## 配色
```css
:root {
  --flat-red: #e74c3c;
  --flat-blue: #3498db;
  --flat-green: #2ecc71;
  --flat-yellow: #f1c40f;
  --flat-purple: #9b59b6;
  --flat-dark: #2c3e50;
  --flat-gray: #95a5a6;
}
```

## 元件

### 按鈕
```css
.btn-flat {
  background: var(--flat-blue);
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  font-weight: 600;
}

.btn-flat:hover {
  background: #2980b9;
}
```

### 卡片
```css
.card-flat {
  background: white;
  border: 2px solid var(--flat-gray);
  border-radius: 4px;
  padding: 20px;
}
```

## 適用場景
- 行動應用
- Dashboard
- 資訊圖表
