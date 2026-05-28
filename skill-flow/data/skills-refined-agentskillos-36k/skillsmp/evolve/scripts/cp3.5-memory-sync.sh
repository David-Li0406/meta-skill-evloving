#!/bin/bash
# Self-Evolving Agent - CP3.5: Memory Sync
# 創建 Memory 文件後立即同步 index.md
#
# 用法: ./scripts/cp3.5-memory-sync.sh [新文件路徑]
#
# 功能:
#   - 自動偵測新文件並加入 index.md
#   - 或指定新文件路徑進行同步

set -e

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

MEMORY_DIR="${MEMORY_DIR:-.claude/memory}"
INDEX_FILE="$MEMORY_DIR/index.md"
NEW_FILE="${1:-}"

echo -e "${BLUE}📝 CP3.5: Memory Sync${NC}"
echo "════════════════════════════════════════"
echo ""

# 檢查 memory 目錄
if [[ ! -d "$MEMORY_DIR" ]]; then
    echo -e "${RED}❌ Memory 目錄不存在: $MEMORY_DIR${NC}"
    exit 1
fi

# 檢查 index.md
if [[ ! -f "$INDEX_FILE" ]]; then
    echo -e "${YELLOW}⚠️  index.md 不存在，正在創建...${NC}"
    cat > "$INDEX_FILE" << 'EOF'
# Memory Index

> 記憶系統索引 - 自動生成

## 目錄

### Learnings
<!-- learnings entries -->

### Failures
<!-- failures entries -->

### Decisions
<!-- decisions entries -->

### Patterns
<!-- patterns entries -->

### Strategies
<!-- strategies entries -->

### Discoveries
<!-- discoveries entries -->

---
最後更新: $(date +%Y-%m-%d)
EOF
    echo -e "${GREEN}✅ index.md 已創建${NC}"
fi

# ─────────────────────────────────────────
# 如果指定了新文件
# ─────────────────────────────────────────
if [[ -n "$NEW_FILE" ]]; then
    if [[ ! -f "$NEW_FILE" ]]; then
        echo -e "${RED}❌ 文件不存在: $NEW_FILE${NC}"
        exit 1
    fi

    # 取得相對路徑
    REL_PATH=${NEW_FILE#$MEMORY_DIR/}
    CATEGORY=$(dirname "$REL_PATH")
    FILENAME=$(basename "$NEW_FILE" .md)

    # 取得標題
    TITLE=$(grep -m1 "^#" "$NEW_FILE" 2>/dev/null | sed 's/^#* *//' || echo "$FILENAME")

    echo -e "新文件: ${CYAN}$REL_PATH${NC}"
    echo -e "類別: ${CYAN}$CATEGORY${NC}"
    echo -e "標題: ${CYAN}$TITLE${NC}"
    echo ""

    # 檢查是否已在 index.md 中
    if grep -q "$REL_PATH" "$INDEX_FILE" 2>/dev/null; then
        echo -e "${YELLOW}⚠️  文件已在 index.md 中${NC}"
        exit 0
    fi

    # 找到對應類別並插入
    CATEGORY_UPPER=$(echo "$CATEGORY" | sed 's/./\U&/')
    ENTRY="- [$TITLE]($REL_PATH)"

    # 使用 sed 在類別標題後插入
    if grep -q "### $CATEGORY_UPPER" "$INDEX_FILE" 2>/dev/null; then
        # macOS sed 需要不同的語法
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "/### $CATEGORY_UPPER/a\\
$ENTRY
" "$INDEX_FILE"
        else
            sed -i "/### $CATEGORY_UPPER/a $ENTRY" "$INDEX_FILE"
        fi
        echo -e "${GREEN}✅ 已加入 index.md${NC}"
    else
        echo -e "${YELLOW}⚠️  找不到類別 '$CATEGORY_UPPER'，請手動加入${NC}"
        echo "  條目: $ENTRY"
    fi

    exit 0
fi

# ─────────────────────────────────────────
# 自動偵測新文件
# ─────────────────────────────────────────
echo -e "${CYAN}▶ 掃描未同步的文件...${NC}"
echo ""

CATEGORIES=("learnings" "failures" "decisions" "patterns" "strategies" "discoveries")
NEW_COUNT=0

for category in "${CATEGORIES[@]}"; do
    if [[ ! -d "$MEMORY_DIR/$category" ]]; then
        continue
    fi

    for file in "$MEMORY_DIR/$category"/*.md; do
        [[ ! -f "$file" ]] && continue

        REL_PATH="$category/$(basename "$file")"

        if ! grep -q "$REL_PATH" "$INDEX_FILE" 2>/dev/null; then
            NEW_COUNT=$((NEW_COUNT + 1))
            TITLE=$(grep -m1 "^#" "$file" 2>/dev/null | sed 's/^#* *//' || basename "$file" .md)

            echo -e "${YELLOW}📄 未同步: $REL_PATH${NC}"
            echo "   標題: $TITLE"

            # 詢問是否加入（非互動模式下自動加入）
            ENTRY="- [$TITLE]($REL_PATH)"

            CATEGORY_UPPER=$(echo "$category" | sed 's/./\U&/')
            if grep -q "### $CATEGORY_UPPER" "$INDEX_FILE" 2>/dev/null; then
                if [[ "$OSTYPE" == "darwin"* ]]; then
                    sed -i '' "/### $CATEGORY_UPPER/a\\
$ENTRY
" "$INDEX_FILE"
                else
                    sed -i "/### $CATEGORY_UPPER/a $ENTRY" "$INDEX_FILE"
                fi
                echo -e "   ${GREEN}✅ 已加入${NC}"
            fi
            echo ""
        fi
    done
done

echo "════════════════════════════════════════"
echo -e "${BLUE}📋 CP3.5 摘要${NC}"
echo "════════════════════════════════════════"

if [[ $NEW_COUNT -eq 0 ]]; then
    echo -e "${GREEN}✅ index.md 已同步，無新文件${NC}"
else
    echo -e "${GREEN}✅ 已同步 $NEW_COUNT 個新文件${NC}"
fi

# 驗證
echo ""
echo -e "${CYAN}▶ 執行驗證...${NC}"
./scripts/validate-memory.sh "$MEMORY_DIR" 2>/dev/null || true
