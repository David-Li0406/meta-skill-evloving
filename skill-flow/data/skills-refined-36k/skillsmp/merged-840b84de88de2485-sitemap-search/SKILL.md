---
name: sitemap-search
description: Use this skill to implement a sitemap page and an internal search function for a website, enhancing navigation and user experience.
---

# サイトマップ & サイト内検索機能スキル

Webサイトにサイトマップページとサイト内検索機能を実装し、ユーザーが目的のページを素早く見つけられるナビゲーション体験を提供します。

## このスキルを使用する時

- サイトマップページを作りたい
- サイト内検索機能を実装したい
- Cmd/Ctrl + K でページ検索できるようにしたい
- タグやカテゴリでページをフィルタリングしたい
- **困った人向けのナビゲーション**を追加したい

## このスキルを使用しない時

- SEO用のsitemap.xmlを生成したい（別スキル/ツールを使用）
- Algoliaなど外部検索サービスと連携したい
- サーバーサイド全文検索を実装したい

## 対応タスク

1. サイトマップページの作成
2. サイト内検索機能（クライアントサイド）
3. タグ・カテゴリによるフィルタリング
4. 検索結果のハイライト表示
5. キーボードショートカット（Cmd/Ctrl + K）
6. **コンテキスト別ナビゲーション（困りごとから探す）**

---

## 重要：コンテキスト別ナビゲーション

サイトマップの本来の目的は「困っている人を助ける」ことです。単なるページ一覧だけでは、どのページに行けばいいかわからないため、ユースケースベースでページを案内します。

### 「困りごとから探す」セクションの例

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

---

## 1. サイトマップページ設計

### 基本構成
```
サイトマップページ
├── ヘッダー（パンくずリスト）
├── コンテキスト別ナビゲーション（困りごとから探す）← 重要！
├── 検索バー（オプション）
├── カテゴリ別グリッド
│   ├── カテゴリA
│   │   ├── ページリンク1
│   │   └── ページリンク2
│   └── カテゴリB
└── フッター
```

### 検索データ構造

```javascript
const searchData = [
  {
    title: "ページタイトル",
    description: "ページの説明文",
    href: "page.html",
    category: "カテゴリ名",
    keywords: ["キーワード1", "キーワード2", "関連語"]
  },
  // ...
];
```

---

## 2. 検索アルゴリズム（スコアリング方式）

```javascript
function fuzzySearch(query, data) {
  const normalizedQuery = query.toLowerCase().trim();

  return data
    .map(item => {
      let score = 0;

      // タイトル完全一致: 100点
      if (item.title.toLowerCase() === normalizedQuery) score += 100;
      // タイトル前方一致: 80点
      else if (item.title.toLowerCase().startsWith(normalizedQuery)) score += 80;
      // タイトル部分一致: 60点
      else if (item.title.toLowerCase().includes(normalizedQuery)) score += 60;

      // 説明文一致: 40点
      if (item.description.toLowerCase().includes(normalizedQuery)) score += 40;

      // キーワード一致: 50点
      if (item.keywords?.some(kw => kw.toLowerCase().includes(normalizedQuery))) {
        score += 50;
      }

      return { ...item, score };
    })
    .filter(item => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 10);
}
```

---

## 3. キーボードショートカット

```javascript
document.addEventListener('keydown', (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault();
    openSearchModal();
  }
  if (e.key === 'Escape') {
    closeSearchModal();
  }
});
```

---

## ヒアリング項目

実装前に以下を確認：

1. **サイト構造**
   - 全ページ数は？
   - カテゴリ分類は？

2. **ユーザーの困りごと**
   - どんな人が使う？
   - よくある質問は？

3. **検索要件**
   - リアルタイム検索が必要か？
   - キーボードショートカットは必要か？

4. **UI/UX**
   - ダークモード対応は必要か？
   - レスポンシブ対応は必要か？

---

## パフォーマンス最適化

### 検索データの規模別対応

| ページ数 | 推奨アプローチ |
|---------|---------------|
| ~100 | クライアントサイド検索（このスキル） |
| 100-1000 | Fuse.js等のライブラリ + インデックス |
| 1000+ | サーバーサイド検索（Algolia, Meilisearch） |

---

## 参考リンク

- [Search UX Best Practices - Pencil & Paper](https://www.pencilandpaper.io/articles/search-ux)
- [Modal Accessibility - A11Y Collective](https://www.a11y-collective.com/blog/modal-accessibility/)
- [Fuse.js - Lightweight fuzzy-search](https://www.fusejs.io/)