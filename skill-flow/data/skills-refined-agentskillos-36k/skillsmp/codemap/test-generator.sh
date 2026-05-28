#!/bin/bash

set -e

echo "🧪 Testing CodeMap Generator..."
echo ""

cd /Users/dengwenyu/.pi/agent/skills/codemap

# 测试参数
QUERY="分析前端路由流程和状态管理"
PROJECT_ROOT="/Users/dengwenyu/.pi/agent/skills/codemap"

FILES='[
  "'"$PROJECT_ROOT"'/client/src/App.tsx",
  "'"$PROJECT_ROOT"'/client/src/stores/codemapStore.ts",
  "'"$PROJECT_ROOT"'/client/src/components/MainPanel.tsx"
]'

echo "📝 Query: $QUERY"
echo "📁 Project Root: $PROJECT_ROOT"
echo "📄 Files: $(echo $FILES | jq 'length')"
echo ""

echo "🚀 Running generator..."
bun run generator/src/index.ts generate "$QUERY" "$FILES" "$PROJECT_ROOT" fast pi 2>&1 | tee /tmp/generator-output.log

echo ""
echo "✅ Test complete"
