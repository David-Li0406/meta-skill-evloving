---
name: 孟菲斯風格
description: Memphis - 幾何圖案與大膽配色的活潑風格
---

# 29. 孟菲斯 Memphis

## 概述
源自 80 年代義大利設計運動，特色是幾何圖案和大膽配色。

## 特徵
- 幾何圖形
- 鮮豔配色
- 不規則形狀
- 活潑動感

## 配色
```css
:root {
  --mem-pink: #ff6f91;
  --mem-yellow: #ffcc00;
  --mem-blue: #3d5afe;
  --mem-green: #00d9a5;
  --mem-purple: #9c27b0;
  --mem-black: #1a1a1a;
}
```

## 幾何圖形
```css
/* 圓形 */
.mem-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: var(--mem-pink);
}

/* 三角形 */
.mem-triangle {
  width: 0;
  height: 0;
  border-left: 30px solid transparent;
  border-right: 30px solid transparent;
  border-bottom: 52px solid var(--mem-yellow);
}

/* 波浪線 */
.mem-wave {
  width: 100px;
  height: 20px;
  background: repeating-linear-gradient(
    90deg,
    var(--mem-blue) 0px,
    var(--mem-blue) 10px,
    transparent 10px,
    transparent 20px
  );
}

/* 點點 */
.mem-dots {
  background-image: radial-gradient(
    circle,
    var(--mem-green) 3px,
    transparent 3px
  );
  background-size: 20px 20px;
}
```

## 元件

### 卡片
```css
.mem-card {
  background: white;
  border: 3px solid var(--mem-black);
  box-shadow: 8px 8px 0 var(--mem-black);
  padding: 24px;
}
```

### 按鈕
```css
.mem-button {
  background: var(--mem-yellow);
  color: var(--mem-black);
  border: 3px solid var(--mem-black);
  padding: 14px 32px;
  font-weight: 700;
  box-shadow: 4px 4px 0 var(--mem-black);
}

.mem-button:active {
  transform: translate(4px, 4px);
  box-shadow: none;
}
```

## 適用場景
- 創意機構
- 藝術活動
- 年輕品牌
- 時尚產業
