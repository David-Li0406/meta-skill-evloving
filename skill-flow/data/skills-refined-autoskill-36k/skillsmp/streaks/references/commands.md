# Command Reference (Concise)

Use `st --help` or `st <command> --help` for full details.

## Global flags

- `--agent` NDJSON output with stable envelopes.
- `--quiet` / `--verbose`
- `--no-output` suppress stdout/stderr (exit code only).
- `--timeout` Shortcuts run timeout (default 30s).
- `--retries` / `--retry-delay` retry Shortcuts runs on failure.
- `--config` override config path (default `~/.config/streaks-cli/config.json`).
- `--shortcuts-output` Shortcuts output UTI (default `public.plain-text`).

## Core commands

- `st discover` capability report (JSON by default).
- `st discover --markdown` human-readable report.
- `st doctor` verify Streaks + Shortcuts readiness.
- `st install` verify shortcuts are ready.
- `st install --import` open bundled `.shortcut` wrapper files.
- `st link <action-id> --shortcut <name-or-id>` map an action to a shortcut.
- `st unlink <action-id>` remove mapping.
- `st links` list mappings.
- `st help [command]` help (NDJSON when `--agent`).
- `st open` open Streaks via URL scheme.

## Actions

- `st actions list` list all actions (NDJSON lines).
- `st actions describe <action>` show action detail and sample input.
- `st <action>` run a Streaks action (e.g., `st task-complete --task "Read"`).

Shortcut matching uses exact names. Helper shortcuts (e.g., "Get Task Object") are not CLI actions.

## Action flags

- `--task` task name for task-based actions.
- `--stdin` read JSON input from stdin.
- `--input` raw JSON input string.
- `--dry-run` print shortcut + payload only.
- `--trace <file>` append JSON trace records (JSONL).
- `--shortcut <name-or-id>` run a specific shortcut.

## Install flags

- `--import` open bundled `.shortcut` files for import.
- `--from-dir` use a custom directory of `.shortcut` files.

Environment:
- `STREAKS_CLI_SHORTCUT_DIR` override default wrapper shortcut directory.
