---
name: 野獸派風格
description: Brutalism - 粗獷大膽的反設計風格
---

# 06. 野獸派 Brutalism

## 概述
反傳統設計規則，強調原始、粗獷的網頁美學。

## 特徵
- 粗黑邊框
- 原始 HTML 感
- 大膽配色
- 不對稱佈局

## 配色
```css
:root {
  --brut-black: #000000;
  --brut-white: #ffffff;
  --brut-yellow: #ffff00;
  --brut-red: #ff0000;
  --brut-blue: #0000ff;
}
```

## 字型
```css
body {
  font-family: 'Times New Roman', serif;
  /* 或使用等寬字型 */
  font-family: 'Courier New', monospace;
}

h1 {
  font-size: 5rem;
  font-weight: 900;
  text-transform: uppercase;
}
```

## 元件

### 粗邊框
```css
.brut-box {
  border: 4px solid var(--brut-black);
  padding: 20px;
  background: var(--brut-white);
}
```

### 按鈕
```css
.brut-button {
  background: var(--brut-yellow);
  color: var(--brut-black);
  border: 3px solid var(--brut-black);
  padding: 12px 24px;
  font-weight: 700;
  text-transform: uppercase;
  cursor: pointer;
}

.brut-button:hover {
  background: var(--brut-black);
  color: var(--brut-yellow);
}
```

### 連結
```css
.brut-link {
  color: var(--brut-blue);
  text-decoration: underline;
  font-weight: bold;
}

.brut-link:hover {
  background: var(--brut-blue);
  color: var(--brut-white);
}
```

### 不規則佈局
```css
.brut-layout {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
}

.brut-item-1 {
  grid-column: 1 / 5;
  grid-row: 1 / 3;
}

.brut-item-2 {
  grid-column: 5 / 13;
  grid-row: 1 / 2;
  transform: rotate(-2deg);
}
```

## 適用場景
- 藝術機構
- 獨立音樂
- 時尚前衛
- 實驗性專案
