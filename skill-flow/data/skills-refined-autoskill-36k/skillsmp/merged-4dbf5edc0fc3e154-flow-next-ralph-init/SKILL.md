---
name: flow-next-ralph-init
description: Scaffold a repo-local Ralph autonomous harness under scripts/ralph/. Use when the user runs /flow-next:ralph-init.
---

# Ralph init

Scaffold a repo-local Ralph harness. Opt-in only.

## Rules

- Only create `scripts/ralph/` in the current repo.
- If `scripts/ralph/` already exists, stop and ask the user to remove it first.
- Copy templates from `templates/` into `scripts/ralph/`.
- Copy `flowctl` and `flowctl.py` from `${PLUGIN_ROOT}/scripts/` into `scripts/ralph/`.
- Set executable bit on `scripts/ralph/ralph.sh`, `scripts/ralph/ralph_once.sh`, and `scripts/ralph/flowctl`.

## Workflow

1. Resolve repo root: `ROOT="$(git rev-parse --show-toplevel)"`
2. Check `scripts/ralph/` does not exist.
3. Detect available review backends:
   ```bash
   HAVE_RP=0
   if command -v rp-cli >/dev/null 2>&1; then
     HAVE_RP=1
   elif [[ -x /opt/homebrew/bin/rp-cli || -x /usr/local/bin/rp-cli ]]; then
     HAVE_RP=1
   fi
   HAVE_CODEX=$(which codex >/dev/null 2>&1 && echo 1 || echo 0)
   ```
4. Determine review backend:
   - If BOTH available, ask user:
     ```
     Both OpenCode and RepoPrompt available. Which review backend?
     a) OpenCode (GPT‑5.2 High)
     b) RepoPrompt (macOS, visual builder)

     (Reply: "a", "opencode", "b", "rp", or just tell me)
     ```
     Wait for response. Default if empty/ambiguous: `opencode`
   - If only rp-cli available: use `rp`
   - If only codex available: use `codex`
   - If neither available: use `none`
5. Write `scripts/ralph/config.env` with:
   - `PLAN_REVIEW=<chosen>` and `WORK_REVIEW=<chosen>`
   - replace `{{PLAN_REVIEW}}` and `{{WORK_REVIEW}}` placeholders in the template
6. Copy templates and flowctl files.
7. Print next steps (run from terminal, NOT inside the coding environment):
   - Edit `scripts/ralph/config.env` to customize settings
   - `./scripts/ralph/ralph_once.sh` (one iteration, observe)
   - `./scripts/ralph/ralph.sh` (full loop, AFK)
   - Uninstall: `rm -rf scripts/ralph/`