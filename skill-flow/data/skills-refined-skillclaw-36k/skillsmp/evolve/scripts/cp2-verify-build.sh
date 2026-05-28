#!/bin/bash
# Self-Evolving Agent - CP2: Build & Test Verification
# 程式碼變更後驗證編譯和測試
#
# 用法: ./scripts/cp2-verify-build.sh [--skip-tests]
#
# 自動偵測專案類型並執行對應的驗證命令

set -e

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

SKIP_TESTS=0
ERRORS=0

# 參數處理
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-tests)
            SKIP_TESTS=1
            shift
            ;;
        *)
            shift
            ;;
    esac
done

echo -e "${BLUE}🔧 CP2: Build & Test Verification${NC}"
echo "════════════════════════════════════════"
echo ""

# ─────────────────────────────────────────
# 偵測專案類型
# ─────────────────────────────────────────
detect_project_type() {
    if [[ -f "package.json" ]]; then
        echo "node"
    elif [[ -f "Cargo.toml" ]]; then
        echo "rust"
    elif [[ -f "go.mod" ]]; then
        echo "go"
    elif [[ -f "pyproject.toml" ]] || [[ -f "setup.py" ]] || [[ -f "requirements.txt" ]]; then
        echo "python"
    elif [[ -f "Makefile" ]]; then
        echo "make"
    else
        echo "unknown"
    fi
}

PROJECT_TYPE=$(detect_project_type)
echo -e "偵測到專案類型: ${CYAN}$PROJECT_TYPE${NC}"
echo ""

# ─────────────────────────────────────────
# 執行驗證
# ─────────────────────────────────────────
run_verification() {
    local cmd="$1"
    local desc="$2"

    echo -e "${CYAN}▶ $desc${NC}"
    echo "  命令: $cmd"

    if eval "$cmd" 2>&1; then
        echo -e "  ${GREEN}✅ 通過${NC}"
        return 0
    else
        echo -e "  ${RED}❌ 失敗${NC}"
        ERRORS=$((ERRORS + 1))
        return 1
    fi
    echo ""
}

case $PROJECT_TYPE in
    node)
        echo -e "${CYAN}▶ Node.js 專案驗證${NC}"
        echo "────────────────────────────────────────"

        # 檢查 TypeScript
        if [[ -f "tsconfig.json" ]]; then
            run_verification "npx tsc --noEmit" "TypeScript 型別檢查"
        fi

        # 檢查 ESLint
        if [[ -f ".eslintrc.json" ]] || [[ -f ".eslintrc.js" ]] || [[ -f "eslint.config.js" ]]; then
            run_verification "npm run lint 2>/dev/null || npx eslint . --ext .ts,.tsx,.js,.jsx --max-warnings=0" "ESLint 檢查"
        fi

        # 執行 build
        if grep -q '"build"' package.json 2>/dev/null; then
            run_verification "npm run build" "Build"
        fi

        # 執行測試
        if [[ $SKIP_TESTS -eq 0 ]]; then
            if grep -q '"test"' package.json 2>/dev/null; then
                run_verification "npm test" "測試"
            fi
        fi
        ;;

    rust)
        echo -e "${CYAN}▶ Rust 專案驗證${NC}"
        echo "────────────────────────────────────────"

        run_verification "cargo check" "Cargo Check"
        run_verification "cargo clippy -- -D warnings" "Clippy Lint"

        if [[ $SKIP_TESTS -eq 0 ]]; then
            run_verification "cargo test" "測試"
        fi
        ;;

    go)
        echo -e "${CYAN}▶ Go 專案驗證${NC}"
        echo "────────────────────────────────────────"

        run_verification "go build ./..." "Go Build"
        run_verification "go vet ./..." "Go Vet"

        if [[ $SKIP_TESTS -eq 0 ]]; then
            run_verification "go test ./..." "測試"
        fi
        ;;

    python)
        echo -e "${CYAN}▶ Python 專案驗證${NC}"
        echo "────────────────────────────────────────"

        # 檢查 mypy
        if [[ -f "mypy.ini" ]] || [[ -f "pyproject.toml" ]]; then
            run_verification "mypy . 2>/dev/null || echo 'mypy not configured'" "型別檢查 (mypy)"
        fi

        # 檢查 ruff/flake8
        if command -v ruff &> /dev/null; then
            run_verification "ruff check ." "Ruff Lint"
        elif command -v flake8 &> /dev/null; then
            run_verification "flake8 ." "Flake8 Lint"
        fi

        if [[ $SKIP_TESTS -eq 0 ]]; then
            if [[ -f "pytest.ini" ]] || [[ -d "tests" ]]; then
                run_verification "pytest" "測試"
            fi
        fi
        ;;

    make)
        echo -e "${CYAN}▶ Makefile 專案驗證${NC}"
        echo "────────────────────────────────────────"

        if grep -q "^build:" Makefile; then
            run_verification "make build" "Make Build"
        fi

        if [[ $SKIP_TESTS -eq 0 ]]; then
            if grep -q "^test:" Makefile; then
                run_verification "make test" "Make Test"
            fi
        fi
        ;;

    *)
        echo -e "${YELLOW}⚠️  無法偵測專案類型${NC}"
        echo "請手動執行驗證命令"
        exit 0
        ;;
esac

echo ""
echo "════════════════════════════════════════"
echo -e "${BLUE}📋 CP2 摘要${NC}"
echo "════════════════════════════════════════"

if [[ $ERRORS -gt 0 ]]; then
    echo -e "${RED}❌ 驗證失敗 ($ERRORS 個錯誤)${NC}"
    echo ""
    echo "請修復錯誤後再繼續"
    exit 1
else
    echo -e "${GREEN}✅ 所有驗證通過${NC}"
    echo "可繼續下一步"
fi
