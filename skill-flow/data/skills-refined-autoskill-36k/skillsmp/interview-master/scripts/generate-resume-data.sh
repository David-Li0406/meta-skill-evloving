#!/usr/bin/env bash

# generate-resume-data.sh - Aggregate all analysis results
# Usage: ./generate-resume-data.sh <author> <repo-path>

set -euo pipefail

GREEN='\033[0;32m'
NC='\033[0m'

if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <author> <repo-path>" >&2
    exit 1
fi

AUTHOR="$1"
REPO_PATH="$2"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${GREEN}Generating comprehensive resume data...${NC}" >&2

# Run all analysis scripts
COMMITS_JSON=$("$SCRIPT_DIR/analyze-commits.sh" "$AUTHOR" "$REPO_PATH" 2>/dev/null)
TECH_JSON=$("$SCRIPT_DIR/extract-tech-stack.sh" "$REPO_PATH" "$AUTHOR" 2>/dev/null)
IMPACT_JSON=$(python3 "$SCRIPT_DIR/calculate-impact.py" "$REPO_PATH" "$AUTHOR" 2>/dev/null)

# Combine results (simplified version - in production use jq for proper merging)
cat <<EOF
{
  "commits_analysis": $COMMITS_JSON,
  "tech_stack": $TECH_JSON,
  "impact_metrics": $IMPACT_JSON,
  "generated_at": "$(date -Iseconds)"
}
EOF

echo -e "${GREEN}✓ Resume data generation complete!${NC}" >&2
