---
name: cli-reference
description: Use this skill when you need a comprehensive guide to Claude Code CLI commands, flags, and automation patterns.
---

# Skill body

## When to Use

- "What CLI flags are available?"
- "How do I use headless mode?"
- "Claude in automation/CI/CD"
- "Output format options"
- "System prompt via CLI"
- "How do I spawn agents properly?"

## Core Commands

| Command | Description | Example |
|---------|-------------|---------|
| `claude` | Start interactive REPL | `claude` |
| `claude "query"` | REPL with initial prompt | `claude "explain this project"` |
| `claude -p "query"` | Headless mode (SDK) | `claude -p "explain function"` |
| `cat file \| claude -p` | Process piped content | `cat logs.txt \| claude -p "explain"` |
| `claude -c` | Continue most recent | `claude -c` |
| `claude -c -p "query"` | Continue via SDK | `claude -c -p "check types"` |
| `claude -r "id" "query"` | Resume session | `claude -r "auth" "finish PR"` |
| `claude update` | Update version | `claude update` |
| `claude mcp` | Configure MCP servers | See MCP docs |

## Session Control

| Flag | Description | Example |
|------|-------------|---------|
| `--continue, -c` | Load most recent conversation | `claude --continue` |
| `--resume, -r` | Resume session by ID/name | `claude --resume auth-refactor` |
| `--session-id` | Use specific UUID | `claude --session-id "550e8400-..."` |
| `--fork-session` | Create new session on resume | `claude --resume abc --fork-session` |

## Headless Mode (Critical for Agents)

| Flag | Description | Example |
|------|-------------|---------|
| `--print, -p` | Non-interactive, exit after | `claude -p "query"` |
| `--output-format` | `text`, `json`, `stream-json` | `claude -p --output-format json` |
| `--max-turns` | Limit agentic turns | `claude -p --max-turns 100 "query"` |
| `--verbose` | Full turn-by-turn output | `claude --verbose` |
| `--dangerously-skip-permissions` | Skip permission prompts | `claude -p --dangerously-skip-permissions` |
| `--include-partial-messages` | Include streaming events | `claude -p --output-format stream-json --include-partial-messages` |
| `--input-format` | Input format (text/stream-json) | `claude -p --input-format stream-json` |

## Tool Control

| Flag | Description | Example |
|------|-------------|---------|
| `--allowedTools` | Auto-approve these tools | `"Bash(git log:*)" "Read"` |
| `--disallowedTools` | Block these tools | `"Bash(rm:*)" `