#!/bin/bash
#
# generate-changelog.sh - 從 git commits 自動生成 CHANGELOG
#
# 支援 Conventional Commits 格式:
#   feat:     → Added
#   fix:      → Fixed
#   docs:     → Documentation
#   refactor: → Changed
#   chore:    → Maintenance
#   perf:     → Performance
#   test:     → Testing
#
# 用法:
#   ./scripts/generate-changelog.sh              # 生成自上次 tag 以來的變更
#   ./scripts/generate-changelog.sh --all        # 生成所有變更
#   ./scripts/generate-changelog.sh --since v4.0.0  # 從指定 tag 開始
#   ./scripts/generate-changelog.sh --preview    # 預覽不寫入檔案
#

set -euo pipefail

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 預設值
SINCE_TAG=""
PREVIEW_MODE=false
OUTPUT_FILE="CHANGELOG.md"
SHOW_ALL=false

# 解析參數
while [[ $# -gt 0 ]]; do
    case $1 in
        --all)
            SHOW_ALL=true
            shift
            ;;
        --since)
            SINCE_TAG="$2"
            shift 2
            ;;
        --preview)
            PREVIEW_MODE=true
            shift
            ;;
        --output|-o)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --help|-h)
            echo "用法: $0 [OPTIONS]"
            echo ""
            echo "從 git commits 自動生成 CHANGELOG"
            echo ""
            echo "Options:"
            echo "  --all           生成所有 commits 的變更記錄"
            echo "  --since TAG     從指定 tag 開始生成"
            echo "  --preview       預覽模式，不寫入檔案"
            echo "  --output FILE   指定輸出檔案 (預設: CHANGELOG.md)"
            echo "  --help          顯示此幫助訊息"
            echo ""
            echo "支援的 Conventional Commits 類型:"
            echo "  feat:     新功能      → Added"
            echo "  fix:      修復        → Fixed"
            echo "  docs:     文檔        → Documentation"
            echo "  refactor: 重構        → Changed"
            echo "  chore:    維護        → Maintenance"
            echo "  perf:     效能        → Performance"
            echo "  test:     測試        → Testing"
            exit 0
            ;;
        *)
            echo -e "${RED}未知參數: $1${NC}"
            exit 1
            ;;
    esac
done

# 確認在 git repo 中
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo -e "${RED}錯誤: 不在 git repository 中${NC}"
    exit 1
fi

# 取得最新 tag
get_latest_tag() {
    git describe --tags --abbrev=0 2>/dev/null || echo ""
}

# 決定起始點
if [[ "$SHOW_ALL" == true ]]; then
    GIT_RANGE=""
    echo -e "${BLUE}生成所有 commits 的變更記錄...${NC}"
elif [[ -n "$SINCE_TAG" ]]; then
    GIT_RANGE="${SINCE_TAG}..HEAD"
    echo -e "${BLUE}生成自 ${SINCE_TAG} 以來的變更記錄...${NC}"
else
    LATEST_TAG=$(get_latest_tag)
    if [[ -n "$LATEST_TAG" ]]; then
        GIT_RANGE="${LATEST_TAG}..HEAD"
        echo -e "${BLUE}生成自 ${LATEST_TAG} 以來的變更記錄...${NC}"
    else
        GIT_RANGE=""
        echo -e "${YELLOW}未找到 tags，生成所有 commits...${NC}"
    fi
fi

# 取得 commits
if [[ -n "$GIT_RANGE" ]]; then
    COMMITS=$(git log "$GIT_RANGE" --pretty=format:"%s|%h|%ai" --reverse 2>/dev/null || echo "")
else
    COMMITS=$(git log --pretty=format:"%s|%h|%ai" --reverse 2>/dev/null || echo "")
fi

if [[ -z "$COMMITS" ]]; then
    echo -e "${YELLOW}沒有找到新的 commits${NC}"
    exit 0
fi

# 分類 commits
declare -a FEAT_COMMITS=()
declare -a FIX_COMMITS=()
declare -a DOCS_COMMITS=()
declare -a REFACTOR_COMMITS=()
declare -a CHORE_COMMITS=()
declare -a PERF_COMMITS=()
declare -a TEST_COMMITS=()
declare -a OTHER_COMMITS=()

while IFS= read -r line; do
    [[ -z "$line" ]] && continue

    MESSAGE=$(echo "$line" | cut -d'|' -f1)
    HASH=$(echo "$line" | cut -d'|' -f2)

    # 解析 conventional commit
    if [[ "$MESSAGE" =~ ^feat(\(.+\))?:\ (.+) ]]; then
        SCOPE="${BASH_REMATCH[1]}"
        DESC="${BASH_REMATCH[2]}"
        FEAT_COMMITS+=("- ${DESC} (\`${HASH}\`)")
    elif [[ "$MESSAGE" =~ ^fix(\(.+\))?:\ (.+) ]]; then
        SCOPE="${BASH_REMATCH[1]}"
        DESC="${BASH_REMATCH[2]}"
        FIX_COMMITS+=("- ${DESC} (\`${HASH}\`)")
    elif [[ "$MESSAGE" =~ ^docs(\(.+\))?:\ (.+) ]]; then
        SCOPE="${BASH_REMATCH[1]}"
        DESC="${BASH_REMATCH[2]}"
        DOCS_COMMITS+=("- ${DESC} (\`${HASH}\`)")
    elif [[ "$MESSAGE" =~ ^refactor(\(.+\))?:\ (.+) ]]; then
        SCOPE="${BASH_REMATCH[1]}"
        DESC="${BASH_REMATCH[2]}"
        REFACTOR_COMMITS+=("- ${DESC} (\`${HASH}\`)")
    elif [[ "$MESSAGE" =~ ^chore(\(.+\))?:\ (.+) ]]; then
        SCOPE="${BASH_REMATCH[1]}"
        DESC="${BASH_REMATCH[2]}"
        CHORE_COMMITS+=("- ${DESC} (\`${HASH}\`)")
    elif [[ "$MESSAGE" =~ ^perf(\(.+\))?:\ (.+) ]]; then
        SCOPE="${BASH_REMATCH[1]}"
        DESC="${BASH_REMATCH[2]}"
        PERF_COMMITS+=("- ${DESC} (\`${HASH}\`)")
    elif [[ "$MESSAGE" =~ ^test(\(.+\))?:\ (.+) ]]; then
        SCOPE="${BASH_REMATCH[1]}"
        DESC="${BASH_REMATCH[2]}"
        TEST_COMMITS+=("- ${DESC} (\`${HASH}\`)")
    else
        OTHER_COMMITS+=("- ${MESSAGE} (\`${HASH}\`)")
    fi
done <<< "$COMMITS"

# 生成 CHANGELOG 內容
TODAY=$(date +%Y-%m-%d)
CHANGELOG_CONTENT=""

# Header
CHANGELOG_CONTENT+="## [Unreleased] - ${TODAY}\n\n"

# Added (feat)
if [[ ${#FEAT_COMMITS[@]} -gt 0 ]]; then
    CHANGELOG_CONTENT+="### Added\n"
    for commit in "${FEAT_COMMITS[@]}"; do
        CHANGELOG_CONTENT+="${commit}\n"
    done
    CHANGELOG_CONTENT+="\n"
fi

# Fixed (fix)
if [[ ${#FIX_COMMITS[@]} -gt 0 ]]; then
    CHANGELOG_CONTENT+="### Fixed\n"
    for commit in "${FIX_COMMITS[@]}"; do
        CHANGELOG_CONTENT+="${commit}\n"
    done
    CHANGELOG_CONTENT+="\n"
fi

# Changed (refactor)
if [[ ${#REFACTOR_COMMITS[@]} -gt 0 ]]; then
    CHANGELOG_CONTENT+="### Changed\n"
    for commit in "${REFACTOR_COMMITS[@]}"; do
        CHANGELOG_CONTENT+="${commit}\n"
    done
    CHANGELOG_CONTENT+="\n"
fi

# Documentation (docs)
if [[ ${#DOCS_COMMITS[@]} -gt 0 ]]; then
    CHANGELOG_CONTENT+="### Documentation\n"
    for commit in "${DOCS_COMMITS[@]}"; do
        CHANGELOG_CONTENT+="${commit}\n"
    done
    CHANGELOG_CONTENT+="\n"
fi

# Performance (perf)
if [[ ${#PERF_COMMITS[@]} -gt 0 ]]; then
    CHANGELOG_CONTENT+="### Performance\n"
    for commit in "${PERF_COMMITS[@]}"; do
        CHANGELOG_CONTENT+="${commit}\n"
    done
    CHANGELOG_CONTENT+="\n"
fi

# Testing (test)
if [[ ${#TEST_COMMITS[@]} -gt 0 ]]; then
    CHANGELOG_CONTENT+="### Testing\n"
    for commit in "${TEST_COMMITS[@]}"; do
        CHANGELOG_CONTENT+="${commit}\n"
    done
    CHANGELOG_CONTENT+="\n"
fi

# Maintenance (chore)
if [[ ${#CHORE_COMMITS[@]} -gt 0 ]]; then
    CHANGELOG_CONTENT+="### Maintenance\n"
    for commit in "${CHORE_COMMITS[@]}"; do
        CHANGELOG_CONTENT+="${commit}\n"
    done
    CHANGELOG_CONTENT+="\n"
fi

# Other
if [[ ${#OTHER_COMMITS[@]} -gt 0 ]]; then
    CHANGELOG_CONTENT+="### Other\n"
    for commit in "${OTHER_COMMITS[@]}"; do
        CHANGELOG_CONTENT+="${commit}\n"
    done
    CHANGELOG_CONTENT+="\n"
fi

# 輸出結果
echo ""
echo -e "${GREEN}=== 生成的 CHANGELOG ===${NC}"
echo ""
echo -e "$CHANGELOG_CONTENT"

# 統計
TOTAL=$((${#FEAT_COMMITS[@]} + ${#FIX_COMMITS[@]} + ${#DOCS_COMMITS[@]} + ${#REFACTOR_COMMITS[@]} + ${#CHORE_COMMITS[@]} + ${#PERF_COMMITS[@]} + ${#TEST_COMMITS[@]} + ${#OTHER_COMMITS[@]}))

echo -e "${BLUE}=== 統計 ===${NC}"
echo -e "  feat:     ${#FEAT_COMMITS[@]} 筆"
echo -e "  fix:      ${#FIX_COMMITS[@]} 筆"
echo -e "  docs:     ${#DOCS_COMMITS[@]} 筆"
echo -e "  refactor: ${#REFACTOR_COMMITS[@]} 筆"
echo -e "  chore:    ${#CHORE_COMMITS[@]} 筆"
echo -e "  perf:     ${#PERF_COMMITS[@]} 筆"
echo -e "  test:     ${#TEST_COMMITS[@]} 筆"
echo -e "  other:    ${#OTHER_COMMITS[@]} 筆"
echo -e "  ${GREEN}總計: ${TOTAL} 筆${NC}"

# 寫入檔案
if [[ "$PREVIEW_MODE" == false ]]; then
    if [[ -f "$OUTPUT_FILE" ]]; then
        # 插入到現有 CHANGELOG 的開頭（在 header 之後）
        echo -e "\n${YELLOW}提示: 現有 CHANGELOG 已存在${NC}"
        echo -e "新內容已顯示在上方，請手動整合到 ${OUTPUT_FILE}"
        echo -e "或使用 --output 指定新檔案"
    else
        # 創建新的 CHANGELOG
        {
            echo "# Changelog"
            echo ""
            echo "All notable changes to this project will be documented in this file."
            echo ""
            echo -e "$CHANGELOG_CONTENT"
        } > "$OUTPUT_FILE"
        echo -e "\n${GREEN}✅ 已寫入 ${OUTPUT_FILE}${NC}"
    fi
else
    echo -e "\n${YELLOW}預覽模式: 未寫入檔案${NC}"
fi

echo ""
echo -e "${GREEN}✅ 完成${NC}"
