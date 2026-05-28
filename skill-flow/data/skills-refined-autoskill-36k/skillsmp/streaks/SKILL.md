---
name: streaks
description: "Use when managing Streaks app habits via the Streaks CLI (`st`): discover actions, link Shortcuts, run habit/task actions, configure output (agent NDJSON, JSON UTI), troubleshoot install/doctor/discover, or interpret exit codes and JSON envelopes for automation."
---

# Streaks CLI

## Overview

Use this skill to manage Streaks app habits via the `st` CLI with Shortcuts-based actions and the `streaks://` URL scheme. The `st` CLI must be installed to use this skill.

Install the CLI with Homebrew (`brew tap vburojevic/tap` then `brew install streaks-cli`) or from source (`make build`).

## Quick start

- Run `st discover` and `st doctor` to validate app + Shortcuts readiness.
- Run `st open` to confirm Streaks launches.
- Run `st help` or `st help <command>` to resolve usage questions.

## Core workflow

1. Discover capabilities: `st discover` (use `--agent` for NDJSON).
2. Verify setup: `st doctor`.
3. Ensure shortcuts exist:
   - If missing, create them in Shortcuts or import wrapper `.shortcut` files with `st install --import`.
4. Map custom shortcut names with `st link <action-id> --shortcut "Name"`.
5. Run actions: `st <action> [--task "Habit"]`.
6. When automating, enable agent mode and parse the last NDJSON line.

## Running actions

- Use `st actions list` and `st actions describe <action>` to inspect available actions and required parameters.
- Use `--task` for habit/task-based actions.
- Use `--input` or `--stdin` to pass raw JSON input.
- Use `--dry-run` to verify shortcut name + payload before execution.
- Use `--trace <file>` to append JSONL trace records.

## Output and automation

- Default output is human-oriented for meta commands and raw shortcut output for actions.
- Use `--agent` or `STREAKS_CLI_AGENT=1` for NDJSON envelopes and stable errors.
- Use `--shortcuts-output public.json` when you need JSON data from Shortcuts.
- Use `--no-output` when only exit codes matter.

## Troubleshooting

- Use `st doctor` for readiness checks.
- Use `st discover --markdown` for a human-readable capability report.
- If an action fails, check stderr JSON in agent mode and consult exit codes.

## References

- Use `references/commands.md` for the full command/flag list and env vars.
- Use `references/agent.md` for NDJSON conventions and integration patterns.
- Use `references/schema.md` for exit codes and envelope schemas.
- Use `references/troubleshooting.md` for common errors and fixes.
