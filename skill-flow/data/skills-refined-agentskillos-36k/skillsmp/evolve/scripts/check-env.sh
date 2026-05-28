#!/bin/bash
# Self-Evolving Agent - Environment Check Script
# PSB Setup 環境檢查自動化

echo "🔍 Self-Evolving Agent Environment Check"
echo "════════════════════════════════════════"
echo ""

PASS=0
WARN=0
FAIL=0

check_pass() {
    echo "✅ $1"
    PASS=$((PASS + 1))
}

check_warn() {
    echo "⚠️  $1"
    WARN=$((WARN + 1))
}

check_fail() {
    echo "❌ $1"
    FAIL=$((FAIL + 1))
}

# === Plan 階段 ===
echo "┌─ Plan（規劃）────────────────────────┐"

# 檢查是否在 Git Repo 中
if git rev-parse --is-inside-work-tree &>/dev/null; then
    check_pass "Git repository detected"
else
    check_fail "Not a git repository"
fi

echo "└────────────────────────────────────────┘"
echo ""

# === Setup 階段 ===
echo "┌─ Setup（環境）───────────────────────┐"

# 檢查 CLAUDE.md
if [[ -f "CLAUDE.md" ]]; then
    check_pass "CLAUDE.md exists"
else
    check_warn "CLAUDE.md not found (recommended)"
fi

# 檢查記憶系統
if [[ -d ".claude/memory" ]]; then
    check_pass ".claude/memory/ directory exists"

    # 檢查 index.md
    if [[ -f ".claude/memory/index.md" ]]; then
        check_pass ".claude/memory/index.md exists"
    else
        check_warn ".claude/memory/index.md not found"
    fi

    # 檢查子目錄
    for dir in learnings failures decisions patterns; do
        if [[ -d ".claude/memory/$dir" ]]; then
            count=$(find ".claude/memory/$dir" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
            check_pass ".claude/memory/$dir/ ($count entries)"
        fi
    done
else
    check_warn ".claude/memory/ not initialized"
fi

# 檢查 skills
if [[ -d ".claude/skills" ]] || [[ -d "skills" ]]; then
    check_pass "Skills directory exists"
else
    check_warn "No skills directory found"
fi

echo "└────────────────────────────────────────┘"
echo ""

# === Build 階段 ===
echo "┌─ Build（執行準備）──────────────────┐"

# 檢查專案類型（使用陣列避免相容性問題）
check_project() {
    local file="$1" type="$2"
    [[ -f "$file" ]] && check_pass "$type project detected ($file)"
}

check_project "package.json" "Node.js"
check_project "requirements.txt" "Python"
check_project "pyproject.toml" "Python (pyproject)"
check_project "Cargo.toml" "Rust"
check_project "go.mod" "Go"

# Node.js 特殊檢查：node_modules
if [[ -f "package.json" ]] && [[ ! -d "node_modules" ]]; then
    check_warn "node_modules/ not found (run npm install?)"
fi

# 檢查測試配置
test_config_found=false
for config in jest.config.js vitest.config.ts pytest.ini; do
    if [[ -f "$config" ]]; then
        check_pass "Test configuration found ($config)"
        test_config_found=true
        break
    fi
done
[[ "$test_config_found" == "false" ]] && check_warn "No test configuration detected"

echo "└────────────────────────────────────────┘"
echo ""

# === 總結 ===
echo "════════════════════════════════════════"
echo "📋 Summary"
echo "════════════════════════════════════════"
echo "   ✅ Passed:   $PASS"
echo "   ⚠️  Warnings: $WARN"
echo "   ❌ Failed:   $FAIL"
echo ""

if [[ $FAIL -gt 0 ]]; then
    echo "❌ Environment NOT ready"
    echo ""
    echo "Fix the failed items before using /evolve"
    exit 1
elif [[ $WARN -gt 3 ]]; then
    echo "⚠️  Environment PARTIAL ready"
    echo ""
    echo "Consider fixing warnings for best experience:"
    echo "  - Create CLAUDE.md for project context"
    echo "  - Initialize memory: mkdir -p .claude/memory/{learnings,failures,decisions,patterns}"
    exit 0
else
    echo "✅ Environment READY"
    echo ""
    echo "You can now use: /evolve [your goal]"
    exit 0
fi
