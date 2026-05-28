---
name: tmux-cli
description: Use this skill when you need to communicate with other CLI Agents or Scripts in different tmux panes, especially for executing commands and detecting their exit codes.
---

# Skill body

## Instructions

Use the `tmux-cli` command to communicate with other CLI Agents or Scripts in other tmux panes. Run `tmux-cli --help` to see how to use it!

This command requires the installation of `claude-code-tools`. If you encounter an error indicating that the command is not available, ask the user to install it using:
```bash
uv tool install claude-code-tools
```

## Key Commands

### Execute with Exit Code Detection

Use `tmux-cli execute` when you need to know if a shell command succeeded or failed:

```bash
tmux-cli execute "make test" --pane=2
# Returns JSON: {"output": "...", "exit_code": 0}

tmux-cli execute "npm install" --pane=ops:1.3 --timeout=60
# Returns exit_code=0 on success, non-zero on failure, -1 on timeout
```

This is useful for:

- Running builds and knowing if they passed
- Running tests and detecting pass/fail
- Multi-step automation that should abort on failure

**Note**: `execute` is for shell commands only, not for agent-to-agent communication. For communicating with another Claude Code instance, use `send`, `wait_idle`, and `capture` instead.