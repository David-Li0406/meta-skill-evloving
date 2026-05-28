#!/bin/bash
# Verify plugin marketplace configuration
# Usage: bash scripts/verify-marketplace.sh [marketplace-dir]

MARKETPLACE_DIR="${1:-.}"
CLAUDE_PLUGIN_DIR="$MARKETPLACE_DIR/.claude-plugin"
SKILLS_DIR="$MARKETPLACE_DIR/skills"

echo "🔍 Reviewing Plugin Marketplace Configuration"
echo "=============================================="
echo ""

# Check if marketplace.json exists
if [ ! -f "$CLAUDE_PLUGIN_DIR/marketplace.json" ]; then
    echo "❌ marketplace.json not found at $CLAUDE_PLUGIN_DIR/marketplace.json"
    exit 1
fi

echo "✓ marketplace.json found"
echo ""

# Display marketplace.json
echo "📄 marketplace.json:"
echo "---"
cat "$CLAUDE_PLUGIN_DIR/marketplace.json"
echo "---"
echo ""

# Check for plugin.json (should not exist)
if [ -f "$CLAUDE_PLUGIN_DIR/plugin.json" ]; then
    echo "⚠️  plugin.json found (Anthropic format uses marketplace.json only)"
else
    echo "✓ No plugin.json (follows Anthropic format)"
fi
echo ""

# Check git remote
echo "📍 Git remote:"
if git -C "$MARKETPLACE_DIR" remote -v &> /dev/null; then
    git -C "$MARKETPLACE_DIR" remote -v | head -2
else
    echo "⚠️  Not a git repository or no remotes configured"
fi
echo ""

# Verify skills paths from marketplace.json
echo "🔍 Verifying skills paths:"
if command -v jq &> /dev/null; then
    # Use jq if available
    SKILLS=$(jq -r '.plugins[].skills[]?' "$CLAUDE_PLUGIN_DIR/marketplace.json" 2>/dev/null)
else
    # Fallback: grep for skill paths
    SKILLS=$(grep -o '"./skills/[^"]*"' "$CLAUDE_PLUGIN_DIR/marketplace.json" | tr -d '"')
fi

if [ -z "$SKILLS" ]; then
    echo "⚠️  No skills found in marketplace.json"
else
    for skill_path in $SKILLS; do
        # Remove leading ./
        skill_path_clean="${skill_path#./}"
        full_path="$MARKETPLACE_DIR/$skill_path_clean/SKILL.md"

        if [ -f "$full_path" ]; then
            echo "  ✓ $skill_path"
        else
            echo "  ❌ $skill_path - SKILL.md not found at $full_path"
        fi
    done
fi
echo ""

# Check README.md for repository references
echo "📖 README.md repository references:"
if [ -f "$MARKETPLACE_DIR/README.md" ]; then
    grep -n "github.com/[^/]*/[^/ ]*" "$MARKETPLACE_DIR/README.md" | head -5
else
    echo "⚠️  README.md not found"
fi
echo ""

# List .claude-plugin directory
echo "📁 .claude-plugin directory:"
ls -lah "$CLAUDE_PLUGIN_DIR"
echo ""

# Check README.md consistency
echo "🔍 Checking README.md consistency:"
README_ISSUES=0

if [ -f "$MARKETPLACE_DIR/README.md" ]; then
    # Extract skill names from marketplace.json
    if command -v jq &> /dev/null; then
        SKILL_NAMES=$(jq -r '.plugins[].skills[]?' "$CLAUDE_PLUGIN_DIR/marketplace.json" 2>/dev/null | xargs -n1 basename)
    else
        SKILL_NAMES=$(grep -o '"./skills/[^"]*"' "$CLAUDE_PLUGIN_DIR/marketplace.json" | tr -d '"' | xargs -n1 basename)
    fi

    # Check if all skills are documented in README
    echo "  📋 Skills documentation:"
    for skill_name in $SKILL_NAMES; do
        if grep -q "###.*$skill_name" "$MARKETPLACE_DIR/README.md"; then
            echo "    ✓ $skill_name documented in Skills Included section"
        else
            echo "    ❌ $skill_name missing from Skills Included section"
            README_ISSUES=$((README_ISSUES + 1))
        fi
    done

    # Check if all skills are in permissions examples
    echo "  🔐 Permissions section:"
    for skill_name in $SKILL_NAMES; do
        if grep -q "Skill($skill_name)" "$MARKETPLACE_DIR/README.md"; then
            echo "    ✓ Skill($skill_name) in permissions examples"
        else
            echo "    ❌ Skill($skill_name) missing from permissions examples"
            README_ISSUES=$((README_ISSUES + 1))
        fi
    done

    # Check for plugin.json in Project Structure
    echo "  📂 Project Structure section:"
    if grep -q "plugin.json.*Plugin manifest" "$MARKETPLACE_DIR/README.md"; then
        echo "    ❌ README mentions 'plugin.json' but should use 'marketplace.json'"
        README_ISSUES=$((README_ISSUES + 1))
    else
        echo "    ✓ No plugin.json reference in Project Structure"
    fi

    if [ $README_ISSUES -eq 0 ]; then
        echo "  ✅ README.md is consistent with marketplace.json"
    else
        echo "  ⚠️  Found $README_ISSUES issue(s) in README.md"
    fi
else
    echo "  ⚠️  README.md not found - cannot check consistency"
fi
echo ""

echo "✅ Review complete!"
