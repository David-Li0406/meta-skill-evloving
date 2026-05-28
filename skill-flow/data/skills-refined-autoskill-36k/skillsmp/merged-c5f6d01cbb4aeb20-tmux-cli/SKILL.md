---
name: tmux-cli
description: Use this skill to communicate with other CLI Agents or Scripts in tmux panes, especially when you need to execute commands and detect their exit codes.
---

# tmux-cli

## Instructions

Use the `tmux-cli` command to communicate with other CLI Agents or Scripts in tmux panes. Run `tmux-cli --help` to see how to use it!

This command requires the installation of `claude-code-tools`. If you encounter an error indicating that the command is not available, ask the user to install it using:
`uv tool install claude-code-tools`.

## Key Commands

### Execute with Exit Code Detection

Use `tmux-cli execute` when you need to know if a shell command succeeded or failed:

```bash
tmux-cli execute "<command>" --pane=<pane_id>
# Returns JSON: {"output": "...", "exit_code": <code>}
```

This is useful for:

- Running builds and knowing if they passed
- Running tests and detecting pass/fail
- Multi-step automation that should abort on failure

**Note**: `execute` is for shell commands only, not for agent-to-agent communication. For communicating with another Claude Code instance, use `send`, `wait_idle`, and `capture` instead.