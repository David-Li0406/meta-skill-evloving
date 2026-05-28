---
source: CodexDocs
last_updated: 2025-01-09
plugin_version: 1.0.0
---

# Codex Configuration Formats Reference

Complete specification for all OpenAI Codex configuration formats.

---

## 1. MCP Server Configuration

Location: `~/.codex/config.toml`

**Note:** Codex only supports user-scope MCP configuration. There is no project-scope `.mcp.json` equivalent.

### STDIO Server Schema

```toml
[mcp_servers.<server-name>]
command = "string"              # REQUIRED: Command to start server
args = ["arg1", "arg2"]         # Optional: Arguments to pass
cwd = "/path/to/dir"            # Optional: Working directory

[mcp_servers.<server-name>.env]
VAR_NAME = "value"              # Optional: Environment variables to set

# Alternative env syntax
env_vars = ["VAR1", "VAR2"]     # Optional: Env vars to allow and forward
```

### HTTP Server Schema

```toml
[mcp_servers.<server-name>]
url = "https://example.com/mcp"             # REQUIRED: Server address
bearer_token_env_var = "TOKEN_ENV_NAME"     # Optional: Env var for bearer token
http_headers = { "Header-Name" = "value" }  # Optional: Static headers
env_http_headers = { "Header" = "ENV_VAR" } # Optional: Headers from env vars
```

### Common Options (Apply to Both Types)

```toml
[mcp_servers.<server-name>]
startup_timeout_sec = 10        # Optional: Startup timeout (default: 10)
tool_timeout_sec = 60           # Optional: Tool execution timeout (default: 60)
enabled = true                  # Optional: Set false to disable without deleting
enabled_tools = ["tool1"]       # Optional: Tool allow list
disabled_tools = ["tool2"]      # Optional: Tool deny list (applied after enabled_tools)
```

### Complete STDIO Example

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
startup_timeout_sec = 15
tool_timeout_sec = 120
enabled = true

[mcp_servers.context7.env]
MY_ENV_VAR = "MY_ENV_VALUE"
```

### Complete HTTP Example

```toml
[mcp_servers.figma]
url = "https://mcp.figma.com/mcp"
bearer_token_env_var = "FIGMA_OAUTH_TOKEN"
http_headers = { "X-Figma-Region" = "us-east-1" }
startup_timeout_sec = 20
tool_timeout_sec = 45
enabled = true
enabled_tools = ["get_design", "export_assets"]
disabled_tools = ["delete_file"]
```

### CLI Commands

```bash
# Add STDIO server
codex mcp add <server-name> --env VAR1=VALUE1 -- <command>

# Example
codex mcp add context7 -- npx -y @upstash/context7-mcp

# View servers in TUI
/mcp

# OAuth login for HTTP servers
codex mcp login <server-name>
```

---

## 2. Skills Configuration

### SKILL.md YAML Frontmatter Schema

```yaml
---
name: skill-name                              # REQUIRED: Non-empty, max 100 chars, single line
description: What it does and when to use it  # REQUIRED: Non-empty, max 500 chars, single line
metadata:
  short-description: User-facing description  # Optional: Brief description for UI
---
```

**Key Differences from Claude:**
- Max `name` length: 100 chars (Claude: 64)
- Max `description` length: 500 chars (Claude: 1024)
- No `allowed-tools`, `model`, `context`, `agent` fields
- No skill-scoped hooks
- Uses `$skill-name` invocation syntax instead of `/skill-name`

### Skill Directory Layout

```
my-skill/
  SKILL.md          # REQUIRED: Instructions + metadata
  scripts/          # Optional: Executable code (Python, etc.)
  references/       # Optional: Documentation, lookup tables
  assets/           # Optional: Templates, schemas, resources
```

### Scope Precedence (High to Low)

| Scope    | Location                              | Use Case                                    |
|----------|---------------------------------------|---------------------------------------------|
| `REPO`   | `$CWD/.codex/skills`                  | Current working directory skills            |
| `REPO`   | `$CWD/../.codex/skills`               | Parent folder skills (in Git repo)          |
| `REPO`   | `$REPO_ROOT/.codex/skills`            | Repository root skills                      |
| `USER`   | `~/.codex/skills`                     | User-specific skills across all repos       |
| `ADMIN`  | `/etc/codex/skills`                   | System-wide admin skills                    |
| `SYSTEM` | Bundled with Codex                    | Built-in skills (can be overwritten)        |

Skills with the same name in higher-precedence scopes override lower ones.

### Complete SKILL.md Example

```md
---
name: draft-commit-message
description: Draft a conventional commit message when the user asks for help writing a commit message.
metadata:
  short-description: Draft an informative commit message.
---

Draft a conventional commit message that matches the change summary provided by the user.

Requirements:

- Use the Conventional Commits format: `type(scope): summary`
- Use the imperative mood in the summary (for example, "Add", "Fix", "Refactor")
- Keep the summary under 72 characters
- If there are breaking changes, include a `BREAKING CHANGE:` footer
```

### Skill Invocation

```text
# Explicit invocation
$skill-name

# With context
$skill-creator Create a skill that drafts commit messages

# Install from GitHub catalog
$skill-installer linear
```

### Validation Rules

- File must be named exactly `SKILL.md`
- `name`: Non-empty, max 100 characters, single line
- `description`: Non-empty, max 500 characters, single line
- Symlinked directories are ignored
- Malformed YAML causes skill to be skipped

---

## 3. Rules Configuration (Starlark)

Location: `~/.codex/rules/*.rules`

**Note:** Codex uses Starlark rules instead of Claude's JSON permissions. Rules use `prefix_rule()` function calls in `.rules` files.

### prefix_rule() Schema

```python
prefix_rule(
    # REQUIRED: Non-empty list defining command prefix to match
    pattern = ["cmd", "subcommand", "arg"],

    # Optional (default: "allow"): Action when rule matches
    # Values: "allow", "prompt", "forbidden"
    # Strictest wins when multiple rules match: forbidden > prompt > allow
    decision = "prompt",

    # Optional: Human-readable reason for the rule
    justification = "Reason for this rule",

    # Optional (default: []): Example commands that SHOULD match
    match = [
        "cmd subcommand arg value",
    ],

    # Optional (default: []): Example commands that should NOT match
    not_match = [
        "cmd other arg",
    ],
)
```

### Pattern Syntax

```python
# Literal string matching
pattern = ["gh", "pr", "view"]  # Matches: gh pr view ...

# Union of literals at a position
pattern = ["gh", "pr", ["view", "list"]]  # Matches: gh pr view ... OR gh pr list ...

# Pattern must be exact prefix match
pattern = ["npm", "install"]  # Matches: npm install lodash
                              # Does NOT match: npm ci
```

### Decision Values

| Value       | Behavior                                    |
|-------------|---------------------------------------------|
| `allow`     | Run outside sandbox without prompting       |
| `prompt`    | Ask user before each matching invocation    |
| `forbidden` | Block request without prompting             |

### Claude Permissions → Codex Rules Mapping

| Claude Permission | Codex Rule Decision |
|-------------------|---------------------|
| `allow` | `"allow"` |
| `ask` | `"prompt"` |
| `deny` | `"forbidden"` |

### Complete Rules Example

```python
# ~/.codex/rules/default.rules

# Allow read-only git commands
prefix_rule(
    pattern = ["git", ["status", "log", "diff", "branch"]],
    decision = "allow",
    justification = "Read-only git commands are safe",
    match = [
        "git status",
        "git log --oneline",
        "git diff HEAD~1",
        "git branch -a",
    ],
)

# Prompt for GitHub PR operations
prefix_rule(
    pattern = ["gh", "pr", ["view", "list", "status"]],
    decision = "prompt",
    justification = "PR viewing requires approval",
    match = [
        "gh pr view 7888",
        "gh pr list --state open",
    ],
    not_match = [
        "gh pr create",  # Different subcommand
    ],
)

# Forbid destructive operations
prefix_rule(
    pattern = ["rm", "-rf"],
    decision = "forbidden",
    justification = "Use safer deletion methods. Consider 'trash' command instead.",
    match = [
        "rm -rf /tmp/test",
    ],
)

# Block grep in favor of rg
prefix_rule(
    pattern = ["grep"],
    decision = "forbidden",
    justification = "Use 'rg' (ripgrep) instead of grep for better performance.",
)
```

### Testing Rules

```bash
# Test how rules apply to a command
codex execpolicy check --pretty \
  --rules ~/.codex/rules/default.rules \
  -- gh pr view 7888 --json title,body

# Combine multiple rule files
codex execpolicy check --pretty \
  --rules ~/.codex/rules/default.rules \
  --rules ~/.codex/rules/custom.rules \
  -- npm install lodash
```

---

## 4. AGENTS.md Configuration

Location: `~/.codex/AGENTS.md` (global) or `AGENTS.md` at repo root (project)

**Note:** This is the Codex equivalent of Claude's CLAUDE.md file.

### File Locations and Precedence

| Scope   | Location                     | Priority |
|---------|------------------------------|----------|
| Global  | `~/.codex/AGENTS.override.md`| Highest  |
| Global  | `~/.codex/AGENTS.md`         | High     |
| Project | `$REPO_ROOT/AGENTS.md`       | Medium   |
| Project | `$CWD/AGENTS.override.md`    | Per-dir  |
| Project | `$CWD/AGENTS.md`             | Per-dir  |

### Discovery Rules

1. **Global scope**: Check `~/.codex/AGENTS.override.md`, then `~/.codex/AGENTS.md`. Use first non-empty file.
2. **Project scope**: Walk from repo root to CWD, checking each directory for:
   - `AGENTS.override.md`
   - `AGENTS.md`
   - Fallback filenames (configured in `project_doc_fallback_filenames`)
3. **Merge**: Concatenate files from root down (later files override earlier).
4. **Limits**: Stop at `project_doc_max_bytes` (default: 32 KiB).

### Override Mechanism

- `AGENTS.override.md` takes precedence over `AGENTS.md` in same directory
- When override exists, `AGENTS.md` is ignored in that directory
- Use override for temporary changes without deleting base file

### Complete Global Example

```md
# ~/.codex/AGENTS.md

## Working agreements

- Always run `npm test` after modifying JavaScript files.
- Prefer `pnpm` when installing dependencies.
- Ask for confirmation before adding new production dependencies.
- Use conventional commit format for all commits.
```

### Complete Project Example

```md
# AGENTS.md (repository root)

## Repository expectations

- Run `npm run lint` before opening a pull request.
- Document public utilities in `docs/` when you change behavior.
- Follow the style guide in `CONTRIBUTING.md`.
```

### Nested Override Example

```md
# services/payments/AGENTS.override.md

## Payments service rules

- Use `make test-payments` instead of `npm test`.
- Never rotate API keys without notifying the security channel.
- All database migrations require review from @db-team.
```

---

## 5. config.toml Structure

Location: `~/.codex/config.toml`

### Complete Schema

```toml
# Project documentation discovery settings
project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md"]  # Alternative instruction filenames
project_doc_max_bytes = 32768                                       # Max combined size (default: 32 KiB)

# MCP Servers (see Section 1 for full schema)
[mcp_servers.server-name]
# ... server configuration
```

### Fallback Filenames Configuration

```toml
# ~/.codex/config.toml

# Custom instruction filenames to check (in addition to AGENTS.md)
project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md", "CODEX.md"]

# Increase limit for large instruction sets
project_doc_max_bytes = 65536  # 64 KiB
```

### Directory Checking Order Per Directory

1. `AGENTS.override.md`
2. `AGENTS.md`
3. Each filename in `project_doc_fallback_filenames` (in order)

### Environment Variables

| Variable      | Purpose                                    |
|---------------|-------------------------------------------|
| `CODEX_HOME`  | Override default config directory (~/.codex)|

### Complete config.toml Example

```toml
# ~/.codex/config.toml

# Project documentation settings
project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md"]
project_doc_max_bytes = 65536

# MCP Servers
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
startup_timeout_sec = 15

[mcp_servers.github]
command = "npx"
args = ["-y", "@github/mcp-server"]
enabled_tools = ["search_code", "get_file_contents", "list_commits"]

[mcp_servers.github.env]
GITHUB_PERSONAL_ACCESS_TOKEN = "ghp_..."

[mcp_servers.figma]
url = "https://mcp.figma.com/mcp"
bearer_token_env_var = "FIGMA_OAUTH_TOKEN"
tool_timeout_sec = 120
enabled = true
```

---

## 6. Feature Comparison: Claude vs Codex

### Features NOT Available in Codex

| Feature | Claude | Codex | Notes |
|---------|--------|-------|-------|
| Hooks | Yes | No | Use rules for command control |
| Plugin system | Yes | No | Use skills for reusable capabilities |
| LSP servers | Yes | No | No LSP integration |
| Project-scope MCP | Yes | No | Only user-scope in config.toml |
| Skill `allowed-tools` | Yes | No | All tools available to skills |
| Skill `context: fork` | Yes | No | No isolated sub-agent context |
| Skill `model` override | Yes | No | No per-skill model selection |

### Translation Notes

When creating configurations for both systems:

1. **MCP Servers**: Claude JSON → Codex TOML translation is straightforward
2. **Skills**: Remove Claude-specific fields (`allowed-tools`, `context`, `model`, `hooks`)
3. **Permissions → Rules**: Convert Claude permission arrays to Codex Starlark `prefix_rule()` calls
4. **Instructions**: CLAUDE.md → AGENTS.md (same markdown format)
5. **Hooks**: No Codex equivalent; document in AGENTS.md as manual guidelines

---

## Quick Reference

### File Locations Summary

| Config Type     | Location                          |
|-----------------|-----------------------------------|
| Main config     | `~/.codex/config.toml`            |
| Rules           | `~/.codex/rules/*.rules`          |
| User skills     | `~/.codex/skills/<name>/SKILL.md` |
| Project skills  | `.codex/skills/<name>/SKILL.md`   |
| Global agents   | `~/.codex/AGENTS.md`              |
| Project agents  | `AGENTS.md` (repo root or subdir) |

### Required vs Optional Fields

| Config Type | Required Fields                | Key Optional Fields              |
|-------------|--------------------------------|----------------------------------|
| MCP STDIO   | `command`                      | `args`, `env`, `env_vars`, `cwd` |
| MCP HTTP    | `url`                          | `bearer_token_env_var`, headers  |
| MCP Common  | -                              | `enabled`, timeouts, tool lists  |
| Skills      | `name`, `description`          | `metadata.short-description`     |
| Rules       | `pattern`                      | `decision`, `justification`      |
| AGENTS.md   | -                              | Any markdown content             |

### Codex CLI Quick Reference

```bash
# MCP management
codex mcp add <name> -- <command>    # Add STDIO server
codex mcp login <name>               # OAuth for HTTP server
/mcp                                 # View in TUI

# Rules testing
codex execpolicy check --rules <file> -- <command>

# Skill invocation
$skill-name                          # Invoke skill
$skill-installer <name>              # Install from catalog
```
