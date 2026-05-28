---
name: 中式現代
description: Chinese Modern - 東方美學的現代詮釋
---

# 40. 中式現代 Chinese Modern

## 概述
結合傳統東方元素與現代設計的融合風格。

## 特徵
- 東方美學
- 現代詮釋
- 典雅留白
- 文化元素

## 配色
```css
:root {
  --cn-red: #c41e3a;
  --cn-gold: #c9a962;
  --cn-black: #1a1a1a;
  --cn-white: #faf9f7;
  --cn-ink: #2c2c2c;
  --cn-jade: #00897b;
}
```

## 字型
```css
h1, h2 {
  font-family: 'Noto Serif TC', '思源宋體', serif;
}

body {
  font-family: 'Noto Sans TC', '思源黑體', sans-serif;
}
```

## 元件

### 卡片
```css
.cn-card {
  background: var(--cn-white);
  padding: 32px;
  position: relative;
}

.cn-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: var(--cn-red);
}
```

### 分隔線
```css
.cn-divider {
  display: flex;
  align-items: center;
  gap: 16px;
  color: var(--cn-gold);
}

.cn-divider::before,
.cn-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--cn-gold);
}
```

### 按鈕
```css
.cn-button {
  background: var(--cn-red);
  color: white;
  padding: 14px 32px;
  border: none;
  font-weight: 500;
}

.cn-button-outline {
  background: transparent;
  color: var(--cn-red);
  border: 1px solid var(--cn-red);
}
```

### 標題
```css
.cn-title {
  font-family: 'Noto Serif TC', serif;
  font-size: 2.5rem;
  font-weight: 400;
  letter-spacing: 0.1em;
  position: relative;
  display: inline-block;
}

.cn-title::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 2px;
  background: var(--cn-red);
}
```

## 適用場景
- 中式餐飲
- 文化機構
- 茶藝/中醫
- 傳統品牌現代化
