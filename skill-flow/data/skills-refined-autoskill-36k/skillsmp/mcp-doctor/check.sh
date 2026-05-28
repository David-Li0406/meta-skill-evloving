#!/usr/bin/env bash
set -euo pipefail

echo "🩺 mcp-doctor — canonical MCP + CLI checks (no secrets)"

STRICT="${MCP_DOCTOR_STRICT:-0}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="${SKILLS_DIR:-"$(cd "${SCRIPT_DIR}/.." && pwd)"}"

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

FILES=(
  "$REPO_ROOT/.claude/settings.json"
  "$REPO_ROOT/.vscode/mcp.json"
  "$REPO_ROOT/codex.mcp.json"
  # NOTE: gemini is deprecated (V4.2.1) - canonical IDEs: antigravity, claude-code, codex-cli, opencode
  "$REPO_ROOT/.mcp.json"
  "$REPO_ROOT/opencode.json"
  "$HOME/.claude/settings.json"
  "$HOME/.claude.json"
  "$HOME/.codex/config.toml"
  # Canonical IDE config paths (V4.2.1)
  "$HOME/.gemini/antigravity/mcp_config.json"
  "$HOME/.opencode/config.json"
  # NOTE: gemini settings deprecated - removed from checks
)

have_in_files() {
  local needle="$1"
  for f in "${FILES[@]}"; do
    [[ -f "$f" ]] || continue
    if rg -F -q "$needle" "$f" 2>/dev/null; then
      echo "$f"
      return 0
    fi
  done
  return 1
}

missing_required=0
missing_optional=0

echo ""
echo "REQUIRED MCP servers:"

# 1) universal-skills (DEPRECATED)
# No longer checked



echo ""
echo "OPTIONAL MCP servers:"

# 2) agent-mail (OPTIONAL)
if f="$(have_in_files \"mcp-agent-mail\")" || f="$(have_in_files \"agent-mail\")"; then
  echo "✅ agent-mail (config seen in: $f)"
else
  echo "⚠️  agent-mail (no config found) — optional"
  missing_optional=$((missing_optional+1))
fi

# 3) serena (DEPRECATED - V4.2.1)
if f="$(have_in_files \"serena\")"; then
  echo "⚠️  serena (config seen in: $f) — DEPRECATED, consider removing"
  missing_optional=$((missing_optional+1))
else
  echo "✅ serena (not configured — correctly removed)"
fi

# 4) z.ai search MCP (OPTIONAL)
if f="$(have_in_files \"z.ai\")" || f="$(have_in_files \"api.z.ai\")" || f="$(have_in_files \"search-mcp\")"; then
  echo "✅ z.ai search (config seen in: $f)"
else
  echo "⚠️  z.ai search (no config found) — optional"
  missing_optional=$((missing_optional+1))
fi

echo ""
echo "REQUIRED skills mount:"

# Check ~/.agent/skills -> ~/agent-skills invariant
SKILLS_MOUNT="$HOME/.agent/skills"
AGENT_SKILLS_DIR="$HOME/agent-skills"

if [[ -L "$SKILLS_MOUNT" ]]; then
  TARGET="$(readlink "$SKILLS_MOUNT")"
  if [[ "$TARGET" == "$AGENT_SKILLS_DIR" ]] || [[ "$(cd "$SKILLS_MOUNT" && pwd)" == "$AGENT_SKILLS_DIR" ]]; then
    echo "✅ ~/.agent/skills -> ~/agent-skills (symlink: $TARGET)"
  else
    echo "❌ ~/.agent/skills points to wrong target: $TARGET (expected: $AGENT_SKILLS_DIR)"
    missing_required=$((missing_required+1))
  fi
elif [[ -d "$SKILLS_MOUNT" ]]; then
  MOUNT_REAL="$(cd "$SKILLS_MOUNT" && pwd)"
  if [[ "$MOUNT_REAL" == "$AGENT_SKILLS_DIR" ]]; then
    echo "✅ ~/.agent/skills -> ~/agent-skills (directory)"
  else
    echo "❌ ~/.agent/skills exists but is not ~/agent-skills: $MOUNT_REAL"
    missing_required=$((missing_required+1))
  fi
else
  echo "❌ ~/.agent/skills does not exist — REQUIRED"
  echo "   Run: ln -sfn ~/agent-skills ~/.agent/skills"
  missing_required=$((missing_required+1))
fi

echo ""
echo "Agent-skills repo freshness:"

# Check if ~/agent-skills is a git repo and compare with trunk (origin/HEAD → origin/master → origin/main)
if [[ -d "$AGENT_SKILLS_DIR/.git" ]]; then
  cd "$AGENT_SKILLS_DIR" || true
  # Fetch only if this is a fresh check (optional, avoid network on every run)
  # git fetch origin >/dev/null 2>&1 || true

  TRUNK_REF="$(git symbolic-ref -q --short refs/remotes/origin/HEAD 2>/dev/null || true)"
  if [[ -z "$TRUNK_REF" ]]; then
    if git show-ref --verify --quiet refs/remotes/origin/master; then
      TRUNK_REF="origin/master"
    elif git show-ref --verify --quiet refs/remotes/origin/main; then
      TRUNK_REF="origin/main"
    fi
  fi

  LOCAL_HASH=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
  REMOTE_HASH=$(git rev-parse "$TRUNK_REF" 2>/dev/null || echo "unknown")

  if [[ -z "${TRUNK_REF:-}" ]] || [[ "$LOCAL_HASH" == "unknown" ]] || [[ "$REMOTE_HASH" == "unknown" ]]; then
    echo "⚠️  ~/agent-skills: unable to check repo freshness"
    missing_optional=$((missing_optional+1))
  elif [[ "$LOCAL_HASH" == "$REMOTE_HASH" ]]; then
    echo "✅ ~/agent-skills: up to date with $TRUNK_REF"
  else
    # Check if local is behind
    if git merge-base --is-ancestor HEAD "$TRUNK_REF" 2>/dev/null; then
      BEHIND_COUNT=$(git rev-list --count HEAD.."$TRUNK_REF" 2>/dev/null || echo "?")
      echo "⚠️  ~/agent-skills: behind $TRUNK_REF by $BEHIND_COUNT commits"
      echo "   Run: cd ~/agent-skills && git pull origin ${TRUNK_REF#origin/}"
      missing_optional=$((missing_optional+1))
    elif git merge-base --is-ancestor "$TRUNK_REF" HEAD 2>/dev/null; then
      AHEAD_COUNT=$(git rev-list --count "$TRUNK_REF"..HEAD 2>/dev/null || echo "?")
      echo "✅ ~/agent-skills: ahead of $TRUNK_REF by $AHEAD_COUNT commits"
    else
      echo "⚠️  ~/agent-skills: diverged from $TRUNK_REF (needs rebase or merge)"
      echo "   Run: cd ~/agent-skills && git status"
      missing_optional=$((missing_optional+1))
    fi
  fi
  cd - >/dev/null 2>&1 || true
else
  echo "⚠️  ~/agent-skills: not a git repository"
  missing_optional=$((missing_optional+1))
fi

echo ""
echo "Git trunk alignment (canonical clones):"

CANONICAL_TARGETS_SH="$SKILLS_DIR/scripts/canonical-targets.sh"
if [[ -f "$CANONICAL_TARGETS_SH" ]]; then
  # shellcheck disable=SC1090
  source "$CANONICAL_TARGETS_SH"
fi

CANONICAL_TRUNK="${CANONICAL_TRUNK_BRANCH:-master}"

repo_warns=0
if declare -p CANONICAL_REPOS >/dev/null 2>&1 && [[ "${#CANONICAL_REPOS[@]}" -gt 0 ]]; then
  for repo in "${CANONICAL_REPOS[@]}"; do
    repo_path="$HOME/$repo"
    if [[ ! -d "$repo_path/.git" ]]; then
      echo "⚠️  $repo_path (missing repo) — expected canonical clone"
      repo_warns=$((repo_warns+1))
      continue
    fi

    current_branch="$(git -C "$repo_path" branch --show-current 2>/dev/null || echo "")"
    if [[ -z "$current_branch" ]]; then
      current_branch="$(git -C "$repo_path" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")"
    fi

    if [[ "$current_branch" != "$CANONICAL_TRUNK" ]]; then
      echo "⚠️  $repo_path: on '$current_branch' (expected '$CANONICAL_TRUNK') — keep canonical clones on trunk for automation"
      repo_warns=$((repo_warns+1))
    else
      echo "✅ $repo_path: on $CANONICAL_TRUNK"
    fi

    if [[ -n "$(git -C "$repo_path" status --porcelain=v1 2>/dev/null || true)" ]]; then
      echo "⚠️  $repo_path: working tree dirty — ru/dx automation will refuse to fast-forward"
      repo_warns=$((repo_warns+1))
    fi
  done
else
  echo "⚠️  Canonical repo list not found (expected: $CANONICAL_TARGETS_SH)"
  repo_warns=$((repo_warns+1))
fi

if [[ "$repo_warns" -gt 0 ]]; then
  missing_optional=$((missing_optional+repo_warns))
fi

echo ""
echo "OPTIONAL CLI tools:"

# Railway (per env-sources contract: optional in local dev, required in CI/CD)
# NOTE: Railway hard-fail enforcement is handled by railway-requirements-check.sh
# which is integrated into dx-status.sh. This check is informational only.
if command -v railway >/dev/null 2>&1; then
  echo "✅ railway ($(railway --version 2>/dev/null | head -1 || echo installed))"

  # Check Login Status (optional - may not be logged in during local dev)
  if ! railway whoami >/dev/null 2>&1; then
    echo "⚠️  railway: NOT LOGGED IN (optional for local dev, run 'railway login' when needed)"
    missing_optional=$((missing_optional+1))
  else
    echo "✅ railway: authenticated (interactive session)"
  fi

  # Check Railway Shell Context (RAILWAY_TOKEN - per ENV_SOURCES_CONTRACT.md)
  # This is the explicit token export for CI/CD and automated workflows
  if [[ -n "${RAILWAY_TOKEN:-}" ]]; then
    echo "✅ railway: RAILWAY_TOKEN set (shell context for automated workflows)"
  elif [[ -n "${RAILWAY_PROJECT_ID:-}" ]] || [[ -n "${RAILWAY_ENVIRONMENT:-}" ]]; then
    echo "✅ railway: inside Railway shell context (PROJECT_ID/ENVIRONMENT set)"
  else
    echo "⚠️  railway: NOT IN SHELL (optional for local dev, see ENV_SOURCES_CONTRACT.md)"
    echo "   For CI/CD: export RAILWAY_TOKEN=\$(op item get --vault dev Railway-Delivery --fields label=token)"
    missing_optional=$((missing_optional+1))
  fi
else
  echo "⚠️  railway (not installed) — optional"
  missing_optional=$((missing_optional+1))
fi

if command -v gh >/dev/null 2>&1; then
  echo "✅ gh ($(gh --version 2>/dev/null | head -1 || echo installed))"
else
  echo "⚠️  gh (not installed) — optional"
  missing_optional=$((missing_optional+1))
fi

echo ""
echo "SLACK MCP configuration (canonical IDEs):"

# Check for Slack MCP in canonical IDE configs
# Canonical IDEs: antigravity, claude-code, codex-cli, opencode
SLACK_MCP_CONFIGURED=false

# Check antigravity config
if [[ -f "$HOME/.gemini/antigravity/mcp_config.json" ]]; then
  if grep -q '"slack"' "$HOME/.gemini/antigravity/mcp_config.json" 2>/dev/null || \
     grep -q 'slack-mcp-server' "$HOME/.gemini/antigravity/mcp_config.json" 2>/dev/null; then
    echo "✅ antigravity: Slack MCP configured"
    SLACK_MCP_CONFIGURED=true
  fi
fi

# Check claude-code config
if [[ -f "$HOME/.claude.json" ]]; then
  if grep -q '"slack"' "$HOME/.claude.json" 2>/dev/null || \
     grep -q 'slack-mcp-server' "$HOME/.claude.json" 2>/dev/null; then
    echo "✅ claude-code: Slack MCP configured"
    SLACK_MCP_CONFIGURED=true
  fi
fi

# Check codex-cli config
if [[ -f "$HOME/.codex/config.toml" ]]; then
  if grep -q "slack" "$HOME/.codex/config.toml" 2>/dev/null || \
     grep -q "slack-mcp-server" "$HOME/.codex/config.toml" 2>/dev/null; then
    echo "✅ codex-cli: Slack MCP configured"
    SLACK_MCP_CONFIGURED=true
  fi
fi

# Check opencode config
if [[ -f "$HOME/.opencode/config.json" ]]; then
  if grep -q '"slack"' "$HOME/.opencode/config.json" 2>/dev/null || \
     grep -q 'slack-mcp-server' "$HOME/.opencode/config.json" 2>/dev/null; then
    echo "✅ opencode: Slack MCP configured"
    SLACK_MCP_CONFIGURED=true
  fi
fi

if [[ "$SLACK_MCP_CONFIGURED" == "false" ]]; then
  echo "⚠️  Slack MCP not configured in any canonical IDE"
  echo "   Run: ~/agent-skills/scripts/setup-slack-mcp.sh --all"
  missing_optional=$((missing_optional+1))
fi

echo ""
echo "SSH Key Doctor:"
if [[ -x "$HOME/agent-skills/ssh-key-doctor/check.sh" ]]; then
  echo "✅ ssh-key-doctor installed"
else
  echo "⚠️  ssh-key-doctor not installed — optional"
  echo "   Run: ~/agent-skills/ssh-key-doctor/check.sh"
  missing_optional=$((missing_optional+1))
fi

echo ""
if [[ "$missing_required" -eq 0 ]]; then
  if [[ "$missing_optional" -eq 0 ]]; then
    echo "✅ mcp-doctor: healthy (all required + optional items present)"
  else
    echo "✅ mcp-doctor: healthy (required items present, $missing_optional optional items missing)"
  fi
  exit 0
fi

echo "❌ mcp-doctor: $missing_required REQUIRED items missing"
if [[ "$missing_optional" -gt 0 ]]; then
  echo "⚠️  Also missing $missing_optional optional items"
fi
echo ""
echo "Setup instructions: $SKILLS_DIR/mcp-doctor/SKILL.md"
if [[ "$STRICT" == "1" ]]; then
  exit 1
fi
exit 0
