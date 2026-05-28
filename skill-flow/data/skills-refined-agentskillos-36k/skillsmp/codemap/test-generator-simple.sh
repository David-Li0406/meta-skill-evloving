#!/bin/bash

set -e

echo "🧪 Testing CodeMap Generator (Simple)..."
echo ""

cd /Users/dengwenyu/.pi/agent/skills/codemap

QUERY="分析前端组件结构"
PROJECT_ROOT="/Users/dengwenyu/.pi/agent/skills/codemap"
FILES='["/Users/dengwenyu/.pi/agent/skills/codemap/client/src/App.tsx"]'

echo "📝 Query: $QUERY"
echo "📁 Project Root: $PROJECT_ROOT"
echo "📄 Files: $FILES"
echo ""

echo "🚀 Running generator..."
bun run generator/src/index.ts generate "$QUERY" "$FILES" "$PROJECT_ROOT" fast pi 2>&1 | tee /tmp/generator-test.log

echo ""
echo "✅ Test complete"
