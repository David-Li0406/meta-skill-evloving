# Common Issues and Solutions

Comprehensive guide to common Claude Code problems and their solutions.

## Tool Permission Denied

### Symptoms
- "Permission denied" error when using tools
- Tool blocked by policy
- "Not allowed" messages

### Solutions

#### 1. Check Current Permissions

```bash
# In Claude Code session
/permissions

# Look for denied tools
```

#### 2. Allow Specific Tool

```bash
# Allow a single tool
/permissions --allow "Write"

# Allow with pattern
/permissions --allow "Bash(npm:*)"

# Allow MCP tools
/permissions --allow "mcp__memory__*"
```

#### 3. Configure in Settings

```json
// ~/.claude/settings.json
{
  "permissions": {
    "allow": [
      "Read",
      "Write",
      "Edit",
      "Bash",
      "Glob",
      "Grep"
    ]
  }
}
```

#### 4. Project-Specific Permissions

```json
// .claude/settings.json
{
  "permissions": {
    "allow": [
      "Bash(bun:*)",
      "Bash(npm:*)",
      "Bash(git:*)"
    ]
  }
}
```

---

## MCP Server Not Connecting

### Symptoms
- Server shows "disconnected" in `/mcp`
- "Connection refused" errors
- MCP tools not appearing

### Solutions

#### 1. Check Server Status

```bash
# List servers
claude mcp list

# Get details
claude mcp get <server-name>

# Interactive status
/mcp
```

#### 2. Reconnect Server

```bash
# In /mcp menu, select server and choose reconnect
/mcp
# Then: r (reconnect)
```

#### 3. Increase Timeout

```bash
# For slow-starting servers
MCP_TIMEOUT=60000 claude
```

#### 4. Test Server Manually

```bash
# For stdio servers
echo '{"jsonrpc":"2.0","method":"initialize","params":{},"id":1}' | npx -y @anthropic/mcp-server-memory

# For HTTP servers
curl -I https://mcp.example.com/mcp
```

#### 5. Check Configuration

```bash
# Validate MCP config
cat .mcp.json | jq .

# Common issues:
# - Wrong command path
# - Missing environment variables
# - Invalid JSON
```

#### 6. Windows-Specific Fix

```bash
# Use cmd wrapper for npx
claude mcp add --transport stdio server -- cmd /c npx -y @package/name
```

---

## Hooks Not Firing

### Symptoms
- Hook configured but never executes
- No debug output for hooks
- Expected behavior not occurring

### Solutions

#### 1. Validate JSON Syntax

```bash
# Check for syntax errors
jq . ~/.claude/settings.json

# Common errors:
# - Trailing commas
# - Unescaped quotes
# - Missing brackets
```

#### 2. Check Hook Registration

```bash
# View registered hooks
/hooks

# Or via CLI
claude --print-hooks
```

#### 3. Verify Matcher Pattern

Matchers are case-sensitive and use regex:

| Pattern | Matches |
|---------|---------|
| `Write` | Only "Write" |
| `Write\|Edit` | "Write" or "Edit" |
| `Write.*` | "Write", "WriteFile", etc. |
| `mcp__.*` | All MCP tools |

```bash
# Debug matcher
claude --debug 2>&1 | grep "Matched.*hooks"
```

#### 4. Check Script Permissions

```bash
# Make executable
chmod +x /path/to/hook.sh

# Verify
ls -la /path/to/hook.sh
# Should show: -rwxr-xr-x
```

#### 5. Use Absolute Paths

```json
// BAD
{ "command": "./hooks/script.sh" }

// GOOD
{ "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/script.sh" }
```

#### 6. Test Script Independently

```bash
# Test with sample input
echo '{"tool_name":"Write","tool_input":{"file_path":"/test.txt"}}' | ./hook.sh
echo "Exit code: $?"
```

---

## Skills Not Loading

### Symptoms
- Skill not appearing in suggestions
- Skill invocation fails
- "Skill not found" errors

### Solutions

#### 1. Check Skill Location

Valid locations:
- `~/.claude/skills/<skill-name>/SKILL.md` (personal)
- `.claude/skills/<skill-name>/SKILL.md` (project)

#### 2. Validate Frontmatter

```yaml
---
name: my-skill
description: Description in third person. Use when...
---
```

Required fields:
- `name`: lowercase, hyphens, max 64 chars
- `description`: third person, max 1024 chars

#### 3. Check YAML Syntax

Common issues:
```yaml
# BAD: Missing quotes around special chars
description: Use when: you need help

# GOOD: Quote strings with colons
description: "Use when: you need help"

# BAD: Tabs instead of spaces
---
	name: skill

# GOOD: Use spaces
---
  name: skill
```

#### 4. Verify File Structure

```
skills/
└── my-skill/
    ├── SKILL.md     # Required
    ├── TEMPLATES.md # Optional
    └── EXAMPLES.md  # Optional
```

#### 5. Check File Size

- Main SKILL.md should be under 500 lines
- Split large content to reference files

#### 6. Restart Claude Code

Skills are loaded at startup. Restart to pick up changes.

---

## Context Overflow

### Symptoms
- "Context limit exceeded" errors
- Claude forgets recent conversation
- Responses become truncated

### Solutions

#### 1. Compact Context

```bash
# In session
/compact

# Summarizes conversation, keeps important parts
```

#### 2. Clear Context

```bash
# Full reset
/clear

# Clears all conversation history
```

#### 3. Use Targeted Tool Outputs

Instead of reading entire files:
```bash
# BAD: Read entire large file
Read entire-codebase.ts

# GOOD: Read specific lines
Read file.ts --offset 100 --limit 50
```

#### 4. Avoid Large Tool Outputs

```bash
# BAD: List all files
Glob "**/*"

# GOOD: Be specific
Glob "src/**/*.ts"
```

#### 5. Monitor Context Usage

```bash
# Check current usage
/context

# Or /status for overview
```

---

## Rate Limiting

### Symptoms
- "Rate limit exceeded" errors
- 429 HTTP status codes
- Requests being rejected

### Solutions

#### 1. Wait and Retry

Most rate limits reset after 60 seconds.

```bash
# Wait
sleep 60

# Retry
```

#### 2. Reduce Request Frequency

- Batch related operations
- Avoid rapid successive requests
- Use larger, fewer requests

#### 3. Check Rate Limit Headers

```bash
# Debug output shows rate limit info
claude --debug 2>&1 | grep -i "rate\|limit"
```

#### 4. Upgrade Plan

Contact Anthropic for higher rate limits if needed.

---

## API Errors

### Symptoms
- "API error" messages
- Authentication failures
- Network errors

### Solutions

#### 1. Check Credentials

```bash
# Verify API key is set
echo $ANTHROPIC_API_KEY

# Or check credentials file
cat ~/.claude/.credentials.json | jq 'keys'
```

#### 2. Refresh Authentication

```bash
# Re-authenticate
claude auth login

# Or reset credentials
rm ~/.claude/.credentials.json
claude
```

#### 3. Test API Connectivity

```bash
# Test endpoint
curl -I https://api.anthropic.com/v1/messages

# Test with auth
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "content-type: application/json" \
  -d '{"model":"claude-sonnet-4-20250514","max_tokens":10,"messages":[{"role":"user","content":"test"}]}'
```

#### 4. Check Proxy Settings

```bash
# If behind proxy
HTTP_PROXY=http://proxy:8080 HTTPS_PROXY=http://proxy:8080 claude
```

#### 5. Check Error Details

```bash
# Get detailed error
claude --debug 2>&1 | grep -i "error\|failed"
```

### Common API Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Check/refresh credentials |
| 403 Forbidden | Insufficient permissions | Check API key permissions |
| 429 Rate Limited | Too many requests | Wait 60s, retry |
| 500 Server Error | API issue | Wait, retry, or report |
| 503 Service Unavailable | API overloaded | Wait and retry |

---

## Session Issues

### Symptoms
- Session hangs or freezes
- Commands not responding
- Stuck in processing state

### Solutions

#### 1. Cancel Current Operation

```bash
# Press Ctrl+C to cancel
^C

# Or Escape key in some terminals
```

#### 2. Restart Session

```bash
# Exit current session
exit

# Or Ctrl+D

# Start new session
claude
```

#### 3. Force Quit

```bash
# Find Claude process
ps aux | grep claude

# Kill process
kill -9 <pid>
```

#### 4. Clear Session Data

```bash
# Remove session files
rm -rf ~/.claude/sessions/current/
```

#### 5. Check for Blocking Hooks

```bash
# A hook might be stuck
# Check for long-running hook processes
ps aux | grep hook
```

---

## Slow Responses

### Symptoms
- Long delays before responses
- Timeouts
- "Processing..." for extended periods

### Solutions

#### 1. Check Network

```bash
# Test latency
ping api.anthropic.com

# Test API response time
time curl -I https://api.anthropic.com/v1/messages
```

#### 2. Reduce Context Size

```bash
# Compact to reduce processing
/compact
```

#### 3. Check MCP Server Performance

```bash
# Slow MCP servers can delay responses
/mcp

# Look for servers with high latency
```

#### 4. Use Faster Model

```bash
# If using opus, try sonnet for faster responses
# In skill frontmatter:
# model: sonnet
```

#### 5. Check System Resources

```bash
# Check CPU/memory
top

# Check disk I/O
iostat
```

---

## Installation Issues

### Symptoms
- `claude` command not found
- Installation fails
- Version mismatch

### Solutions

#### 1. Verify Installation

```bash
# Check if installed
which claude

# Check version
claude --version
```

#### 2. Reinstall

```bash
# npm
npm uninstall -g @anthropic/claude-code
npm install -g @anthropic/claude-code

# bun
bun remove -g @anthropic/claude-code
bun add -g @anthropic/claude-code
```

#### 3. Check PATH

```bash
# Verify npm/bun global bin is in PATH
echo $PATH

# Add if missing
export PATH="$PATH:$(npm prefix -g)/bin"
```

#### 4. Clear npm Cache

```bash
npm cache clean --force
```

---

## Configuration Conflicts

### Symptoms
- Settings not taking effect
- Unexpected behavior
- Multiple configs interfering

### Solutions

#### 1. Check Configuration Precedence

Settings load in order (later overrides earlier):
1. Default
2. User (`~/.claude/settings.json`)
3. Project (`.claude/settings.json`)
4. Local (`.claude/settings.local.json`)
5. Environment variables
6. Command-line flags

#### 2. Debug Configuration Loading

```bash
claude --debug 2>&1 | grep -i "config\|settings\|loading"
```

#### 3. Identify Conflicting Settings

```bash
# Compare configs
diff ~/.claude/settings.json .claude/settings.json
```

#### 4. Reset to Defaults

```bash
# Backup and remove
mv ~/.claude/settings.json ~/.claude/settings.json.bak
```

---

## Error Reference Table

| Error Message | Likely Cause | Quick Fix |
|---------------|--------------|-----------|
| "Permission denied" | Tool not allowed | `/permissions --allow "Tool"` |
| "Connection refused" | MCP server down | Check server, `/mcp` |
| "Invalid JSON" | Config syntax error | `jq . file.json` |
| "Skill not found" | Invalid skill path | Check location/frontmatter |
| "Context limit" | Too much data | `/compact` or `/clear` |
| "Rate limit" | Too many requests | Wait 60 seconds |
| "API key invalid" | Auth issue | `claude auth login` |
| "Timeout" | Slow response | Increase timeout/retry |
| "Hook failed" | Script error | Test script in isolation |
| "Command not found" | Bad path | Use absolute path |
