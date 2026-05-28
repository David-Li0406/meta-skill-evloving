# Diagnostic Techniques

Comprehensive diagnostic procedures for Claude Code troubleshooting.

## claude doctor Command

The `claude doctor` command performs comprehensive health checks.

### Basic Usage

```bash
# Full health check
claude doctor

# Check specific component
claude doctor --component api
claude doctor --component mcp
claude doctor --component hooks
claude doctor --component permissions
claude doctor --component config
```

### Output Interpretation

```
Claude Code Health Check
========================

[PASS] API Connection
  - Endpoint: api.anthropic.com
  - Latency: 145ms
  - Auth: Valid

[PASS] Configuration
  - Settings: ~/.claude/settings.json
  - Projects: 3 configured

[WARN] MCP Servers
  - memory: Connected (3 tools)
  - filesystem: Disconnected (timeout)

[PASS] Hooks
  - 5 hooks registered
  - 0 syntax errors

[FAIL] Permissions
  - Write denied for /etc/*
  - (This is expected for system directories)
```

### Status Meanings

| Status | Icon | Meaning |
|--------|------|---------|
| PASS | Green checkmark | Component working correctly |
| WARN | Yellow warning | Non-critical issue |
| FAIL | Red X | Critical issue requiring attention |
| SKIP | Gray dash | Check skipped (not applicable) |

## Debug Flag Usage

### --debug Flag

Enables verbose output for all operations:

```bash
# Start with debug mode
claude --debug

# Redirect to file for analysis
claude --debug 2>&1 | tee debug-output.log
```

### Debug Output Sections

```
[DEBUG] 2025-01-08T10:30:00.000Z - Initializing Claude Code
[DEBUG] 2025-01-08T10:30:00.050Z - Loading config from ~/.claude/settings.json
[DEBUG] 2025-01-08T10:30:00.100Z - Found 5 hooks in settings
[DEBUG] 2025-01-08T10:30:00.150Z - Connecting to MCP server: memory
[DEBUG] 2025-01-08T10:30:00.500Z - MCP server memory connected with 3 tools
[DEBUG] 2025-01-08T10:30:01.000Z - API request: chat/completions
[DEBUG] 2025-01-08T10:30:02.500Z - API response received (1500ms)
[DEBUG] 2025-01-08T10:30:02.550Z - Tool call: Read
[DEBUG] 2025-01-08T10:30:02.600Z - Executing PreToolUse hooks for: Read
[DEBUG] 2025-01-08T10:30:02.650Z - Hook approved: Read
[DEBUG] 2025-01-08T10:30:02.700Z - Tool completed: Read (50ms)
[DEBUG] 2025-01-08T10:30:02.750Z - Executing PostToolUse hooks for: Read
```

### Filtering Debug Output

```bash
# Filter for specific patterns
claude --debug 2>&1 | grep "MCP"
claude --debug 2>&1 | grep "Hook"
claude --debug 2>&1 | grep "ERROR\|WARN"

# Filter for tool execution
claude --debug 2>&1 | grep "Tool"

# Filter for API calls
claude --debug 2>&1 | grep "API"
```

## ANTHROPIC_LOG Environment Variable

### Log Levels

| Level | Output |
|-------|--------|
| `error` | Only errors |
| `warn` | Errors and warnings |
| `info` | General information |
| `debug` | Verbose debugging |
| `trace` | Maximum verbosity |

### Usage

```bash
# Debug level logging
ANTHROPIC_LOG=debug claude

# Trace level (maximum detail)
ANTHROPIC_LOG=trace claude

# Combine with --debug
ANTHROPIC_LOG=debug claude --debug

# Save to file
ANTHROPIC_LOG=debug claude 2>&1 | tee ~/claude-log.txt
```

### Log Output Analysis

```bash
# Count log entries by level
grep -c "\[ERROR\]" ~/claude-log.txt
grep -c "\[WARN\]" ~/claude-log.txt
grep -c "\[DEBUG\]" ~/claude-log.txt

# Find specific errors
grep "\[ERROR\]" ~/claude-log.txt | sort | uniq -c | sort -rn

# Timeline of events
grep "^\[" ~/claude-log.txt | head -50
```

## Checking Tool Permissions

### View Current Permissions

```bash
# In Claude Code session
/permissions

# Show tool permissions specifically
/permissions --tools

# Show file access patterns
/permissions --files
```

### Permission Output

```
Current Permissions
===================

Tools:
  [ALLOW] Read, Edit, Write, Bash, Glob, Grep
  [ALLOW] WebFetch, WebSearch
  [DENY]  Task (requires approval)
  [ALLOW] mcp__memory__* (all memory tools)
  [DENY]  mcp__filesystem__delete_file

Files:
  [ALLOW] /Users/me/projects/**
  [DENY]  /etc/**
  [DENY]  ~/.ssh/**
  [ASK]   Everything else
```

### Permission Configuration

```json
// ~/.claude/settings.json
{
  "permissions": {
    "allow": [
      "Read",
      "Write",
      "Edit",
      "Bash(npm:*)",
      "mcp__memory__*"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "mcp__filesystem__delete_file"
    ]
  }
}
```

### Testing Permissions

```bash
# Test if a tool would be allowed
claude --test-permission "Write" "/path/to/file.txt"

# Debug permission decisions
claude --debug 2>&1 | grep "Permission"
```

## MCP Server Diagnostics

### List Servers

```bash
# CLI command
claude mcp list

# Output:
# NAME        STATUS       TOOLS  TRANSPORT
# memory      connected    3      stdio
# filesystem  disconnected 0      stdio
# web-search  connected    2      http
```

### Get Server Details

```bash
# Get specific server info
claude mcp get memory

# Output:
# Server: memory
# Status: Connected
# Transport: stdio
# Command: npx -y @anthropic/mcp-server-memory
# Tools:
#   - create_entities
#   - search_entities
#   - delete_entities
```

### Interactive MCP Status

```bash
# In Claude Code session
/mcp

# Shows:
# MCP Servers
# ===========
#
# [*] memory (connected)
#     Tools: create_entities, search_entities, delete_entities
#
# [ ] filesystem (disconnected)
#     Error: Connection timeout after 30000ms
#
# Actions: [r]econnect, [d]isconnect, [c]onfigure
```

### MCP Debug Logging

```bash
# Debug MCP connections
MCP_DEBUG=1 claude --debug

# Debug specific server
claude mcp get memory --debug

# Test server manually (stdio)
echo '{"jsonrpc":"2.0","method":"initialize","params":{},"id":1}' | npx -y @anthropic/mcp-server-memory
```

### Common MCP Issues

```bash
# Timeout issues - increase timeout
MCP_TIMEOUT=60000 claude

# Connection refused - check if server runs
npx -y @anthropic/mcp-server-memory

# Permission denied - check file permissions
ls -la ~/.claude/mcp/

# Environment variables not working
env | grep MCP
```

## Hook Debugging

### View Registered Hooks

```bash
# CLI command
claude --print-hooks

# In session
/hooks
```

### Hook Output Example

```
Registered Hooks
================

PreToolUse:
  1. Matcher: "Write|Edit"
     Command: /path/to/validate-changes.sh
     Timeout: 60000ms

PostToolUse:
  1. Matcher: "Write"
     Command: /path/to/format-file.sh
     Timeout: 30000ms

SessionStart:
  1. Matcher: ""
     Command: /path/to/setup-env.sh
     Timeout: 10000ms
```

### Validate Hook Configuration

```bash
# Validate JSON syntax
jq . ~/.claude/settings.json

# Pretty print hooks section
jq '.hooks' ~/.claude/settings.json

# Check for common errors
jq '.hooks | to_entries[] | .key as $event | .value[] | {event: $event, matcher: .matcher}' ~/.claude/settings.json
```

### Test Hook Scripts

```bash
# Create test input
cat > /tmp/hook-test.json << 'EOF'
{
  "session_id": "test-session",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/test/file.txt",
    "content": "test content"
  }
}
EOF

# Run hook script
cat /tmp/hook-test.json | /path/to/your-hook.sh
echo "Exit code: $?"
```

### Hook Debug Output

```bash
# Enable hook debugging
claude --debug 2>&1 | grep -i hook

# Sample output:
# [DEBUG] Executing hooks for PreToolUse:Write
# [DEBUG] Found 2 hook matchers in settings
# [DEBUG] Matched 1 hooks for query "Write"
# [DEBUG] Executing hook command: /path/to/hook.sh
# [DEBUG] Hook command completed with status 0
```

### Common Hook Issues

| Issue | Check | Solution |
|-------|-------|----------|
| Hook not found | `/hooks` output | Check JSON syntax |
| Matcher not matching | Case sensitivity | Use exact tool name |
| Script not running | File permissions | `chmod +x script.sh` |
| Script fails | Exit code | Test script in isolation |
| Wrong output | stdout vs stderr | Errors to stderr |

## Network Diagnostics

### API Connectivity

```bash
# Test API endpoint
curl -I https://api.anthropic.com/v1/messages

# Test with authentication
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "content-type: application/json" \
  -d '{"model":"claude-sonnet-4-20250514","max_tokens":10,"messages":[{"role":"user","content":"Hi"}]}'
```

### Proxy Configuration

```bash
# Check proxy settings
env | grep -i proxy

# Test with proxy
HTTP_PROXY=http://proxy:8080 curl -I https://api.anthropic.com

# Configure Claude with proxy
HTTP_PROXY=http://proxy:8080 HTTPS_PROXY=http://proxy:8080 claude
```

### DNS and Network

```bash
# Check DNS resolution
nslookup api.anthropic.com

# Check network path
traceroute api.anthropic.com

# Check firewall (macOS)
sudo pfctl -sr | grep anthropic
```

## Configuration Diagnostics

### View Configuration

```bash
# View settings (without secrets)
cat ~/.claude/settings.json | jq 'del(.credentials)'

# View project settings
cat .claude/settings.json

# View MCP configuration
cat .mcp.json
```

### Validate Configuration

```bash
# Validate all JSON files
for f in ~/.claude/*.json .claude/*.json .mcp.json; do
  if [ -f "$f" ]; then
    echo "Validating $f"
    jq . "$f" > /dev/null && echo "  OK" || echo "  INVALID"
  fi
done
```

### Configuration Precedence

Settings are merged in this order (later overrides earlier):

1. Default settings (built-in)
2. User settings (`~/.claude/settings.json`)
3. Project settings (`.claude/settings.json`)
4. Local settings (`.claude/settings.local.json`)
5. Environment variables
6. Command-line flags

### Debug Configuration Loading

```bash
# See which configs are loaded
claude --debug 2>&1 | grep -i "config\|settings\|loading"
```

## Session Diagnostics

### View Session Status

```bash
# In session
/status

# Shows:
# Session Status
# ==============
# ID: abc123
# Duration: 15m 30s
# Messages: 42
# Tokens: 15,000 / 200,000
# Tools Used: Read (10), Write (5), Bash (3)
```

### Session Files

```bash
# List recent sessions
ls -la ~/.claude/sessions/

# View session transcript
cat ~/.claude/sessions/latest/transcript.json | jq '.messages | length'

# Find large sessions
du -sh ~/.claude/sessions/* | sort -h | tail -10
```

### Context Usage

```bash
# Check context in session
/context

# Shows:
# Context Usage
# =============
# Used: 45,000 tokens (22%)
# Available: 155,000 tokens
#
# Breakdown:
#   System prompt: 5,000
#   Conversation: 25,000
#   Tool outputs: 15,000
```

## Creating Diagnostic Reports

### Comprehensive Report

```bash
#!/bin/bash
# diagnostic-report.sh

echo "=== Claude Code Diagnostic Report ==="
echo "Generated: $(date)"
echo ""

echo "=== Version ==="
claude --version
echo ""

echo "=== System Info ==="
uname -a
echo ""

echo "=== Health Check ==="
claude doctor
echo ""

echo "=== Hooks ==="
claude --print-hooks
echo ""

echo "=== MCP Servers ==="
claude mcp list
echo ""

echo "=== Configuration Files ==="
for f in ~/.claude/settings.json .claude/settings.json .mcp.json; do
  if [ -f "$f" ]; then
    echo "--- $f ---"
    jq . "$f" 2>/dev/null || echo "Invalid JSON"
  fi
done
echo ""

echo "=== Recent Logs ==="
if [ -d ~/Library/Logs/Claude\ Code/ ]; then
  tail -100 ~/Library/Logs/Claude\ Code/latest.log 2>/dev/null
fi
```

### Usage

```bash
chmod +x diagnostic-report.sh
./diagnostic-report.sh > ~/claude-diagnostic-report.txt
```

### Sharing Reports

When sharing diagnostic reports:

1. Remove sensitive information:
   ```bash
   sed -i '' 's/sk-[a-zA-Z0-9]*/**API_KEY**/g' report.txt
   sed -i '' 's/Bearer [a-zA-Z0-9]*/**TOKEN**/g' report.txt
   ```

2. Include:
   - Claude Code version
   - OS and version
   - Error messages
   - Steps to reproduce

3. Submit via:
   - `/bug` command in Claude Code
   - GitHub issues (if applicable)
   - Support channels
