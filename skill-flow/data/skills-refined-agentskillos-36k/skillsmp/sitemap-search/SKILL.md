---
name: sitemap-search
description: "Webサイトのサイトマップページとサイト内検索機能を実装する。サイトマップ、サイト内検索、ページ一覧、ナビゲーション、検索機能、困った人向けナビ、コンテキストナビを追加したい時に使用。"
user-invocable: true
argument-hint: "[framework: react|next|vanilla] [--tags] [--keyboard] [--context-nav]"
---

# サイトマップ & サイト内検索機能スキル

Webサイトにサイトマップページとサイト内検索機能を実装するスキル。
ユーザーが目的のページを素早く見つけられるナビゲーション体験を提供。

## このスキルを使用する時

- サイトマップページを作りたい
- サイト内検索機能を実装したい
- Cmd/Ctrl + K でページ検索できるようにしたい
- **困った人向けのナビゲーション**を追加したい

## このスキルを使用しない時

- SEO用のsitemap.xmlを生成したい
- Algoliaなど外部検索サービスと連携したい

## 対応タスク

1. サイトマップページの作成
2. サイト内検索機能（モーダル + リアルタイム検索）
3. タグ・カテゴリによるフィルタリング
4. キーボードショートカット（Cmd/Ctrl + K）
5. **コンテキスト別ナビゲーション（困りごとから探す）** ← 重要！

---

## 重要：コンテキスト別ナビゲーション

**サイトマップの本来の目的は「困っている人を助ける」こと。**
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
      { title: "〇〇を作りたい", href: "/create-xxx" },
      { title: "△△したい", href: "/do-yyy" },
    ]
  },
];
```

### UI実装例（React/Next.js）

```tsx
<section className="py-12">
  <h2 className="text-2xl font-bold mb-2">困りごとから探す</h2>
  <p className="text-neutral-500 mb-6">何を探せばいいかわからない方はこちら</p>
  <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
    {contextNavItems.map((item) => (
      <div
        key={item.title}
        className="p-5 bg-white dark:bg-neutral-900 rounded-xl border hover:shadow-lg transition"
      >
        <div className="flex items-center gap-3 mb-3">
          <span className="text-2xl">{item.icon}</span>
          <div>
            <h3 className="font-bold">{item.title}</h3>
            <p className="text-xs text-neutral-500">{item.description}</p>
          </div>
        </div>
        <ul className="space-y-2">
          {item.links.map((link) => (
            <li key={link.href}>
              <a href={link.href} className="text-sm text-indigo-500 hover:underline">
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

## サイトマップページ設計

### 推奨構成

```
サイトマップページ
├── ヘッダー
├── 困りごとから探す（コンテキストナビ）← 最初に配置！
├── 検索バー
├── カテゴリ別一覧
└── フッター
```

---

## 検索データ構造

```typescript
interface SearchItem {
  title: string;
  description: string;
  href: string;
  category: string;
  keywords: string[];
}

export const searchData: SearchItem[] = [
  {
    title: "環境構築",
    description: "インストールと初期設定",
    href: "/setup",
    category: "はじめに",
    keywords: ["インストール", "設定", "セットアップ"],
  },
];
```

---

## 検索アルゴリズム（スコアリング方式）

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
      if (item.keywords.some(kw => kw.toLowerCase().includes(normalized))) score += 50;
      // 説明文一致: 40点
      if (item.description.toLowerCase().includes(normalized)) score += 40;
      return { ...item, score };
    })
    .filter(item => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 10);
}
```

---

## キーボードショートカット

```typescript
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

## IME対応（日本語入力）

```typescript
const [isComposing, setIsComposing] = useState(false);

<input
  onCompositionStart={() => setIsComposing(true)}
  onCompositionEnd={() => setIsComposing(false)}
  onChange={(e) => {
    if (!isComposing) search(e.target.value);
  }}
/>
```

---

## ヒアリング項目

実装前に確認：

1. **ユーザーの困りごと**
   - どんな人が使う？
   - よくある質問は？
   - つまずきポイントは？

2. **サイト構造**
   - 全ページ数は？
   - カテゴリ分類は？

3. **検索要件**
   - キーボードショートカットは必要か？

---

## UXベストプラクティス

- 検索ボックス幅: 27文字以上
- サジェスト数: 10件以下
- アクセシビリティ: `role="dialog"`, `aria-modal="true"`
- フォーカストラップ実装

## パフォーマンス

| ページ数 | 推奨 |
|---------|------|
| ~100 | クライアントサイド |
| 100-1000 | Fuse.js |
| 1000+ | Algolia |
