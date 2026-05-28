---
name: 無邊框風格
description: Borderless - 流動佈局的現代無界限設計
---

# 55. 無邊框 Borderless

## 概述
打破傳統邊界，創造流動無縫的視覺體驗。

## 特徵
- 無明確邊界
- 流動佈局
- 全屏體驗
- 沉浸感

## 配色
```css
:root {
  --bl-bg: #fafafa;
  --bl-text: #1a1a1a;
  --bl-accent: #000000;
  --bl-muted: #666666;
}
```

## 佈局

### 全屏區塊
```css
.section-full {
  min-height: 100vh;
  display: flex;
  align-items: center;
}

.section-content {
  width: 100%;
  max-width: none;
  padding: 0 8vw;
}
```

### 錯落佈局
```css
.staggered-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
}

.staggered-item:nth-child(odd) {
  grid-column: 1 / 7;
}

.staggered-item:nth-child(even) {
  grid-column: 6 / 13;
  margin-top: -20vh;
}
```

### 全幅圖片
```css
.full-bleed-image {
  width: 100vw;
  margin-left: calc(-50vw + 50%);
  height: 80vh;
  object-fit: cover;
}
```

## 元件

### 文字區塊
```css
.text-block {
  max-width: 60ch;
  font-size: clamp(1rem, 2vw, 1.25rem);
  line-height: 1.8;
}

.text-block-large {
  font-size: clamp(1.5rem, 3vw, 2.5rem);
  line-height: 1.4;
}
```

### 極簡導航
```css
.minimal-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  padding: 24px 8vw;
  display: flex;
  justify-content: space-between;
  z-index: 100;
}

.minimal-nav a {
  color: inherit;
  text-decoration: none;
  font-size: 14px;
}
```

### 滾動指示
```css
.scroll-indicator {
  position: fixed;
  right: 40px;
  bottom: 40px;
  writing-mode: vertical-rl;
  font-size: 12px;
  letter-spacing: 0.2em;
}
```

## 適用場景
- 創意機構
- 藝術展覽
- 時尚品牌
- 攝影作品
