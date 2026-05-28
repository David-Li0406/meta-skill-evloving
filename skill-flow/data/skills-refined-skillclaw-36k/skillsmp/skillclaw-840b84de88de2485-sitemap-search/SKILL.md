---
name: sitemap-search
description: Use this skill when you need to implement a sitemap page and an internal search function for a website, helping users quickly find the pages they are looking for.
---

# Skill body

## Overview

This skill allows you to create a sitemap page and implement an internal search function on your website, enhancing navigation and user experience.

## When to Use This Skill

- You want to create a sitemap page.
- You need to implement an internal search function.
- You want to enable page search using Cmd/Ctrl + K.
- You need to filter pages by tags or categories.
- You want to add navigation for users who are having trouble finding information.

## When Not to Use This Skill

- You want to generate an SEO-friendly sitemap.xml (use a different skill/tool).
- You need to integrate with external search services like Algolia.
- You want to implement server-side full-text search.

## Tasks Covered

1. Create a sitemap page.
2. Implement client-side internal search functionality.
3. Enable filtering by tags and categories.
4. Highlight search results.
5. Implement keyboard shortcuts (Cmd/Ctrl + K).
6. Add context-based navigation to assist users.

## Important: Context-Based Navigation

The primary purpose of a sitemap is to assist users who are having trouble. A simple list of pages may not be sufficient for guiding users effectively.

### Example Structure for Context-Based Navigation

```javascript
const contextNavItems = [
  {
    icon: "🚀",
    title: "はじめて使う",
    description: "初めての方はこちら",
    links: [
      { title: "環境構築", href: "/setup" },
      { title: "チュートリアル", href: "/tutorial" },
    ]
  },
  {
    icon: "🔧",
    title: "うまく動かない",
    description: "トラブルシューティング",
    links: [
      { title: "よくある問題", href: "/faq" },
      { title: "エラー対処法", href: "/troubleshooting" },
    ]
  },
  {
    icon: "📚",
    title: "もっと学びたい",
    description: "応用的な使い方",
    links: [
      { title: "ベストプラクティス", href: "/best-practices" },
      { title: "応用例", href: "/examples" },
    ]
  },
  {
    icon: "🎯",
    title: "特定のことをしたい",
    description: "目的別ガイド",
    links: [
      { title: "教材を作りたい", href: "/create-material" },
      { title: "成績処理したい", href: "/grading" },
    ]
  },
];
```

### Example HTML Structure

```html
<div class="sitemap-container">
  <div class="sitemap-grid">
    <section class="sitemap-section">
      <div class="sitemap-section-header">
        <span class="material-symbols-outlined">folder</span>
        <h2>カテゴリ名</h2>
      </div>
      <div class="sitemap-links">
        <a href="page.html" class="sitemap-link">
          <span class="sitemap-link-num">1</span>
          <div class="sitemap-link-content">
            <span class="sitemap-link-title">ページタイトル</span>
            <span class="sitemap-link-desc">ページの説明文</span>
          </div>
        </a>
      </div>
    </section>
  </div>
</div>
```

### Example CSS Styles

```css
.sitemap-container {
  /* Add your styles here */
}
```