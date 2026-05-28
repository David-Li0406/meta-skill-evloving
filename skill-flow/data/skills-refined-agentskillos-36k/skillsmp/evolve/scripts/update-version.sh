#!/bin/bash
# update-version.sh
# 統一更新所有版本號，確保一致性
# 用法: ./scripts/update-version.sh <new-version>

set -e

NEW_VERSION="$1"

if [ -z "$NEW_VERSION" ]; then
  echo "❌ 用法: ./scripts/update-version.sh <new-version>"
  echo ""
  echo "範例: ./scripts/update-version.sh 5.4.0"
  echo ""
  echo "會更新以下檔案:"
  echo "  - skills/SKILL.md"
  echo "  - .claude-plugin/plugin.json"
  echo "  - .claude-plugin/marketplace.json"
  exit 1
fi

# 驗證版本格式
if ! [[ "$NEW_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "❌ 版本格式錯誤: $NEW_VERSION"
  echo "   正確格式: X.Y.Z (例如 5.3.0)"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🔄 更新版本號至 v$NEW_VERSION"
echo ""

# 檔案列表
FILES=(
  "skills/SKILL.md"
  ".claude-plugin/plugin.json"
  ".claude-plugin/marketplace.json"
  "README.md"
)

# 顯示當前版本
echo "📋 當前版本:"
for file in "${FILES[@]}"; do
  filepath="$REPO_ROOT/$file"
  if [ -f "$filepath" ]; then
    current=$(grep -oE '"?version"?:?\s*"?[0-9]+\.[0-9]+\.[0-9]+"?' "$filepath" 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
    echo "  $file: ${current:-unknown}"
  fi
done
echo ""

# 更新 skills/SKILL.md
echo "📝 更新 skills/SKILL.md..."
sed -i '' -E "s/^version: [0-9]+\.[0-9]+\.[0-9]+$/version: $NEW_VERSION/" "$REPO_ROOT/skills/SKILL.md"
sed -i '' -E "s/Self-Evolving Agent v[0-9]+\.[0-9]+\.[0-9]+/Self-Evolving Agent v$NEW_VERSION/" "$REPO_ROOT/skills/SKILL.md"

# 更新 .claude-plugin/plugin.json
echo "📝 更新 .claude-plugin/plugin.json..."
sed -i '' -E "s/\"version\": \"[0-9]+\.[0-9]+\.[0-9]+\"/\"version\": \"$NEW_VERSION\"/" "$REPO_ROOT/.claude-plugin/plugin.json"

# 更新 .claude-plugin/marketplace.json
echo "📝 更新 .claude-plugin/marketplace.json..."
sed -i '' -E "s/\"version\": \"[0-9]+\.[0-9]+\.[0-9]+\"/\"version\": \"$NEW_VERSION\"/" "$REPO_ROOT/.claude-plugin/marketplace.json"

# 更新 README.md badge
echo "📝 更新 README.md badge..."
sed -i '' -E "s/version-[0-9]+\.[0-9]+\.[0-9]+-blue/version-$NEW_VERSION-blue/" "$REPO_ROOT/README.md"

echo ""
echo "✅ 版本更新完成！"
echo ""

# 驗證結果
echo "📋 更新後版本:"
for file in "${FILES[@]}"; do
  filepath="$REPO_ROOT/$file"
  if [ -f "$filepath" ]; then
    current=$(grep -oE '"?version"?:?\s*"?[0-9]+\.[0-9]+\.[0-9]+"?' "$filepath" 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
    if [ "$current" = "$NEW_VERSION" ]; then
      echo "  ✅ $file: $current"
    else
      echo "  ❌ $file: $current (預期 $NEW_VERSION)"
    fi
  fi
done

echo ""
echo "下一步:"
echo "  1. 更新 CHANGELOG.md"
echo "  2. git add -A && git commit -m 'chore: bump version to v$NEW_VERSION'"
echo "  3. git tag -a v$NEW_VERSION -m 'Release v$NEW_VERSION'"
echo "  4. git push && git push --tags"
echo "  5. ./scripts/sync-plugin-cache.sh  # 同步到本地 plugin cache"
echo "  6. gh release create v$NEW_VERSION --generate-notes (可選)"
