---
name: flow-next-ralph-init
description: Use this skill to scaffold or update a repo-local Ralph autonomous harness under scripts/ralph/. It is invoked when the user runs /flow-next:ralph-init.
---

# Ralph init

Scaffold or update repo-local Ralph harness. Opt-in only.

## Rules

- Only create/update `scripts/ralph/` in the current repo.
- If `scripts/ralph/` already exists, offer to update (preserves `config.env`).
- Copy templates from `templates/` into `scripts/ralph/`.
- Copy `flowctl` and `flowctl.py` from `${CLAUDE_PLUGIN_ROOT}/scripts/` into `scripts/ralph/`.
- Set executable bit on `scripts/ralph/ralph.sh`, `scripts/ralph/ralph_once.sh`, and `scripts/ralph/flowctl`.

## Workflow

1. Resolve repo root: `git rev-parse --show-toplevel`
2. Check if `scripts/ralph/` exists:
   - If exists: ask "Update existing Ralph setup? (preserves config.env and runs/) [y/n]"
     - If no: stop
     - If yes: set `UPDATE_MODE=1`
   - If not exists: set `UPDATE_MODE=0`
3. Detect available review backends (skip if `UPDATE_MODE=1`):
   ```bash
   HAVE_RP=$(which rp-cli >/dev/null 2>&1 && echo 1 || echo 0)
   HAVE_CODEX=$(which codex >/dev/null 2>&1 && echo 1 || echo 0)
   ```
4. Determine review backend (skip if `UPDATE_MODE=1`):
   - If BOTH available, ask user:
     ```
     Both RepoPrompt and Codex available. Which review backend?
     a) RepoPrompt (macOS, visual builder)
     b) Codex CLI (cross-platform, GPT 5.2 High)

     (Reply: "a", "rp", "b", "codex", or just tell me)
     ```
     Wait for response. Default if empty/ambiguous: `rp`
   - If only `rp-cli` available: use `rp`
   - If only `codex` available: use `codex`
   - If neither available: use `none`
5. Write `scripts/ralph/config.env` with:
   - `PLAN_REVIEW=<chosen>` and `WORK_REVIEW=<chosen>`
   - replace `{{PLAN_REVIEW}}` and `{{WORK_REVIEW}}` placeholders in the template
6. Copy files using bash (MUST use `cp`, NOT Write tool):
   **If `UPDATE_MODE=1` (updating):**
   ```bash
   # Backup config.env
   cp scripts/ralph/config.env /tmp/ralph-config-backup.env

   # Update templates (preserves runs/)
   cp "${CLAUDE_PLUGIN_ROOT}/skills/flow-next-ralph-init/templates/ralph.sh" scripts/ralph/
   cp "${CLAUDE_PLUGIN_ROOT}/skills/flow-next-ralph-init/templates/ralph_once.sh" scripts/ralph/
   cp "${CLAUDE_PLUGIN_ROOT}/skills/flow-next-ralph-init/templates/prompt_plan.md" scripts/ralph/
   cp "${CLAUDE_PLUGIN_ROOT}/skills/flow-next-ralph-init/templates/prompt_work.md" scripts/ralph/
   cp "${CLAUDE_PLUGIN_ROOT}/skills/flow-next-ralph-init/templates/watch-filter.py" scripts/ralph/
   cp "${CLAUDE_PLUGIN_ROOT}/scripts/flowctl" "${CLAUDE_PLUGIN_ROOT}/scripts/flowctl.py" scripts/ralph/
   chmod +x scripts/ralph/ralph.sh scripts/ralph/ralph_once.sh scripts/ralph/flowctl
   ```
7. Print next steps (run from terminal, NOT inside Claude Code):
   - Edit `scripts/ralph/config.env` to customize settings
   - `./scripts/ralph/ralph_once.sh` (one iteration, observe)
   - `./scripts/ralph/ralph.sh` (full loop, AFK)
   - Uninstall: `rm -rf scripts/ralph/`