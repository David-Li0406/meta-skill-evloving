# リポジトリ更新の取り込み

## 基本的な同期手順

```bash
cd ~/dev/projects/dotfiles

# 1. 変更を取得
git fetch origin

# 2. 現在の状態確認
git status

# 3. マージまたはリベース
git pull --rebase origin main

# 4. stowで再適用
./install.sh
```

## コンフリクト発生時

### ローカル変更がある場合

```bash
# 一時退避
git stash

# 更新取り込み
git pull --rebase origin main

# 退避分を復元
git stash pop

# コンフリクト解消後
git add -A
git rebase --continue
```

### 特定パッケージのみ更新

```bash
# 該当パッケージのみ再適用
./install.sh shell nvim
```

## 別マシンからの変更を反映

### 状況: 別PCで設定変更してpush済み

```bash
# 1. 取得
git fetch origin

# 2. 差分確認
git diff HEAD origin/main

# 3. 取り込み
git pull --rebase origin main

# 4. 必要に応じてstow再適用
./install.sh
```

## miseツールの同期

```bash
# config.tomlが更新された場合
mise install
```

## MCPサーバーの同期

```bash
# mcp-servers.yamlが更新された場合
~/.claude/scripts/install-mcp.sh
```

## トラブルシューティング

### stowがコンフリクトを報告

```bash
# 既存ファイルをdotfilesに取り込む
./install.sh -a <package>

# または既存ファイルを削除してから再実行
rm ~/.conflicting-file
./install.sh <package>
```

### シンボリックリンクが切れている

```bash
# 再適用
./install.sh -D <package>  # 削除
./install.sh <package>      # 再作成
```
