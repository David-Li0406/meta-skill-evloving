#!/bin/bash
# Self-Evolving Agent - Installation Verification Script
# 驗證 skill 安裝是否成功

set -e

echo "🔍 Self-Evolving Agent Installation Verification"
echo "════════════════════════════════════════════════"
echo ""

PASS=0
FAIL=0
WARN=0

check_pass() {
    echo "✅ $1"
    PASS=$((PASS + 1))
}

check_fail() {
    echo "❌ $1"
    FAIL=$((FAIL + 1))
}

check_warn() {
    echo "⚠️  $1"
    WARN=$((WARN + 1))
}

# Detect installation location
# Priority: source repo (skills/) > local install > global install
# When developing, prefer skills/ which has full atomic structure

SKILL_DIR=""

# First check if we're in the source repo (has skills/ with modules)
if [[ -f "skills/SKILL.md" && -d "skills/00-getting-started" ]]; then
    SKILL_DIR="skills"
# Then check installed locations
elif [[ -f ".claude/skills/evolve/SKILL.md" ]]; then
    SKILL_DIR=".claude/skills/evolve"
elif [[ -f "$HOME/.claude/skills/evolve/SKILL.md" ]]; then
    SKILL_DIR="$HOME/.claude/skills/evolve"
fi

if [[ -z "$SKILL_DIR" ]]; then
    check_fail "Skill not found in any standard location"
    echo ""
    echo "Expected locations:"
    for loc in "${SKILL_LOCATIONS[@]}"; do
        echo "  - $loc/SKILL.md"
    done
    exit 1
fi

check_pass "Skill found at: $SKILL_DIR"

echo ""
echo "┌─ Core Files ────────────────────────────────┐"

# Check main skill file
if [[ -f "$SKILL_DIR/SKILL.md" ]]; then
    # Check version
    version=$(grep -oE 'version: [0-9]+\.[0-9]+\.[0-9]+' "$SKILL_DIR/SKILL.md" | head -1 | cut -d' ' -f2)
    if [[ -n "$version" ]]; then
        check_pass "SKILL.md exists (v$version)"
    else
        check_pass "SKILL.md exists"
    fi
else
    check_fail "SKILL.md not found"
fi

echo "└──────────────────────────────────────────────┘"
echo ""
echo "┌─ Modules ────────────────────────────────────┐"

# Check required modules
MODULES=(
    "00-getting-started:入門"
    "01-core:核心流程"
    "02-checkpoints:檢查點"
    "03-memory:記憶系統"
    "04-emergence:涌現機制"
    "05-integration:外部整合"
    "06-scaling:擴展策略"
    "99-evolution:自我進化"
)

for module_info in "${MODULES[@]}"; do
    module_name="${module_info%%:*}"
    module_desc="${module_info##*:}"

    if [[ -d "$SKILL_DIR/$module_name" ]]; then
        # Count files in module
        file_count=$(find "$SKILL_DIR/$module_name" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
        check_pass "$module_name ($module_desc) - $file_count files"
    else
        check_fail "$module_name ($module_desc) - missing"
    fi
done

echo "└──────────────────────────────────────────────┘"
echo ""
echo "┌─ Scripts ────────────────────────────────────┐"

# Check scripts (only if in repo root)
if [[ -d "scripts" ]]; then
    SCRIPTS=(
        "scripts/check-env.sh"
        "scripts/validate-memory.sh"
        "scripts/sync-global.sh"
    )

    for script in "${SCRIPTS[@]}"; do
        if [[ -f "$script" ]]; then
            if [[ -x "$script" ]]; then
                check_pass "$script (executable)"
            else
                check_warn "$script (not executable)"
            fi
        else
            check_warn "$script (not found)"
        fi
    done
else
    echo "  (Scripts check skipped - not in repo root)"
fi

echo "└──────────────────────────────────────────────┘"
echo ""
echo "┌─ Memory System ─────────────────────────────┐"

# Check memory system
if [[ -d ".claude/memory" ]]; then
    check_pass ".claude/memory/ exists"

    if [[ -f ".claude/memory/index.md" ]]; then
        check_pass ".claude/memory/index.md exists"
    else
        check_warn ".claude/memory/index.md missing"
    fi

    # Count memory entries
    for dir in learnings failures decisions patterns; do
        if [[ -d ".claude/memory/$dir" ]]; then
            count=$(find ".claude/memory/$dir" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
            echo "  📁 $dir: $count entries"
        fi
    done
else
    check_warn ".claude/memory/ not initialized"
    echo "  Run: mkdir -p .claude/memory/{learnings,failures,decisions,patterns}"
fi

echo "└──────────────────────────────────────────────┘"

# Summary
echo ""
echo "════════════════════════════════════════════════"
echo "📋 Summary"
echo "════════════════════════════════════════════════"
echo "   ✅ Passed:   $PASS"
echo "   ⚠️  Warnings: $WARN"
echo "   ❌ Failed:   $FAIL"
echo ""

if [[ $FAIL -gt 0 ]]; then
    echo "❌ Installation INCOMPLETE"
    echo ""
    echo "Try reinstalling:"
    echo "  curl -fsSL https://raw.githubusercontent.com/miles990/self-evolving-agent/main/install.sh | bash -s -- --with-memory"
    exit 1
elif [[ $WARN -gt 2 ]]; then
    echo "⚠️  Installation PARTIAL"
    echo ""
    echo "Consider running with full options:"
    echo "  curl -fsSL .../install.sh | bash -s -- --with-hooks --with-memory"
    exit 0
else
    echo "✅ Installation VERIFIED"
    echo ""
    echo "You can now use: /evolve [your goal]"
    exit 0
fi
