# config.toml Format Reference

## stdio Transport

**With version locking (npm package):**

```toml
transport = "stdio"
command = "npx"
args = ["@modelcontextprotocol/server-filesystem@0.6.2", "/tmp"]
version = "0.6.2"                    # Optional - only if version is locked
versionLockedAt = "2026-01-20"       # Optional - when version was locked
```

**Without version locking (local binary or unlockable):**

```toml
transport = "stdio"
command = "/usr/local/bin/my-mcp-server"
args = ["--port", "3000"]
# No version/versionLockedAt - cannot lock version
```

**With environment variables (for tokens):**

```toml
transport = "stdio"
command = "npx"
args = ["@github/mcp-server@1.0.0"]
version = "1.0.0"
versionLockedAt = "2026-01-20"

[env]
GITHUB_TOKEN = "${MCP_GITHUB_TOKEN}"
```

## HTTP Transport

**Basic:**

```toml
transport = "http"
url = "http://localhost:3000/mcp"
```

**With authentication:**

```toml
transport = "http"
url = "https://api.example.com/mcp"

[headers]
Authorization = "Bearer ${MCP_EXAMPLE_API_KEY}"
X-Custom-Header = "value"
```

## Environment Variables

`${VAR_NAME}` syntax references environment variables.

**Optional vs Required:**

- Variables in `[headers]` and `[env]` sections are **optional** - if not set, the entry is simply not included
- Variables elsewhere (e.g., in `url` or `args`) are **required** - will throw error if not set

**Optional authentication example:**

```toml
[headers]
# If MCP_EXAMPLE_API_KEY is not set, Authorization header won't be sent
Authorization = "Bearer ${MCP_EXAMPLE_API_KEY}"
```

## Naming Convention

Use unified prefix to avoid conflicts:

```
MCP_<SKILL_NAME>_<VAR_NAME>
```

Examples:
- `MCP_GITHUB_TOKEN` - for mcp-github skill
- `MCP_CONTEXT7_API_KEY` - for mcp-context7 skill

Benefits:
- `MCP_` prefix identifies MCP skill variables
- `<SKILL_NAME>` distinguishes different skills
- Avoids conflicts with user's existing environment variables
