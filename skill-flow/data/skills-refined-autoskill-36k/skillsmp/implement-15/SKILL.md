---
name: implement
description: |
  ドキュメント駆動で機能を実装。関連ドキュメントを自動収集し、既存パターンに沿ったコードを生成。
  トリガー: 「実装して」「implement」「機能を作って」「コード生成」「ドキュメントから実装」
---

# implement: ドキュメント駆動実装スキル

## 目的
仕様ドキュメントと既存コードパターンに基づき、一貫性のある実装を生成。

## 実行手順

### Step 1: 関連ドキュメント収集

機能名から以下を検索・収集:

```bash
# 機能名でドキュメント検索
grep -r "機能名" docs/

# 関連仕様を特定
cat docs/fastapi-htmx-spec.md
cat docs/TODOS.md
```

収集対象:
| ドキュメント | 確認内容 |
|-------------|----------|
| `docs/fastapi-htmx-spec.md` | API仕様、画面仕様 |
| `docs/TODOS.md` | タスク定義、実装要件 |
| `docs/ui/*.html` | UIモック、HTML構造 |
| `CLAUDE.md` | コード規約、既存モジュール |

### Step 2: 既存パターン分析

実装前に類似機能のコードを確認:

```bash
# 既存エンドポイント例
ls demo_app/routers/

# 既存サービス例
ls demo_app/services/

# 既存テンプレート例
ls demo_app/templates/
```

抽出するパターン:
- ディレクトリ構成
- 命名規則
- エラーハンドリング
- 依存注入方式

### Step 3: 実装計画の提示

コード生成前に計画を提示:

```
## 実装計画: [機能名]

### 参照ドキュメント
- docs/fastapi-htmx-spec.md (該当セクション)
- docs/TODOS.md (タスクID: xxx)

### 作成/変更ファイル
1. demo_app/routers/xxx.py - 新規エンドポイント
2. demo_app/services/xxx_service.py - ビジネスロジック
3. demo_app/templates/xxx.html - 画面テンプレート

### 既存パターン準拠
- エラーハンドリング: routers/auth.py と同様
- サービス層: services/llm_service.py と同様
```

### Step 4: コード生成

CLAUDE.mdルール遵守:
- 既存モジュール優先（`azure_/`配下）
- 絵文字禁止（コード内）
- 仮想環境前提

### Step 5: 実装後のドキュメント同期

実装完了後、doc-syncスキルと連携:
- 関連ドキュメントの更新提案
- TODOS.mdのステータス更新

## 入力形式

以下のいずれかで呼び出し可能:

```
implement: PDF透かし機能
implement: docs/TODOS.mdの「バッチ登録API」
implement: fastapi-htmx-spec.mdの02ページ仕様
```

## 注意事項

- 仕様が曖昧な場合は実装前に確認
- 大規模機能は分割して段階的に実装
- テストコードも同時に検討
