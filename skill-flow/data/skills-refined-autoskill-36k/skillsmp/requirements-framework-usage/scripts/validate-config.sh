#!/bin/bash
# Validate Requirements Framework Configuration
#
# Checks YAML syntax and required fields in requirements.yaml files.
# Usage: ./validate-config.sh [path-to-config]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default paths to check
CONFIG_PATHS=(
    ".claude/requirements.yaml"
    ".claude/requirements.local.yaml"
    "$HOME/.claude/requirements.yaml"
)

# If path provided, use that instead
if [ -n "$1" ]; then
    CONFIG_PATHS=("$1")
fi

echo "🔍 Validating Requirements Framework Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

errors=0
warnings=0

for config_path in "${CONFIG_PATHS[@]}"; do
    if [ -f "$config_path" ]; then
        echo "📄 Checking: $config_path"

        # Check YAML syntax
        if python3 -c "import yaml; yaml.safe_load(open('$config_path'))" 2>/dev/null; then
            echo -e "   ${GREEN}✓${NC} YAML syntax valid"
        else
            echo -e "   ${RED}✗${NC} YAML syntax error"
            python3 -c "import yaml; yaml.safe_load(open('$config_path'))" 2>&1 | sed 's/^/   /'
            ((errors++))
            continue
        fi

        # Check for common issues
        content=$(cat "$config_path")

        # Check version field
        if echo "$content" | grep -q "^version:"; then
            echo -e "   ${GREEN}✓${NC} Version field present"
        else
            echo -e "   ${YELLOW}⚠${NC} No version field (recommended: version: \"1.0\")"
            ((warnings++))
        fi

        # Check enabled field
        if echo "$content" | grep -q "^enabled:"; then
            echo -e "   ${GREEN}✓${NC} Enabled field present"
        else
            echo -e "   ${YELLOW}⚠${NC} No top-level enabled field"
            ((warnings++))
        fi

        # Check requirements section
        if echo "$content" | grep -q "^requirements:"; then
            echo -e "   ${GREEN}✓${NC} Requirements section present"

            # Count requirements
            req_count=$(echo "$content" | grep -E "^  [a-z_]+:" | wc -l | tr -d ' ')
            echo "   ℹ️  Found $req_count requirement(s)"
        else
            echo -e "   ${YELLOW}⚠${NC} No requirements section"
            ((warnings++))
        fi

        echo ""
    fi
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $errors -eq 0 ] && [ $warnings -eq 0 ]; then
    echo -e "${GREEN}✅ All configurations valid${NC}"
    exit 0
elif [ $errors -eq 0 ]; then
    echo -e "${YELLOW}⚠️  $warnings warning(s) found${NC}"
    exit 0
else
    echo -e "${RED}❌ $errors error(s), $warnings warning(s)${NC}"
    exit 1
fi
