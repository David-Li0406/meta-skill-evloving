---
name: sitemap-search
description: |
  Webサイトのサイトマップページとサイト内検索機能を実装するスキル。
  Use when: サイトマップ、サイト内検索、ページ一覧、ナビゲーション、検索機能、sitemap、search、フィルタリング、タグ検索、カテゴリ検索、Cmd+K、ページを探す、困った人向けナビ
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
6. **コンテキスト別ナビゲーション（困りごとから探す）**

---

## 重要：コンテキスト別ナビゲーション

サイトマップの本来の目的は「困っている人を助ける」こと。
単なるページ一覧だけでは、どのページに行けばいいかわからない。

### 「困りごとから探す」セクション

ユースケースベースでページを案内する：

```typescript
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

### UI実装例（React/Next.js）

```tsx
<section className="py-12">
  <h2 className="text-2xl font-bold mb-6">困りごとから探す</h2>
  <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
    {contextNavItems.map((item) => (
      <div
        key={item.title}
        className="p-6 bg-white dark:bg-neutral-800 rounded-xl border hover:shadow-lg transition"
      >
        <span className="text-3xl mb-3 block">{item.icon}</span>
        <h3 className="font-bold text-lg mb-1">{item.title}</h3>
        <p className="text-sm text-neutral-500 mb-4">{item.description}</p>
        <ul className="space-y-2">
          {item.links.map((link) => (
            <li key={link.href}>
              <a
                href={link.href}
                className="text-indigo-500 hover:underline text-sm flex items-center gap-1"
              >
                → {link.title}
              </a>
            </li>
          ))}
        </ul>
      </div>
    ))}
  </div>
</section>
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

```typescript
interface SearchItem {
  title: string;
  description: string;
  href: string;
  category: string;
  keywords: string[];
  // コンテキストナビ用
  useCase?: string[];  // どんな時に使うか
  difficulty?: "beginner" | "intermediate" | "advanced";
}

const searchData: SearchItem[] = [
  {
    title: "環境構築",
    description: "Gemini CLIのインストールと初期設定",
    href: "/setup",
    category: "はじめに",
    keywords: ["インストール", "設定", "セットアップ"],
    useCase: ["初めて使う", "環境を作りたい"],
    difficulty: "beginner"
  },
  // ...
];
```

---

## 2. 検索アルゴリズム（スコアリング方式）

```typescript
function searchItems(query: string, items: SearchItem[]): SearchItem[] {
  const normalized = query.toLowerCase().trim();
  if (!normalized) return [];

  return items
    .map(item => {
      let score = 0;

      // タイトル完全一致: 100点
      if (item.title.toLowerCase() === normalized) score += 100;
      // タイトル前方一致: 80点
      else if (item.title.toLowerCase().startsWith(normalized)) score += 80;
      // タイトル部分一致: 60点
      else if (item.title.toLowerCase().includes(normalized)) score += 60;

      // キーワード一致: 50点
      if (item.keywords.some(kw => kw.toLowerCase().includes(normalized))) {
        score += 50;
      }

      // 説明文一致: 40点
      if (item.description.toLowerCase().includes(normalized)) score += 40;

      // ユースケース一致: 45点
      if (item.useCase?.some(uc => uc.toLowerCase().includes(normalized))) {
        score += 45;
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

```typescript
// Cmd/Ctrl + K でモーダルを開く
useEffect(() => {
  const handleKeyDown = (e: KeyboardEvent) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      setIsSearchOpen(true);
    }
    if (e.key === 'Escape') {
      setIsSearchOpen(false);
    }
  };

  document.addEventListener('keydown', handleKeyDown);
  return () => document.removeEventListener('keydown', handleKeyDown);
}, []);
```

---

## 4. IME対応（日本語入力）

```typescript
const [isComposing, setIsComposing] = useState(false);

<input
  onCompositionStart={() => setIsComposing(true)}
  onCompositionEnd={() => setIsComposing(false)}
  onChange={(e) => {
    if (!isComposing) {
      search(e.target.value);
    }
  }}
/>
```

---

## ヒアリング項目

実装前に確認：

1. **サイト構造**
   - 全ページ数は？
   - カテゴリ分類は？

2. **ユーザーの困りごと**
   - どんな人が使う？
   - よくある質問は？
   - つまずきポイントは？

3. **検索要件**
   - キーボードショートカットは必要か？
   - タグ・フィルタリングは必要か？

4. **UI/UX**
   - ダークモード対応は？
   - レスポンシブ対応は？

---

## UXベストプラクティス

### 検索UX

- 検索ボックス幅: 27文字以上（90%のクエリをカバー）
- サジェスト数: 10件以下（スクロールなし）
- Spotlight風: 現在画面上にオーバーレイ表示
- 背景ぼかし: `backdrop-filter: blur(4px)`

### アクセシビリティ（ARIA）

```tsx
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="search-title"
>
  <h2 id="search-title" className="sr-only">サイト内検索</h2>
</div>
```

### フォーカストラップ

モーダル内でTabキーがループするように実装。

---

## パフォーマンス

| ページ数 | 推奨アプローチ |
|---------|---------------|
| ~100 | クライアントサイド（このスキル） |
| 100-1000 | Fuse.js + インデックス |
| 1000+ | Algolia / Meilisearch |

---

## 出力形式

- HTML/CSS/JavaScript
- React/Next.js コンポーネント
- TypeScript対応
