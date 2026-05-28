---
name: flow-next-ralph-init
description: Scaffold or update a repo-local Ralph autonomous harness under scripts/ralph/. Use when the user runs /flow-next:ralph-init.
---

# Ralph Init

Scaffold or update the repo-local Ralph harness. Opt-in only.

## Rules

- Only create or update `scripts/ralph/` in the current repo.
- If `scripts/ralph/` already exists, offer to update (preserves `config.env`).
- Copy templates from `templates/` into `scripts/ralph/`.
- Copy `flowctl` and `flowctl.py` from `${CLAUDE_PLUGIN_ROOT}/scripts/` into `scripts/ralph/`.
- Set executable bit on `scripts/ralph/ralph.sh`, `scripts/ralph/ralph_once.sh`, and `scripts/ralph/flowctl`.

## Workflow

1. Resolve repo root: `git rev-parse --show-toplevel`.
2. Check if `scripts/ralph/` exists:
   - If it exists, ask "Update existing Ralph setup? (preserves config.env and runs/) [y/n]":
     - If no, stop.
     - If yes, set `UPDATE_MODE=1`.
   - If it does not exist, set `UPDATE_MODE=0`.
3. Detect available review backends (skip if `UPDATE_MODE=1`):
   ```bash
   HAVE_RP=$(which rp-cli >/dev/null 2>&1 && echo 1 || echo 0)
   HAVE_CODEX=$(which codex >/dev/null 2>&1 && echo 1 || echo 0)
   ```
4. Determine review backend (skip if `UPDATE_MODE=1`):
   - If both available, ask user:
     ```
     Both RepoPrompt and Codex available. Which review backend?
     a) RepoPrompt (macOS, visual builder)
     b) Codex CLI (cross-platform, GPT 5.2 High)

     (Reply: "a", "rp", "b", "codex", or just tell me)
     ```
     Wait for response. Default if empty/ambiguous: `rp`.
   - If only `rp-cli` available, use `rp`.
   - If only `codex` available, use `codex`.
   - If neither available, use `none`.
5. Copy files using bash (MUST use `cp`, NOT Write tool):
   - If `UPDATE_MODE=1` (updating):
   ```bash
   # Backup config.env
   cp scripts/ralph/config.env /tmp/ralph-config-backup.env

   # Update templates (preserves runs/)
   cp -R templates/. scripts/ralph/
   cp "${CLAUDE_PLUGIN_ROOT}/scripts/flowctl" "${CLAUDE_PLUGIN_ROOT}/scripts/flowctl.py" scripts/ralph/
   chmod +x scripts/ralph/ralph.sh scripts/ralph/ralph_once.sh scripts/ralph/flowctl

   # Restore config.env
   cp /tmp/ralph-config-backup.env scripts/ralph/config.env
   ```
   - If `UPDATE_MODE=0` (fresh install):
   ```bash
   mkdir -p scripts/ralph/runs
   cp -R templates/. scripts/ralph/
   cp "${CLAUDE_PLUGIN_ROOT}/scripts/flowctl" "${CLAUDE_PLUGIN_ROOT}/scripts/flowctl.py" scripts/ralph/
   chmod +x scripts/ralph/ralph.sh scripts/ralph/ralph_once.sh scripts/ralph/flowctl
   ```
6. Edit `scripts/ralph/config.env` to set the chosen review backend (skip if `UPDATE_MODE=1`):
   - Replace `PLAN_REVIEW=codex` with `PLAN_REVIEW=<chosen>`.
   - Replace `WORK_REVIEW=codex` with `WORK_REVIEW=<chosen>`.
7. Print next steps (run from terminal, NOT inside Claude Code):
   - If `UPDATE_MODE=1`:
   ```
   Ralph updated! Your config.env was preserved.

   Run from terminal:
   - ./scripts/ralph/ralph_once.sh (one iteration, observe)
   - ./scripts/ralph/ralph.sh (full loop, AFK)
   ```
   - If `UPDATE_MODE=0`:
   ```
   Ralph initialized!

   Next steps (run from terminal, NOT inside Claude Code):
   - Edit scripts/ralph/config.env to customize settings
   - ./scripts/ralph/ralph_once.sh (one iteration, observe)
   - ./scripts/ralph/ralph.sh (full loop, AFK)

   Maintenance:
   - Re-run /flow-next:ralph-init after plugin updates to refresh scripts
   - Uninstall: rm -rf scripts/ralph/
   ```