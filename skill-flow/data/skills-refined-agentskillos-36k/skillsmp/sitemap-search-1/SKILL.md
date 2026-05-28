---
name: sitemap-search
description: |
  Webサイトのサイトマップページとサイト内検索機能を実装するスキル。
  Use when: サイトマップ、サイト内検索、ページ一覧、ナビゲーション、検索機能、sitemap、search、フィルタリング、タグ検索、カテゴリ検索、Cmd+K、ページを探す、困った人向けナビ、コンテキストナビ
  Do not use when: SEO用sitemap.xml生成、外部検索エンジン連携、サーバーサイド全文検索
---

# サイトマップ & サイト内検索機能スキル

Webサイトにサイトマップページとサイト内検索機能を実装する。
ユーザーが目的のページを素早く見つけられるナビゲーション体験を提供。

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
6. **コンテキスト別ナビゲーション（困りごとから探す）** ← 重要！

---

## 重要：コンテキスト別ナビゲーション

**サイトマップの本来の目的は「困っている人を助ける」こと。**
単なるページ一覧だけでは、どのページに行けばいいかわからない。

### 推奨構成（コンテキストナビを最初に配置）

```
サイトマップページ
├── ヘッダー
├── 困りごとから探す（コンテキストナビ）← 最初に配置！
├── 検索バー
├── カテゴリ別一覧
└── フッター
```

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
];
```

---

## 1. サイトマップページ設計

### 基本構成
```
サイトマップページ
├── ヘッダー（パンくずリスト）
├── 検索バー（オプション）
├── カテゴリ別グリッド
│   ├── カテゴリA
│   │   ├── ページリンク1（番号バッジ + タイトル + 説明）
│   │   ├── ページリンク2
│   │   └── サブページリンク（インデント表示）
│   └── カテゴリB
│       └── ...
├── コンテキスト別ナビゲーション（「こんな時は？」セクション）
└── フッター
```

### HTML構造例
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

### CSS設計パターン
```css
.sitemap-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.sitemap-section {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 1.5rem;
}

.sitemap-link {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 0.75rem;
  border-radius: 8px;
  transition: background 0.2s;
}

.sitemap-link:hover {
  background: var(--bg-tertiary);
}

.sitemap-link-num {
  min-width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--accent-color);
  color: white;
  border-radius: 6px;
  font-weight: 600;
}
```

---

## 2. サイト内検索機能

### 検索データ構造
```javascript
const searchData = [
  {
    title: "ページタイトル",
    desc: "ページの説明文",
    url: "page.html",
    icon: "description",
    category: "カテゴリ名",
    keywords: ["キーワード1", "キーワード2", "関連語"]
  },
  // ...
];
```

### 検索アルゴリズム（スコアリング方式）
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
      if (item.desc.toLowerCase().includes(normalizedQuery)) score += 40;

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

### 検索モーダルUI
```html
<div class="search-modal" id="searchModal">
  <div class="search-modal-content">
    <div class="search-input-wrapper">
      <span class="material-symbols-outlined">search</span>
      <input type="text" id="searchInput" placeholder="ページを検索... (Ctrl+K)">
      <kbd>ESC</kbd>
    </div>
    <div class="search-results" id="searchResults">
      <!-- 検索結果がここに表示 -->
    </div>
  </div>
</div>
```

### キーボードナビゲーション
```javascript
// Ctrl/Cmd + K で検索モーダルを開く
document.addEventListener('keydown', (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault();
    openSearchModal();
  }
  if (e.key === 'Escape') {
    closeSearchModal();
  }
});

// 検索結果内の矢印キーナビゲーション
searchInput.addEventListener('keydown', (e) => {
  const results = document.querySelectorAll('.search-result-item');

  if (e.key === 'ArrowDown') {
    e.preventDefault();
    selectedIndex = Math.min(selectedIndex + 1, results.length - 1);
    updateSelection(results);
  }
  if (e.key === 'ArrowUp') {
    e.preventDefault();
    selectedIndex = Math.max(selectedIndex - 1, 0);
    updateSelection(results);
  }
  if (e.key === 'Enter' && selectedIndex >= 0) {
    results[selectedIndex].click();
  }
});
```

---

## 3. タグ・カテゴリシステム

### タグ定義
```javascript
const tags = {
  categories: ["入門", "応用", "リファレンス", "チュートリアル"],
  topics: ["AI", "開発", "デザイン", "ビジネス"],
  difficulty: ["初級", "中級", "上級"]
};
```

### タグHTML構造
```html
<div class="tags-container">
  <span class="tag" data-category="入門">入門</span>
  <span class="tag" data-topic="AI">AI</span>
</div>
```

### タグCSS
```css
.tags-container {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tag {
  padding: 0.25rem 0.75rem;
  background: var(--bg-secondary);
  border-radius: 9999px;
  font-size: 0.75rem;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s;
}

.tag:hover,
.tag.active {
  background: var(--accent-color);
  color: white;
}
```

### タグフィルタリング
```javascript
function filterByTag(tag) {
  const items = document.querySelectorAll('[data-tags]');
  items.forEach(item => {
    const itemTags = item.dataset.tags.split(',');
    if (tag === 'all' || itemTags.includes(tag)) {
      item.style.display = '';
    } else {
      item.style.display = 'none';
    }
  });
}
```

---

## 4. ハイライト表示

```javascript
function highlightMatch(text, query) {
  if (!query) return escapeHtml(text);
  const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
  return escapeHtml(text).replace(regex, '<mark>$1</mark>');
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
```

---

## ヒアリング項目

実装前に以下を確認：

1. **サイト構造**
   - 全ページ数は？
   - カテゴリ分類は？
   - 階層構造は？

2. **検索要件**
   - リアルタイム検索が必要か？
   - キーボードショートカットは必要か？
   - 検索対象は何か？（タイトル、説明、本文）

3. **タグ・カテゴリ**
   - どのような分類軸が必要か？
   - フィルタリングは必要か？

4. **UI/UX**
   - ダークモード対応は必要か？
   - レスポンシブ対応は必要か？
   - アニメーションは必要か？

---

## 出力形式

- HTML/CSS/JavaScriptファイル
- React/Vue/Svelteコンポーネント
- Next.js/Nuxtページ
- 必要に応じてTypeScript対応

---

## 実装のポイント（実績あるパターン）

以下は実際のプロジェクトで使用され、効果的だった実装パターン：

### 検索データの最適化

```javascript
// キーワードに同義語・関連語を含める
keywords: ["GAS", "Apps Script", "自動化", "業務改善", "スプレッドシート"]
```

### コンテキスト別ナビゲーション

「こんな時は？」セクションでユースケース別にページを案内：

```html
<section class="context-nav">
  <h2>困りごとから探す</h2>
  <div class="context-cards">
    <a href="#" class="context-card">
      <span class="icon">create</span>
      <span class="title">教材を作りたい</span>
      <span class="links">→ 教材作成ガイド、テンプレート集</span>
    </a>
  </div>
</section>
```

### IME対応（日本語入力）

```javascript
// compositionstart/endでIME入力中は検索を遅延
let isComposing = false;
input.addEventListener('compositionstart', () => isComposing = true);
input.addEventListener('compositionend', () => {
  isComposing = false;
  search(input.value);
});
input.addEventListener('input', () => {
  if (!isComposing) search(input.value);
});
```

## 参考実装パターン

| パターン | 技術スタック | 適用場面 |
|---------|-------------|---------|
| 静的サイト | HTML/CSS/バニラJS | シンプルなサイト |
| React | useState/useEffect | SPA、コンポーネント指向 |
| Next.js | App Router | SSR/SSG対応サイト |

---

## UXベストプラクティス

### 検索UX

1. **検索ボックスの幅**: 27文字以上を推奨（90%のクエリをカバー）
2. **サジェスト数**: 10件以下（スクロールなしで表示）
3. **ショートカット表示**: 検索バーに `⌘K` などを表示して発見性向上
4. **Spotlight風検索**: 現在の画面上にオーバーレイ表示（ページ遷移なし）
5. **背景ぼかし**: モーダル表示時は背景を軽くぼかして集中を促す

### キーボードナビゲーション

```javascript
// ベストプラクティス: 結果リストのループナビゲーション
if (e.key === 'ArrowDown') {
  selectedIndex = (selectedIndex + 1) % results.length; // 最後→最初
}
if (e.key === 'ArrowUp') {
  selectedIndex = (selectedIndex - 1 + results.length) % results.length; // 最初→最後
}
```

### サイトマップ設計

1. **フラット構造**: 10ページ以上なら4階層以下に抑える
2. **ユーザー中心**: ユーザーの検索・ナビゲーション方法を意識
3. **シンプルさ**: 複雑なサイトでも可能な限りシンプルに
4. **成長対応**: 新しいページ・セクションを追加しやすい構造

---

## アクセシビリティ（ARIA）

### 検索モーダルの必須属性

```html
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="search-title"
  aria-describedby="search-desc"
>
  <h2 id="search-title" class="sr-only">サイト内検索</h2>
  <p id="search-desc" class="sr-only">ページ名やキーワードで検索できます</p>
  <!-- ... -->
</div>
```

### フォーカストラップ実装

```javascript
function trapFocus(modal) {
  const focusable = modal.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const first = focusable[0];
  const last = focusable[focusable.length - 1];

  modal.addEventListener('keydown', (e) => {
    if (e.key !== 'Tab') return;

    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });

  first.focus(); // モーダル開始時にフォーカス
}

// モーダルを閉じた時は元のトリガー要素にフォーカスを戻す
function closeModal(trigger) {
  modal.hidden = true;
  trigger.focus();
}
```

### スクリーンリーダー対応

- `aria-modal="true"` で仮想カーソルをモーダル内に制限
- `aria-live="polite"` で検索結果の更新を通知
- 結果リストには `role="listbox"` と `aria-activedescendant`

---

## パフォーマンス最適化

### 検索データの規模別対応

| ページ数 | 推奨アプローチ |
|---------|---------------|
| ~100 | クライアントサイド検索（このスキル） |
| 100-1000 | Fuse.js等のライブラリ + インデックス |
| 1000+ | サーバーサイド検索（Algolia, Meilisearch） |

### ライブラリ選択ガイド

| ライブラリ | 特徴 | 適用場面 |
|-----------|------|---------|
| 自前実装 | 軽量、カスタマイズ自由 | 小規模サイト |
| Fuse.js | 柔軟、豊富なオプション | 中規模、複雑な検索 |
| microfuzz | 超高速（<1.5ms） | リアルタイム検索 |

### 検索パフォーマンスTips

```javascript
// デバウンス: 入力が止まってから検索実行
function debounce(fn, delay = 150) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

const debouncedSearch = debounce((query) => {
  const results = fuzzySearch(query, searchData);
  renderResults(results);
}, 150);
```

---

## 参考リンク

- [Search UX Best Practices - Pencil & Paper](https://www.pencilandpaper.io/articles/search-ux)
- [Modal Accessibility - A11Y Collective](https://www.a11y-collective.com/blog/modal-accessibility/)
- [Fuse.js - Lightweight fuzzy-search](https://www.fusejs.io/)
