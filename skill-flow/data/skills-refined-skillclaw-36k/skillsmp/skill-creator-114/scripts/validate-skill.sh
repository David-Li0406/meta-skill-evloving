#!/bin/bash
# Skill 驗證腳本
# 用法: ./validate-skill.sh <skill-directory>

set -e

SKILL_DIR="$1"

if [ -z "$SKILL_DIR" ]; then
  echo "❌ 用法: ./validate-skill.sh <skill-directory>"
  exit 1
fi

if [ ! -d "$SKILL_DIR" ]; then
  echo "❌ 目錄不存在: $SKILL_DIR"
  exit 1
fi

SKILL_FILE="$SKILL_DIR/SKILL.md"

if [ ! -f "$SKILL_FILE" ]; then
  echo "❌ SKILL.md 不存在"
  exit 1
fi

echo "🔍 驗證 Skill: $SKILL_DIR"
echo ""

# 檢查 frontmatter
echo "檢查 frontmatter..."

if ! head -1 "$SKILL_FILE" | grep -q "^---$"; then
  echo "  ❌ 缺少 frontmatter 開頭 (---)"
  exit 1
fi
echo "  ✅ frontmatter 開頭存在"

# 檢查必要欄位
if ! grep -q "^name:" "$SKILL_FILE"; then
  echo "  ❌ 缺少 name 欄位"
  exit 1
fi
echo "  ✅ name 欄位存在"

if ! grep -q "^description:" "$SKILL_FILE"; then
  echo "  ❌ 缺少 description 欄位"
  exit 1
fi
echo "  ✅ description 欄位存在"

if ! grep -q "^version:" "$SKILL_FILE"; then
  echo "  ❌ 缺少 version 欄位"
  exit 1
fi
echo "  ✅ version 欄位存在"

# 檢查 scripts 是否可執行
if [ -d "$SKILL_DIR/scripts" ]; then
  echo ""
  echo "檢查 scripts..."
  for script in "$SKILL_DIR/scripts/"*.sh; do
    if [ -f "$script" ]; then
      if [ -x "$script" ]; then
        echo "  ✅ $script 可執行"
      else
        echo "  ⚠️ $script 不可執行，正在修正..."
        chmod +x "$script"
        echo "  ✅ 已修正"
      fi
    fi
  done
fi

echo ""
echo "✅ 驗證通過！"
