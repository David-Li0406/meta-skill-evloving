# Google Gemini CLI Reference

Complete command reference for Gemini CLI - Google's open-source AI coding agent.

## Installation

```bash
# npm (recommended)
npm i -g @google/gemini-cli

# Verify
gemini --version
```

## Authentication

### Option 1: Google Account (Free Tier)
```bash
# First run prompts OAuth
gemini
# Follow browser prompts to sign in
```

**Free tier limits**: 60 requests/min, 1,000 requests/day

### Option 2: API Key
```bash
# Get key from: https://aistudio.google.com/apikey
export GEMINI_API_KEY="your-api-key"

# Or in shell profile (~/.bashrc, ~/.zshrc)
echo 'export GEMINI_API_KEY="your-key"' >> ~/.bashrc
```

### Option 3: Vertex AI
```bash
export GOOGLE_API_KEY="your-gcp-key"
export GOOGLE_GENAI_USE_VERTEXAI=true
gemini
```

## Command-Line Flags

### Core Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--prompt <text>` | `-p` | Non-interactive mode with prompt |
| `--prompt-interactive <text>` | `-i` | Interactive mode with initial prompt |
| `--model <model>` | `-m` | Model selection |
| `--yolo` | `-y` | Auto-approve all tool calls |
| `--sandbox` | `-s` | Run tools in Docker container |
| `--debug` | `-d` | Verbose debug output |
| `--help` | `-h` | Show help |

### Output Flags

| Flag | Description |
|------|-------------|
| `--output-format text` | Plain text (default) |
| `--output-format json` | JSON for scripting |
| `--output-format stream-json` | Streaming JSON |

### Session Flags

| Flag | Description |
|------|-------------|
| `--resume latest` | Resume most recent session |
| `--resume <index>` | Resume by session number |
| `--resume <uuid>` | Resume by session UUID |
| `--checkpointing` | Enable restore points |

### Advanced Flags

| Flag | Description |
|------|-------------|
| `--allowed-tools "tool1,tool2"` | Bypass confirmation for specific tools |
| `--extensions <name>` / `-e` | Load specific extensions |
| `-e none` | Disable all extensions |
| `--list-extensions` | List available extensions |
| `--sandbox-image <uri>` | Custom sandbox Docker image |
| `--include-dir` | Recursively include current directory |

## Usage Patterns

### Interactive Mode

```bash
# Launch interactive TUI
gemini

# With initial prompt
gemini -i "Explain this codebase"

# With YOLO (auto-approve)
gemini --yolo
```

### Non-Interactive Mode

```bash
# Basic prompt
gemini -p "Summarize README.md"

# Full auto with all permissions
gemini --yolo \
  --model gemini-3-pro-preview \
  -p "YOUR_TASK"

# With sandbox
gemini --yolo --sandbox \
  -p "Run tests and fix failures"

# JSON output for scripting
gemini -p "List all TODO comments" --output-format json

# Pipe input
echo "Fix linting errors" | gemini -p -
cat code.py | gemini -p "Review this code"
```

### File References

```bash
# Reference specific file
gemini -p "Explain @./src/main.py"

# Reference directory
gemini -p "Summarize all files in @./docs/"

# Reference image
gemini -p "What's in this image? @./screenshot.png"

# Reference PDF
gemini -p "Summarize @./report.pdf"
```

### Piping Content

```bash
# Pipe file content
cat requirements.txt | gemini -p "Check for security issues"

# Pipe command output
git diff | gemini -p "Review these changes"

# Pipe multiple files
cat src/*.py | gemini -p "Find potential bugs"
```

## Slash Commands (Interactive)

| Command | Description |
|---------|-------------|
| `/help` | Show available commands |
| `/chat` | Start new conversation |
| `/clear` | Clear screen |
| `/settings` | View/modify settings |
| `/model` | Change model |
| `/memory show` | Show current context |
| `/memory refresh` | Reload GEMINI.md |
| `/restore` | Restore from checkpoint |
| `/mcp` | List MCP tools |
| `/tools` | List available tools |
| `/stats` | Show token usage |
| `/bug` | Report a bug |
| `/quit` | Exit |

## Shell Mode

```bash
# In interactive mode, prefix with ! for shell
> !git status
> !npm test

# Toggle persistent shell mode
> !
# Now in shell mode, type ! again to exit
```

## Built-in Tools

| Tool | Description |
|------|-------------|
| `read_file` | Read file contents |
| `write_file` | Create/modify files |
| `list_directory` | List directory contents |
| `search_file_content` | Search in files |
| `run_shell_command` | Execute shell commands |
| `web_fetch` | Fetch URL contents |
| `google_web_search` | Search the web |
| `save_memory` | Save to conversation memory |
| `write_todos` | Create TODO items |
| `codebase_investigator` | Analyze codebase |

## Configuration

### Settings Files (Precedence: System > Project > User)

```bash
# User settings
~/.gemini/settings.json

# Project settings
.gemini/settings.json

# System settings (all users)
/etc/gemini-cli/settings.json
```

### settings.json Example

```json
{
  "model": "gemini-3-pro-preview",
  "theme": "dark",
  "yolo": false,
  "sandbox": false,
  "checkpointing": true,
  "telemetry": false,
  
  "safeTools": [
    "ShellTool(git status)",
    "ShellTool(npm test)",
    "ReadFile(*)"
  ],
  
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_..."
      }
    },
    "postgres": {
      "command": "npx", 
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://..."
      }
    }
  }
}
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | API key for authentication |
| `GEMINI_SANDBOX` | Enable sandbox mode |
| `BUILD_SANDBOX` | Build custom sandbox image |
| `NO_COLOR` | Disable color output |
| `DEBUG` | Enable debug logging |

## GEMINI.md (Project Context)

Create `GEMINI.md` in project root for persistent instructions:

```markdown
# Project: Medical Data Pipeline

## Overview
Python ETL pipeline for clinical research data.

## Code Standards
- Python 3.11+
- Type hints required
- Black formatting
- pytest for testing

## Security Requirements
- HIPAA compliant
- No PII in logs
- Encrypted at rest

## Commands
- Install: `poetry install`
- Test: `pytest tests/ -v`
- Lint: `black --check src/`

## Important Files
- src/pipeline.py - Main ETL logic
- src/validators.py - Data validation
- config/settings.yaml - Configuration
```

## MCP Integration

### Configure MCP Servers

```json
// ~/.gemini/settings.json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"]
    },
    "database": {
      "url": "https://mcp.example.com/db",
      "bearerToken": "${DB_MCP_TOKEN}"
    }
  }
}
```

### Use MCP Tools

```bash
# In interactive mode
> @github List my open PRs
> @slack Send message to #dev-channel
> @database Query users table
```

## Sandbox Mode

### Enable Sandbox

```bash
# Via flag
gemini --sandbox -p "Run tests"

# Via environment
export GEMINI_SANDBOX=true
gemini -p "Run tests"

# With YOLO (auto-approve in sandbox)
gemini --yolo --sandbox -p "Run all tests and fix failures"
```

### Custom Sandbox Image

```dockerfile
# .gemini/sandbox.Dockerfile
FROM gemini-cli-sandbox

# Add project dependencies
RUN apt-get update && apt-get install -y python3-pip
RUN pip install pytest black mypy

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
```

```bash
# Build and use custom sandbox
BUILD_SANDBOX=true gemini --sandbox -p "Run tests"
```

### macOS Seatbelt (Alternative)

```bash
# Uses sandbox-exec instead of Docker
# Lighter weight, restricts writes outside project

# Create custom profile
# .gemini/sandbox-macos-custom.sb
gemini --sandbox -p "..."
```

## Session Management

```bash
# Resume latest
gemini --resume latest

# Resume by index (from session list)
gemini --resume 5

# Resume by UUID
gemini --resume a1b2c3d4-e5f6-7890-abcd-ef1234567890

# With checkpointing (for rollback)
gemini --checkpointing

# Restore from checkpoint (in interactive)
> /restore
```

## Custom Commands

Create reusable commands in `~/.gemini/commands/` or `.gemini/commands/`:

```toml
# ~/.gemini/commands/review.toml
# Usage: /review "path/to/file.py"

description = "Critical code review for clinical research"
prompt = """
Critically review this code for clinical research application.

REQUIRED CHECKS:
1. Correctness: Does it do what it claims?
2. Edge cases: All inputs handled?
3. Error handling: Failures graceful?
4. Security: Any vulnerabilities?
5. Performance: Any bottlenecks?
6. Documentation: Intent clear?
7. Tests: What tests needed?

BE HARSH. FIND PROBLEMS.

File: $1
"""
```

```toml
# ~/.gemini/commands/test.toml
# Usage: /test:gen "component description"

description = "Generate unit tests"
prompt = """
You are an expert test engineer.
Generate comprehensive unit tests for: $1
Use pytest. Include edge cases.
"""
```

## VS Code Integration

```bash
# Install VS Code extension
> /ide install

# Enable connection
> /ide enable

# Features:
# - Workspace context (recent files, cursor position)
# - Native diff viewer for code changes
# - Seamless editor integration
```

## Models

| Model | Description |
|-------|-------------|
| `gemini-3-pro-preview` | Latest, most capable |
| `gemini-2.5-pro` | Stable, 1M context |
| `gemini-2.5-flash` | Fast, cost-effective |

```bash
# Select model
gemini -m gemini-3-pro-preview -p "..."

# Change in settings
> /settings
# or edit ~/.gemini/settings.json
```

## Common Patterns

### Critical Review (Clinical Research)

```bash
gemini --yolo --model gemini-3-pro-preview \
  -p "Review this code critically for clinical research. \
      Check: correctness, edge cases, error handling, \
      security, performance. Be rigorous. \
      Code: $(cat src/analysis.py)"
```

### Automated Analysis

```bash
# Analyze codebase
gemini --yolo -p "Analyze this codebase. Find: \
  - Security vulnerabilities \
  - Performance issues \
  - Code smells \
  - Missing tests"
```

### CI/CD Integration

```yaml
# .github/workflows/gemini.yml
- name: Code Review
  run: |
    npm i -g @google/gemini-cli
    gemini -p "Review changes in this PR" --output-format json > review.json
  env:
    GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Tool confirmation spam | Use `--yolo` flag or configure `safeTools` |
| Sandbox not working | Install Docker/Podman |
| Sandbox fails (Fedora) | Known issue, use non-sandbox mode |
| Model not found | Check spelling, use `/model` to list |
| Auth fails | Re-run `gemini` for OAuth or check API key |
| Context too large | Use `/memory show`, add `.geminiignore` |
| Slow responses | Try `gemini-2.5-flash` model |

## .geminiignore

Exclude files from context (like .gitignore):

```gitignore
# .geminiignore
node_modules/
*.log
.env
dist/
build/
__pycache__/
*.pyc
.git/
```
