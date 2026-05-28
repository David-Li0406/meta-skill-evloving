---
name: claude-code-cli
description: Use this skill when you need help with Claude Code commands, flags, or CLI usage.
---

# CLI Reference for Claude Code

This document serves as a complete reference for the Claude Code command-line interface, including commands, flags, and usage examples.

## CLI Commands

| Command                         | Description                                            | Example                                           |
| :------------------------------ | :--------------------------------------------------- | :------------------------------------------------ |
| `claude`                        | Start interactive REPL                               | `claude`                                          |
| `claude "query"`               | Start REPL with initial prompt                       | `claude "explain this project"`                  |
| `claude -p "query"`            | Query via SDK, then exit                             | `claude -p "explain this function"`              |
| `cat file \| claude -p "query"`| Process piped content                                | `cat logs.txt \| claude -p "explain"`           |
| `claude -c`                    | Continue most recent conversation in current directory| `claude -c`                                       |
| `claude -c -p "query"`         | Continue via SDK                                     | `claude -c -p "Check for type errors"`           |
| `claude -r "<session>" "query"`| Resume session by ID or name                         | `claude -r "auth-refactor" "Finish this PR"`     |
| `claude update`                | Update to latest version                             | `claude update`                                   |
| `claude mcp`                   | Configure Model Context Protocol (MCP) servers       | See the Claude Code MCP documentation             |

## CLI Flags

Customize Claude Code's behavior with these command-line flags:

| Flag                                   | Description                                                                                                                                                                                               | Example                                                                                            |
| :------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| :------------------------------------------------------------------------------------------------- |
| `-c key=value`                        | Set configuration options for the session.                                                                                                                                                               | `claude -c mode=debug`                                                                             |
| `--json`                               | Enable JSONL streaming for outputs.                                                                                                                                                                      | `claude exec --json`                                                                                |
| `--sandbox`                            | Run in a sandboxed environment to restrict access to system resources.                                                                                                                                  | `claude --sandbox`                                                                                 |

This skill consolidates the information from both pieces of evidence, providing a comprehensive reference for using the Claude Code CLI effectively.