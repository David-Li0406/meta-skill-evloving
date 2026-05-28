#!/usr/bin/env bash
set -euo pipefail

# Vibe Prescan - Static pattern detection
# Outputs findings to .agents/assessments/

TARGET="${1:-.}"
DATE=$(date +%Y-%m-%d)
OUTPUT_DIR=".agents/assessments"
OUTPUT_FILE="${OUTPUT_DIR}/${DATE}-vibe-prescan.md"

mkdir -p "$OUTPUT_DIR"

# Initialize report
cat > "$OUTPUT_FILE" << EOF
# Vibe Prescan Report

**Date:** ${DATE}
**Target:** ${TARGET}

## Findings

EOF

CRITICAL_COUNT=0
HIGH_COUNT=0
MEDIUM_COUNT=0

# P2: Hardcoded secrets (CRITICAL)
# Uses path-based filtering to exclude test directories (not line content)
echo "### P2: Hardcoded Secrets" >> "$OUTPUT_FILE"
SECRETS=$(grep -rn --include="*.py" --include="*.go" --include="*.ts" --include="*.js" \
    -E "(password|secret|api_key|apikey|token)\s*=\s*['\"][^'\"]+['\"]" "$TARGET" 2>/dev/null | \
    grep -v "/test/" | grep -v "/tests/" | grep -v "_test\." | \
    grep -v "/example/" | grep -v "/examples/" | \
    grep -v "\.example\." | head -20 || true)

if [[ -n "$SECRETS" ]]; then
    echo "**Severity:** CRITICAL" >> "$OUTPUT_FILE"
    echo '```' >> "$OUTPUT_FILE"
    echo "$SECRETS" >> "$OUTPUT_FILE"
    echo '```' >> "$OUTPUT_FILE"
    CRITICAL_COUNT=$((CRITICAL_COUNT + $(echo "$SECRETS" | wc -l)))
else
    echo "None found." >> "$OUTPUT_FILE"
fi
echo "" >> "$OUTPUT_FILE"

# P4: TODO/FIXME (HIGH)
echo "### P4: TODO/FIXME Comments" >> "$OUTPUT_FILE"
TODOS=$(grep -rn --include="*.py" --include="*.go" --include="*.ts" --include="*.js" --include="*.md" \
    -E "(TODO|FIXME|XXX|HACK):" "$TARGET" 2>/dev/null | head -20 || true)

if [[ -n "$TODOS" ]]; then
    echo "**Severity:** HIGH" >> "$OUTPUT_FILE"
    echo '```' >> "$OUTPUT_FILE"
    echo "$TODOS" >> "$OUTPUT_FILE"
    echo '```' >> "$OUTPUT_FILE"
    HIGH_COUNT=$((HIGH_COUNT + $(echo "$TODOS" | wc -l)))
else
    echo "None found." >> "$OUTPUT_FILE"
fi
echo "" >> "$OUTPUT_FILE"

# P5: High complexity functions (HIGH) - Python only
echo "### P5: High Complexity (CC > 10)" >> "$OUTPUT_FILE"
if command -v radon &> /dev/null; then
    COMPLEXITY=$(radon cc "$TARGET" -a -s --min C 2>/dev/null | head -20 || true)
    if [[ -n "$COMPLEXITY" ]]; then
        echo "**Severity:** HIGH" >> "$OUTPUT_FILE"
        echo '```' >> "$OUTPUT_FILE"
        echo "$COMPLEXITY" >> "$OUTPUT_FILE"
        echo '```' >> "$OUTPUT_FILE"
        HIGH_COUNT=$((HIGH_COUNT + $(echo "$COMPLEXITY" | grep -c "^" || echo 0)))
    else
        echo "None found." >> "$OUTPUT_FILE"
    fi
else
    echo "radon not installed - skipping Python complexity check" >> "$OUTPUT_FILE"
fi
echo "" >> "$OUTPUT_FILE"

# P11: Shellcheck violations (HIGH)
echo "### P11: Shellcheck Violations" >> "$OUTPUT_FILE"
if command -v shellcheck &> /dev/null; then
    SHELL_ISSUES=$(find "$TARGET" -name "*.sh" -exec shellcheck -f gcc {} \; 2>/dev/null | head -20 || true)
    if [[ -n "$SHELL_ISSUES" ]]; then
        echo "**Severity:** HIGH" >> "$OUTPUT_FILE"
        echo '```' >> "$OUTPUT_FILE"
        echo "$SHELL_ISSUES" >> "$OUTPUT_FILE"
        echo '```' >> "$OUTPUT_FILE"
        HIGH_COUNT=$((HIGH_COUNT + $(echo "$SHELL_ISSUES" | wc -l)))
    else
        echo "None found." >> "$OUTPUT_FILE"
    fi
else
    echo "shellcheck not installed - skipping" >> "$OUTPUT_FILE"
fi
echo "" >> "$OUTPUT_FILE"

# Summary
cat >> "$OUTPUT_FILE" << EOF
## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | ${CRITICAL_COUNT} |
| HIGH | ${HIGH_COUNT} |
| MEDIUM | ${MEDIUM_COUNT} |

**Gate Status:** $(if [[ $CRITICAL_COUNT -gt 0 ]]; then echo "BLOCKED (${CRITICAL_COUNT} critical)"; else echo "PASS"; fi)
EOF

echo "Prescan complete: $OUTPUT_FILE"
echo ""
cat "$OUTPUT_FILE"

# Exit codes per vibe spec
if [[ $CRITICAL_COUNT -gt 0 ]]; then
    exit 2
elif [[ $HIGH_COUNT -gt 0 ]]; then
    exit 3
else
    exit 0
fi
