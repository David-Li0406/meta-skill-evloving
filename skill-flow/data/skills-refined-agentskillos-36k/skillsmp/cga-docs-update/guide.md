# cga-docs-update 詳細ガイド

## 概要

コード変更に伴うドキュメント更新漏れを防ぐためのスキル。
`git diff main..HEAD` を分析し、更新すべきドキュメントを提案する。

**対象**: `doc/domain/`、`doc/decisions/`
**対象外**: `.claude/skills/`（`cga-skills-update` で対応）

## 基本ルール

- **読み取り優先**: まず分析し、変更は確認後に行う
- **過剰提案しない**: 実際に影響がある箇所のみ提案
- **コード変更しない**: ドキュメントのみ対象

## 実行フロー

### Step 1: 差分分析

```bash
# 変更されたファイルを取得
git diff main..HEAD --stat

# 詳細な差分を確認（必要に応じて）
git diff main..HEAD -- src/ordering/
```

### Step 2: 影響範囲の特定

変更されたファイルのパスから、影響を受けるドキュメントをマッピング:

| 変更パス | 影響ドキュメント |
|----------|------------------|
| `src/ordering/models/` | `doc/domain/ordering-todo.md` |
| `src/ordering/usecases/` | `doc/domain/ordering-todo.md` |
| `src/ordering/controllers/` | `doc/domain/ordering-todo.md` |
| `src/ordering/validators/` | `doc/domain/ordering-todo.md` |
| `src/shipping/` | `doc/domain/shipping-todo.md` |
| `prisma/schema.prisma` | `doc/domain/glossary.md` |
| `src/shared/errors/` | 該当ユーザーストーリーのエラー型定義 |

### Step 3: ドキュメント読み込みと比較

1. 影響を受けるドキュメントを読み込む
2. 実装状況と記載内容を比較
3. 差分を抽出

### Step 4: 提案生成

具体的な更新内容を提案形式で出力:

```markdown
## 更新提案

### doc/domain/ordering-todo.md

**現状テーブル更新**:
```diff
- | ドメインモデル | ❌ 0% | 未実装 |
+ | ドメインモデル | ✅ 100% | Order, OrderItem, ShippingAddress |
```

**US-ORD-001 受け入れ条件**:
- [x] `POST /orders` で注文を作成できる ← チェック追加
- [x] 注文には顧客ID、配送先住所、1件以上の注文明細が必要 ← チェック追加
```

### Step 5: ユーザー確認

AskUserQuestion で確認:
- 全て更新
- 選択的に更新
- 更新しない

### Step 6: 更新実行

確認後、Edit ツールで更新を実行。

## 注意事項

- コードの変更は行わない
- 提案は具体的かつ最小限に
- 既存の記述スタイルを維持
- 未完了のタスクを完了にしない（実装確認が必要）
