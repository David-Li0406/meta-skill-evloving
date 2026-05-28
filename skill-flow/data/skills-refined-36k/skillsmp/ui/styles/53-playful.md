---
name: 童趣風格
description: Playful/Kids - 活潑可愛的兒童風格
---

# 53. 童趣風 Playful/Kids

## 概述
活潑、可愛、充滿樂趣的設計風格。

## 特徵
- 鮮豔色彩
- 圓角設計
- 可愛插圖
- 有趣動效

## 配色
```css
:root {
  --play-pink: #f472b6;
  --play-blue: #38bdf8;
  --play-yellow: #fbbf24;
  --play-green: #4ade80;
  --play-purple: #c084fc;
  --play-orange: #fb923c;
}
```

## 字型
```css
body {
  font-family: 'Nunito', 'Noto Sans TC', sans-serif;
}

h1, h2, h3 {
  font-weight: 800;
}
```

## 元件

### 卡片
```css
.playful-card {
  background: white;
  border-radius: 24px;
  padding: 32px;
  box-shadow: 0 8px 0 var(--play-blue);
}

.playful-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 0 var(--play-blue);
}
```

### 按鈕
```css
.playful-button {
  background: var(--play-pink);
  color: white;
  padding: 16px 32px;
  border-radius: 100px;
  font-weight: 700;
  font-size: 1.125rem;
  box-shadow: 0 4px 0 #ec4899;
}

.playful-button:active {
  transform: translateY(4px);
  box-shadow: none;
}
```

### 標籤
```css
.fun-tag {
  background: var(--play-yellow);
  color: #78350f;
  padding: 6px 16px;
  border-radius: 100px;
  font-weight: 700;
  font-size: 14px;
}
```

### 彈跳動畫
```css
.bounce {
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
```

## 適用場景
- 兒童教育
- 遊戲應用
- 玩具品牌
- 家庭活動
