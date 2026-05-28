# CLI Flags Reference

Complete reference for Claude Code CLI flags in headless/automation mode.

## Core Flags

### Output Control

| Flag | Values | Description |
|------|--------|-------------|
| `-p`, `--print` | - | Run non-interactively, print response and exit |
| `--output-format` | `text`, `json`, `stream-json` | Response format |
| `--json-schema` | JSON Schema string | Force structured output matching schema |
| `--include-partial-messages` | - | Include streaming events (requires `stream-json`) |
| `--verbose` | - | Enable detailed logging |

### Tool Control

| Flag | Values | Description |
|------|--------|-------------|
| `--allowedTools` | Tool names | Tools that execute without permission prompts |
| `--disallowedTools` | Tool names | Tools removed from model's context |
| `--tools` | Tool names or `""` | Restrict which tools are available |
| `--dangerously-skip-permissions` | - | Skip all permission prompts (use with caution) |

### Session Management

| Flag | Values | Description |
|------|--------|-------------|
| `-c`, `--continue` | - | Continue most recent conversation in current directory |
| `-r`, `--resume` | Session ID or name | Resume specific session |
| `--session-id` | UUID | Use specific session ID for conversation |
| `--fork-session` | - | Create new session when resuming (use with --resume/--continue) |

### System Prompt

| Flag | Description |
|------|-------------|
| `--system-prompt` | Replace entire system prompt with custom text |
| `--system-prompt-file` | Load system prompt from file (print mode only) |
| `--append-system-prompt` | Append to default prompt (keeps Claude Code behavior) |

### Execution Limits

| Flag | Values | Description |
|------|--------|-------------|
| `--max-turns` | Number | Limit agentic turns in non-interactive mode |
| `--max-budget-usd` | Number | Set spending limit for session |

### Model Configuration

| Flag | Values | Description |
|------|--------|-------------|
| `--model` | Model name or alias | Set model (`sonnet`, `opus`, or full name) |
| `--fallback-model` | Model alias | Fallback when default is overloaded (print mode) |
| `--permission-mode` | Mode name | Begin in specified permission mode |

### Context & Configuration

| Flag | Description |
|------|-------------|
| `--add-dir` | Add additional working directories |
| `--mcp-config` | Load MCP servers from JSON files |
| `--strict-mcp-config` | Only use MCP servers from --mcp-config |
| `--settings` | Load settings from JSON file or string |
| `--setting-sources` | Comma-separated setting sources (`user`, `project`, `local`) |
| `--plugin-dir` | Load plugins from directories |

### Subagents

| Flag | Description |
|------|-------------|
| `--agent` | Specify agent for current session |
| `--agents` | Define custom subagents via JSON |

## Output Format Details

### text (Default)

Plain text response, suitable for simple scripts:

```bash
claude -p "What is this project?"
# Output: This project is a TypeScript library for...
```

### json

Structured response with metadata:

```bash
claude -p "Summarize" --output-format json
```

Response structure:
```json
{
  "result": "Summary text...",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "usage": {
    "input_tokens": 1500,
    "output_tokens": 200
  },
  "metadata": {
    "model": "claude-sonnet-4-5-20250929",
    "duration_ms": 3500
  }
}
```

With `--json-schema`, adds `structured_output` field:
```json
{
  "result": "...",
  "structured_output": { /* matches your schema */ },
  "session_id": "..."
}
```

### stream-json

Newline-delimited JSON for real-time streaming:

```bash
claude -p "Generate report" --output-format stream-json
```

Each line is a complete JSON object:
```json
{"type":"content_block_delta","delta":{"type":"text_delta","text":"First"}}
{"type":"content_block_delta","delta":{"type":"text_delta","text":" chunk"}}
{"type":"message_stop"}
```

## Tool Specification Syntax

### Basic Tool Names

```bash
--allowedTools "Read,Edit,Bash"
```

### Granular Bash Patterns

Restrict bash to specific commands:

```bash
--allowedTools "Bash(git diff:*),Bash(git log:*)"
```

Pattern syntax: `Bash(command:args)`

Examples:
- `Bash(npm:*)` - Allow all npm commands
- `Bash(git commit:*)` - Allow git commit with any args
- `Bash(python:*.py)` - Allow running Python files

### Disable All Tools

```bash
--tools ""
```

### Use Default Tools

```bash
--tools "default"
```

## System Prompt Flags

### --system-prompt

Replaces the entire default system prompt:

```bash
claude -p "Review code" \
  --system-prompt "You are a security auditor. Only report vulnerabilities."
```

Use when: Complete control needed, custom persona required.

### --system-prompt-file

Load prompt from a file (print mode only):

```bash
claude -p "Analyze" --system-prompt-file ./prompts/auditor.txt
```

Use when: Version-controlled prompts, team consistency.

### --append-system-prompt

Add instructions while keeping defaults:

```bash
claude -p "Review PR" \
  --append-system-prompt "Focus on performance issues"
```

Use when: Add context without losing Claude Code capabilities.

**Note:** `--system-prompt` and `--system-prompt-file` are mutually exclusive.

## Subagent Configuration

### --agents Flag Format

Define custom subagents via JSON:

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on quality and security.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors and provide fixes."
  }
}'
```

Subagent fields:

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Yes | When to invoke this subagent |
| `prompt` | Yes | System prompt for subagent |
| `tools` | No | Tool restrictions (inherits all if omitted) |
| `model` | No | Model alias (`sonnet`, `opus`, `haiku`) |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | API key for authentication |
| `CLAUDE_CODE_EXIT_AFTER_STOP_DELAY` | Delay before exit after stop signal (ms) |
| `CLAUDE_CODE_USE_BEDROCK` | Use Amazon Bedrock as provider |
| `CLAUDE_CODE_USE_VERTEX` | Use Google Vertex AI as provider |

## Examples

### Minimal Headless

```bash
claude -p "What files are in this project?"
```

### Full Automation

```bash
claude -p "Fix all TypeScript errors" \
  --output-format json \
  --allowedTools "Read,Edit,Bash(npx tsc:*)" \
  --max-turns 10 \
  --append-system-prompt "Only fix type errors, don't refactor"
```

### CI/CD Pipeline

```bash
claude -p "Review this PR for issues" \
  --output-format json \
  --allowedTools "Read,Glob,Grep" \
  --max-turns 3 \
  --dangerously-skip-permissions \
  | jq -r '.result'
```

### Multi-turn Workflow

```bash
# Start session
SESSION=$(claude -p "Analyze codebase" --output-format json | jq -r '.session_id')

# Continue with context
claude -p "Focus on performance" --resume "$SESSION"
claude -p "Generate report" --resume "$SESSION" --output-format json
```

### Custom Model with Fallback

```bash
claude -p "Complex analysis" \
  --model opus \
  --fallback-model sonnet \
  --output-format json
```
