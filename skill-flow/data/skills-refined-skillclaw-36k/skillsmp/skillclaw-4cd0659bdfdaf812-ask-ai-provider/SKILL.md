---
name: ask-ai-provider
description: Use this skill when you want to send a request to a specified AI provider asynchronously and end your turn immediately.
---

# Ask AI Provider

Send the user's request to the specified AI provider via the `ask` command.

## Usage

The first argument must be the provider name. The message MUST be provided via stdin (heredoc or pipe), not as CLI arguments, to avoid shell globbing issues. Supported providers include:
- `gemini` - Send to Gemini
- `codex` - Send to Codex
- `opencode` - Send to OpenCode
- `droid` - Send to Droid
- `claude` - Send to Claude

Optional flags after the provider:
- `--foreground` / `--background`
- Env overrides: `CCB_ASK_FOREGROUND=1` / `CCB_ASK_BACKGROUND=1`

## Execution (MANDATORY)

```bash
CCB_CALLER=<provider> command ask "$PROVIDER" <<'EOF'
$MESSAGE
EOF
```

## Rules

- STRICT: Execute the bash snippet in the Execution section, then immediately end your turn.
- Do not run any other commands/tools besides this snippet unless the user explicitly asks.
- Do not add any extra commentary/output (including "processing..."); the `ask` command already prints the task ID and log path.
- Do not wait for results or check status in the same turn.

## Examples

- `/ask gemini What is 12+12?` (send via heredoc)
- `CCB_CALLER=codex command ask gemini <<'EOF'`
  `What is 12+12?`
  `EOF`

## Notes

- If it fails, stop after reporting the failure output; only run diagnostics in a new turn if the user requests it.