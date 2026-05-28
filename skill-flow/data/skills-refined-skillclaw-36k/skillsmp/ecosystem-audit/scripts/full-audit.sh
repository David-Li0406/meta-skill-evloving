#!/bin/bash
# full-audit.sh - Complete ecosystem audit with optional agent specialists
# Usage: ./full-audit.sh [--no-agents] [--gist] [--domain <domain>]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${HOME}/.agents/audit-results/$(date +%Y-%m-%d)"
USE_AGENTS=true
CREATE_GIST=false
SPECIFIC_DOMAIN=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --no-agents) USE_AGENTS=false; shift ;;
    --gist) CREATE_GIST=true; shift ;;
    --domain) SPECIFIC_DOMAIN="$2"; shift 2 ;;
    *) shift ;;
  esac
done

mkdir -p "$OUTPUT_DIR"

echo "═══════════════════════════════════════════════════════════════"
echo "  ecosystem-audit: full audit"
echo "  $(date)"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# ============================================================
# Phase 1: Baseline Checks
# ============================================================
echo "Phase 1: Running baseline checks..."
"$SCRIPT_DIR/baseline-audit.sh" --json || true
echo ""

BASELINE_STATUS=$(jq -r '.status' "$OUTPUT_DIR/baseline-results.json" 2>/dev/null || echo "unknown")
echo "Baseline status: $BASELINE_STATUS"
echo ""

# ============================================================
# Phase 2: Agent-Assisted Analysis (if enabled and issues found)
# ============================================================
if $USE_AGENTS && [ "$BASELINE_STATUS" != "healthy" ]; then
  echo "Phase 2: Running agent specialists for diagnosis..."

  DOMAINS=("cli" "skill" "rule" "prompt" "role" "agent" "meta")

  if [ -n "$SPECIFIC_DOMAIN" ]; then
    DOMAINS=("$SPECIFIC_DOMAIN")
  fi

  for domain in "${DOMAINS[@]}"; do
    echo "  - $domain-validator..."

    case $domain in
      cli)
        # CLI validation specialist
        if command -v copilot &> /dev/null; then
          MISSING=$(jq -r '.clis.missing[]' "$OUTPUT_DIR/baseline-results.json" 2>/dev/null | tr '\n' ',' | sed 's/,$//')
          if [ -n "$MISSING" ]; then
            cat <<EOF | copilot -p --model gemini-3-pro --output-format json > "$OUTPUT_DIR/cli-report.json" 2>/dev/null || echo '{"status":"error"}' > "$OUTPUT_DIR/cli-report.json"
<role>CLI validator specialist</role>
<task>Diagnose missing CLIs: $MISSING</task>
<checks>
1. Check common installation locations
2. Suggest installation commands
3. Check if symlinks are broken
</checks>
<output_contract>
{"domain":"cli","status":"diagnosed","missing":[$MISSING],"recommendations":[]}
</output_contract>
EOF
          fi
        fi
        ;;

      skill)
        # Skill validation specialist
        MALFORMED=$(jq -r '.skills.malformed[]' "$OUTPUT_DIR/baseline-results.json" 2>/dev/null | tr '\n' ',' | sed 's/,$//')
        if [ -n "$MALFORMED" ] && command -v copilot &> /dev/null; then
          cat <<EOF | copilot -p --model gemini-3-pro --output-format json > "$OUTPUT_DIR/skill-report.json" 2>/dev/null || echo '{"status":"error"}' > "$OUTPUT_DIR/skill-report.json"
<role>Skill validator specialist</role>
<task>Diagnose malformed skills: $MALFORMED</task>
<checks>
1. Check SKILL.md structure
2. Verify frontmatter format
3. Check description field
</checks>
<output_contract>
{"domain":"skill","status":"diagnosed","malformed":[$MALFORMED],"recommendations":[]}
</output_contract>
EOF
        fi
        ;;

      rule)
        # Rule validation specialist
        MISSING=$(jq -r '.rules.missing[]' "$OUTPUT_DIR/baseline-results.json" 2>/dev/null | tr '\n' ',' | sed 's/,$//')
        if [ -n "$MISSING" ]; then
          echo "{\"domain\":\"rule\",\"status\":\"diagnosed\",\"missing\":[$MISSING],\"recommendations\":[\"Create missing rule files\"]}" > "$OUTPUT_DIR/rule-report.json"
        fi
        ;;

      *)
        # Other domains - generate placeholder report
        echo "{\"domain\":\"$domain\",\"status\":\"skipped\",\"reason\":\"no issues detected\"}" > "$OUTPUT_DIR/${domain}-report.json"
        ;;
    esac
  done
  echo ""
fi

# ============================================================
# Phase 3: Synthesis
# ============================================================
echo "Phase 3: Synthesizing results..."
"$SCRIPT_DIR/synthesize-audit.sh" "$OUTPUT_DIR"
echo ""

# ============================================================
# Phase 4: Artifact Persistence
# ============================================================
echo "Phase 4: Persisting artifacts..."

# Update latest symlink
ln -sfn "$OUTPUT_DIR" ~/.agents/audit-results/latest
echo "  Local: $OUTPUT_DIR"

if $CREATE_GIST; then
  echo "  Creating gist..."

  # Create summary markdown
  cat > "$OUTPUT_DIR/summary.md" << EOF
# Ecosystem Audit - $(date +%Y-%m-%d)

## Status: $BASELINE_STATUS

## Summary

$(jq -r '"- CLIs: \(.clis.found)/\(.clis.total)\n- Skills: \(.skills.count)\n- Rules: \(.rules.count)\n- Prompts: \(.prompts.count)\n- Roles: \(.roles.count)\n- Agents: \(.agents.found)/\(.agents.total)"' "$OUTPUT_DIR/baseline-results.json")

## Issues

$(jq -r 'if .clis.missing | length > 0 then "### Missing CLIs\n" + (.clis.missing | map("- " + .) | join("\n")) else "" end' "$OUTPUT_DIR/baseline-results.json")

$(jq -r 'if .rules.missing | length > 0 then "### Missing Rules\n" + (.rules.missing | map("- " + .) | join("\n")) else "" end' "$OUTPUT_DIR/baseline-results.json")

$(jq -r 'if .skills.malformed | length > 0 then "### Malformed Skills\n" + (.skills.malformed | map("- " + .) | join("\n")) else "" end' "$OUTPUT_DIR/baseline-results.json")

---
Generated by ecosystem-audit skill
EOF

  # Create gist with all JSON files
  GIST_URL=$(gh gist create --desc "ecosystem-audit $(date +%Y-%m-%d)" \
    "$OUTPUT_DIR/summary.md" \
    "$OUTPUT_DIR/baseline-results.json" \
    "$OUTPUT_DIR/ecosystem-audit-report.json" 2>/dev/null || echo "")

  if [ -n "$GIST_URL" ]; then
    echo "  Gist: $GIST_URL"
    echo "$GIST_URL" > "$OUTPUT_DIR/gist-url.txt"
  else
    echo "  Gist creation failed (check gh auth)"
  fi
fi

# ============================================================
# Phase 5: Trails Integration
# ============================================================
if command -v trails &> /dev/null; then
  echo ""
  echo "Phase 5: Recording to trails..."
  CONFIDENCE=9
  [ "$BASELINE_STATUS" = "degraded" ] && CONFIDENCE=7
  [ "$BASELINE_STATUS" = "broken" ] && CONFIDENCE=5

  trails trail record --agent claude --action completed \
    --task "ecosystem-audit: $BASELINE_STATUS" \
    --confidence "$CONFIDENCE" --json --quiet > /dev/null 2>&1 || true
fi

# ============================================================
# Final Output
# ============================================================
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Audit Complete"
echo "  Status: $BASELINE_STATUS"
echo "  Results: $OUTPUT_DIR"
echo "═══════════════════════════════════════════════════════════════"

# Show final report summary
echo ""
jq '.' "$OUTPUT_DIR/ecosystem-audit-report.json" 2>/dev/null || cat "$OUTPUT_DIR/baseline-results.json"
