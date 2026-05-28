#!/bin/bash
#
# scan-design-ops.sh - Inventory current Design Ops structure
#
# Usage: ./tools/freshness/scan-design-ops.sh [--output <file>]
#
# Generates a markdown summary of all Design Ops components for freshness analysis.

set -euo pipefail

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESIGN_OPS_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
OUTPUT_FILE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [--output <file>]"
            echo "Scans Design Ops structure and generates inventory."
            exit 0
            ;;
        *)
            shift
            ;;
    esac
done

# Default output
if [[ -z "$OUTPUT_FILE" ]]; then
    OUTPUT_FILE="$DESIGN_OPS_ROOT/docs/freshness/current-state.md"
fi

# Ensure output directory exists
mkdir -p "$(dirname "$OUTPUT_FILE")"

echo -e "${CYAN}Scanning Design Ops structure...${NC}"

# Start building output
cat > "$OUTPUT_FILE" << EOF
# Design Ops Current State

> Auto-generated inventory of Design Ops components
> Scanned: $(date '+%Y-%m-%d %H:%M:%S')

---

## Summary

| Component | Count | Last Modified |
|-----------|-------|---------------|
EOF

# Count templates
TEMPLATE_COUNT=$(find "$DESIGN_OPS_ROOT/templates" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
TEMPLATE_MODIFIED=$(find "$DESIGN_OPS_ROOT/templates" -name "*.md" -exec stat -f "%m %N" {} \; 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2- | xargs basename 2>/dev/null || echo "N/A")
echo "| Templates | $TEMPLATE_COUNT | $TEMPLATE_MODIFIED |" >> "$OUTPUT_FILE"

# Count tools
TOOL_COUNT=$(find "$DESIGN_OPS_ROOT/tools" -name "*.sh" 2>/dev/null | wc -l | tr -d ' ')
TOOL_MODIFIED=$(find "$DESIGN_OPS_ROOT/tools" -name "*.sh" -exec stat -f "%m %N" {} \; 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2- | xargs basename 2>/dev/null || echo "N/A")
echo "| Tools | $TOOL_COUNT | $TOOL_MODIFIED |" >> "$OUTPUT_FILE"

# Count examples
EXAMPLE_COUNT=$(find "$DESIGN_OPS_ROOT/examples" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
echo "| Examples | $EXAMPLE_COUNT | - |" >> "$OUTPUT_FILE"

# Count docs
DOC_COUNT=$(find "$DESIGN_OPS_ROOT/docs" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
echo "| Docs | $DOC_COUNT | - |" >> "$OUTPUT_FILE"

# Count invariants
INVARIANT_COUNT=$(find "$DESIGN_OPS_ROOT/invariants" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
echo "| Invariants | $INVARIANT_COUNT | - |" >> "$OUTPUT_FILE"

# Count agents
AGENT_COUNT=$(find "$DESIGN_OPS_ROOT/agents" -name "*.sh" 2>/dev/null | wc -l | tr -d ' ')
echo "| Agents | $AGENT_COUNT | - |" >> "$OUTPUT_FILE"

cat >> "$OUTPUT_FILE" << 'EOF'

---

## Templates

EOF

# List templates
if [[ -d "$DESIGN_OPS_ROOT/templates" ]]; then
    echo "| Template | Purpose |" >> "$OUTPUT_FILE"
    echo "|----------|---------|" >> "$OUTPUT_FILE"

    for template in "$DESIGN_OPS_ROOT/templates"/*.md; do
        [[ -f "$template" ]] || continue
        name=$(basename "$template")
        # Extract first line description if available
        desc=$(head -5 "$template" | grep -E "^>" | head -1 | sed 's/^> //' || echo "-")
        echo "| \`$name\` | $desc |" >> "$OUTPUT_FILE"
    done
fi

cat >> "$OUTPUT_FILE" << 'EOF'

---

## Tools

### Enforcement Tools
EOF

# List enforcement tools
if [[ -d "$DESIGN_OPS_ROOT/enforcement" ]]; then
    for tool in "$DESIGN_OPS_ROOT/enforcement"/*.sh; do
        [[ -f "$tool" ]] || continue
        name=$(basename "$tool")
        echo "- \`enforcement/$name\`" >> "$OUTPUT_FILE"
    done
fi

cat >> "$OUTPUT_FILE" << 'EOF'

### Automation Tools
EOF

# List other tools
if [[ -d "$DESIGN_OPS_ROOT/tools" ]]; then
    for tool in "$DESIGN_OPS_ROOT/tools"/*.sh; do
        [[ -f "$tool" ]] || continue
        name=$(basename "$tool")
        echo "- \`tools/$name\`" >> "$OUTPUT_FILE"
    done

    # Check subdirectories
    for subdir in "$DESIGN_OPS_ROOT/tools"/*/; do
        [[ -d "$subdir" ]] || continue
        subname=$(basename "$subdir")
        echo "" >> "$OUTPUT_FILE"
        echo "### $subname Tools" >> "$OUTPUT_FILE"
        for tool in "$subdir"*.sh; do
            [[ -f "$tool" ]] || continue
            name=$(basename "$tool")
            echo "- \`tools/$subname/$name\`" >> "$OUTPUT_FILE"
        done
    done
fi

cat >> "$OUTPUT_FILE" << 'EOF'

---

## Agents

EOF

# List agents
if [[ -d "$DESIGN_OPS_ROOT/agents" ]]; then
    echo "| Agent | Role |" >> "$OUTPUT_FILE"
    echo "|-------|------|" >> "$OUTPUT_FILE"

    for agent in "$DESIGN_OPS_ROOT/agents"/*.sh; do
        [[ -f "$agent" ]] || continue
        name=$(basename "$agent" .sh)
        # Extract description from script header
        desc=$(head -10 "$agent" | grep -E "^#.*-" | head -1 | sed 's/^#.*- //' || echo "-")
        echo "| \`$name\` | $desc |" >> "$OUTPUT_FILE"
    done
fi

cat >> "$OUTPUT_FILE" << 'EOF'

---

## Examples Library

EOF

# List examples
if [[ -d "$DESIGN_OPS_ROOT/examples" ]]; then
    echo "| Pattern | Description |" >> "$OUTPUT_FILE"
    echo "|---------|-------------|" >> "$OUTPUT_FILE"

    for example in "$DESIGN_OPS_ROOT/examples"/*.md; do
        [[ -f "$example" ]] || continue
        name=$(basename "$example" .md)
        [[ "$name" == "README" ]] && continue
        # Extract first description line
        desc=$(head -5 "$example" | grep -E "^>" | head -1 | sed 's/^> //' || echo "-")
        echo "| \`$name\` | $desc |" >> "$OUTPUT_FILE"
    done
fi

cat >> "$OUTPUT_FILE" << 'EOF'

---

## Invariant Domains

EOF

# List invariants
if [[ -d "$DESIGN_OPS_ROOT/invariants" ]]; then
    echo "| Domain | Invariant Count |" >> "$OUTPUT_FILE"
    echo "|--------|-----------------|" >> "$OUTPUT_FILE"

    for inv in "$DESIGN_OPS_ROOT/invariants"/*.md; do
        [[ -f "$inv" ]] || continue
        name=$(basename "$inv" .md)
        # Count invariant entries (lines starting with ##)
        count=$(grep -c "^## " "$inv" 2>/dev/null || echo "?")
        echo "| \`$name\` | $count |" >> "$OUTPUT_FILE"
    done
fi

cat >> "$OUTPUT_FILE" << 'EOF'

---

## Configuration

EOF

# List config files
if [[ -d "$DESIGN_OPS_ROOT/config" ]]; then
    for config in "$DESIGN_OPS_ROOT/config"/*; do
        [[ -f "$config" ]] || continue
        name=$(basename "$config")
        echo "- \`config/$name\`" >> "$OUTPUT_FILE"
    done
fi

cat >> "$OUTPUT_FILE" << EOF

---

## Metadata

- **Design Ops Version**: 2.0
- **Scan Date**: $(date '+%Y-%m-%d')
- **Location**: $DESIGN_OPS_ROOT
EOF

echo -e "${GREEN}Scan complete: $OUTPUT_FILE${NC}"
echo ""
echo "Summary:"
echo "  Templates:  $TEMPLATE_COUNT"
echo "  Tools:      $TOOL_COUNT"
echo "  Examples:   $EXAMPLE_COUNT"
echo "  Agents:     $AGENT_COUNT"
echo "  Invariants: $INVARIANT_COUNT"
