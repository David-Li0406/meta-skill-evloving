---
name: 中式傳統
description: Chinese Traditional - 古典書法元素的傳統風格
---

# 39. 中式傳統 Chinese Traditional

## 概述
運用傳統書法、水墨等元素的中國古典風格。

## 特徵
- 書法元素
- 紅金配色
- 傳統紋樣
- 古典韻味

## 配色
```css
:root {
  --trad-red: #c41e3a;
  --trad-gold: #d4af37;
  --trad-black: #1a1a1a;
  --trad-cream: #f5f0e6;
  --trad-ink: #2a2a2a;
}
```

## 字型
```css
h1, h2 {
  font-family: '楷體', 'KaiTi', 'Noto Serif TC', serif;
}
```

## 元件

### 傳統邊框
```css
.trad-box {
  border: 2px solid var(--trad-gold);
  padding: 40px;
  position: relative;
}

.trad-box::before {
  content: '囍';
  position: absolute;
  top: -15px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--trad-cream);
  color: var(--trad-red);
  padding: 0 12px;
  font-size: 24px;
}
```

### 印章效果
```css
.seal {
  width: 80px;
  height: 80px;
  border: 3px solid var(--trad-red);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--trad-red);
  font-family: '楷體', serif;
  font-size: 1.5rem;
  transform: rotate(-5deg);
}
```

### 按鈕
```css
.trad-button {
  background: var(--trad-red);
  color: var(--trad-gold);
  padding: 14px 40px;
  border: none;
  font-family: '楷體', serif;
  letter-spacing: 0.2em;
}
```

## 適用場景
- 傳統文化
- 中式婚禮
- 書法藝術
- 歷史博物館
