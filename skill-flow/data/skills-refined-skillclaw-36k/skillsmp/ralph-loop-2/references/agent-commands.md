# Agent commands (stdin-based)

## What is the agent command?

The agent command is the exact CLI string ralph-loop runs each iteration. ralph-loop pipes `prompt.md` to the command via stdin; the command should run unattended and write its response to stdout.

## Choose a command

- Use an auto/non-interactive flag so the loop can run unattended.
- Verify the binary exists with `command -v <agent>`.
- Ensure it accepts stdin and does not hang.

## Common commands

- Codex CLI: `codex exec --full-auto`
- Claude Code: `claude --dangerously-skip-permissions`
- Gemini CLI: `gemini --yolo`
- Qwen Code: `qwen` (requires YOLO mode in `.qwen/settings.json`)

## Validate stdin

```bash
echo test | <agent cmd>
```

If the command errors or waits for input, use a wrapper script.

## Prompt echo issue

If the loop finishes immediately and logs show your prompt text, the agent is echoing stdin and the completion tag can be detected from the prompt. Use a quiet/disable-echo mode if available, or pass the prompt via a file/flag instead of stdin. If neither is possible, adjust `ralph.sh` to check for `<promise>COMPLETE</promise>` only in the model output portion.

## Wrapper for non-stdin agents

Create `agent-wrapper.sh` in the project root:
```bash
#!/usr/bin/env bash
set -e
PROMPT="$(cat)"
your-agent --prompt "$PROMPT"
```

Then:
```bash
chmod +x agent-wrapper.sh
./ralph-loop/ralph.sh "./agent-wrapper.sh" 20
```

## Quoting

`ralph.sh` invokes the command via shell word splitting. If you need nested quotes, env vars, or complex args, use a wrapper script.
