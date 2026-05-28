---
name: [tool-name]-wrapper
description: [Action] [Context] via CLI/API interface. Use when [User Trigger].
allowed-tools: [bash, [tool-name]]
license: Apache-2.0
metadata:
  author: [Author]
  version: "1.0"
---

# [Tool Name] Wrapper

This skill wraps the [Tool Name] CLI to provide safe and structured access for agents.

## When to use this skill

Use this skill when you need to interact with [Tool Name] for tasks like [Common Task 1], [Common Task 2].

## Supported Commands

The following commands are authorized and recommended:

- `[command 1]`: [Description of what it does]
  - Example: `[tool-name] [command 1] --flag`
- `[command 2]`: [Description]

## Usage Guidelines

- **Do**: Use `--json` output when available for easier parsing.
- **Don't**: specific dangerous flags (e.g., `--force`) without explicit user request.

## Error Handling

- If `[Error X]` occurs, try running `[Recovery Command]`.
- Common exit codes:
  - `1`: General error (check logs).

## Progressive Disclosure

If the tool has complex configuration or many subcommands, store detailed command references in `references/[TOOL_NAME]_COMMANDS.md`.
