---
name: mcp-setup-guide
description: MCP設定ガイド - Claude Code向けMCPサーバーのセットアップ・トラブルシュート
---

## 設定ファイル

| スコープ | パス |
|---------|------|
| グローバル | `~/.claude.json` |
| プロジェクト | `.claude/mcp.json` |

## 設定例

```json
{
  "mcpServers": {
    "serena": {
      "command": "serena",
      "args": ["start-mcp-server", "--context", "ide-assistant"]
    },
    "jira": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-jira"],
      "env": {
        "JIRA_HOST": "https://your.atlassian.net",
        "JIRA_EMAIL": "your@email.com",
        "JIRA_API_TOKEN": "your-token"
      }
    },
    "confluence": {
      "command": "node",
      "args": ["/path/to/confluence-mcp/dist/index.js"],
      "env": {
        "CONFLUENCE_HOST": "https://your.atlassian.net",
        "CONFLUENCE_EMAIL": "your@email.com",
        "CONFLUENCE_API_TOKEN": "your-token"
      }
    }
  }
}
```

## トラブルシュート

### 1. Failed to connect

```bash
# コマンドが存在するか確認
which serena
# または
ls /path/to/command

# 手動実行でエラー確認
serena start-mcp-server --context ide-assistant
```

### 2. 権限エラー

```bash
chmod +x /path/to/command
```

### 3. 環境変数問題

```bash
# シェルで直接テスト
JIRA_HOST="..." JIRA_EMAIL="..." npx -y @anthropic/mcp-jira
```

### 4. npx/node パス問題

```json
{
  "command": "node",
  "args": ["/path/to/script.js"]
}
```

## よく使うMCPサーバー

| 名前 | 用途 | インストール |
|------|------|-------------|
| Serena | コード分析 | `pip install serena` |
| Jira | チケット管理 | `npx @anthropic/mcp-jira` |
| Confluence | ドキュメント | カスタム実装 |
| Context7 | ライブラリドキュメント | `npx @anthropic/mcp-context7` |
| Codex | AI補完 | `codex-mcp` |

## 確認方法

```bash
# Claude Code内で
/mcp
# → 接続状態を確認
```
