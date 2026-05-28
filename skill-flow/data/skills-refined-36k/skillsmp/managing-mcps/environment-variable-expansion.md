# Environment Variable Expansion in .mcp.json

Using variables to parameterize MCP configurations for team sharing and machine-specific paths.

## Overview

`.mcp.json` supports environment variable expansion enabling:
- Team-shared configurations checked into git
- Machine-specific values (paths, API keys, tokens)
- Development vs production configurations
- Default values if variables not set

## Syntax

**Reference environment variable:**
```
${VAR_NAME}
```

**Reference with default value:**
```
${VAR_NAME:-default_value}
```

## Supported Locations

Variables can be expanded in:
- `command`: Server executable path
- `args`: Command-line arguments
- `env`: Environment variables passed to server
- `url`: HTTP/SSE server URL
- `headers`: Authentication headers

## Examples

### Example 1: API Key from Environment

Development team shares `.mcp.json`:

```json
{
  "mcpServers": {
    "stripe": {
      "type": "http",
      "url": "https://api.stripe.com/mcp",
      "headers": {
        "Authorization": "Bearer ${STRIPE_API_KEY}"
      }
    }
  }
}
```

**Setup per developer:**
```bash
export STRIPE_API_KEY="sk_test_your_key_here"
claude
```

Each developer supplies their own API key via environment variable.

### Example 2: Path with Default

Portable path configuration:

```json
{
  "mcpServers": {
    "local-server": {
      "type": "stdio",
      "command": "${MCP_SERVER_PATH:-/usr/local/bin/my-server}",
      "args": []
    }
  }
}
```

**Behavior:**
- If `MCP_SERVER_PATH` is set: Uses that value
- If `MCP_SERVER_PATH` not set: Uses `/usr/local/bin/my-server` (default)

Allows team to share `.mcp.json` with sensible default.

### Example 3: Database Connection String

Team API server with machine-specific database:

```json
{
  "mcpServers": {
    "database": {
      "type": "http",
      "url": "${DB_MCP_URL:-http://localhost:3000}",
      "headers": {
        "Authorization": "Bearer ${DB_TOKEN}"
      }
    }
  }
}
```

Development machine:
```bash
export DB_MCP_URL="http://localhost:3000"
export DB_TOKEN="dev-token"
claude
```

Production machine:
```bash
export DB_MCP_URL="https://db-mcp.company.internal"
export DB_TOKEN="prod-token"
claude
```

### Example 4: Complex Server Configuration

Multiple variables with defaults:

```json
{
  "mcpServers": {
    "company-api": {
      "type": "http",
      "url": "${COMPANY_API_URL:-https://api.company.internal}/mcp",
      "headers": {
        "Authorization": "Bearer ${COMPANY_API_TOKEN}",
        "X-Client-Version": "${API_VERSION:-1.0}",
        "X-Environment": "${ENVIRONMENT:-development}"
      }
    }
  }
}
```

Team can check into git with defaults, each machine overrides as needed.

### Example 5: Local Server with Arguments

Command-line arguments with paths:

```json
{
  "mcpServers": {
    "custom-server": {
      "type": "stdio",
      "command": "python",
      "args": [
        "${MCP_SCRIPTS_DIR:-~/mcp-scripts}/server.py",
        "--config",
        "${MCP_CONFIG_DIR:-~/.mcp}/config.json",
        "--port",
        "${MCP_PORT:-8080}"
      ],
      "env": {
        "DATA_DIR": "${MCP_DATA_DIR:-./data}",
        "LOG_LEVEL": "${LOG_LEVEL:-info}"
      }
    }
  }
}
```

## Variable Expansion Rules

**Expansion locations:**
- Values are expanded (not keys)
- Expansion happens when `.mcp.json` is loaded
- All locations support same syntax

**Error handling:**
- If required variable not set and no default: Claude Code fails to parse config
- If default provided: Uses default value
- Empty string `""` is valid default

**Escaping:**
- Cannot escape `${}` syntax
- If you need literal `${text}`, request documentation

## Team Workflow Example

### Step 1: Create Shared .mcp.json

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_TOKEN}"
      }
    },
    "internal-api": {
      "type": "http",
      "url": "${INTERNAL_API_URL:-http://localhost:3000}",
      "headers": {
        "Authorization": "Bearer ${INTERNAL_API_TOKEN}"
      }
    }
  }
}
```

### Step 2: Check into Git

Team repository includes `.mcp.json` with team defaults and variable placeholders.

### Step 3: Developer Setup

Each developer creates `.env` or shell profile:

```bash
# ~/.bashrc or ~/.zshrc
export GITHUB_TOKEN="ghp_your_personal_token"
export INTERNAL_API_URL="http://localhost:3000"
export INTERNAL_API_TOKEN="dev-token"
```

Or use `.env` file (load before running Claude Code):
```bash
source .env
claude
```

### Step 4: Run Claude Code

Claude Code loads `.mcp.json`, expands variables, connects to servers:

```bash
claude
```

## Production Deployment Example

### Development Machine

```bash
export INTERNAL_API_URL="http://localhost:3000"
export INTERNAL_API_TOKEN="dev-token"
export INTERNAL_API_KEY="dev-key"
claude
```

### Staging Machine

```bash
export INTERNAL_API_URL="https://staging-api.company.internal"
export INTERNAL_API_TOKEN="${STAGING_TOKEN}"  # From secrets manager
export INTERNAL_API_KEY="${STAGING_KEY}"      # From secrets manager
claude
```

### Production Machine

```bash
export INTERNAL_API_URL="https://api.company.internal"
export INTERNAL_API_TOKEN="${PRODUCTION_TOKEN}"    # From secure vault
export INTERNAL_API_KEY="${PRODUCTION_KEY}"        # From secure vault
claude
```

Same `.mcp.json` file, different environments via environment variables.

## Security Best Practices

**Never hardcode secrets:**
```json
// BAD - Don't do this
{
  "mcpServers": {
    "api": {
      "headers": {
        "Authorization": "Bearer sk_live_actual_key_12345"
      }
    }
  }
}
```

**Use environment variables:**
```json
// GOOD - Use variables
{
  "mcpServers": {
    "api": {
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

**Use defaults only for non-sensitive values:**
```json
{
  "mcpServers": {
    "api": {
      // Good default - no sensitive data
      "url": "${API_URL:-http://localhost:3000}",
      // Bad default - exposes structure (don't expose sensitive even in structure)
      "headers": {
        "Authorization": "Bearer ${API_KEY}"  // No default here
      }
    }
  }
}
```

**Store secrets in:**
- Environment variables (set before running Claude Code)
- Secrets manager (1Password, HashiCorp Vault, AWS Secrets Manager)
- `.env` file (never check into git, use `.env.example` with placeholders)
- System keychain

## Troubleshooting

**Config fails to parse:**
- Check variable names: `${VAR}` not `$VAR` or `${VAR`
- Verify variable is set: `echo $VAR_NAME`
- Try with default: `${VAR:-default}`
- Check .mcp.json JSON syntax

**Variable not expanding:**
- Verify variable is exported: `export VAR_NAME="value"`
- Check spelling matches exactly (case-sensitive)
- Restart Claude Code (env vars loaded on startup)
- Test: `echo $VAR_NAME` to confirm variable is set

**Default not used:**
- Syntax: `${VAR:-default}` (colon and hyphen required)
- Not `${VAR-default}` or `${VAR :- default}`
- Default must be valid for context (URL, path, token, etc.)

**Shared .mcp.json not working:**
- Check all required variables are documented
- Verify defaults provided for optional variables
- Create setup guide for team
- Include `.env.example` showing required variables
