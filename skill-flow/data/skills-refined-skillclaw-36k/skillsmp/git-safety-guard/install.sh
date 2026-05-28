#!/usr/bin/env bash
#
# install.sh
# Installs Claude Code hook to block destructive git/filesystem commands
# and git hooks for DX hygiene.
#
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_DIR="${SCRIPT_DIR}/hooks"

GLOBAL_MODE=0
if [[ "${1:-}" == "--global" ]]; then
  GLOBAL_MODE=1
fi

timestamp() { date +"%Y%m%d-%H%M%S"; }

link_hook() {
  local src="$1"
  local dest="$2"
  mkdir -p "$(dirname -- "$dest")"
  ln -sf "$src" "$dest"
}

echo -e "${BLUE}git-safety-guard:${NC} hooks dir: ${HOOKS_DIR}"

if [[ "$GLOBAL_MODE" == "1" ]]; then
  echo -e "${BLUE}Installing globally to ~/.claude/${NC}"

  mkdir -p "$HOME/.claude/hooks"
  link_hook "${HOOKS_DIR}/git_safety_guard.py" "$HOME/.claude/hooks/git_safety_guard.py"

  SETTINGS_FILE="$HOME/.claude/settings.json"
  if [[ ! -f "$SETTINGS_FILE" ]]; then
    cat > "$SETTINGS_FILE" << 'EOF'
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$HOME/.claude/hooks/git_safety_guard.py"
          }
        ]
      }
    ]
  }
}
EOF
    echo -e "${GREEN}✓${NC} Created $SETTINGS_FILE"
  else
    echo -e "${YELLOW}ℹ  Skipping existing $SETTINGS_FILE${NC}"
  fi
fi

echo -e "${BLUE}Installing git hooks into current repo (.git/hooks)${NC}"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo -e "${RED}✗${NC} Not inside a git repository."
  exit 1
fi

GIT_DIR="$(git rev-parse --git-dir)"
HOOK_DIR="${GIT_DIR%/}/hooks"
mkdir -p "$HOOK_DIR"

link_hook "${HOOKS_DIR}/pre-push" "${HOOK_DIR}/pre-push"
link_hook "${HOOKS_DIR}/state-recovery" "${HOOK_DIR}/post-merge"
link_hook "${HOOKS_DIR}/state-recovery" "${HOOK_DIR}/post-checkout"
link_hook "${HOOKS_DIR}/permission-sentinel" "${HOOK_DIR}/pre-commit"

echo -e "${GREEN}✓${NC} Linked hooks into $HOOK_DIR"

# Cleanup: remove prior untracked .claude/hooks files created by older versions.
if [[ -d ".claude/hooks" ]]; then
  top_level="$(git rev-parse --show-toplevel)"
  repo_name="$(basename -- "$top_level")"
  wip_dir="$HOME/.cache/git-safety-guard/${repo_name}/claude-hooks.wip.$(timestamp)"
  moved=0
  for f in git_safety_guard.py pre-push state-recovery permission-sentinel; do
    if [[ -f ".claude/hooks/$f" ]] && ! git ls-files --error-unmatch ".claude/hooks/$f" >/dev/null 2>&1; then
      mkdir -p "$wip_dir"
      mv ".claude/hooks/$f" "$wip_dir/$f"
      moved=1
    fi
  done
  if [[ "$moved" == "1" ]]; then
    echo -e "${YELLOW}ℹ  Moved old untracked .claude/hooks files to $wip_dir${NC}"
  fi

  # If the hooks dir is now empty, remove it (keeps repos clean).
  if [[ -d ".claude/hooks" ]] && [[ -z "$(ls -A ".claude/hooks" 2>/dev/null || true)" ]]; then
    rmdir ".claude/hooks" 2>/dev/null || true
  fi
fi

# --- 3. Settings JSON ---
echo -e "${GREEN}✓${NC} Done."
