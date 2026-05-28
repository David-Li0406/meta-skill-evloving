# Codex CLI Reference

## Overview

Codex CLI is OpenAI's command-line interface for AI-powered code analysis and generation.

## Installation

```bash
# Install via npm
npm install -g @openai/codex

# Or via Homebrew
brew install openai-codex
```

## Authentication

```bash
codex login
```

## Main Commands

### `codex exec` - Non-interactive execution

Run Codex without interactive prompts. Best for scripting and automation.

```bash
codex exec [OPTIONS] [PROMPT]
```

**Key Options:**
| Option | Description |
|--------|-------------|
| `-m, --model <MODEL>` | Model to use (e.g., gpt-5.2-codex, o4-mini) |
| `-s, --sandbox <MODE>` | Sandbox mode: read-only, workspace-write, danger-full-access |
| `-C, --cd <DIR>` | Working directory for the agent |
| `--search` | Enable web search |
| `-o, --output-last-message <FILE>` | Write final response to file |
| `-c, --config <key=value>` | Override configuration |

### `codex review` - Code review

Run automated code review on repository changes.

```bash
codex review [OPTIONS]
```

### `codex apply` - Apply diffs

Apply the latest diff produced by Codex agent.

```bash
codex apply
```

### `codex resume` - Continue session

Resume a previous interactive session.

```bash
codex resume --last
```

## Available Models

| Model | Description | Use Case |
|-------|-------------|----------|
| `gpt-5.2-codex` | Most advanced agentic coding model | Complex architecture, deep analysis |
| `o4-mini` | Fast and cost-efficient | Quick queries, simple tasks |
| `o3` | Balanced performance | General purpose |

## Sandbox Modes

| Mode | Description |
|------|-------------|
| `read-only` | No file modifications allowed (safest) |
| `workspace-write` | Can modify files in workspace |
| `danger-full-access` | Full system access (dangerous) |

## Configuration

Configuration file location: `~/.codex/config.toml`

```toml
# Default model
model = "gpt-5.2-codex"

# Default sandbox mode
sandbox = "read-only"

# Enable web search by default
search = true
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `CODEX_MODEL` | Override default model |
| `OPENAI_API_KEY` | API key for authentication |

## Examples

### Basic query
```bash
codex exec "Explain the architecture of this project"
```

### With specific model and output
```bash
codex exec -m gpt-5.2-codex -o result.md "Design a caching strategy"
```

### Scoped to directory
```bash
codex exec -C ./src "Review error handling patterns"
```

### With web search enabled
```bash
codex exec --search "What's the latest best practice for JWT authentication?"
```
