---
name: doc-sync
description: |
  実装変更後にドキュメント同期を支援。変更ファイルから影響するドキュメントを特定し、更新提案を行う。
  トリガー: 「ドキュメント同期」「doc-sync」「ドキュメント更新」「実装とドキュメントの同期」
allowed-tools: Read, Grep, Glob, Bash
---

# doc-sync: ドキュメント同期スキル

## 目的
実装変更後、関連ドキュメントの更新漏れを防止する。

## 実行手順

### Step 1: 変更ファイルの特定

```bash
# 直近のコミット差分を取得
git diff --name-only HEAD~1

# またはステージング中の変更
git diff --name-only --cached

# 未コミットの変更
git diff --name-only
```

### Step 2: 影響ドキュメントのマッピング

変更ファイルのパスに基づき、以下のルールで関連ドキュメントを特定:

| 変更パス | 関連ドキュメント |
|----------|------------------|
| `demo_app/` | `docs/fastapi-htmx-spec.md`, `docs/TODOS.md` |
| `demo_app/templates/` | `docs/ui/*.html` (UIモック) |
| `demo_app/services/` | `docs/fastapi-htmx-spec.md` |
| `azure_/` | `CLAUDE.md` (既存モジュール節) |
| `requirements.txt` | `README.md` (セットアップ節) |
| `*.py` (新規) | 対応する `docs/<module>.md` 作成検討 |

### Step 3: ドキュメント更新チェック

各関連ドキュメントを読み、以下を確認:
1. 変更内容が既存記述と矛盾していないか
2. 新機能/変更が未記載でないか
3. 削除された機能の記述が残っていないか

### Step 4: 更新提案の出力

以下のフォーマットで報告:

```
## doc-sync レポート

### 変更ファイル
- path/to/changed/file.py

### 要更新ドキュメント
1. **docs/fastapi-htmx-spec.md**
   - 理由: 新エンドポイント追加
   - 推奨: API一覧に `/api/new-endpoint` を追記

2. **docs/TODOS.md**
   - 理由: タスク完了
   - 推奨: 該当タスクを完了済みに変更

### 更新不要
- docs/ui/index.html (影響なし)
```

### Step 5: 自動更新オプション

ユーザー確認後、以下を実行可能:
- ドキュメントへの追記
- TODOステータス更新
- 新規ドキュメント雛形作成

## 注意事項

- CLAUDE.mdの簡潔性ルールを遵守
- 推測による更新は行わない（確認を優先）
- 大規模変更時は優先度付けして報告
