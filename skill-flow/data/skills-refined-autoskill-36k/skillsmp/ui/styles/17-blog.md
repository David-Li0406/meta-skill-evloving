---
name: 部落格風格
description: Blog - 內容優先的閱讀友善風格
---

# 17. 部落格 Blog

## 概述
以閱讀體驗為優先的內容網站設計。

## 特徵
- 閱讀友善字型
- 適當行寬
- 清晰層次
- 分類導航

## 配色
```css
:root {
  --blog-bg: #fafafa;
  --blog-card: #ffffff;
  --blog-text: #1a1a1a;
  --blog-secondary: #666666;
  --blog-accent: #2563eb;
  --blog-border: #e5e5e5;
}
```

## 字型
```css
body {
  font-family: 'Noto Sans TC', 'Inter', sans-serif;
  font-size: 18px;
  line-height: 1.8;
  color: var(--blog-text);
}

.article-content {
  max-width: 680px;
  margin: 0 auto;
}

h1 { font-size: 2.5rem; line-height: 1.2; }
h2 { font-size: 1.75rem; margin-top: 48px; }
h3 { font-size: 1.25rem; margin-top: 32px; }
```

## 元件

### 文章卡片
```css
.article-card {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 24px;
  padding: 24px;
  background: var(--blog-card);
  border-radius: 12px;
}

.article-card-image {
  aspect-ratio: 16/10;
  border-radius: 8px;
  object-fit: cover;
}

.article-card-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 8px;
}

.article-card-meta {
  font-size: 14px;
  color: var(--blog-secondary);
}
```

### 標籤
```css
.tag {
  display: inline-block;
  padding: 4px 12px;
  background: #f3f4f6;
  border-radius: 100px;
  font-size: 13px;
  color: var(--blog-secondary);
}
```

## 適用場景
- 個人部落格
- 技術文章
- 新聞媒體
- 內容行銷
