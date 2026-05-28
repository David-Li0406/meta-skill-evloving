#!/bin/bash
# synthesize-audit.sh - Aggregate specialist reports into final audit report
# Usage: ./synthesize-audit.sh <output_dir>

set -euo pipefail

OUTPUT_DIR="${1:-${HOME}/.agents/audit-results/$(date +%Y-%m-%d)}"

if [ ! -f "$OUTPUT_DIR/baseline-results.json" ]; then
  echo "Error: baseline-results.json not found in $OUTPUT_DIR"
  exit 1
fi

# Read baseline results
BASELINE=$(cat "$OUTPUT_DIR/baseline-results.json")

# Extract baseline data
AUDIT_DATE=$(echo "$BASELINE" | jq -r '.audit_date')
STATUS=$(echo "$BASELINE" | jq -r '.status')
CLI_FOUND=$(echo "$BASELINE" | jq -r '.clis.found')
CLI_TOTAL=$(echo "$BASELINE" | jq -r '.clis.total')
CLI_MISSING=$(echo "$BASELINE" | jq -c '.clis.missing')
SKILL_COUNT=$(echo "$BASELINE" | jq -r '.skills.count')
SKILL_MALFORMED=$(echo "$BASELINE" | jq -c '.skills.malformed')
RULE_COUNT=$(echo "$BASELINE" | jq -r '.rules.count')
RULE_MISSING=$(echo "$BASELINE" | jq -c '.rules.missing')
PROMPT_COUNT=$(echo "$BASELINE" | jq -r '.prompts.count')
ROLE_COUNT=$(echo "$BASELINE" | jq -r '.roles.count')
AGENT_FOUND=$(echo "$BASELINE" | jq -r '.agents.found')
AGENT_TOTAL=$(echo "$BASELINE" | jq -r '.agents.total')
AGENT_MISSING=$(echo "$BASELINE" | jq -c '.agents.missing')

# Determine domain statuses
CLI_STATUS="pass"
[ "$(echo "$CLI_MISSING" | jq 'length')" -gt 0 ] && CLI_STATUS="fail"

SKILL_STATUS="pass"
[ "$(echo "$SKILL_MALFORMED" | jq 'length')" -gt 0 ] && SKILL_STATUS="warn"

RULE_STATUS="pass"
[ "$(echo "$RULE_MISSING" | jq 'length')" -gt 0 ] && RULE_STATUS="warn"

PROMPT_STATUS="pass"
[ "$PROMPT_COUNT" -eq 0 ] && PROMPT_STATUS="fail"

ROLE_STATUS="pass"
[ "$ROLE_COUNT" -eq 0 ] && ROLE_STATUS="fail"

AGENT_STATUS="pass"
[ "$(echo "$AGENT_MISSING" | jq 'length')" -gt 0 ] && AGENT_STATUS="fail"

META_STATUS="pass"

# Collect specialist reports if they exist
SPECIALIST_REPORTS=()
for report in "$OUTPUT_DIR"/*-report.json; do
  if [ -f "$report" ] && [ "$(basename "$report")" != "ecosystem-audit-report.json" ]; then
    SPECIALIST_REPORTS+=("$report")
  fi
done

# Generate recommendations based on findings
RECOMMENDATIONS=()

if [ "$CLI_STATUS" = "fail" ]; then
  RECOMMENDATIONS+=("Fix missing CLIs: $(echo "$CLI_MISSING" | jq -r 'join(", ")')")
fi

if [ "$SKILL_STATUS" = "warn" ]; then
  RECOMMENDATIONS+=("Fix malformed skills: $(echo "$SKILL_MALFORMED" | jq -r 'join(", ")')")
fi

if [ "$RULE_STATUS" = "warn" ]; then
  RECOMMENDATIONS+=("Create missing rule files: $(echo "$RULE_MISSING" | jq -r 'join(", ")')")
fi

if [ "$AGENT_STATUS" = "fail" ]; then
  RECOMMENDATIONS+=("Install missing agent CLIs: $(echo "$AGENT_MISSING" | jq -r 'join(", ")')")
fi

# Calculate confidence
CONFIDENCE=9
[ "$STATUS" = "degraded" ] && CONFIDENCE=7
[ "$STATUS" = "broken" ] && CONFIDENCE=5

# Generate final report
RECOMMENDATIONS_JSON=$(printf '%s\n' "${RECOMMENDATIONS[@]:-}" | jq -R . | jq -s .)

cat > "$OUTPUT_DIR/ecosystem-audit-report.json" << EOF
{
  "audit_date": "$AUDIT_DATE",
  "status": "$STATUS",
  "summary": "Ecosystem audit completed. CLIs: $CLI_FOUND/$CLI_TOTAL, Skills: $SKILL_COUNT, Rules: $RULE_COUNT, Prompts: $PROMPT_COUNT, Roles: $ROLE_COUNT, Agents: $AGENT_FOUND/$AGENT_TOTAL",
  "domains": {
    "clis": {
      "status": "$CLI_STATUS",
      "count": $CLI_FOUND,
      "total": $CLI_TOTAL,
      "issues": $CLI_MISSING
    },
    "skills": {
      "status": "$SKILL_STATUS",
      "count": $SKILL_COUNT,
      "issues": $SKILL_MALFORMED
    },
    "rules": {
      "status": "$RULE_STATUS",
      "count": $RULE_COUNT,
      "issues": $RULE_MISSING
    },
    "prompts": {
      "status": "$PROMPT_STATUS",
      "count": $PROMPT_COUNT,
      "issues": []
    },
    "roles": {
      "status": "$ROLE_STATUS",
      "count": $ROLE_COUNT,
      "issues": []
    },
    "agents": {
      "status": "$AGENT_STATUS",
      "count": $AGENT_FOUND,
      "total": $AGENT_TOTAL,
      "issues": $AGENT_MISSING
    },
    "meta": {
      "status": "$META_STATUS",
      "issues": []
    }
  },
  "artifacts": {
    "local_path": "$OUTPUT_DIR"
  },
  "specialist_reports": ${#SPECIALIST_REPORTS[@]},
  "recommendations": $RECOMMENDATIONS_JSON,
  "confidence": $CONFIDENCE
}
EOF

echo "Synthesized report: $OUTPUT_DIR/ecosystem-audit-report.json"
