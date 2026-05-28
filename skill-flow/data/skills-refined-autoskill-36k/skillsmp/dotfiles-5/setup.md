# 新規PCセットアップ

## 前提条件

- Git
- GNU Stow
- curl（mise インストール用）

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y git stow curl

# macOS
brew install git stow curl
```

## セットアップ手順

### 1. リポジトリのクローン

```bash
mkdir -p ~/dev/projects
cd ~/dev/projects
git clone git@github.com:<user>/dotfiles.git
cd dotfiles
```

### 2. 既存設定のバックアップ

```bash
# 重要な既存設定をバックアップ
mkdir -p ~/dotfiles-backup
cp -r ~/.zshrc ~/.bashrc ~/.config ~/dotfiles-backup/ 2>/dev/null || true
```

### 3. dotfilesのインストール

```bash
# ドライランで確認
./install.sh -n

# 問題なければ実行
./install.sh
```

### 4. mise（ツール管理）のセットアップ

```bash
# miseインストール
curl https://mise.run | sh

# シェル再起動またはsource
source ~/.zshrc

# ツールインストール
mise install
```

### 5. Claude Code MCPサーバー

```bash
# MCPサーバーインストール
~/.claude/scripts/install-mcp.sh
```

### 6. Gemini CLI認証

```bash
# OAuth認証
gemini auth login
```

## パッケージ別の追加設定

### nvim

```bash
# プラグインインストール（初回起動時に自動）
nvim
```

### shell

```bash
# シェル再起動
exec $SHELL
```

## 確認

```bash
# シンボリックリンク確認
ls -la ~/.zshrc ~/.config/nvim ~/.claude

# mise確認
mise doctor

# Claude MCP確認
claude mcp list
```

## トラブルシューティング

### stowエラー: 既存ファイルとコンフリクト

```bash
# 既存ファイルをdotfilesに取り込む
./install.sh -a

# または手動で既存ファイルを削除/移動してから再実行
```

### mise: command not found

```bash
# PATHに追加（一時的）
export PATH="$HOME/.local/bin:$PATH"

# または.zshrcをsource
source ~/.zshrc
```
