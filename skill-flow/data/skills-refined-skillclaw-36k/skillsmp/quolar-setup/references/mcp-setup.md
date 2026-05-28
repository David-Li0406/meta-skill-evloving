# MCP Server Setup Reference

Detailed instructions for setting up MCP servers required by Quolar.

---

## Overview

Quolar requires these MCP servers:

| Server | Status | Purpose |
|--------|--------|---------|
| **linear** | Required | Ticket fetching, PR linking |
| **quoth** | Required | Pattern documentation (MANDATORY per project rules) |
| **exolar** | Optional | Test analytics, failure classification |

---

## Linear MCP Setup

### Prerequisites

- Node.js 18+ installed
- Linear account with API access
- LINEAR_API_KEY environment variable or config

### Step 1: Get API Key

1. Log into Linear at https://linear.app
2. Click your avatar → Settings
3. Navigate to "API" section
4. Click "Personal API keys"
5. Click "Create key"
6. Copy the generated key (starts with `lin_api_`)

### Step 2: Configure MCP Server

Add to your Claude settings file:

**Location (macOS):**
- Claude Code: `~/.claude/settings.json`
- Claude Desktop: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Location (Linux):**
- Claude Code: `~/.claude/settings.json`
- Claude Desktop: `~/.config/Claude/claude_desktop_config.json`

**Location (Windows):**
- Claude Code: `%USERPROFILE%\.claude\settings.json`
- Claude Desktop: `%APPDATA%\Claude\claude_desktop_config.json`

**Configuration:**
```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@linear/mcp-server"],
      "env": {
        "LINEAR_API_KEY": "lin_api_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

### Step 3: Verify Connection

Restart Claude Code and run:
```
/mcp
```

Should show `linear` in the list of connected servers.

### Step 4: Test Access

Try fetching a ticket:
```
Use Linear MCP to list recent issues
```

---

## Quoth MCP Setup

### Prerequisites

- Claude Code or Claude Desktop installed
- Internet access for OAuth authentication

### Step 1: Add MCP Server

Run in terminal:

```bash
claude mcp add --transport http quoth https://quoth.ai-innovation.site/api/mcp
```

### Step 2: Complete OAuth

1. A browser window will open
2. Log into Quoth (or create account)
3. Authorize Claude Code access
4. Return to terminal

### Step 3: Verify Connection

```
/mcp
```

Should show `quoth` in the list.

### Step 4: Test Access

```
Search Quoth for "playwright test patterns"
```

### OAuth Token Refresh

Tokens are automatically refreshed. If authentication fails:

```bash
# Remove and re-add
claude mcp remove quoth
claude mcp add --transport http quoth https://quoth.ai-innovation.site/api/mcp
```

---

## Exolar MCP Setup (Optional)

### Prerequisites

- Claude Code or Claude Desktop installed
- Exolar account (optional, can create during OAuth)

### Step 1: Add MCP Server

```bash
claude mcp add exolar-qa --transport http https://exolar.ai-innovation.site/api/mcp/mcp -s user
```

### Step 2: Complete OAuth

Follow browser prompts to authenticate.

### Step 3: Verify Connection

```
/mcp
```

Should show `exolar-qa` in the list.

### Step 4: Test Access

```
Use Exolar to list recent test executions
```

---

## Troubleshooting

### Server Not Starting

**Symptoms:**
- Server not in `/mcp` list
- "Connection refused" errors

**Solutions:**

1. Check Node.js version:
   ```bash
   node --version  # Should be 18+
   ```

2. Test npx manually:
   ```bash
   npx -y @linear/mcp-server
   ```

3. Check settings file syntax:
   ```bash
   cat ~/.claude/settings.json | jq .
   ```

### Authentication Failures

**Symptoms:**
- 401 Unauthorized errors
- Token expired messages

**Solutions:**

1. For Linear: Generate new API key
2. For Quoth/Exolar: Re-run OAuth flow
   ```bash
   claude mcp remove quoth
   claude mcp add --transport http quoth https://quoth.ai-innovation.site/api/mcp
   ```

### Slow Startup

**Symptoms:**
- Long delay when starting Claude Code
- Timeout errors on first request

**Solutions:**

1. Increase timeout in settings (if available)
2. Check network latency to MCP endpoints
3. Pre-cache npx packages:
   ```bash
   npx -y @linear/mcp-server --version
   ```

---

## Configuration Reference

### Full settings.json Example

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@linear/mcp-server"],
      "env": {
        "LINEAR_API_KEY": "lin_api_xxx"
      }
    }
  }
}
```

### Environment Variable Alternative

Instead of hardcoding in config, use environment variables:

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@linear/mcp-server"],
      "env": {
        "LINEAR_API_KEY": "${LINEAR_API_KEY}"
      }
    }
  }
}
```

Then set in shell profile:
```bash
export LINEAR_API_KEY="lin_api_xxx"
```

---

## MCP Tools Available

### Linear MCP Tools

| Tool | Purpose |
|------|---------|
| `get_issue` | Fetch single ticket by ID |
| `list_issues` | List tickets with filters |
| `create_issue` | Create new ticket |
| `update_issue` | Update ticket fields |

### Quoth MCP Tools

| Tool | Purpose |
|------|---------|
| `quoth_search_index` | Semantic search across docs |
| `quoth_read_doc` | Read specific document |
| `quoth_propose_update` | Propose doc changes |
| `quoth_list_templates` | List doc templates |

### Exolar MCP Tools

| Tool | Purpose |
|------|---------|
| `explore_exolar_index` | Discover data categories |
| `query_exolar_data` | Query test data |
| `perform_exolar_action` | Execute operations |
| `get_semantic_definition` | Get metric definitions |

---

## Security Notes

1. **API Keys**: Store Linear API key securely, not in version control
2. **OAuth Tokens**: Managed automatically, stored in Claude config
3. **Network**: All MCP connections use HTTPS
4. **Permissions**: Grant minimum required scopes
