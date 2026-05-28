---
name: setup-statusline
description: Setup Claude Code statusline configuration automatically (global)
trigger: ユーザーが「ステータスラインを設定」「statuslineをセットアップ」「ステータスライン設定して」「statusline設定」などと指示した場合、または自然言語で「ステータスバーを設定して」「status lineを初期化して」などと指示した場合
---

# Claude Code ステータスライン設定スキル

**MANDATORY**: このスキルは、ユーザーが Claude Code のステータスライン設定を要求した場合に **MUST** 使用されます。

## トリガー条件

以下のいずれかの指示があった場合、このスキルを自動的に使用してください：
- 「ステータスラインを設定」
- 「statuslineをセットアップ」
- 「ステータスライン設定して」
- 「statusline設定」
- 「ステータスバーを設定して」
- 「status lineを初期化して」
- 「Claude Codeのステータスライン」

## 目的

- Claude Code のステータスライン表示を自動設定
- グローバル設定 (`~/.claude/settings.json`) にステータスライン設定を追加
- カスタムスクリプト (`~/.claude/statusline.sh`) を作成
- 既存の設定を保持しながら安全にマージ

## スキル呼び出し方法

このスキルは Skill ツールで呼び出します：

```
Skill(skill="setup-statusline")
```

引数は不要です。

## 実行手順

### 1. セットアップの実行

```bash
.claude/skills/setup-statusline/setup.sh
```

このスクリプトは以下を自動的に実行します：
1. **前提条件チェック**: `jq` コマンドのインストール確認
2. **ディレクトリ作成**: `~/.claude/` ディレクトリの確認/作成
3. **設定ファイルのマージ**: `~/.claude/settings.json` に statusLine セクションを追加（既存設定は保持）
4. **スクリプト作成**: `~/.claude/statusline.sh` を作成して実行権限を付与

### 2. 設定内容

**追加される設定 (`~/.claude/settings.json`):**
```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 0
  }
}
```

**作成されるスクリプト (`~/.claude/statusline.sh`):**
- ディレクトリ名（青色）
- Git ブランチ名（括弧内、薄い色）
- モデル名（角括弧内、薄い色）
- トークン情報（合計、入力、出力、キャッシュ）

### 3. 表示例

```
skillth (feature/setup-statusline) [Sonnet] | 📊 38.8K (In:37442 Out:0 Cache:0)
```

### 4. 実行結果の判定

- ✅ **成功**: スクリプトが終了コード 0 で終了、成功メッセージを表示
- ❌ **失敗**: スクリプトが非 0 の終了コードで終了、エラーメッセージを表示

## 重要なルール

1. **既存設定の保護**: 既存の `settings.json` の設定は保持される
2. **バックアップ作成**: 設定ファイル更新時に自動的に `.backup` ファイルを作成
3. **冪等性**: 複数回実行しても安全
4. **jq必須**: JSON操作に `jq` コマンドが必要

## セキュリティ

- スクリプト権限: 755 (rwxr-xr-x)
- 設定ファイル権限: 644 (rw-r--r--)
- ホームディレクトリ内のみ操作
- sudo 権限不要

## トラブルシューティング

### jq が見つからない場合

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

### 権限エラーの場合

`~/.claude/` ディレクトリの権限を確認：
```bash
ls -ld ~/.claude/
chmod 755 ~/.claude/
```

## 参考資料

- [README.md](README.md) - 詳細な使用方法とトラブルシューティング
