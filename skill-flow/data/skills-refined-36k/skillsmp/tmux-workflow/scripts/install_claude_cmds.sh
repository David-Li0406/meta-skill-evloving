#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE' >&2
Install Claude custom command markdown files that call this skill's scripts.

Writes into (auto-detected, override via CODEX_CLAUDE_COMMAND_DIR):
  ~/.claude/commands
  ~/.config/claude/commands
  ~/.local/share/claude/commands

Files installed (backups created if already exist):
  cask.md, cpend.md, cping.md

USAGE
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

detect_claude_dir() {
  if [[ -n "${CODEX_CLAUDE_COMMAND_DIR:-}" ]]; then
    echo "$CODEX_CLAUDE_COMMAND_DIR"
    return
  fi

  local candidates=(
    "$HOME/.claude/commands"
    "$HOME/.config/claude/commands"
    "$HOME/.local/share/claude/commands"
  )

  for dir in "${candidates[@]}"; do
    if [[ -d "$dir" ]]; then
      echo "$dir"
      return
    fi
  done

  local fallback="$HOME/.claude/commands"
  mkdir -p "$fallback"
  echo "$fallback"
}

cmd_dir="$(detect_claude_dir)"
mkdir -p "$cmd_dir"

timestamp="$(date +%Y%m%d-%H%M%S)"

backup_if_exists() {
  local path="$1"
  if [[ -f "$path" ]]; then
    mv "$path" "${path}.bak.${timestamp}"
  fi
}

backup_if_exists "$cmd_dir/cask.md"
backup_if_exists "$cmd_dir/cpend.md"
backup_if_exists "$cmd_dir/cping.md"

cat >"$cmd_dir/cask.md" <<'MD'
Send message to Codex (running in tmux) and wait for reply via `codex_ask.py`.

Designed for Claude Code: run with `run_in_background=true` so Claude can continue working while Codex processes.

Execution:
- Run:
  - `Bash(python3 "$(git rev-parse --show-toplevel)/.codex/skills/tmux-workflow/scripts/codex_ask.py" "<content>", run_in_background=true)`

Parameters:
- `<content>` required
- `--timeout SECONDS` optional (default from `TWF_TIMEOUT`, fallback 3600)
- `--session-file PATH` optional (default `./.codex-tmux-session.json`, override via `TWF_SESSION_FILE`)

Output contract:
- stdout: reply text only
- stderr: progress/errors
- exit code: 0 = got reply, 2 = timeout/no reply, 1 = error
MD

cat >"$cmd_dir/cpend.md" <<'MD'
View latest Codex reply from official Codex JSONL logs.

Execution:
- Run `Bash(python3 "$(git rev-parse --show-toplevel)/.codex/skills/tmux-workflow/scripts/codex_pend.py" [N])`

Parameters:
- `N` optional: number of Q/A rounds (default 1). When N=1, prints reply only.
- `--session-file PATH` optional (default `./.codex-tmux-session.json`, override via `TWF_SESSION_FILE`)
MD

cat >"$cmd_dir/cping.md" <<'MD'
Check if tmux Codex worker is alive and whether session file is bound to a log file.

Execution:
- Run `Bash(python3 "$(git rev-parse --show-toplevel)/.codex/skills/tmux-workflow/scripts/codex_ping.py")`

Notes:
- Default session file: `./.codex-tmux-session.json` (override via `TWF_SESSION_FILE`)
MD

echo "✅ Installed Claude commands into: $cmd_dir" >&2
