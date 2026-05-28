# Claude Code CLI Reference

Complete command reference for Claude Code - Anthropic's agentic coding assistant for terminal.

## Installation

```bash
# Native Install (Recommended - macOS, Linux, WSL)
curl -fsSL https://claude.ai/install.sh | bash

# Homebrew (macOS)
brew install --cask claude-code

# Upgrade (Homebrew)
brew upgrade claude-code

# WinGet (Windows)
winget install Anthropic.ClaudeCode
```

## Authentication

Claude Code requires a Claude subscription (Pro, Max, Teams, or Enterprise) or Claude Console account.

```bash
# First run - follow OAuth prompts
claude

# Or use API key
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Command-Line Flags

### Core Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--print <prompt>` | `-p` | Non-interactive mode, run prompt and exit |
| `--model <model>` | `-m` | Model selection (e.g., sonnet, opus, haiku) |
| `--dangerously-skip-permissions` | | YOLO mode - skip all permission prompts |
| `--allowedTools <tools>` | | Whitelist specific tools |
| `--help` | `-h` | Show help |
| `--version` | `-v` | Show version |

### Output Flags

| Flag | Description |
|------|-------------|
| `--output-format text` | Plain text output (default) |
| `--output-format json` | JSON output for scripting |

### Session Flags

| Flag | Description |
|------|-------------|
| `--resume` | Resume previous session |
| `--continue` | Continue last conversation |

## Usage Patterns

### Interactive Mode

```bash
# Launch interactive TUI
claude

# With initial context
cd your-project
claude
```

### Non-Interactive Mode

```bash
# Basic prompt
claude -p "Summarize README.md"

# Full auto with all permissions (YOLO mode)
claude --dangerously-skip-permissions \
  
  -p "YOUR_TASK"

# Piping input
cat code.py | claude -p "Review this code"
git diff | claude -p "Explain these changes"

# JSON output for scripting
claude -p "List all TODO comments" --output-format json
```

### File References

```bash
# Claude automatically reads files in working directory
cd project/
claude -p "Explain the main function in src/main.py"

# Reference specific file (via context)
claude -p "Review @src/main.py critically"
```

## Slash Commands (Interactive)

| Command | Description |
|---------|-------------|
| `/help` | Show available commands |
| `/clear` | Clear conversation |
| `/model` | Change model |
| `/compact` | Summarize to save context |
| `/cost` | Show token usage and cost |
| `/memory` | View/manage memory |
| `/mcp` | List MCP tools |
| `/quit`, `/exit` | Exit |

## CLAUDE.md (Project Context)

Create `CLAUDE.md` in project root for persistent instructions. Claude automatically loads this as context.

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
```

## MCP Integration

Configure MCP servers in Claude settings:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
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

## Safety Levels

| Level | Approvals | Use Case |
|-------|-----------|----------|
| Default | Every sensitive action | Daily development |
| AllowedTools | Whitelisted only | Semi-trusted automation |
| **YOLO** | **None** | **Automation, CI, consensus workflows** |

**For consensus workflows, use YOLO mode (`--dangerously-skip-permissions`).**

> [!CAUTION]
> YOLO mode bypasses all safety prompts. Only use in sandboxed environments or when you trust the task completely.

## Common Patterns

### Critical Review (Clinical Research)

```bash
claude --dangerously-skip-permissions \
  
  -p "Review this code critically for clinical research. \
      Check: correctness, edge cases, error handling, \
      security, performance. Be rigorous. \
      Code: $(cat src/analysis.py)"
```

### Concise Output

```bash
claude --dangerously-skip-permissions \
  -p "BE CONCISE. No preamble. Review this plan. Output:
- ISSUES: [list]
- MISSING: [list]
- VERDICT: APPROVED/NEEDS CHANGES

Plan: $(cat plan.md)"
```

### Automated Analysis

```bash
claude --dangerously-skip-permissions \
  -p "Analyze this codebase. Find: \
    - Security vulnerabilities \
    - Performance issues \
    - Code smells \
    - Missing tests"
```

### CI/CD Integration

```yaml
# .github/workflows/claude.yml
- name: Code Review
  run: |
    curl -fsSL https://claude.ai/install.sh | bash
    claude -p "Review changes in this PR" --output-format json > review.json
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

## Models

| Model | Description |
|-------|-------------|
| `sonnet` | Latest, balanced performance/cost |
| `opus` | Most capable, highest cost |
| `haiku` | Fast, cost-effective |

```bash
# Select model
claude -m sonnet -p "..."

# Change in interactive mode
> /model opus
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Permission prompts interrupting | Use `--dangerously-skip-permissions` (sandboxed env only) |
| Context too large | Use `/compact` or add `.claudeignore` |
| Auth fails | Re-run `claude` for OAuth or check API key |
| Slow responses | Try `haiku` model |
| Model not found | Check spelling, use `/model` to list |

## .claudeignore

Exclude files from context (like .gitignore):

```gitignore
# .claudeignore
node_modules/
*.log
.env
dist/
build/
__pycache__/
*.pyc
.git/
```
