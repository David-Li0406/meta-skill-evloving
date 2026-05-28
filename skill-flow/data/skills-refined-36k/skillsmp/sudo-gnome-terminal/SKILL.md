---
name: "sudo-gnome-terminal"
description: "Run sudo commands that require password entry by opening a separate gnome-terminal on Ubuntu, capturing stdout/stderr/exit code, and returning them to Codex. Use when privileged commands need the user to type a sudo password and the main terminal cannot accept interactive input."
---

# Sudo Gnome Terminal

## Overview

Run privileged commands in a separate gnome-terminal so the user can enter the sudo password. A helper script captures stdout/stderr and the exit code, then returns them to the calling terminal.

## Quick Start

1. Build a non-interactive command (only the sudo password prompt should require input). For TUI editors or interactive tools, use `--interactive`.
2. Run the helper script with the command prefixed by `sudo`.
3. The new terminal window appears; the user enters the password if prompted.
4. The helper script returns stdout/stderr and the exit code to the caller.
5. The command is echoed in the terminal window in a highlighted color before execution for user verification.

Examples:

```bash
SKILL_RUNNER=""
for base in "$HOME/.claude/skills" "$HOME/.codex/skills" "$HOME/.config/opencode/skills"; do
  candidate="$base/sudo-gnome-terminal/scripts/run_sudo_gnome_terminal.sh"
  if [ -x "$candidate" ]; then
    SKILL_RUNNER="$candidate"
    break
  fi
done
if [ -z "$SKILL_RUNNER" ]; then
  echo "sudo-gnome-terminal skill not found" >&2
  exit 1
fi

"$SKILL_RUNNER" -- sudo systemctl restart ssh
"$SKILL_RUNNER" --cmd "sudo apt-get update && sudo apt-get install -y curl"
"$SKILL_RUNNER" --interactive -- sudo vim /etc/apt/sources.list
```

## Workflow

1. Confirm the command is safe and necessary to run as root.
2. Prefer a single, non-interactive command. If the task needs additional interaction beyond the sudo password, ask the user to run it manually.
3. Use `run_sudo_gnome_terminal.sh` to execute the command and capture results.
4. Do not ask for extra confirmation once the command starts; wait until it completes or the user interrupts it (e.g., Ctrl+C).
5. If running via a tool that has a default timeout, set a very long timeout so the user can enter the password at their pace.
6. Inspect stdout/stderr and the exit code returned by the script before continuing.

## Script Reference

### `scripts/run_sudo_gnome_terminal.sh`

Usage:

```bash
run_sudo_gnome_terminal.sh -- <command> [args...]
run_sudo_gnome_terminal.sh --cmd "<shell command>"
run_sudo_gnome_terminal.sh --interactive -- <command> [args...]
run_sudo_gnome_terminal.sh --interactive --cmd "<shell command>"
run_sudo_gnome_terminal.sh --self-test
```

Notes:
- Prefer `-- <command> [args...]` for precise argument handling.
- Use `--cmd` for pipelines or shell operators.
- Use `--interactive` for TUI editors or commands that require a real TTY. Stdout capture is disabled; stderr is still captured and the exit code is returned.
- Requires a graphical session and `gnome-terminal` to be installed.
- Ctrl+C sends an interrupt to the helper; it will close the gnome-terminal window and exit with code 130. If a host agent does not pass signals, close the gnome-terminal window to stop the run.

Environment variables:
- `CODEX_SUDO_TERMINAL_TITLE`: window title (default: `Codex sudo`)
- `CODEX_SUDO_TERMINAL_KEEP_LOGS=1`: keep temp logs instead of deleting them

Limitations:
- Intended for sudo password entry only. Avoid commands that require additional interactive prompts.
- If the terminal window does not close after the command finishes, check GNOME Terminal preferences ("When command exits" should be set to close the terminal).
