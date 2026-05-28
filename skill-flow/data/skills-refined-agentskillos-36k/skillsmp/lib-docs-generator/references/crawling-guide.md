# クローリングガイド

WebFetch および curl を使ったドキュメント取得の**技術的詳細**。

> **Note:** 実行フローはSKILL.mdを参照。このファイルは取得方法の詳細に特化。

## 取得方法の使い分け

| ケース | 推奨方法 | 理由 |
|--------|----------|------|
| llms.txt | **curl** | WebFetchは大きなファイルを要約してしまう |
| 軽量クロール（タイトル+概要抽出） | **WebFetch** | 必要な情報だけを効率的に抽出 |
| スキル発動時の詳細取得 | **WebFetch** | 都度最新情報を取得 |

## llms.txtファイルの取得

llms.txtはLLM向けに最適化されたドキュメントファイル。**WebFetchではなくcurlで直接ダウンロード**する。

### なぜcurlを使うのか

- WebFetchは大きなファイルを要約してしまう
- llms.txtは数百KB〜数MBになることがある
- curlなら完全な内容をそのまま取得できる

### 手順

1. llms.txtを確認
2. llms.txtのみをcurlでダウンロード（llms-full.txtは無視）
3. referencesディレクトリに.md拡張子で保存

### コマンド例

**重要: 拡張子は`.md`で保存する**（スキルのreferencesは.mdファイルのみ読み込まれる）

```bash
# ディレクトリ作成
mkdir -p .claude/skills/{library}/references

# llms.txtのみダウンロード（llms-full.txtは不要）
curl -s https://example.com/llms.txt -o .claude/skills/{library}/references/llms.md
```

### llms.txtの一般的なパターン

| サイト | llms.txt URL |
|--------|--------------|
| Expo | https://docs.expo.dev/llms.txt |
| Vercel | https://vercel.com/llms.txt |
| Tamagui | https://tamagui.dev/llms.txt |
| その他 | `/llms.txt` を確認 |

---

## 軽量クロール（llms.txtがない場合）

llms.txtがないサイトでは、各ページから**タイトルと概要のみ**を抽出してllms.md形式のファイルを自動生成する。

### 目的

- 全文クロールは不要
- タイトル + 最初の1-2文だけで十分
- スキル発動時にWebFetchで詳細取得するため

### WebFetchプロンプト

```
WebFetch(
  url="[URL]",
  prompt="Extract ONLY: 1) The page title 2) The first 1-2 sentences of the main content. Return in format: TITLE: [title] | DESCRIPTION: [description]"
)
```

### 並列取得

ページ数が多い場合はTaskエージェントを並列起動:

```
Task(subagent_type="Explore", prompt="以下のURLからタイトルと概要を抽出: [URLリストA]")
Task(subagent_type="Explore", prompt="以下のURLからタイトルと概要を抽出: [URLリストB]")
```

### カテゴリ分け

URLパターンで自動分類:

| パターン | カテゴリ |
|----------|----------|
| `/getting-started`, `/quickstart`, `/intro` | Getting Started |
| `/installation`, `/setup` | Getting Started |
| `/api`, `/reference` | API Reference |
| `/concepts`, `/fundamentals` | Core Concepts |
| `/guides`, `/how-to` | Guides |
| `/examples`, `/tutorials` | Examples |
| `/advanced`, `/configuration` | Optional |

---

## WebFetchによるドキュメント取得

WebFetchは内部で小さなモデルがHTML→Markdown変換を処理するため、コンテキスト効率が良い。

### 基本的な使い方

```
WebFetch(
  url="https://example.com/docs/getting-started",
  prompt="Extract the main documentation content. Include all code blocks, API definitions, and usage examples. Exclude navigation, footer, and advertisements."
)
```

### プロンプトの書き方

**汎用プロンプト:**
```
Extract the main documentation content from this page.
Include:
- All code blocks with language tags
- API definitions and type information
- Usage examples
- Warnings and notes

Exclude:
- Navigation menus
- Footer content
- Advertisements
```

**API リファレンス向け:**
```
Extract API documentation. For each API:
- Function/method signature
- Parameters with types and descriptions
- Return value type and description
- Code examples
```

**軽量クロール向け（タイトル+概要のみ）:**
```
Extract ONLY:
1) The page title
2) The first 1-2 sentences of the main content

Return in format: TITLE: [title] | DESCRIPTION: [description]
```

### WebFetchの特性

**メリット:**
- HTML→Markdown変換が自動で行われる
- コンテキスト消費が少ない
- raw/ディレクトリの管理が不要

**制限事項:**
- 非常に長いページは要約される可能性がある
- JavaScript実行不可（SPAは困難）
- 認証が必要なページは取得困難

---

## URL収集テクニック

### 1. サイトマップ確認

多くのドキュメントサイトはsitemap.xmlを提供:

```bash
curl -s https://example.com/sitemap.xml -o sitemap.xml
# Readツールで読み取り、/docs/または/api/を含むURLを抽出
```

### 2. ナビゲーション解析

サイトマップがない場合:

```
WebFetch(
  url="https://example.com/docs",
  prompt="Extract all documentation page URLs from the navigation/sidebar. Return as a list of URLs."
)
```

### 3. 重要ページの特定

一般的なドキュメント構造:

| パターン | 内容 |
|----------|------|
| `/docs/getting-started` | 導入ガイド |
| `/docs/api/*` | APIリファレンス |
| `/docs/guides/*` | 使い方ガイド |
| `/docs/examples/*` | サンプルコード |

---

## エラーハンドリング

### 404エラー
- URLパターンを変えて再試行
- 代替ドキュメントソースを検討

### タイムアウト
- ページが重い場合は特定セクションのみ取得

### リダイレクト
- `curl -L` オプションでリダイレクトを自動追跡

---

## 生成されるファイルの品質チェック

- [ ] llms.md形式（タイトル + URL + 概要）になっている
- [ ] URLが実際にアクセス可能
- [ ] カテゴリ分けが適切
- [ ] 重複エントリがない
