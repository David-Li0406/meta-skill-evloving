#!/bin/bash
# Self-Evolving Agent - Memory Validation Script
# 驗證 .claude/memory/ 的完整性和一致性

set -e

MEMORY_DIR="${1:-.claude/memory}"
INDEX_FILE="$MEMORY_DIR/index.md"
ERRORS=0
WARNINGS=0

echo "🔍 Validating Memory System: $MEMORY_DIR"
echo ""

# 檢查目錄是否存在
if [[ ! -d "$MEMORY_DIR" ]]; then
    echo "❌ Memory directory not found: $MEMORY_DIR"
    exit 1
fi

# 檢查 index.md 是否存在
if [[ ! -f "$INDEX_FILE" ]]; then
    echo "❌ index.md not found"
    ERRORS=$((ERRORS + 1))
else
    echo "✅ index.md exists"
fi

# 檢查必要子目錄
REQUIRED_DIRS=("learnings" "failures" "decisions" "patterns" "strategies" "discoveries")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [[ -d "$MEMORY_DIR/$dir" ]]; then
        count=$(find "$MEMORY_DIR/$dir" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
        echo "✅ $dir/ exists ($count files)"
    else
        echo "⚠️  $dir/ not found (optional)"
        WARNINGS=$((WARNINGS + 1))
    fi
done

echo ""
echo "📊 Index Consistency Check"
echo ""

# 檢查 index.md 中的連結是否有效
if [[ -f "$INDEX_FILE" ]]; then
    # 提取所有 markdown 連結
    links=$(grep -oE '\[.*\]\([^)]+\.md\)' "$INDEX_FILE" 2>/dev/null | grep -oE '\([^)]+\.md\)' | tr -d '()' || true)

    if [[ -z "$links" ]]; then
        echo "⚠️  No markdown links found in index.md"
        WARNINGS=$((WARNINGS + 1))
    else
        for link in $links; do
            # 處理相對路徑
            full_path="$MEMORY_DIR/$link"
            if [[ -f "$full_path" ]]; then
                echo "✅ $link"
            else
                echo "❌ $link (file not found)"
                ERRORS=$((ERRORS + 1))
            fi
        done
    fi
fi

echo ""
echo "📂 Orphan Files Check (files not in index)"
echo ""

# 找出不在 index.md 中的文件
for dir in "${REQUIRED_DIRS[@]}"; do
    if [[ -d "$MEMORY_DIR/$dir" ]]; then
        for file in "$MEMORY_DIR/$dir"/*.md; do
            [[ ! -f "$file" ]] && continue
            filename=$(basename "$file")
            relative_path="$dir/$filename"

            if ! grep -q "$relative_path" "$INDEX_FILE" 2>/dev/null; then
                echo "⚠️  Orphan: $relative_path (not in index)"
                WARNINGS=$((WARNINGS + 1))
            fi
        done
    fi
done

echo ""
echo "════════════════════════════════════════"
echo "📋 Summary"
echo "════════════════════════════════════════"
echo "   Errors:   $ERRORS"
echo "   Warnings: $WARNINGS"
echo ""

if [[ $ERRORS -gt 0 ]]; then
    echo "❌ Validation FAILED"
    echo ""
    echo "Fix suggestions:"
    echo "  1. Update index.md to include all memory files"
    echo "  2. Remove broken links from index.md"
    echo "  3. Run: scripts/sync-global.sh to regenerate"
    exit 1
elif [[ $WARNINGS -gt 0 ]]; then
    echo "⚠️  Validation PASSED with warnings"
    exit 0
else
    echo "✅ Validation PASSED"
    exit 0
fi
