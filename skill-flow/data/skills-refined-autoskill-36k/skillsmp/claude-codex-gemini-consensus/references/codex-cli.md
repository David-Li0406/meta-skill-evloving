# OpenAI Codex CLI Reference

Complete command reference for Codex CLI - OpenAI's coding agent for terminal.

## Installation

```bash
# npm (recommended)
npm i -g @openai/codex

# Homebrew (macOS)
brew install --cask codex

# Upgrade
codex --upgrade
# or: npm update -g @openai/codex
```

## Authentication

```bash
# Interactive OAuth (opens browser)
codex login

# API key via stdin
printenv OPENAI_API_KEY | codex login --with-api-key

# Environment variable
export OPENAI_API_KEY="sk-..."

# Check status
codex login status

# Logout
codex logout
```

## Global Flags

| Flag | Type | Description |
|------|------|-------------|
| `PROMPT` | string | Initial instruction (omit to launch TUI) |
| `--image, -i` | path[,path...] | Attach images to prompt |
| `--model, -m` | string | Model override (e.g., `gpt-5.2-codex`, `gpt-5`, `o3`) |
| `--oss` | boolean | Use local Ollama models |
| `--profile, -p` | string | Config profile from config.toml |
| `--sandbox, -s` | enum | `read-only`, `workspace-write`, `danger-full-access` |
| `--ask-for-approval, -a` | enum | `untrusted`, `on-failure`, `on-request`, `never` |
| `--full-auto` | boolean | Sets `-a on-failure -s workspace-write` |
| `--yolo` | boolean | No approvals, no sandbox (DANGEROUS) |
| `--cd, -C` | path | Working directory |
| `--add-dir` | path | Additional writable directories |
| `--search` | boolean | Enable web search tool |
| `--skip-git-repo-check` | boolean | Allow running outside Git repositories |
| `-c key=value` | config | Override config values |

## Commands

### Interactive Mode

```bash
# Launch TUI
codex

# With initial prompt
codex "Explain this codebase"

# With image
codex -i screenshot.png "Implement this design"

# Full auto mode
codex --full-auto "Run tests and fix failures"

# With web search
codex --search "Find latest API docs and update code"
```

### Non-Interactive (exec)

```bash
# Basic execution
codex exec "Generate unit tests"
codex e "Generate unit tests"  # alias

# YOLO mode - full permissions, no approvals (recommended for automation)
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  "YOUR_TASK"

# Short form with --yolo alias
codex exec --yolo \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  "YOUR_TASK"

# With web search
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  --search \
  "Search for best practices and implement"

# Read prompt from stdin
echo "Fix all linting errors" | codex exec -

# JSON output for scripting
codex exec --json "Analyze this repo"

# Resume previous session
codex exec resume --last "Continue the implementation"
codex exec resume SESSION_ID "Add error handling"
```

### Session Management

```bash
# Interactive session picker
codex resume

# Resume most recent
codex resume --last

# Resume specific session
codex resume SESSION_UUID

# Show all sessions (including other directories)
codex resume --all

# Resume with new prompt
codex resume --last "Now add tests"
```

### Codex Cloud

```bash
# Interactive task picker
codex cloud

# Submit cloud task
codex cloud exec --env ENV_ID "Implement feature X"

# Apply cloud task diff locally
codex apply TASK_ID
codex a TASK_ID  # alias
```

### MCP (Model Context Protocol)

```bash
# List configured servers
codex mcp list
codex mcp list --json

# Get server config
codex mcp get servername
codex mcp get servername --json

# Add stdio server
codex mcp add myserver -- npx -y @my/mcp-server
codex mcp add dbserver --env DB_URL=... -- node db-mcp.js

# Add HTTP server
codex mcp add apiserver --url https://api.example.com/mcp
codex mcp add apiserver --url https://... --bearer-token-env-var API_TOKEN

# Remove server
codex mcp remove servername

# OAuth login (for HTTP servers)
codex mcp login servername --scopes read,write

# Logout
codex mcp logout servername
```

### Other Commands

```bash
# Run as MCP server (for other agents)
codex mcp-server

# Run command in sandbox
codex sandbox --full-auto -- npm test

# Generate shell completions
codex completion bash > ~/.bash_completion.d/codex
codex completion zsh > "${fpath[1]}/_codex"
codex completion fish > ~/.config/fish/completions/codex.fish

# Check execpolicy rules
codex execpolicy evaluate rules.toml "rm -rf /"
```

## Slash Commands (Interactive TUI)

| Command | Description |
|---------|-------------|
| `/model` | Switch model |
| `/mode` | Change approval mode |
| `/status` | Show current settings |
| `/compact` | Summarize conversation to save context |
| `/diff` | Show Git diff |
| `/review` | Code review mode |
| `/mention path` | Add file to context |
| `/new` | Start new conversation |
| `/resume` | Resume previous session |
| `/fork` | Branch from saved session |
| `/init` | Create AGENTS.md scaffold |
| `/mcp` | List MCP tools |
| `/feedback` | Submit feedback |
| `/logout` | Clear credentials |
| `/quit`, `/exit` | Exit CLI |

## Configuration (~/.codex/config.toml)

```toml
# Model selection
model = "gpt-5.2-codex"

# Approval policy: untrusted, on-failure, on-request, never
approval_policy = "on-request"

# Sandbox mode: read-only, workspace-write, danger-full-access
sandbox_mode = "workspace-write"

# Enable web search
web_search = true

# Network access in sandbox
[sandbox_workspace_write]
network_access = true

# Custom writable paths
writable_roots = ["/tmp", "~/projects"]

# MCP servers
[mcp_servers.github]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-github"]
env = { GITHUB_TOKEN = "..." }

# Feature flags
[features]
rmcp_client = true

# Named profiles
[profiles.safe]
sandbox_mode = "read-only"
approval_policy = "untrusted"

[profiles.yolo]
sandbox_mode = "danger-full-access"
approval_policy = "never"
```

## AGENTS.md (Repository Instructions)

Create `AGENTS.md` in repo root to provide persistent context:

```markdown
# Project Context

This is a Python medical imaging analysis project.

## Code Standards
- Use type hints everywhere
- Follow PEP 8
- All functions need docstrings

## Testing
- Run: pytest tests/ -v
- Coverage must be > 90%

## Security
- Never log patient data
- All PHI must be encrypted

## Build
- poetry install
- poetry run python main.py
```

## Safety Levels

| Level | Approvals | Sandbox | Use Case |
|-------|-----------|---------|----------|
| Safe | Every command | read-only | Exploration, audits |
| Balanced | On failure | workspace-write | Daily development |
| Full Auto | On failure | workspace-write | Trusted tasks |
| **YOLO** | **Never** | **None** | **Automation, CI, consensus workflows** |

**For consensus workflows, use YOLO mode (`--dangerously-bypass-approvals-and-sandbox` or `--yolo`).**

## Common Patterns

### General Code Review

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  "Review this code critically. Check: correctness, edge cases, \
   error handling, security, performance. Code: $(cat src/main.py)"
```

### Critical Review (Clinical Research)

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  "Review this code critically for clinical research. \
   Check: correctness, edge cases, error handling, \
   security, performance. Be rigorous. Code: $(cat src/analysis.py)"
```

### Automated Testing

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  "Run all tests, fix any failures, ensure 100% pass rate"
```

### With Web Search

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  --search \
  "Search PubMed for latest findings on [TOPIC] and summarize"
```

### CI/CD Integration

```yaml
# .github/workflows/codex.yml
- name: Run Codex
  run: |
    npm i -g @openai/codex
    codex exec --full-auto "Update CHANGELOG for this PR"
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

## Models

| Model | Best For |
|-------|----------|
| `gpt-5.2-codex` | Default, repo-scale reasoning |
| `gpt-5` | Fast reasoning (Windows default) |
| `o3` | Deep reasoning tasks |
| Local (Ollama) | Privacy-sensitive work |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Not a git repository" error | Add `--skip-git-repo-check` flag |
| Network blocked | `-c 'sandbox_workspace_write.network_access=true'` |
| Sandbox errors (WSL) | Update WSL2, use container, or `--yolo` in isolated env |
| Sandbox errors (macOS) | `xcode-select --install` |
| Auth loops | `codex logout && codex login` |
| Model not found | Check model string spelling |
| Approvals won't stop | Check profile, use `codex -a never` |
| Permission denied | Use `--sandbox danger-full-access` |
