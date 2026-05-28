#!/bin/bash
# check-version.sh
# 檢查所有版本號是否一致
# 用法: ./scripts/check-version.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🔍 檢查版本號一致性..."
echo ""

# 檔案列表
FILES=(
  "skills/SKILL.md"
  ".claude-plugin/plugin.json"
  ".claude-plugin/marketplace.json"
)

# 收集所有版本
FIRST_VERSION=""
ALL_MATCH=true

for file in "${FILES[@]}"; do
  filepath="$REPO_ROOT/$file"
  if [ -f "$filepath" ]; then
    version=$(grep -oE '[0-9]+\.[0-9]+\.[0-9]+' "$filepath" | head -1)

    if [ -z "$FIRST_VERSION" ]; then
      FIRST_VERSION="$version"
      echo "  ✅ $file: $version"
    elif [ "$version" = "$FIRST_VERSION" ]; then
      echo "  ✅ $file: $version"
    else
      echo "  ❌ $file: $version (預期 $FIRST_VERSION)"
      ALL_MATCH=false
    fi
  else
    echo "  ⚠️  $file: 檔案不存在"
    ALL_MATCH=false
  fi
done

echo ""

if [ "$ALL_MATCH" = true ]; then
  echo "✅ 所有版本一致: v$FIRST_VERSION"
  exit 0
else
  echo "❌ 版本不一致！"
  echo ""
  echo "修復方式:"
  echo "  ./scripts/update-version.sh $FIRST_VERSION"
  exit 1
fi
