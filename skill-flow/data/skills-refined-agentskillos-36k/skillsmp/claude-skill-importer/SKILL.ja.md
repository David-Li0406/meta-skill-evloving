---
name: claude-skill-importer (JP)
description: Claude Code のスキル（Markdownファイル）を Antigravity のスキル構造に自動的にインポート・正規化します。
language: ja
---

> **Note**: This is a placeholder for the Japanese translation.
> **注記**: これは日本語訳のプレースホルダーです。

# Claude Skill Importer

このスキルは、"Claude Code" 用に定義されたスキル（例：`any-forward/skills` や個別の `.md` ファイル）をインポートし、Antigravity Agents で必要な構造化フォーマットに変換するユーティリティを提供します。

## 機能

1. **インポート**: ソースディレクトリからスキルをコピーします。
2. **正規化**:
   - 有効な YAML Frontmatter (`name`, `description`) が存在することを確認します。
   - フラットな `.md` ファイルを有効なスキルディレクトリ (`folder/SKILL.md`) に変換します。
3. **完全性担保**:
   - `metadata.json` を自動生成します。
   - 厳格なフォーマット要件を満たすために `SKILL.ja.md`（日本語プレースホルダー）を自動生成します。

## 使用方法

同梱のスクリプトを `run_command` 経由で実行することで呼び出せます。

### コマンド構文

```bash
node .gemini/antigravity/skills/ai-tools/claude-skill-importer/scripts/importer.js <SOURCE_DIRECTORY> [TARGET_CATEGORY_NAME]
```

- **SOURCE_DIRECTORY**: Claudeスキルを含むフォルダへの絶対パス。以下がサポートされます：
  - `.md` ファイルを含むフラットなフォルダ。
  - 標準的な `plugins/` 構造（Trail of Bits スタイル）。
- **TARGET_CATEGORY_NAME** (オプション): これらが配置される `antigravity/skills/` 内のサブディレクトリ名。デフォルトは `imported-skills` です。

## 翻訳プロセス（インポート後）

インポートスクリプトは `SKILL.ja.md` を**プレースホルダー**として生成します。以下の手順で翻訳を完了させてください。

1. **確認**: 生成された `SKILL.ja.md` を確認します。`> 注記: これは日本語訳のプレースホルダーです` というブロックが含まれています。
2. **翻訳実行**:
   - 英語版 `SKILL.md` の内容を読み込みます。
   - タイトル、説明、本文を日本語に翻訳してください。
   - **重要**: YAML Frontmatter のキー（`name`, `description` など）は英語のまま維持しますが、その**値**は必要に応じて翻訳（または `(JP)` を付与）してください。また `language: ja` が含まれていることを確認してください。
3. **上書き**: `SKILL.ja.md` のプレースホルダー内容を、完全な翻訳内容で上書き保存してください。
