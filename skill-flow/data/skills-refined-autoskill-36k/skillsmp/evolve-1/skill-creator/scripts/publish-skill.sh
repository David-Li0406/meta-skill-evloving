#!/bin/bash
# Skill 發布腳本
# 用法: ./publish-skill.sh <skill-directory> [--new-repo]

set -e

SKILL_DIR="$1"
NEW_REPO="$2"

if [ -z "$SKILL_DIR" ]; then
  echo "❌ 用法: ./publish-skill.sh <skill-directory> [--new-repo]"
  exit 1
fi

if [ ! -d "$SKILL_DIR" ]; then
  echo "❌ 目錄不存在: $SKILL_DIR"
  exit 1
fi

SKILL_FILE="$SKILL_DIR/SKILL.md"
SKILL_NAME=$(grep "^name:" "$SKILL_FILE" | sed 's/name: *//')
SKILL_DESC=$(grep "^description:" "$SKILL_FILE" | sed 's/description: *//')

echo "📦 準備發布 Skill: $SKILL_NAME"
echo "   描述: $SKILL_DESC"
echo ""

# 生成 README.md
README_FILE="$SKILL_DIR/README.md"
if [ ! -f "$README_FILE" ]; then
  echo "📝 生成 README.md..."
  cat > "$README_FILE" << EOF
# $SKILL_NAME

> $SKILL_DESC

## 安裝

\`\`\`bash
/plugin install <user>/<repo>
\`\`\`

## 使用

參見 SKILL.md

## License

MIT
EOF
  echo "  ✅ README.md 已生成"
fi

# Git 操作
cd "$SKILL_DIR"

if [ "$NEW_REPO" == "--new-repo" ]; then
  echo ""
  echo "🆕 建立新 repo..."
  if [ ! -d ".git" ]; then
    git init
    echo "  ✅ git init 完成"
  fi
fi

if [ -d ".git" ]; then
  echo ""
  echo "📤 準備 commit..."
  git add -A
  git status
  echo ""
  echo "⏸️ 請手動執行:"
  echo "   git commit -m 'feat: initial skill release'"
  echo "   git remote add origin <your-repo-url>"
  echo "   git push -u origin main"
else
  echo ""
  echo "⚠️ 不是 git repo，請先執行:"
  echo "   cd $SKILL_DIR"
  echo "   git init"
fi

echo ""
echo "✅ 發布準備完成！"
