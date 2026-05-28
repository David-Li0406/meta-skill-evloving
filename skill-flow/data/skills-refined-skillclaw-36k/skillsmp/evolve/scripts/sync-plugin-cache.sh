#!/bin/bash
# sync-plugin-cache.sh
# 同步當前版本到 Claude Code plugin cache
# 用法: ./scripts/sync-plugin-cache.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
PLUGIN_NAME="self-evolving-agent"
SKILL_NAME="evolve"

# 從 plugin.json 讀取版本
PLUGIN_JSON="$REPO_ROOT/.claude-plugin/plugin.json"
if [[ ! -f "$PLUGIN_JSON" ]]; then
    echo "❌ 找不到 $PLUGIN_JSON"
    exit 1
fi

VERSION=$(grep -oE '"version": "[0-9]+\.[0-9]+\.[0-9]+"' "$PLUGIN_JSON" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
if [[ -z "$VERSION" ]]; then
    echo "❌ 無法從 plugin.json 讀取版本號"
    exit 1
fi

CACHE_DIR="$HOME/.claude/plugins/cache/$PLUGIN_NAME/$SKILL_NAME/$VERSION"

echo "🔄 同步 plugin cache..."
echo "   版本: v$VERSION"
echo "   來源: $REPO_ROOT"
echo "   目標: $CACHE_DIR"
echo ""

# 清除該版本的舊 cache（如果存在）
if [[ -d "$CACHE_DIR" ]]; then
    echo "🗑️  清除舊 cache..."
    rm -rf "$CACHE_DIR"
fi

# 建立目錄
mkdir -p "$CACHE_DIR"

# 使用 rsync 同步（包括隱藏檔案）
echo "📦 複製檔案..."
rsync -av --quiet \
    --exclude='.git' \
    --exclude='.github' \
    --exclude='node_modules' \
    --exclude='__pycache__' \
    --exclude='.DS_Store' \
    "$REPO_ROOT/" "$CACHE_DIR/"

# 驗證
echo ""
echo "✅ 同步完成！"
echo ""

# 驗證關鍵文件
echo "📋 驗證:"
if [[ -f "$CACHE_DIR/.claude-plugin/plugin.json" ]]; then
    cache_version=$(grep -oE '"version": "[0-9]+\.[0-9]+\.[0-9]+"' "$CACHE_DIR/.claude-plugin/plugin.json" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
    if [[ "$cache_version" == "$VERSION" ]]; then
        echo "   ✅ plugin.json: v$cache_version"
    else
        echo "   ❌ plugin.json 版本不匹配: $cache_version (預期 $VERSION)"
        exit 1
    fi
else
    echo "   ❌ plugin.json 不存在"
    exit 1
fi

if [[ -f "$CACHE_DIR/skills/SKILL.md" ]]; then
    skill_version=$(grep -oE '^version: [0-9]+\.[0-9]+\.[0-9]+' "$CACHE_DIR/skills/SKILL.md" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
    if [[ "$skill_version" == "$VERSION" ]]; then
        echo "   ✅ SKILL.md: v$skill_version"
    else
        echo "   ❌ SKILL.md 版本不匹配: $skill_version (預期 $VERSION)"
        exit 1
    fi
else
    echo "   ❌ SKILL.md 不存在"
    exit 1
fi

echo ""
echo "🎉 Plugin cache 已更新到 v$VERSION"
echo "   下次啟動 Claude Code 時將自動載入新版本"
