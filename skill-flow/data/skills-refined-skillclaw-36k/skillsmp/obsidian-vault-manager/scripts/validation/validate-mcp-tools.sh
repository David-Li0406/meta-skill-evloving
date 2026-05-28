#!/bin/bash
# Validation script to check for common MCP tool name mistakes

set -e

SKILL_DIR="$HOME/.claude/skills/obsidian-vault-manager"
SKILL_FILE="$SKILL_DIR/SKILL.md"

echo "🔍 Validating MCP tool names in SKILL.md..."
echo ""

ERRORS=0

# Check for incorrect Obsidian tool references in MCP_DOCKER
if grep -q "mcp__MCP_DOCKER__obsidian" "$SKILL_FILE"; then
    echo "❌ ERROR: Found MCP_DOCKER__obsidian references!"
    echo "   MCP_DOCKER does not have Obsidian tools."
    echo "   Use: mcp__obsidian-mcp-tools__* instead"
    echo ""
    grep -n "mcp__MCP_DOCKER__obsidian" "$SKILL_FILE"
    echo ""
    ERRORS=$((ERRORS + 1))
fi

# Check for incorrect gitingest underscore naming
if grep -q "mcp__MCP_DOCKER__gitingest_" "$SKILL_FILE"; then
    echo "❌ ERROR: Found gitingest with underscore!"
    echo "   GitIngest tools use HYPHENS, not underscores."
    echo "   Use: mcp__MCP_DOCKER__gitingest-analyze (with hyphen)"
    echo ""
    grep -n "mcp__MCP_DOCKER__gitingest_" "$SKILL_FILE"
    echo ""
    ERRORS=$((ERRORS + 1))
fi

# Check for old non-Docker tool references that should be updated
if grep -q "mcp__github__create_or_update_file" "$SKILL_FILE"; then
    echo "⚠️  WARNING: Found old mcp__github__ reference"
    echo "   Consider using: mcp__MCP_DOCKER__create_or_update_file"
    echo ""
    grep -n "mcp__github__create_or_update_file" "$SKILL_FILE"
    echo ""
fi

if grep -q "mcp__fetch__fetch" "$SKILL_FILE"; then
    echo "⚠️  WARNING: Found old mcp__fetch__ reference"
    echo "   Consider using: mcp__MCP_DOCKER__fetch"
    echo ""
    grep -n "mcp__fetch__fetch" "$SKILL_FILE"
    echo ""
fi

if grep -q "mcp__gitingest__gitingest-analyze" "$SKILL_FILE"; then
    echo "⚠️  WARNING: Found old mcp__gitingest__ reference"
    echo "   Consider using: mcp__MCP_DOCKER__gitingest-analyze"
    echo ""
    grep -n "mcp__gitingest__gitingest-analyze" "$SKILL_FILE"
    echo ""
fi

# Verify correct allowed-tools configuration
echo "📋 Checking allowed-tools section..."
if grep -q "mcp__obsidian-mcp-tools__\*" "$SKILL_FILE"; then
    echo "✅ Obsidian tools wildcard: CORRECT"
else
    echo "❌ ERROR: Missing mcp__obsidian-mcp-tools__* wildcard!"
    ERRORS=$((ERRORS + 1))
fi

if grep -q "mcp__MCP_DOCKER__gitingest-analyze" "$SKILL_FILE"; then
    echo "✅ GitIngest tool (with hyphen): CORRECT"
else
    echo "⚠️  WARNING: GitIngest tool not found in allowed-tools"
fi

echo ""
echo "═══════════════════════════════════════"

if [ $ERRORS -eq 0 ]; then
    echo "✅ Validation PASSED! No errors found."
    exit 0
else
    echo "❌ Validation FAILED! Found $ERRORS error(s)."
    echo ""
    echo "Please review MCP_ARCHITECTURE.md for correct naming"
    exit 1
fi
