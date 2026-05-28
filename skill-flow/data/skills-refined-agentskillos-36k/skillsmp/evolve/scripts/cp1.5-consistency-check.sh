#!/bin/bash
# Self-Evolving Agent - CP1.5: Consistency Check
# 在寫程式碼前檢查一致性
#
# 用法: ./scripts/cp1.5-consistency-check.sh "功能關鍵字" [src目錄]
#
# Phase 1 (基礎檢查):
#   1. 搜尋現有實作
#   2. 檢查專案慣例
#   3. 檢查 Schema/API

set -e

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 參數
KEYWORD="${1:-}"
SRC_DIR="${2:-src}"
FOUND_SIMILAR=0
WARNINGS=0

if [[ -z "$KEYWORD" ]]; then
    echo -e "${RED}❌ 請提供功能關鍵字${NC}"
    echo ""
    echo "用法: $0 \"功能關鍵字\" [src目錄]"
    echo ""
    echo "範例:"
    echo "  $0 \"formatDate\" src/"
    echo "  $0 \"UserService\""
    exit 1
fi

echo -e "${BLUE}🔍 CP1.5: Consistency Check - Phase 1${NC}"
echo "════════════════════════════════════════"
echo -e "關鍵字: ${GREEN}$KEYWORD${NC}"
echo -e "搜尋目錄: $SRC_DIR"
echo ""

# ─────────────────────────────────────────
# Phase 1.1: 搜尋現有實作
# ─────────────────────────────────────────
echo -e "${CYAN}▶ 1. 搜尋現有實作${NC}"
echo "────────────────────────────────────────"

if [[ -d "$SRC_DIR" ]]; then
    # 搜尋函數/類別定義
    IMPL_RESULTS=$(grep -rn "$KEYWORD" "$SRC_DIR" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" --include="*.py" --include="*.go" --include="*.rs" 2>/dev/null | head -10 || true)

    if [[ -n "$IMPL_RESULTS" ]]; then
        FOUND_SIMILAR=1
        echo -e "${YELLOW}⚠️  找到類似實作:${NC}"
        echo ""
        echo "$IMPL_RESULTS" | while IFS= read -r line; do
            echo "  $line"
        done
        echo ""
        echo -e "${YELLOW}💡 建議：檢查是否可複用現有實作${NC}"
    else
        echo -e "${GREEN}✅ 無現有類似實作${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  $SRC_DIR 目錄不存在，跳過搜尋${NC}"
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

# ─────────────────────────────────────────
# Phase 1.2: 檢查專案慣例
# ─────────────────────────────────────────
echo -e "${CYAN}▶ 2. 檢查專案慣例${NC}"
echo "────────────────────────────────────────"

# 檢查 CLAUDE.md
if [[ -f "CLAUDE.md" ]]; then
    echo -e "${GREEN}✅ CLAUDE.md 存在${NC}"
    # 搜尋命名慣例
    NAMING=$(grep -i "naming\|convention\|style\|format" CLAUDE.md 2>/dev/null | head -3 || true)
    if [[ -n "$NAMING" ]]; then
        echo "   相關慣例:"
        echo "$NAMING" | while IFS= read -r line; do
            echo "   │ $line"
        done
    fi
else
    echo -e "${YELLOW}⚠️  CLAUDE.md 不存在${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

# 檢查 README.md
if [[ -f "README.md" ]]; then
    echo -e "${GREEN}✅ README.md 存在${NC}"
else
    echo -e "${YELLOW}⚠️  README.md 不存在${NC}"
fi

# 檢查 eslint/prettier 配置
for config in ".eslintrc" ".eslintrc.js" ".eslintrc.json" ".prettierrc" ".prettierrc.js" "eslint.config.js"; do
    if [[ -f "$config" ]]; then
        echo -e "${GREEN}✅ $config 存在（程式碼風格已定義）${NC}"
        break
    fi
done
echo ""

# ─────────────────────────────────────────
# Phase 1.3: 檢查 Schema/API
# ─────────────────────────────────────────
echo -e "${CYAN}▶ 3. 檢查 Schema/API${NC}"
echo "────────────────────────────────────────"

# 搜尋型別定義
TYPE_FILES=$(find . -type f \( -name "*.d.ts" -o -name "types.ts" -o -name "schema.ts" -o -name "models.py" \) 2>/dev/null | head -5 || true)

if [[ -n "$TYPE_FILES" ]]; then
    echo "找到型別定義檔案:"
    echo "$TYPE_FILES" | while IFS= read -r file; do
        echo "  📄 $file"
    done

    # 搜尋相關型別
    TYPE_MATCHES=$(grep -l "$KEYWORD" $TYPE_FILES 2>/dev/null || true)
    if [[ -n "$TYPE_MATCHES" ]]; then
        echo ""
        echo -e "${YELLOW}⚠️  在型別定義中找到相關內容:${NC}"
        echo "$TYPE_MATCHES" | while IFS= read -r file; do
            echo "  📄 $file"
            grep -n "$KEYWORD" "$file" 2>/dev/null | head -3 | while IFS= read -r line; do
                echo "     │ $line"
            done
        done
    fi
else
    echo -e "${GREEN}✅ 無獨立型別定義檔案${NC}"
fi
echo ""

# ─────────────────────────────────────────
# 摘要
# ─────────────────────────────────────────
echo "════════════════════════════════════════"
echo -e "${BLUE}📋 Phase 1 摘要${NC}"
echo "════════════════════════════════════════"

if [[ $FOUND_SIMILAR -eq 1 ]]; then
    echo -e "${YELLOW}⚠️  發現類似實作，請確認:${NC}"
    echo "   • 是否可直接複用？"
    echo "   • 是否應該擴展現有功能？"
    echo "   • 命名是否符合現有慣例？"
    echo ""
    echo -e "${RED}❌ 請先確認後再開始寫程式碼${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Phase 1 通過${NC}"
    echo "   • 無重複實作"
    echo "   • 可開始寫程式碼"
    if [[ $WARNINGS -gt 0 ]]; then
        echo -e "   • ${YELLOW}Warnings: $WARNINGS${NC}"
    fi
fi
