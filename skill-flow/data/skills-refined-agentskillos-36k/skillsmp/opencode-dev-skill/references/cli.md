# CLI Commands

## Basic Usage

```bash
# Start TUI (default)
opencode

# Start TUI in specific directory
opencode /path/to/project

# Non-interactive mode
opencode run "Your prompt here"
```

## TUI Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--continue` | `-c` | Continue last session |
| `--session` | `-s` | Session ID to continue |
| `--prompt` | | Initial prompt |
| `--model` | `-m` | Model (provider/model format) |
| `--agent` | | Agent to use (build/plan) |
| `--port` | | Server port |
| `--hostname` | | Server hostname |

## Commands

### `opencode run`

Non-interactive mode for scripting:

```bash
opencode run "Explain closures in JavaScript"
opencode run -m anthropic/claude-sonnet-4-20250514 "Write tests"
opencode run -c "Continue the previous task"  # Continue last session
opencode run -f file.ts "Review this file"    # Attach file
opencode run --format json "Query"            # Raw JSON events output
opencode run --attach http://localhost:4096 "Query"  # Use existing server
```

| Flag | Short | Description |
|------|-------|-------------|
| `--command` | | Command to run |
| `--continue` | `-c` | Continue last session |
| `--session` | `-s` | Session ID |
| `--share` | | Share session after completion |
| `--model` | `-m` | Model (provider/model) |
| `--agent` | | Agent (build/plan) |
| `--file` | `-f` | File(s) to attach |
| `--format` | | Output: default or json |
| `--title` | | Session title |
| `--attach` | | Attach to running server |
| `--port` | | Local server port |

### `opencode serve`

Start headless HTTP server:

```bash
opencode serve
opencode serve --port 4096 --hostname 0.0.0.0
```

| Flag | Description |
|------|-------------|
| `--port` | Port (default: 4096) |
| `--hostname` | Hostname (default: 127.0.0.1) |
| `--mdns` | Enable mDNS discovery |
| `--cors` | Additional CORS origins |

### `opencode attach`

Attach TUI to running server:

```bash
# Start server in one terminal
opencode serve --port 4096

# Attach TUI in another
opencode attach http://localhost:4096
```

| Flag | Short | Description |
|------|-------|-------------|
| `--dir` | | Working directory |
| `--session` | `-s` | Session ID |

### `opencode web`

Start server with web interface:

```bash
opencode web
opencode web --port 8080
```

### `opencode auth`

Manage provider credentials:

```bash
opencode auth login     # Configure API keys
opencode auth list      # List authenticated providers
opencode auth logout    # Remove credentials
```

### `opencode session`

Session management:

```bash
opencode session list           # List all sessions
opencode session list -n 10     # Last 10 sessions
opencode session list --format json
```

### `opencode models`

List available models:

```bash
opencode models              # All models
opencode models anthropic    # Filter by provider
opencode models --refresh    # Refresh cache
opencode models --verbose    # Include metadata/costs
```

### `opencode mcp`

Manage MCP servers:

```bash
opencode mcp add      # Add MCP server
opencode mcp list     # List configured servers
opencode mcp auth     # Authenticate with OAuth server
opencode mcp logout   # Remove OAuth credentials
```

### `opencode agent`

Manage agents:

```bash
opencode agent list    # List agents
opencode agent create  # Create custom agent
```

### `opencode github`

GitHub agent integration:

```bash
opencode github install  # Install in repository
opencode github run      # Run (for CI)
```

### Other Commands

```bash
opencode stats              # Token usage & costs
opencode export [sessionID] # Export session as JSON
opencode import <file>      # Import session
opencode upgrade            # Update to latest version
opencode uninstall          # Uninstall OpenCode
```

## Global Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--help` | `-h` | Display help |
| `--version` | `-v` | Print version |
| `--print-logs` | | Print logs to stderr |
| `--log-level` | | Log level (DEBUG, INFO, WARN, ERROR) |

## Environment Variables

### General

| Variable | Description |
|----------|-------------|
| `OPENCODE_CONFIG` | Path to config file |
| `OPENCODE_CONFIG_DIR` | Path to config directory |
| `OPENCODE_CONFIG_CONTENT` | Inline JSON config |
| `OPENCODE_CLIENT` | Client identifier (default: cli) |

### Server

| Variable | Description |
|----------|-------------|
| `OPENCODE_SERVER_PASSWORD` | Enable HTTP basic auth |
| `OPENCODE_SERVER_USERNAME` | Override auth username (default: opencode) |

### Feature Flags

| Variable | Description |
|----------|-------------|
| `OPENCODE_AUTO_SHARE` | Auto-share sessions |
| `OPENCODE_DISABLE_AUTOUPDATE` | Disable update checks |
| `OPENCODE_DISABLE_LSP_DOWNLOAD` | Disable LSP downloads |
| `OPENCODE_DISABLE_CLAUDE_CODE` | Disable reading .claude |
| `OPENCODE_ENABLE_EXA` | Enable Exa web search |

### Experimental

| Variable | Description |
|----------|-------------|
| `OPENCODE_EXPERIMENTAL` | Enable all experimental features |
| `OPENCODE_EXPERIMENTAL_BASH_MAX_OUTPUT_LENGTH` | Max bash output |
| `OPENCODE_EXPERIMENTAL_BASH_DEFAULT_TIMEOUT_MS` | Bash timeout |
| `OPENCODE_EXPERIMENTAL_OUTPUT_TOKEN_MAX` | Max output tokens |

## Programmatic Usage Examples

### Batch Processing

```bash
# Process multiple files
for file in src/*.ts; do
  opencode run -f "$file" "Add JSDoc comments" --title "JSDoc: $file"
done
```

### CI Integration

```bash
# In GitHub Actions
opencode run --attach http://localhost:4096 \
  "Review the changes in this PR" \
  --format json > review.json
```

### Server + Client Pattern

```bash
# Terminal 1: Start server
opencode serve --port 4096

# Terminal 2+: Send queries
opencode run --attach http://localhost:4096 "Query 1"
opencode run --attach http://localhost:4096 "Query 2"
# Avoids MCP cold boot on each query
```
