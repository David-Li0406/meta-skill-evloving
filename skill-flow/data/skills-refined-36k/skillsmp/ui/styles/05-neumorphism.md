---
name: 新擬物
description: Neumorphism - 柔和陰影的凸起效果
---

# 05. 新擬物 Neumorphism

## 概述
使用柔和的內外陰影，創造凸起或凹陷的柔軟質感。

## 特徵
- 柔和雙向陰影
- 凸起/凹陷效果
- 低對比色彩
- 圓角設計

## 配色
```css
:root {
  --neu-bg: #e0e5ec;
  --neu-shadow-dark: #a3b1c6;
  --neu-shadow-light: #ffffff;
  --neu-text: #6d7b8d;
}
```

## 凸起效果
```css
.neu-raised {
  background: var(--neu-bg);
  border-radius: 16px;
  box-shadow: 
    8px 8px 16px var(--neu-shadow-dark),
    -8px -8px 16px var(--neu-shadow-light);
}
```

## 凹陷效果
```css
.neu-inset {
  background: var(--neu-bg);
  border-radius: 16px;
  box-shadow: 
    inset 4px 4px 8px var(--neu-shadow-dark),
    inset -4px -4px 8px var(--neu-shadow-light);
}
```

## 按鈕
```css
.neu-button {
  background: var(--neu-bg);
  border: none;
  border-radius: 12px;
  padding: 12px 24px;
  color: var(--neu-text);
  box-shadow: 
    6px 6px 12px var(--neu-shadow-dark),
    -6px -6px 12px var(--neu-shadow-light);
}

.neu-button:active {
  box-shadow: 
    inset 4px 4px 8px var(--neu-shadow-dark),
    inset -4px -4px 8px var(--neu-shadow-light);
}
```

## 注意事項
⚠️ 對比度較低，需注意無障礙
⚠️ 只適合特定類型的專案
