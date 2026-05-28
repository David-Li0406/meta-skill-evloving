#!/usr/bin/env bash
set -euo pipefail

echo "🔎 skills-doctor — checking required skills"

SKILLS_DIR="${AGENT_SKILLS_DIR:-$HOME/.agent/skills}"
PROFILE="${SKILLS_DOCTOR_PROFILE:-}"

if [[ ! -d "$SKILLS_DIR" ]]; then
  echo "❌ skills dir not found: $SKILLS_DIR"
  echo "   Fix: set AGENT_SKILLS_DIR or install agent-skills into ~/.agent/skills"
  exit 1
fi

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
REMOTE_URL="$(git -C "$REPO_ROOT" remote get-url origin 2>/dev/null || true)"

if [[ -z "$PROFILE" ]]; then
  case "$REMOTE_URL" in
    *stars-end/prime-radiant-ai*|*stars-end/prime-radiant-ai.git*)
      PROFILE="prime-radiant-ai"
      ;;
    *stars-end/affordabot*|*stars-end/affordabot.git*)
      PROFILE="affordabot"
      ;;
    *stars-end/llm-common*|*stars-end/llm-common.git*)
      PROFILE="llm-common"
      ;;
    *)
      PROFILE="$(basename "$REPO_ROOT")"
      ;;
  esac
fi

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROFILES_DIR="$HERE/../skill-profiles"
PROFILE_FILE_JSON="$PROFILES_DIR/${PROFILE}.json"

if [[ ! -f "$PROFILE_FILE_JSON" ]]; then
  echo "⚠️  no profile found for: $PROFILE"
  echo "   Looked for: $PROFILE_FILE_JSON"
  echo "   Tip: set SKILLS_DOCTOR_PROFILE=prime-radiant-ai|affordabot|llm-common"
  exit 0
fi

REQ=$(python3 - "$PROFILE_FILE_JSON" <<'PY'
import json,sys
path = sys.argv[1]
with open(path, "r", encoding="utf-8") as f:
  data = json.load(f)
skills = []
for key in ("required", "recommended"):
  skills.extend(data.get(key, []))
skills = [s for s in skills if isinstance(s, str) and s.strip()]
print("\n".join(dict.fromkeys(skills)))
PY
)

MISSING=0
while IFS= read -r skill; do
  [[ -z "$skill" ]] && continue
  if [[ -d "$SKILLS_DIR/$skill" ]]; then
    echo "✅ $skill"
  else
    echo "❌ missing: $skill"
    MISSING=$((MISSING + 1))
  fi
done <<< "$REQ"

if [[ $MISSING -eq 0 ]]; then
  echo "✅ skills-doctor: all required skills present ($PROFILE)"
  exit 0
fi

echo ""
echo "❌ skills-doctor: $MISSING missing skills ($PROFILE)"
echo "Fix:"
echo "  cd \"$SKILLS_DIR\" && git pull"
exit 1

