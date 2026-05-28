# Web検索

Codex CLI を使用して Web 検索を実行する。

## 使用方法

```bash
${CLAUDE_PLUGIN_ROOT}/skills/use-codex/scripts/web-search.sh "検索クエリ"
```

## 引数

| 引数 | 必須 | 説明 |
|------|------|------|
| query | ○ | 検索クエリ |

## 例

```bash
${CLAUDE_PLUGIN_ROOT}/skills/use-codex/scripts/web-search.sh "TypeScript 5.0 new features"
```

## 技術詳細

- `codex exec --sandbox workspace-write --enable web_search_request` で実行
- ネットワークアクセスが必要なため `workspace-write` サンドボックスを使用
