#!/usr/bin/env bash
set -euo pipefail

# Usage: generate-validation-report.sh <validation-output-file>
# Generates a markdown validation report from validation results

VALIDATION_OUTPUT="${1:-/dev/stdin}"
TODAY=$(date +%Y-%m-%d)

cat <<EOF
# Design Documentation Validation Report

**Date:** $TODAY

## Validation Results

EOF

# Read validation results and format
if [[ -f "$VALIDATION_OUTPUT" ]]; then
  cat "$VALIDATION_OUTPUT"
elif [[ "$VALIDATION_OUTPUT" == "/dev/stdin" ]]; then
  cat
else
  echo "No validation results found"
fi

cat <<'EOF'

## Next Steps

- Fix validation errors before merging
- Update design docs to match current codebase state
- Run \`/design-validate\` locally to verify changes

EOF
