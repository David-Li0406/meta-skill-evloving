# MCP Server Setup

## Architecture

```text
MCP Client (Claude) <--stdio/http--> Unity-MCP-Server <--SignalR--> Unity-MCP-Plugin
```

## Startup Order (Critical)

1. **Run `start-mcp-server.bat`** in the project root- MUST be first, keep window open
2. **Open Unity Editor** - Plugin auto-connects (keepConnected: true)
3. **Open Claude Code** - Run `/mcp` to verify connection

## Configuration Files

| File                                                                                           | Purpose                       |
| ---------------------------------------------------------------------------------------------- | ----------------------------- |
| `C:/Users/jon/.claude/plugins/marketplaces/vui-vux/plugins/zero-day-dev/mcp.json`              | Claude Code MCP server config |
| `C:/Users/jon/Documents/GitHub/zero-day-attack/Assets/Resources/AI-Game-Developer-Config.json` | Unity plugin settings         |
| `C:/Users/jon/Documents/GitHub/zero-day-attack/start-mcp-server.bat`                           | Server startup script         |

## Server Location

```text
Library/mcp-server/win-x64/unity-mcp-server.exe
```

## HTTP Mode (Multi-Session)

```json
{
  "mcpServers": {
    "ai-game-developer": {
      "type": "http",
      "url": "http://localhost:56688"
    }
  }
}
```

## CLI Arguments

| Argument             | Purpose                       | Default |
| -------------------- | ----------------------------- | ------- |
| `--port`             | SignalR port for Unity Plugin | `8080`  |
| `--client-transport` | Protocol (`http` or `stdio`)  | `http`  |
| `--plugin-timeout`   | Response timeout (ms)         | `10000` |

## Transport Types

- **STDIO**: Direct integration, single session
- **HTTP**: Server-Sent Events + POST, multi-session capable

## Troubleshooting

### Server Won't Connect

1. Verify Unity Editor is running with plugin active
2. Check port not in use by another process
3. Check firewall settings
4. View logs

### Unity Plugin Reconnection

If Unity opened before server:

1. Run `start-mcp-server.bat` in project root
2. Plugin auto-reconnects via `keepConnected: true`
3. Manual: `Window > AI Game Developer (Unity-MCP)`
