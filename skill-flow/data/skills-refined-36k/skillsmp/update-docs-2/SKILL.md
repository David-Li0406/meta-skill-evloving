---
name: update-docs
description: .docs/ の仕様書を更新する。「ドキュメント更新」「仕様書を同期」などのリクエスト時に使用。
---

# Update Docs

`.docs/` の仕様書をコードと同期して更新する。

## 基本方針

メインは司令塔。実作業はサブエージェントで並列実行。

- 探索: サブエージェントで並列
- 更新: ファイルの数だけサブエージェントを並列実行
- 不明点: サブエージェントはメインに戻す → メインで Ask → 解決後サブエージェントで並走
- 最後: 仕様バグ・矛盾・食い違いをチェック

## ワークフロー

### Phase 0: 初期化（初回のみ）

`.docs/` ディレクトリが存在しない、または `product/` も `products/` もない場合は初回実行。

初回実行時:

1. AskUserQuestion で製品数を確認:
   - 「このリポジトリにはいくつの製品がありますか？」
   - 選択肢: 「1つ」「複数」
2. 回答に応じてディレクトリを作成:
   - 1つ → `.docs/product/`
   - 複数 → AskUserQuestion で製品名を確認 → `.docs/products/<name>/`

既存の `.docs/` がある場合:

- `product/` がある → 単一製品として継続
- `products/` がある → 複数製品として継続
- どちらもない → 初回実行と同様に確認

### Phase 1: 変更対象の特定

```bash
git diff main...HEAD --name-only
```

`--full` オプションがある場合は全ファイルを対象にする。

### Phase 2: 探索 (並列)

サブエージェント (Explore) で変更されたコードを並列調査。

### Phase 3: 更新 (並列)

ファイルごとにサブエージェント (general-purpose) を並列起動。

サブエージェントへの指示:

```
記述ルールに従ってファイルを更新してください。
不明点があればメインに戻してください。
```

不明点が返ってきたら:

1. メインで AskUserQuestion で質問
2. 解決したら再度サブエージェントで並走

### Phase 4: 整合性チェック

サブエージェントで仕様バグ・矛盾・食い違いをチェック。

問題があれば:

1. 該当ディレクトリに `issues/` を作成
2. Issue ファイルを作成

### Phase 5: Issue 解決

Issue ごとにユーザーに質問。

- 解決 → Issue ファイルを削除
- 未解決 → FrontMatter で `status: unresolved` をマーク

### Phase 6: CLAUDE.md の同期

CLAUDE.md に `## Docs` セクションがあるか確認。

なければ、以下の形式で追記:

```markdown
## Docs

`.docs/` に仕様書を配置。

- `glossary.md` - 用語の正式名称を確認してハルシネーションを回避
- `features/` - 機能の仕様を確認して実装漏れを防ぐ
- `integrations/` - 外部サービス連携の仕様を確認
- `stories/` - ユーザーストーリーを確認して要件を把握

`.docs/` 配下のディレクトリツリー
```

ルール:

- 見出しは必ず `## Docs` (固定)
- 実際の `.docs/` 構造をそのまま反映
- 抽象化せず、存在するディレクトリ・ファイルのみ記載

製品ディレクトリの判定:

- `product/` (単数) → 製品が1つ。`Product:` 記載は不要
- `products/` (複数) → 製品が複数。CLAUDE.md に `Product: <製品名>` を記載
- どちらもない → Phase 0 で確認済みのはず。確認されていなければ AskUserQuestion で尋ねる

複数製品の場合の CLAUDE.md 記載形式:

```markdown
## Docs

Product: website

`.docs/` に仕様書を配置。
```

## Issue ファイル

### 配置

問題があるファイルと同じディレクトリに `issues/` を作成。

```
.docs/products/<product>/
├── features/
│   ├── <feature>.md
│   └── issues/
│       └── YYYY-MM-DD.<issue-summary>.md
```

### ファイル名

`YYYY-MM-DD.簡潔な説明.md`

例: `2026-01-19.api-endpoint-count.md`

### テンプレート

```markdown
---
status: unresolved
related: <related-file>.md
created: YYYY-MM-DD
---

# 不一致の内容

<file>.md では「Xと記載」されているが、コードでは Y と定義されている。

確認事項:

- 正しい値はどちらか
- 変更があったか、追加予定があるか
```

### ステータス

- `status: unresolved` - 未解決
- `status: resolved` - 解決済み (その後削除)

## 記述ルール

### 基本方針 (最重要)

コードから分かることは資料に書かない。

資料の目的:

- 概要を整理して探索を助ける
- コードから読み取れない意図や背景を残す

書く内容:

- システム全体の構成・関係性
- 認証方式、データフローなどの設計概要
- コードに現れない制約や注意事項
- 技術選定の重要な理由 (脚注で)

書かない内容:

- API エンドポイント一覧
- 関数・クラス・コンポーネントの一覧
- データ構造の詳細
- 実装の詳細手順
- コードを読めば分かる仕様

判断基準: 「コードを grep/read すれば分かるか?」 → Yes なら書かない

### architecture.md と operations.md の役割分担

architecture.md:

- 技術スタック (フレームワーク、ライブラリ)
- 状態管理、フォーム、スタイリングなどの構成
- 用途の簡潔な説明

operations.md:

- デプロイ手順・コマンド
- 監視方法・ツール
- アラート設定
- 障害対応・ロールバック

### features/ の記述ルール

非開発者が製品の機能を理解するための資料。

見出し1の下に説明文、その下に箇条書き。

禁止: 「目的」「概要」セクション、長い説明文、API エンドポイント、コンポーネント名、ルート構成、技術的な実装詳細

### api.md の記述ルール

書く内容: 認証方式、アーキテクチャ図、セキュリティヘッダー

禁止: エンドポイント一覧、詳細説明

### sitemap.md の記述ルール

フラットな箇条書き。セクション分け・テーブル形式禁止。

### services/ の記述ルール

非開発者がサービスでできることを理解するための資料。

見出し1の下に説明文、その下にユースケース(h3)を日本語で列挙。

```markdown
### 予約を作成する

- 店舗・日時・目的を指定して来店予約を作成
- ゲスト予約と会員予約の両方に対応
```

禁止: 英語のユースケース名 (CreateReservation など)、技術的な制約・副作用、API・コンポーネント名

### 主観的表現の禁止

禁止: 思想・ビジョン、将来の展望、「〜だからこそ」

### 脚注の使用

コードから読み取れない意図・背景は脚注で残す。

ルール:

- 必ず番号を使用 (`[^1]`, `[^2]`)
- 名前付き脚注は禁止 (`[^oxygen]`, `[^tada]` など)
- 脚注定義はファイル末尾に `---` で区切って配置
- 全ての脚注を箇条書きで並べる

例:

```markdown
## ランタイム

Cloudflare Workers (Shopify Oxygen) [^1]

## GraphQL

gql.tada [^2]

---

[^1]: 2024-01-15 - Hydrogen 向けに最適化。KV バインディングが自動構成される。

[^2]: 2024-01-15 - コード生成なしで型安全性を実現。
```

### 図は必ず mermaid

flowchart, sequenceDiagram, erDiagram を使用。ASCII アート禁止。

## ディレクトリ構造

単一製品の場合:

```
.docs/
├── overview.md
├── architecture.md
├── glossary.md
├── notes/
└── product/              # 製品仕様は直下に配置
    ├── overview.md
    ├── features/
    └── ...
```

複数製品の場合:

```
.docs/
├── overview.md
├── architecture.md
├── glossary.md
├── notes/
└── products/
    ├── <product-a>/
    └── <product-b>/
```

製品ディレクトリの内容:

```
# product/ または products/<product-name>/
├── overview.md
├── architecture.md
├── operations.md
├── database.md
├── personas.md
├── actors.md
├── relationships.md
├── api.md
├── sitemap.md
├── stories/
├── models/
├── services/
├── policies/
├── integrations/
├── pages/
├── features/
└── issues/           # 仕様の問題点
```
