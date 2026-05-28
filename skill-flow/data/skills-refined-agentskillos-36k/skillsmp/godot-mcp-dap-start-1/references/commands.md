# MCP + Debug Quick Checks

## MCP handshake
- `npx -y godot-mcp-cli@latest --list-tools --verbose --timeout 7000`

## Start game (debug connection)
- `npx -y godot-mcp-cli@latest run_project --timeout 7000`

## Port checks
- MCP WebSocket: `Get-NetTCPConnection -LocalPort 9080`
- Godot debug: `Get-NetTCPConnection -LocalPort 6007`

## One-editor rule
If MCP is flaky, stop all Godot processes and relaunch a single editor instance.
