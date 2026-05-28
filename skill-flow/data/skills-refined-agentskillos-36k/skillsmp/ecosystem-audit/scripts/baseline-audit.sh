#!/bin/bash
# baseline-audit.sh - Deterministic ecosystem health checks
# Usage: ./baseline-audit.sh [--quick] [--json]

set -euo pipefail

QUICK_MODE=false
JSON_OUTPUT=false
OUTPUT_DIR="${HOME}/.agents/audit-results/$(date +%Y-%m-%d)"

while [[ $# -gt 0 ]]; do
  case $1 in
    --quick) QUICK_MODE=true; shift ;;
    --json) JSON_OUTPUT=true; shift ;;
    *) shift ;;
  esac
done

# Initialize counters
CLI_FOUND=0
CLI_MISSING=0
SKILL_COUNT=0
SKILL_MALFORMED=0
RULE_COUNT=0
RULE_MISSING=0
PROMPT_COUNT=0
ROLE_COUNT=0
AGENT_FOUND=0
AGENT_MISSING=0

MISSING_CLIS=()
MISSING_RULES=()
MALFORMED_SKILLS=()
MISSING_AGENTS=()

# ============================================================
# CLI Presence Checks
# ============================================================
CLIS=(outline layer verify agents trails mem slack linear format prompts roles epub)

for cli in "${CLIS[@]}"; do
  if command -v "$cli" &> /dev/null; then
    ((CLI_FOUND++))
    if ! $QUICK_MODE; then
      echo "✓ $cli"
    fi
  else
    ((CLI_MISSING++))
    MISSING_CLIS+=("$cli")
    if ! $QUICK_MODE; then
      echo "✗ $cli NOT ON PATH"
    fi
  fi
done

# ============================================================
# Agent CLI Checks
# ============================================================
AGENT_CLIS=(claude codex copilot)

for agent in "${AGENT_CLIS[@]}"; do
  if command -v "$agent" &> /dev/null; then
    ((AGENT_FOUND++))
    if ! $QUICK_MODE; then
      VERSION=$("$agent" --version 2>/dev/null | head -1 || echo "unknown")
      echo "✓ $agent ($VERSION)"
    fi
  else
    ((AGENT_MISSING++))
    MISSING_AGENTS+=("$agent")
    if ! $QUICK_MODE; then
      echo "✗ $agent NOT ON PATH"
    fi
  fi
done

# ============================================================
# Skill Structure Checks
# ============================================================
# Skip non-skill directories (components, runbooks are supporting dirs)
SKIP_DIRS=("components" "runbooks")

for skill_dir in ~/.agents/skills/*/; do
  if [ -d "$skill_dir" ]; then
    skill_name=$(basename "$skill_dir")
    # Skip known non-skill directories
    if [[ " ${SKIP_DIRS[*]} " =~ " ${skill_name} " ]]; then
      continue
    fi
    if [ -f "$skill_dir/SKILL.md" ]; then
      ((SKILL_COUNT++))
      # Check frontmatter
      if ! head -1 "$skill_dir/SKILL.md" | grep -q "^---"; then
        ((SKILL_MALFORMED++))
        MALFORMED_SKILLS+=("$skill_name (missing frontmatter)")
      fi
    else
      ((SKILL_MALFORMED++))
      MALFORMED_SKILLS+=("$skill_name (no SKILL.md)")
    fi
  fi
done

# ============================================================
# Rule File Checks
# ============================================================
RULE_COUNT=$(ls ~/.agents/rules/*.md 2>/dev/null | wc -l | tr -d ' ')

# Check which CLIs have rule files
for cli in "${CLIS[@]}"; do
  if [ ! -f ~/.agents/rules/"$cli".md ]; then
    ((RULE_MISSING++))
    MISSING_RULES+=("$cli.md")
  fi
done

# ============================================================
# Prompts Check
# ============================================================
if command -v prompts &> /dev/null; then
  PROMPT_COUNT=$(prompts commands list --json --quiet 2>/dev/null | jq length 2>/dev/null || echo "0")
fi

# ============================================================
# Roles Check
# ============================================================
if command -v roles &> /dev/null; then
  ROLE_COUNT=$(roles list --json --quiet 2>/dev/null | jq length 2>/dev/null || echo "0")
fi

# ============================================================
# Determine Overall Status
# ============================================================
STATUS="healthy"
if [ $CLI_MISSING -gt 0 ] || [ $AGENT_MISSING -gt 0 ]; then
  STATUS="degraded"
fi
if [ $CLI_MISSING -gt 2 ] || [ $AGENT_MISSING -gt 1 ]; then
  STATUS="broken"
fi

# ============================================================
# Output
# ============================================================
if $QUICK_MODE; then
  echo "CLIs: $CLI_FOUND/${#CLIS[@]} $([ $CLI_MISSING -eq 0 ] && echo '✓' || echo '✗')"
  echo "Skills: $SKILL_COUNT found $([ $SKILL_MALFORMED -eq 0 ] && echo '✓' || echo "($SKILL_MALFORMED malformed)")"
  echo "Rules: $RULE_COUNT found $([ $RULE_MISSING -eq 0 ] && echo '✓' || echo "($RULE_MISSING missing)")"
  echo "Prompts: $PROMPT_COUNT commands $([ $PROMPT_COUNT -gt 0 ] && echo '✓' || echo '✗')"
  echo "Roles: $ROLE_COUNT personas $([ $ROLE_COUNT -gt 0 ] && echo '✓' || echo '✗')"
  echo "Agents: $AGENT_FOUND/${#AGENT_CLIS[@]} $([ $AGENT_MISSING -eq 0 ] && echo '✓' || echo '✗')"
  echo ""
  echo "Status: $STATUS"
fi

if $JSON_OUTPUT; then
  mkdir -p "$OUTPUT_DIR"
  cat > "$OUTPUT_DIR/baseline-results.json" << EOF
{
  "audit_date": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "status": "$STATUS",
  "clis": {
    "found": $CLI_FOUND,
    "total": ${#CLIS[@]},
    "missing": $(if [ ${#MISSING_CLIS[@]} -eq 0 ]; then echo "[]"; else printf '%s\n' "${MISSING_CLIS[@]}" | jq -R . | jq -s .; fi)
  },
  "skills": {
    "count": $SKILL_COUNT,
    "malformed": $(if [ ${#MALFORMED_SKILLS[@]} -eq 0 ]; then echo "[]"; else printf '%s\n' "${MALFORMED_SKILLS[@]}" | jq -R . | jq -s .; fi)
  },
  "rules": {
    "count": $RULE_COUNT,
    "missing": $(if [ ${#MISSING_RULES[@]} -eq 0 ]; then echo "[]"; else printf '%s\n' "${MISSING_RULES[@]}" | jq -R . | jq -s .; fi)
  },
  "prompts": {
    "count": $PROMPT_COUNT
  },
  "roles": {
    "count": $ROLE_COUNT
  },
  "agents": {
    "found": $AGENT_FOUND,
    "total": ${#AGENT_CLIS[@]},
    "missing": $(if [ ${#MISSING_AGENTS[@]} -eq 0 ]; then echo "[]"; else printf '%s\n' "${MISSING_AGENTS[@]}" | jq -R . | jq -s .; fi)
  }
}
EOF
  echo "Results written to: $OUTPUT_DIR/baseline-results.json"

  # Update latest symlink
  ln -sfn "$OUTPUT_DIR" ~/.agents/audit-results/latest
fi

# Exit with appropriate code
if [ "$STATUS" = "healthy" ]; then
  exit 0
elif [ "$STATUS" = "degraded" ]; then
  exit 1
else
  exit 2
fi
