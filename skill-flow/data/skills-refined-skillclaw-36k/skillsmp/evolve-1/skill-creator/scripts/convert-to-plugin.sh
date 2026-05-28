#!/bin/bash
# convert-to-plugin.sh
# 將 Skills 倉庫轉換為 Claude Code Plugin 格式
# 用法: ./convert-to-plugin.sh <skills-repo-path> [--marketplace|--category]

set -e

REPO_PATH="$1"
MODE="${2:---category}"

if [ -z "$REPO_PATH" ]; then
  echo "❌ 用法: ./convert-to-plugin.sh <skills-repo-path> [--marketplace|--category]"
  echo ""
  echo "模式:"
  echo "  --marketplace  建立 marketplace.json，頂層目錄成為 plugin"
  echo "  --category     為每個頂層分類建立 plugin.json（預設）"
  exit 1
fi

if [ ! -d "$REPO_PATH" ]; then
  echo "❌ 目錄不存在: $REPO_PATH"
  exit 1
fi

REPO_NAME=$(basename "$REPO_PATH")
echo "🔄 轉換 Skills 倉庫: $REPO_NAME"
echo "   模式: $MODE"
echo ""

# 建立 .claude-plugin 目錄
mkdir -p "$REPO_PATH/.claude-plugin"

# 找出頂層分類目錄（排除隱藏目錄、docs、scripts 等）
CATEGORIES=""
for dir in "$REPO_PATH"/*/; do
  dirname=$(basename "$dir")
  # 排除非 skill 目錄
  if [[ ! "$dirname" =~ ^(\.|docs|scripts|examples|vendor|node_modules|dist|build)$ ]]; then
    # 檢查是否有 SKILL.md（在此目錄或子目錄中）
    if find "$dir" -maxdepth 2 -name "SKILL.md" -print -quit | grep -q .; then
      CATEGORIES="$CATEGORIES $dirname"
    fi
  fi
done

echo "📋 找到的分類: $CATEGORIES"
echo ""

if [ "$MODE" == "--marketplace" ]; then
  echo "📦 建立 marketplace.json..."

  # 開始 JSON
  cat > "$REPO_PATH/.claude-plugin/marketplace.json" << 'HEADER'
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
HEADER

  cat >> "$REPO_PATH/.claude-plugin/marketplace.json" << EOF
  "name": "$REPO_NAME",
  "description": "Skills collection converted to Plugin format",
  "owner": {
    "name": "$(git -C "$REPO_PATH" config user.name 2>/dev/null || echo "Unknown")",
    "email": "opensource@example.com"
  },
  "plugins": [
EOF

  FIRST=true
  for category in $CATEGORIES; do
    if [ -d "$REPO_PATH/$category" ]; then
      if [ "$FIRST" = true ]; then
        FIRST=false
      else
        echo "," >> "$REPO_PATH/.claude-plugin/marketplace.json"
      fi

      # 計算這個分類下的 skill 數量
      SKILL_COUNT=$(find "$REPO_PATH/$category" -name "SKILL.md" | wc -l | tr -d ' ')

      # 建立描述
      DESC="$SKILL_COUNT skills in $category category"

      cat >> "$REPO_PATH/.claude-plugin/marketplace.json" << EOF
    {
      "name": "$category",
      "description": "$DESC",
      "source": "./$category",
      "category": "development"
    }
EOF
      echo "  ✅ $category ($SKILL_COUNT skills)"
    fi
  done

  # 結束 JSON
  cat >> "$REPO_PATH/.claude-plugin/marketplace.json" << EOF
  ]
}
EOF

  echo ""
  echo "  ✅ marketplace.json 已建立"
  echo ""

  # 為每個分類建立 plugin.json（marketplace 模式也需要）
  echo "📦 為每個分類建立 plugin.json..."
  for category in $CATEGORIES; do
    if [ -d "$REPO_PATH/$category" ]; then
      mkdir -p "$REPO_PATH/$category/.claude-plugin"
      SKILL_COUNT=$(find "$REPO_PATH/$category" -name "SKILL.md" | wc -l | tr -d ' ')
      cat > "$REPO_PATH/$category/.claude-plugin/plugin.json" << EOF
{
  "name": "$category",
  "description": "$SKILL_COUNT skills for $category",
  "version": "1.0.0"
}
EOF
      echo "    ✅ $category/.claude-plugin/plugin.json"
    fi
  done

else
  # --category 模式：為每個頂層分類建立 plugin.json
  echo "📦 為每個分類建立 plugin.json..."

  for category in $CATEGORIES; do
    if [ -d "$REPO_PATH/$category" ]; then
      echo "  處理: $category"

      # 建立 plugin 目錄
      mkdir -p "$REPO_PATH/$category/.claude-plugin"

      # 計算 skill 數量
      SKILL_COUNT=$(find "$REPO_PATH/$category" -name "SKILL.md" | wc -l | tr -d ' ')

      # 建立 plugin.json
      cat > "$REPO_PATH/$category/.claude-plugin/plugin.json" << EOF
{
  "name": "$category",
  "description": "$SKILL_COUNT skills for $category",
  "version": "1.0.0"
}
EOF
      echo "    ✅ $category/.claude-plugin/plugin.json ($SKILL_COUNT skills)"
    fi
  done
fi

echo ""
echo "✅ 轉換完成！"
echo ""
echo "下一步:"
if [ "$MODE" == "--marketplace" ]; then
  echo "  1. cd $REPO_PATH"
  echo "  2. git add .claude-plugin/marketplace.json"
  echo "  3. git commit -m 'feat: add Plugin marketplace format'"
  echo "  4. git push"
  echo ""
  echo "安裝指令:"
  echo "  /plugin marketplace add <user>/$REPO_NAME"
  echo "  /plugin install <plugin-name>@$REPO_NAME"
else
  echo "  1. cd $REPO_PATH"
  echo "  2. git add */.claude-plugin/"
  echo "  3. git commit -m 'feat: add Plugin format to all categories'"
  echo "  4. git push"
  echo ""
  echo "各分類可獨立作為 Plugin 安裝"
fi
