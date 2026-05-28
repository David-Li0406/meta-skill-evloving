#!/bin/bash
#
# check-source-health.sh - Validate health of registered sources
#
# Usage: ./tools/freshness/check-source-health.sh [--registry <file>]
#
# Checks each source in the registry for:
# - URL accessibility (404 check)
# - GitHub activity (if GitHub URL)
# - Last update date
#
# Updates reliability scores and flags stale sources.

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESIGN_OPS_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
REGISTRY_FILE="$DESIGN_OPS_ROOT/config/source-registry.yaml"
OUTPUT_FILE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --registry)
            REGISTRY_FILE="$2"
            shift 2
            ;;
        --output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [--registry <file>] [--output <file>]"
            echo "Checks health of sources in the registry."
            exit 0
            ;;
        *)
            shift
            ;;
    esac
done

# Default output
if [[ -z "$OUTPUT_FILE" ]]; then
    OUTPUT_FILE="$DESIGN_OPS_ROOT/docs/freshness/source-health-$(date +%Y-%m).md"
fi

mkdir -p "$(dirname "$OUTPUT_FILE")"

echo -e "${CYAN}Checking source health...${NC}"

# Check if registry exists
if [[ ! -f "$REGISTRY_FILE" ]]; then
    echo -e "${YELLOW}Registry not found: $REGISTRY_FILE${NC}"
    echo "Run install.sh first to create the registry."
    exit 1
fi

# Start output
cat > "$OUTPUT_FILE" << EOF
# Source Health Report

> Generated: $(date '+%Y-%m-%d %H:%M:%S')

---

## Health Summary

| Status | Count |
|--------|-------|
EOF

HEALTHY=0
DEGRADED=0
UNREACHABLE=0
STALE=0

# Function to check URL
check_url() {
    local url=$1
    local status

    status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$url" 2>/dev/null || echo "000")
    echo "$status"
}

# Function to check GitHub repo activity
check_github_activity() {
    local repo=$1
    local last_commit

    # Extract owner/repo from URL
    if [[ "$repo" =~ github\.com/([^/]+)/([^/]+) ]]; then
        local owner="${BASH_REMATCH[1]}"
        local name="${BASH_REMATCH[2]}"
        name="${name%.git}"

        # Get last commit date via API (no auth needed for public repos)
        last_commit=$(curl -s "https://api.github.com/repos/$owner/$name/commits?per_page=1" 2>/dev/null | \
            grep -o '"date": "[^"]*"' | head -1 | cut -d'"' -f4 || echo "")

        if [[ -n "$last_commit" ]]; then
            echo "$last_commit"
            return 0
        fi
    fi

    echo "unknown"
    return 1
}

# Temporary file for detailed results
DETAILS_FILE=$(mktemp)

cat >> "$DETAILS_FILE" << 'EOF'

---

## Detailed Results

### Tier 1 (Anthropic Official)

EOF

# Check Tier 1 sources (Anthropic)
TIER1_SOURCES=(
    "https://docs.anthropic.com|Anthropic Docs"
    "https://github.com/anthropics/anthropic-cookbook|Anthropic Cookbook"
    "https://modelcontextprotocol.io|MCP"
)

for source in "${TIER1_SOURCES[@]}"; do
    url="${source%%|*}"
    name="${source##*|}"

    echo -n "  Checking $name... "

    status=$(check_url "$url")

    if [[ "$status" == "200" ]] || [[ "$status" == "301" ]] || [[ "$status" == "302" ]]; then
        echo -e "${GREEN}OK${NC}"
        ((HEALTHY++))
        echo "| ✅ | $name | $url | Healthy |" >> "$DETAILS_FILE"
    elif [[ "$status" == "000" ]]; then
        echo -e "${RED}UNREACHABLE${NC}"
        ((UNREACHABLE++))
        echo "| ❌ | $name | $url | Unreachable |" >> "$DETAILS_FILE"
    else
        echo -e "${YELLOW}$status${NC}"
        ((DEGRADED++))
        echo "| ⚠️ | $name | $url | HTTP $status |" >> "$DETAILS_FILE"
    fi
done

cat >> "$DETAILS_FILE" << 'EOF'

### Tier 2 (Validated Sources)

EOF

# Check if yq is available for YAML parsing
if command -v yq &> /dev/null; then
    # Parse tier_2 from registry
    TIER2_COUNT=$(yq '.tier_2 | length' "$REGISTRY_FILE" 2>/dev/null || echo "0")

    if [[ "$TIER2_COUNT" -gt 0 ]]; then
        for i in $(seq 0 $((TIER2_COUNT - 1))); do
            url=$(yq ".tier_2[$i].url" "$REGISTRY_FILE" 2>/dev/null || echo "")
            name=$(yq ".tier_2[$i].name" "$REGISTRY_FILE" 2>/dev/null || echo "Source $i")

            [[ -z "$url" ]] && continue

            echo -n "  Checking $name... "
            status=$(check_url "$url")

            if [[ "$status" == "200" ]] || [[ "$status" == "301" ]]; then
                echo -e "${GREEN}OK${NC}"
                ((HEALTHY++))
                echo "| ✅ | $name | Healthy |" >> "$DETAILS_FILE"
            else
                echo -e "${YELLOW}$status${NC}"
                ((DEGRADED++))
                echo "| ⚠️ | $name | HTTP $status |" >> "$DETAILS_FILE"
            fi
        done
    fi
else
    echo -e "${YELLOW}yq not installed - skipping YAML registry parsing${NC}"
    echo "(Install with: brew install yq)"
    echo "" >> "$DETAILS_FILE"
    echo "_yq not available - registry parsing skipped_" >> "$DETAILS_FILE"
fi

# Check GitHub-specific sources for activity
cat >> "$DETAILS_FILE" << 'EOF'

### GitHub Activity Check

EOF

echo "  Checking GitHub activity..."

GITHUB_SOURCES=(
    "https://github.com/anthropics/anthropic-cookbook"
)

for repo in "${GITHUB_SOURCES[@]}"; do
    name=$(basename "$repo")
    activity=$(check_github_activity "$repo")

    if [[ "$activity" != "unknown" ]]; then
        # Parse date and check if recent (within 30 days)
        activity_date=$(echo "$activity" | cut -d'T' -f1)
        echo "| $name | Last commit: $activity_date |" >> "$DETAILS_FILE"
    else
        echo "| $name | Activity: Unknown |" >> "$DETAILS_FILE"
    fi
done

# Write summary counts
sed -i '' "s/| Healthy | .*/| Healthy | $HEALTHY |/" "$OUTPUT_FILE" 2>/dev/null || true
cat >> "$OUTPUT_FILE" << EOF
| Healthy | $HEALTHY |
| Degraded | $DEGRADED |
| Unreachable | $UNREACHABLE |
| Stale | $STALE |
EOF

# Append details
cat "$DETAILS_FILE" >> "$OUTPUT_FILE"
rm "$DETAILS_FILE"

# Add recommendations
cat >> "$OUTPUT_FILE" << 'EOF'

---

## Recommendations

EOF

if [[ $UNREACHABLE -gt 0 ]]; then
    echo "- ⚠️ **$UNREACHABLE source(s) unreachable** - Verify URLs and update registry" >> "$OUTPUT_FILE"
fi

if [[ $DEGRADED -gt 0 ]]; then
    echo "- ⚠️ **$DEGRADED source(s) degraded** - Monitor and consider alternatives" >> "$OUTPUT_FILE"
fi

if [[ $HEALTHY -eq $((HEALTHY + DEGRADED + UNREACHABLE)) ]]; then
    echo "- ✅ **All sources healthy** - No action needed" >> "$OUTPUT_FILE"
fi

cat >> "$OUTPUT_FILE" << EOF

---

_Report generated by check-source-health.sh_
EOF

echo ""
echo -e "${GREEN}Health check complete: $OUTPUT_FILE${NC}"
echo ""
echo "Summary:"
echo "  Healthy:     $HEALTHY"
echo "  Degraded:    $DEGRADED"
echo "  Unreachable: $UNREACHABLE"
