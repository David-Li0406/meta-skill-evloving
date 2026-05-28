---
name: 區塊鏈風格
description: Blockchain - 加密貨幣與區塊鏈的視覺風格
---

# 47. 區塊鏈 Blockchain

## 概述
展現區塊鏈技術、加密貨幣的科技視覺風格。

## 特徵
- 網格連接
- 加密元素
- 去中心化視覺
- 科技感

## 配色
```css
:root {
  --chain-bg: #0a0a0f;
  --chain-primary: #627eea;
  --chain-secondary: #00d4aa;
  --chain-gold: #f7931a;
  --chain-grid: rgba(98, 126, 234, 0.1);
}
```

## 網格背景
```css
.chain-grid {
  background: 
    linear-gradient(var(--chain-grid) 1px, transparent 1px),
    linear-gradient(90deg, var(--chain-grid) 1px, transparent 1px);
  background-size: 50px 50px;
}
```

## 元件

### 節點連接
```css
.node {
  width: 12px;
  height: 12px;
  background: var(--chain-primary);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--chain-primary);
}

.node-line {
  height: 2px;
  background: linear-gradient(90deg, var(--chain-primary), var(--chain-secondary));
}
```

### 卡片
```css
.chain-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(98, 126, 234, 0.3);
  border-radius: 16px;
  padding: 24px;
  backdrop-filter: blur(10px);
}
```

### 統計
```css
.chain-stat {
  text-align: center;
}

.chain-stat-value {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--chain-primary), var(--chain-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

### 按鈕
```css
.chain-button {
  background: var(--chain-primary);
  color: white;
  padding: 14px 32px;
  border-radius: 8px;
  font-weight: 600;
}

.chain-button-connect {
  background: transparent;
  border: 1px solid var(--chain-primary);
  color: var(--chain-primary);
}
```

## 適用場景
- 加密貨幣
- DeFi 平台
- NFT 市場
- 區塊鏈項目
