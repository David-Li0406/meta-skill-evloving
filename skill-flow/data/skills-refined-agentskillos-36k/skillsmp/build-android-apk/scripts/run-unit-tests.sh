#!/bin/bash
# run-unit-tests.sh - 运行单元测试
# 在构建 APK 前运行 Jest 测试

set -e

PROJECT_ROOT="${1:-/Users/jietaoxie/my-prototype-logistics/frontend/CretasFoodTrace}"

echo "================================================"
echo "  运行单元测试"
echo "================================================"
echo ""

cd "$PROJECT_ROOT"

# 检查是否有测试配置
if [ ! -f "jest.config.js" ] && [ ! -f "jest.config.json" ] && ! grep -q '"jest"' package.json 2>/dev/null; then
    echo "⚠️ 未找到 Jest 配置，跳过测试"
    exit 0
fi

# 检查是否有测试文件
TEST_FILES=$(find src -name "*.test.ts" -o -name "*.test.tsx" -o -name "*.spec.ts" -o -name "*.spec.tsx" 2>/dev/null | wc -l)
if [ "$TEST_FILES" -eq 0 ]; then
    echo "⚠️ 未找到测试文件，跳过测试"
    exit 0
fi

echo "找到 $TEST_FILES 个测试文件"
echo ""

# 运行测试
echo "运行 Jest 测试..."
npm test -- --passWithNoTests --coverage --coverageReporters=text-summary 2>&1 | tail -30

TEST_EXIT_CODE=${PIPESTATUS[0]}

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ 所有测试通过"
    exit 0
else
    echo ""
    echo "❌ 测试失败，请修复后重新构建"
    exit 1
fi
