# Claude Code ステータスライン設定スキル

Claude Code のステータスライン表示を自動的に設定するスキルです。

## 概要

このスキルを使用すると、以下の情報を表示するカスタムステータスラインを自動設定できます：

- 📁 **ディレクトリ名**（青色で強調）
- 🌿 **Git ブランチ名**（括弧内、現在のブランチ）
- 🤖 **モデル名**（角括弧内、使用中のモデル）
- 📊 **トークン情報**（合計、入力、出力、キャッシュ読み取り）

### 表示例

```
skillth (feature/setup-statusline) [Sonnet] | 📊 38.8K (In:37442 Out:0 Cache:0)
```

## 主な機能

- ✅ **自動設定**: 1コマンドでステータスライン設定が完了
- ✅ **既存設定の保護**: 既存の `settings.json` を保持しながらマージ
- ✅ **バックアップ作成**: 設定ファイル更新前に自動バックアップ
- ✅ **冪等性**: 複数回実行しても安全
- ✅ **エラーハンドリング**: 分かりやすいエラーメッセージ

## 使用方法

### スキル経由での実行（推奨）

Claude Code の対話中に以下のように指示してください：

```
ステータスラインを設定して
```

または

```
statuslineをセットアップ
```

### 直接実行

```bash
.claude/skills/setup-statusline/setup.sh
```

## 前提条件

### 必須

- **jq**: JSON処理に使用

#### jq のインストール

**macOS:**
```bash
brew install jq
```

**Ubuntu/Debian:**
```bash
sudo apt-get install jq
```

**Fedora/RHEL:**
```bash
sudo dnf install jq
```

**確認方法:**
```bash
jq --version
# jq-1.6 のような出力が表示されればOK
```

## 設定内容

### 1. `~/.claude/settings.json`

以下の設定が追加されます（既存設定は保持）：

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 0
  }
}
```

### 2. `~/.claude/statusline.sh`

カスタムスクリプトが作成され、以下の情報を表示します：

- **ディレクトリ名**: `basename` で現在のディレクトリ名を取得
- **Git ブランチ**: `git branch --show-current` で現在のブランチを取得
- **モデル名**: Claude Code から渡される `model.display_name` を使用
- **トークン情報**: 入力トークン、出力トークン、キャッシュトークンの詳細

## トラブルシューティング

### ❌ "jq が見つかりません"

**原因**: `jq` コマンドがインストールされていません

**解決方法**: 上記の「前提条件」セクションに従って `jq` をインストールしてください

### ❌ "~/.claude/ ディレクトリの作成に失敗しました"

**原因**: ホームディレクトリへの書き込み権限がありません

**解決方法**:
```bash
# ホームディレクトリの権限を確認
ls -ld ~/
# 必要に応じて権限を修正
chmod 755 ~/
```

### ❌ ステータスラインが表示されない

**確認事項**:
1. Claude Code を再起動してください
2. `~/.claude/settings.json` に `statusLine` セクションがあることを確認
3. `~/.claude/statusline.sh` が実行可能であることを確認:
   ```bash
   ls -l ~/.claude/statusline.sh
   # -rwxr-xr-x のような表示が必要
   ```

### ❌ トークン情報が表示されない

**原因**: スクリプトの実行に必要な `jq` が正しく動作していない可能性があります

**解決方法**:
```bash
# jq が正しくインストールされているか確認
jq --version

# スクリプトを直接テストしてエラーを確認
echo '{"workspace":{"current_dir":"/app"},"model":{"display_name":"Sonnet"},"context_window":{"current_usage":{"input_tokens":1000,"output_tokens":500}}}' | ~/.claude/statusline.sh
```

## 技術詳細

### スクリプトの動作

1. **JSON入力の受信**: Claude Code からステータスライン情報を JSON 形式で受信
2. **データ抽出**: `jq` で必要な情報を抽出
3. **Git 情報取得**: 現在のディレクトリから Git ブランチ情報を取得
4. **フォーマット**: ANSI エスケープコードでカラー表示
5. **出力**: フォーマット済みの文字列を標準出力に出力

### 設計上の考慮事項

- **エラーハンドリング**: `set -e` で厳格なエラー処理
- **冪等性**: 複数回実行しても同じ結果
- **バックアップ**: 既存ファイルは `.backup` サフィックスで保存
- **セキュリティ**: ホームディレクトリ内のみ操作、sudo 不要

## ファイル構成

```
plugins/awesome-statusline/skills/setup-statusline/
├── SKILL.md
├── README.md
└── setup.sh
```

## ライセンス

このスキルは awesome-statusline プラグインの一部として提供されています。
