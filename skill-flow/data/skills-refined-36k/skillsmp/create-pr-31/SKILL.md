---
name: create-pr
description: ブランチ作成・コミット・PR作成ワークフロー
---

# Create PR Command

検証済みの実装をブランチにコミットし、PRを作成するコマンドです。

## 前提条件

- `/verify-feature` で検証が完了していること
- すべての検証が ✅ であること（推奨）

---

## 開始時の処理

コマンド実行時、**必ず TodoWrite ツールを呼び出して**タスクリストを初期化する。
末尾の「TodoWrite用データ」セクションのJSONを使用し、最初のタスクを `in_progress` に設定。

---

## Phase 1: 準備

### Step 1: 変更内容の確認

```
PRを作成します。

まず、変更内容を確認しています...
```

以下を実行:
```bash
git status
git diff --stat
```

変更ファイル一覧とステータスを表示。

### Step 2: ステアリングディレクトリの特定

`docs/steering/` 内の進行中ディレクトリを特定し、機能名を取得。

---

## Phase 2: ブランチ作成・コミット

### Step 3: ブランチ作成

```bash
git checkout -b feature/{機能名}
```

### Step 4: 変更のステージング

```
以下のファイルをコミットします:

{変更ファイル一覧}

コミットしてよいですか？
```

ユーザーの確認後:
```bash
git add .
```

### Step 5: コミット

```bash
git commit -m "feat({機能名}): implement {機能名}"
```

コミットメッセージはユーザーが指定した場合はそれを使用。

---

## Phase 3: PR作成

### Step 6: プッシュ

```bash
git push -u origin feature/{機能名}
```

### Step 7: PR作成

```bash
gh pr create \
  --base main \
  --title "[{機能名}] 実装" \
  --body "$(cat <<'EOF'
## 概要
{機能名}の実装

## 検証状況
- [x] ビルド通過
- [x] テスト通過
- [x] セキュリティチェック通過
- [x] ドキュメント整合性確認

## 設計ドキュメント
- `docs/steering/{YYYYMMDD}-{機能名}/`
EOF
)"
```

### Step 8: 完了

```
PRを作成しました！

**PR URL**: {pr_url}
**ブランチ**: feature/{機能名}

ステアリングディレクトリをアーカイブする場合:
mv docs/steering/{YYYYMMDD}-{機能名} docs/steering/archive/
```

---

## エラーハンドリング

- **コンフリクト**: main をマージして解決を促す
- **プッシュ失敗**: エラー内容を表示し、対処法を提示
- **PR作成失敗**: gh auth status を確認するよう促す

---

## 注意事項

- コミット前にユーザーの確認を取る
- 機密情報（.env等）がコミットされないよう確認
- PR作成後、ステアリングディレクトリのアーカイブを提案

---

## TodoWrite用データ

```json
[
  {"content": "変更内容の確認", "activeForm": "変更内容を確認中", "status": "pending"},
  {"content": "ステアリングディレクトリの特定", "activeForm": "ステアリングディレクトリを特定中", "status": "pending"},
  {"content": "ブランチ作成", "activeForm": "ブランチを作成中", "status": "pending"},
  {"content": "変更のステージング", "activeForm": "変更をステージング中", "status": "pending"},
  {"content": "コミット", "activeForm": "コミット中", "status": "pending"},
  {"content": "プッシュ", "activeForm": "プッシュ中", "status": "pending"},
  {"content": "PR作成", "activeForm": "PRを作成中", "status": "pending"},
  {"content": "完了処理", "activeForm": "完了処理中", "status": "pending"}
]
```
