# Enterprise MCP Configuration

Centralized MCP management for organizations requiring standardized tool access and compliance controls.

## Overview

Enterprise configuration allows system administrators to:
- Deploy standardized MCP servers across the organization
- Prevent unauthorized MCP connections
- Enforce security policies
- Disable MCP functionality if needed

## Configuration Files

**managed-mcp.json:** Define approved MCP servers
**managed-settings.json:** Control which servers users can configure

### Deployment Locations

- **macOS**: `/Library/Application Support/ClaudeCode/managed-mcp.json`
- **Windows**: `C:\ProgramData\ClaudeCode\managed-mcp.json`
- **Linux**: `/etc/claude-code/managed-mcp.json`

## Managed MCP Server Definition

**managed-mcp.json** provides enterprise-approved MCP servers:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "sentry": {
      "type": "http",
      "url": "https://mcp.sentry.dev/mcp"
    },
    "company-internal": {
      "type": "stdio",
      "command": "/usr/local/bin/company-mcp-server",
      "args": ["--config", "/etc/company/mcp-config.json"],
      "env": {
        "COMPANY_API_URL": "https://internal.company.com"
      }
    }
  }
}
```

**Features:**
- All servers available automatically to users
- Supports HTTP, SSE, and stdio transports
- Cannot be overridden by user/project/local configurations
- Highest precedence in scope hierarchy

## Server Control Configuration

**managed-settings.json** restricts which servers users can add:

```json
{
  "allowedMcpServers": [
    {"serverName": "github"},
    {"serverName": "sentry"},
    {"serverName": "company-internal"}
  ],
  "deniedMcpServers": [
    {"serverName": "filesystem"},
    {"serverName": "untrusted-external-service"}
  ]
}
```

### Allowlist Behavior

When `allowedMcpServers` is set, users can **only** configure listed servers:

```json
{
  "allowedMcpServers": [
    {"serverName": "approved-server-1"},
    {"serverName": "approved-server-2"}
  ]
}
```

- Default (undefined): No restrictions
- Empty array `[]`: Users cannot add any servers
- Named servers: Users can only add these specific servers

### Denylist Behavior

When `deniedMcpServers` is set, users **cannot** configure listed servers:

```json
{
  "deniedMcpServers": [
    {"serverName": "risky-server"},
    {"serverName": "untrusted-external"}
  ]
}
```

- Default (undefined): No servers blocked
- Empty array `[]`: No servers blocked
- Named servers: These servers are blocked everywhere

### Precedence Rules

1. **Denylist takes absolute precedence** - If server appears in both lists, it is blocked
2. **Restrictions apply to all scopes** - User, project, local, and enterprise
3. **Enterprise servers unaffected** - `managed-mcp.json` servers always available regardless of allowlist/denylist

## Scope Hierarchy

Enterprise configuration has highest priority:

```
Enterprise (managed-mcp.json) > User > Project > Local
```

**Resolution:**
- Server defined in enterprise: Always available, cannot be disabled
- Same server defined at lower scope: Enterprise version takes precedence
- User/project/local can only add servers if allowed by allowlist and not in denylist

## Setup Workflow

### Step 1: Create managed-mcp.json

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "internal-api": {
      "type": "http",
      "url": "https://mcp-gateway.company.internal/api",
      "headers": {
        "Authorization": "Bearer ${INTERNAL_MCP_TOKEN}"
      }
    }
  }
}
```

Place at: `/Library/Application Support/ClaudeCode/managed-mcp.json` (macOS)

### Step 2: Create managed-settings.json (Optional)

```json
{
  "allowedMcpServers": [
    {"serverName": "github"},
    {"serverName": "internal-api"},
    {"serverName": "sentry"}
  ],
  "deniedMcpServers": [
    {"serverName": "filesystem"}
  ]
}
```

Place at: `/Library/Application Support/ClaudeCode/managed-settings.json`

### Step 3: Deploy to Machines

Use configuration management tools (Intune, Jamf, MDM):
- Copy managed-mcp.json to correct location
- Copy managed-settings.json to correct location
- Requires administrator privileges

### Step 4: Verify Configuration

Users verify with:
```bash
/mcp
```

Should show:
- Enterprise-provided servers (from managed-mcp.json)
- Applied restrictions (allowlist/denylist)

## Common Patterns

### Pattern 1: Internal-Only Servers

Enterprise policy: Only internal servers allowed

```json
{
  "allowedMcpServers": [
    {"serverName": "internal-api"},
    {"serverName": "internal-database"},
    {"serverName": "internal-tools"}
  ]
}
```

Result: Users cannot add external MCP servers.

### Pattern 2: Approved + Internal

Enterprise policy: Approved external + internal servers only

```json
{
  "allowedMcpServers": [
    {"serverName": "github"},
    {"serverName": "sentry"},
    {"serverName": "internal-api"}
  ]
}
```

Result: Users can add GitHub and Sentry, plus internal-api.

### Pattern 3: Blacklist Dangerous Servers

Enterprise policy: Block filesystem and risky servers

```json
{
  "deniedMcpServers": [
    {"serverName": "filesystem"},
    {"serverName": "shell-exec"},
    {"serverName": "unsafe-external"}
  ]
}
```

Result: Users cannot add filesystem or shell-exec servers.

### Pattern 4: Complete Lockdown

Enterprise policy: No user-configured servers allowed

```json
{
  "allowedMcpServers": []
}
```

Result: Only enterprise-provided servers available.

### Pattern 5: Disable MCP Entirely

Enterprise policy: MCP disabled for all users

Remove all servers from managed-mcp.json and restrict all additions:

```json
{
  "deniedMcpServers": [{"serverName": "*"}]
}
```

Alternative: Remove MCP files entirely or empty mcpServers object.

## Security Considerations

**Precedence Guarantee:** Denylist always takes precedence - if you need to block a server, it will be blocked regardless of allowlist

**Scope Isolation:** Enterprise config applies organization-wide, cannot be overridden locally

**Variable Expansion:** Supports `${ENV_VAR}` for tokens and paths (see environment-variable-expansion.md)

**Audit Trail:** Track which users add/remove servers via Claude Code logs

## Implementation Checklist

- [ ] Identify approved MCP servers for organization
- [ ] Decide on allowlist vs denylist strategy
- [ ] Create managed-mcp.json with approved servers
- [ ] Create managed-settings.json with restrictions
- [ ] Test configuration on single machine first
- [ ] Deploy via MDM/configuration management tool
- [ ] Verify users see correct servers (/mcp command)
- [ ] Document policy for users
- [ ] Plan for regular policy updates

## Troubleshooting

**Enterprise servers not appearing:**
- Verify file location matches OS
- Check file permissions (readable by all users)
- Restart Claude Code (config loaded on startup)
- Check mcpServers object is not empty

**User restrictions not enforced:**
- Verify managed-settings.json in correct location
- Check allowedMcpServers/deniedMcpServers syntax
- Restart Claude Code
- Verify denylist isn't conflicting with allowlist

**Configuration conflicts:**
- Check if denylist includes servers from allowlist (denylist wins)
- Verify enterprise servers aren't blocked
- Review scope hierarchy - enterprise takes precedence
