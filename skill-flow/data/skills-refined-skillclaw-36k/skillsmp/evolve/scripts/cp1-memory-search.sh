#!/bin/bash
# Self-Evolving Agent - CP1: Memory Search
# 在任務開始前搜尋相關經驗
#
# 用法: ./scripts/cp1-memory-search.sh "關鍵字1" ["關鍵字2" ...]
#
# 輸出:
#   - 找到相關經驗：列出檔案路徑和摘要
#   - 無相關經驗：顯示「無相關經驗，可繼續執行」

set -e

MEMORY_DIR="${MEMORY_DIR:-.claude/memory}"

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 檢查參數
if [[ $# -eq 0 ]]; then
    echo -e "${RED}❌ 請提供搜尋關鍵字${NC}"
    echo ""
    echo "用法: $0 \"關鍵字1\" [\"關鍵字2\" ...]"
    echo ""
    echo "範例:"
    echo "  $0 \"token\" \"optimization\""
    echo "  $0 \"skillpkg\""
    exit 1
fi

# 檢查 memory 目錄
if [[ ! -d "$MEMORY_DIR" ]]; then
    echo -e "${YELLOW}⚠️  Memory 目錄不存在: $MEMORY_DIR${NC}"
    echo "無相關經驗，可繼續執行"
    exit 0
fi

# 建立搜尋模式（OR 邏輯）
PATTERN=$(IFS="|"; echo "$*")

echo -e "${BLUE}🔍 CP1: Memory Search${NC}"
echo "────────────────────────────────────────"
echo -e "搜尋: ${GREEN}$PATTERN${NC}"
echo -e "目錄: $MEMORY_DIR"
echo ""

# 執行搜尋
RESULTS=$(grep -ril "$PATTERN" "$MEMORY_DIR" 2>/dev/null || true)

if [[ -z "$RESULTS" ]]; then
    echo -e "${YELLOW}📭 無相關經驗${NC}"
    echo ""
    echo "✅ 可繼續執行任務"
    exit 0
fi

echo -e "${GREEN}📚 找到相關經驗:${NC}"
echo ""

# 顯示結果
COUNT=0
for file in $RESULTS; do
    COUNT=$((COUNT + 1))
    # 取得檔案標題（第一個 # 開頭的行）
    TITLE=$(grep -m1 "^#" "$file" 2>/dev/null | sed 's/^#* *//' || basename "$file")
    # 取得相對路徑
    REL_PATH=${file#$MEMORY_DIR/}

    echo -e "  ${BLUE}[$COUNT]${NC} $TITLE"
    echo -e "      📁 $REL_PATH"

    # 顯示匹配的上下文（最多 2 行）
    CONTEXT=$(grep -i -m2 "$PATTERN" "$file" 2>/dev/null | head -2 | sed 's/^/      │ /')
    if [[ -n "$CONTEXT" ]]; then
        echo "$CONTEXT"
    fi
    echo ""
done

echo "────────────────────────────────────────"
echo -e "共找到 ${GREEN}$COUNT${NC} 個相關文件"
echo ""
echo -e "${YELLOW}💡 建議：閱讀相關經驗後再開始執行${NC}"
