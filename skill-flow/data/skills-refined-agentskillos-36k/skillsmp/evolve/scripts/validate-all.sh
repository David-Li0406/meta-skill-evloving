#!/bin/bash
# Self-Evolving Agent - Complete Validation Script
# 一鍵執行所有驗證腳本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🔍 Self-Evolving Agent Complete Validation"
echo "════════════════════════════════════════════"
echo ""

TOTAL_PASS=0
TOTAL_FAIL=0

run_check() {
    local name="$1"
    local script="$2"

    echo "┌─ $name ─────────────────────────────────────┐"

    if [[ -x "$script" ]]; then
        if "$script" 2>&1; then
            TOTAL_PASS=$((TOTAL_PASS + 1))
            echo ""
            echo "✅ $name PASSED"
        else
            TOTAL_FAIL=$((TOTAL_FAIL + 1))
            echo ""
            echo "❌ $name FAILED"
        fi
    else
        echo "⚠️  Script not found or not executable: $script"
        TOTAL_FAIL=$((TOTAL_FAIL + 1))
    fi

    echo "└──────────────────────────────────────────────┘"
    echo ""
}

# Change to project root
cd "$PROJECT_ROOT"

# Run all validation scripts
run_check "Environment Check" "$SCRIPT_DIR/check-env.sh"
run_check "Installation Verification" "$SCRIPT_DIR/verify-install.sh"
run_check "Memory Validation" "$SCRIPT_DIR/validate-memory.sh"

# Additional checks
echo "┌─ Additional Checks ────────────────────────────┐"

# Check for required files
required_files=(
    "README.md"
    "LICENSE"
    "CLAUDE.md"
    "CHANGELOG.md"
    "skills/SKILL.md"
    ".gitignore"
)

missing=0
for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
        missing=$((missing + 1))
    fi
done

if [[ $missing -eq 0 ]]; then
    echo ""
    echo "✅ All required files present"
    TOTAL_PASS=$((TOTAL_PASS + 1))
else
    echo ""
    echo "❌ $missing required files missing"
    TOTAL_FAIL=$((TOTAL_FAIL + 1))
fi

echo "└──────────────────────────────────────────────┘"
echo ""

# Check scripts are executable
echo "┌─ Script Permissions ───────────────────────────┐"

scripts=(
    "install.sh"
    "scripts/check-env.sh"
    "scripts/validate-memory.sh"
    "scripts/verify-install.sh"
    "scripts/sync-global.sh"
)

non_exec=0
for script in "${scripts[@]}"; do
    if [[ -f "$script" ]]; then
        if [[ -x "$script" ]]; then
            echo "✅ $script (executable)"
        else
            echo "⚠️  $script (not executable)"
            non_exec=$((non_exec + 1))
        fi
    fi
done

if [[ $non_exec -eq 0 ]]; then
    echo ""
    echo "✅ All scripts executable"
    TOTAL_PASS=$((TOTAL_PASS + 1))
else
    echo ""
    echo "⚠️  $non_exec scripts not executable"
fi

echo "└──────────────────────────────────────────────┘"
echo ""

# Final Summary
echo "════════════════════════════════════════════════"
echo "📋 Final Summary"
echo "════════════════════════════════════════════════"
echo "   ✅ Checks Passed: $TOTAL_PASS"
echo "   ❌ Checks Failed: $TOTAL_FAIL"
echo ""

if [[ $TOTAL_FAIL -gt 0 ]]; then
    echo "❌ VALIDATION INCOMPLETE"
    echo ""
    echo "Please fix the failed checks before releasing."
    exit 1
else
    echo "✅ ALL VALIDATIONS PASSED"
    echo ""
    echo "Project is ready for release!"
    exit 0
fi
