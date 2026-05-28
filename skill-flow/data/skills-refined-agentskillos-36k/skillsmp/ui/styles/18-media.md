---
name: 新聞媒體風格
description: Media - 資訊密集的新聞媒體設計
---

# 18. 新聞媒體 Media

## 概述
資訊密集、快速掃描的新聞媒體設計。

## 特徵
- 多欄佈局
- 資訊密集
- 快速掃描
- 時效性

## 配色
```css
:root {
  --media-primary: #dc2626;
  --media-dark: #111827;
  --media-bg: #f9fafb;
  --media-border: #e5e7eb;
  --media-text: #1f2937;
}
```

## 字型
```css
h1, h2, h3 {
  font-family: 'Noto Serif TC', Georgia, serif;
  font-weight: 700;
}

body {
  font-family: 'Noto Sans TC', sans-serif;
}
```

## 佈局
```css
.news-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 1px;
  background: var(--media-border);
}

.news-grid > * {
  background: white;
  padding: 20px;
}

.news-featured {
  grid-row: span 2;
}
```

## 元件

### 新聞卡片
```css
.news-card {
  border-bottom: 1px solid var(--media-border);
  padding: 20px 0;
}

.news-category {
  color: var(--media-primary);
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 8px;
}

.news-title {
  font-size: 1.25rem;
  font-weight: 700;
  line-height: 1.3;
  margin-bottom: 8px;
}

.news-meta {
  font-size: 13px;
  color: #6b7280;
}
```

### 頭條
```css
.headline {
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 16px;
}

.headline-deck {
  font-size: 1.25rem;
  color: #4b5563;
  line-height: 1.5;
}
```

### 即時新聞
```css
.breaking-news {
  background: var(--media-primary);
  color: white;
  padding: 12px 24px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.breaking-label {
  background: white;
  color: var(--media-primary);
  padding: 4px 12px;
  font-weight: 700;
  font-size: 12px;
}
```

## 適用場景
- 新聞網站
- 雜誌媒體
- 入口網站
- 內容平台
