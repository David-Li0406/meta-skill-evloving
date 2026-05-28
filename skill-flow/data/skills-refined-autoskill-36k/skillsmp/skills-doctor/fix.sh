#!/usr/bin/env bash
set -euo pipefail

SKILLS_DIR="${AGENT_SKILLS_DIR:-$HOME/.agent/skills}"

if [[ ! -d "$SKILLS_DIR/.git" ]]; then
  echo "❌ $SKILLS_DIR is not a git checkout"
  echo "   Fix: install agent-skills to ~/.agent/skills"
  exit 1
fi

echo "🔧 Updating agent-skills in: $SKILLS_DIR"
git -C "$SKILLS_DIR" pull --ff-only
echo "✅ Updated."
echo ""
echo "Re-run:"
echo "  $SKILLS_DIR/skills-doctor/check.sh"

