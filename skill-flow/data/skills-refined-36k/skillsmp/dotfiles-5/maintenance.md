# メンテナンス方針

## 設定変更時のワークフロー

### 1. 既存設定の編集

シンボリックリンク先のファイルを直接編集可能:

```bash
# 例: nvim設定を編集
nvim ~/.config/nvim/init.lua
# → 実体は packages/nvim/.config/nvim/init.lua
```

### 2. 新規ファイル追加

```bash
# 1. パッケージディレクトリに追加
cp ~/.new-config packages/<package>/

# 2. 既存ファイルがある場合は削除してstow
rm ~/.new-config
./install.sh <package>
```

### 3. 変更のコミット

```bash
cd ~/dev/projects/dotfiles
git add -A
git commit -m "feat(<package>): 変更内容"
git push
```

## パッケージ追加手順

### 新規ツールの設定を追加

```bash
# 1. ディレクトリ作成
mkdir -p packages/<name>/.config/<name>

# 2. 設定ファイル配置
cp ~/.config/<name>/config.yaml packages/<name>/.config/<name>/

# 3. 元ファイル削除
rm -rf ~/.config/<name>

# 4. stowで適用
./install.sh <name>

# 5. 確認
ls -la ~/.config/<name>
```

## 依存関係の管理

### mise（ツールバージョン管理）

```bash
# ツール追加
nvim ~/.config/mise/config.toml

# 適用
mise install
```

config.toml例:
```toml
[tools]
"aqua:mikefarah/yq" = "latest"
node = "22"
python = "3.12"
```

### MCPサーバー

```bash
# リスト編集
nvim ~/.claude/scripts/mcp-servers.yaml

# 適用
~/.claude/scripts/install-mcp.sh
```

### Claude Codeプラグイン

```bash
# リスト編集
nvim ~/.claude/scripts/plugins.yaml

# 適用
~/.claude/scripts/install-plugins.sh

# ドライラン
~/.claude/scripts/install-plugins.sh --dry-run
```

plugins.yaml例:
```yaml
marketplaces:
  - name: anthropic-agent-skills
    repo: anthropics/skills

plugins:
  - name: example-skills
    marketplace: anthropic-agent-skills
    description: docx/pdf/pptx/xlsx等
```

## 定期メンテナンス

### 月次

- [ ] 未使用パッケージの確認・削除
- [ ] mise/ツールのバージョン更新
- [ ] MCPサーバーの確認
- [ ] プラグインの更新確認

### 不要ファイルの削除

```bash
# stowリンク解除
./install.sh -D <package>

# パッケージ削除
rm -rf packages/<package>
```
