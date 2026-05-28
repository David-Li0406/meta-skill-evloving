# ファイルレビュー

Codex CLI を使用してファイルのコードレビューを実行する。

## 使用方法

```bash
${CLAUDE_PLUGIN_ROOT}/skills/use-codex/scripts/file-review.sh <file-path> [review-focus]
```

## 引数

| 引数 | 必須 | 説明 |
|------|------|------|
| file-path | ○ | レビュー対象のファイルパス |
| review-focus | - | レビューの観点（例: security, performance, readability） |

## 例

```bash
# 基本的なレビュー
${CLAUDE_PLUGIN_ROOT}/skills/use-codex/scripts/file-review.sh src/auth.ts

# セキュリティ観点でのレビュー
${CLAUDE_PLUGIN_ROOT}/skills/use-codex/scripts/file-review.sh src/auth.ts "security"
```

## 技術詳細

- `codex exec --sandbox read-only` で実行
- ファイル読み取りのみなので安全な read-only サンドボックスを使用
