#!/bin/bash
# pre-build-check.sh - 构建前环境检查
# 检查所有必需的依赖和配置

set -e

PROJECT_ROOT="${1:-/Users/jietaoxie/my-prototype-logistics/frontend/CretasFoodTrace}"

echo "================================================"
echo "  APK 构建前检查"
echo "================================================"
echo ""

ERRORS=0
WARNINGS=0

# 1. 检查项目目录
echo "1. 检查项目目录..."
if [ ! -d "$PROJECT_ROOT" ]; then
    echo "   ❌ 项目目录不存在: $PROJECT_ROOT"
    exit 1
fi
echo "   ✅ 项目目录: $PROJECT_ROOT"

# 2. 检查 Node.js
echo "2. 检查 Node.js..."
if ! command -v node &> /dev/null; then
    echo "   ❌ Node.js 未安装"
    ((ERRORS++))
else
    NODE_VERSION=$(node --version)
    echo "   ✅ Node.js: $NODE_VERSION"
fi

# 3. 检查 npm
echo "3. 检查 npm..."
if ! command -v npm &> /dev/null; then
    echo "   ❌ npm 未安装"
    ((ERRORS++))
else
    NPM_VERSION=$(npm --version)
    echo "   ✅ npm: $NPM_VERSION"
fi

# 4. 检查 Java 17
echo "4. 检查 Java..."
if [ -d "/Library/Java/JavaVirtualMachines/jdk-17.0.1.jdk" ]; then
    echo "   ✅ JDK 17: /Library/Java/JavaVirtualMachines/jdk-17.0.1.jdk"
elif [ -d "/Library/Java/JavaVirtualMachines/jdk-17.jdk" ]; then
    echo "   ✅ JDK 17: /Library/Java/JavaVirtualMachines/jdk-17.jdk"
else
    echo "   ⚠️ JDK 17 未在默认位置找到"
    ((WARNINGS++))
fi

# 5. 检查 Android SDK
echo "5. 检查 Android SDK..."
ANDROID_HOME="${ANDROID_HOME:-$HOME/Library/Android/sdk}"
if [ -d "$ANDROID_HOME" ]; then
    echo "   ✅ Android SDK: $ANDROID_HOME"

    # 检查 platform-tools
    if [ -d "$ANDROID_HOME/platform-tools" ]; then
        echo "   ✅ platform-tools: 已安装"
    else
        echo "   ⚠️ platform-tools: 缺失"
        ((WARNINGS++))
    fi

    # 检查 build-tools
    if [ -d "$ANDROID_HOME/build-tools" ]; then
        BUILD_TOOLS=$(ls "$ANDROID_HOME/build-tools" | tail -1)
        echo "   ✅ build-tools: $BUILD_TOOLS"
    else
        echo "   ❌ build-tools: 缺失"
        ((ERRORS++))
    fi
else
    echo "   ❌ Android SDK 未安装"
    ((ERRORS++))
fi

# 6. 检查 node_modules
echo "6. 检查依赖..."
cd "$PROJECT_ROOT"
if [ -d "node_modules" ]; then
    echo "   ✅ node_modules: 已安装"
else
    echo "   ⚠️ node_modules: 缺失，需要运行 npm install"
    ((WARNINGS++))
fi

# 7. 检查 android 目录
echo "7. 检查 Android 项目..."
if [ -d "android" ]; then
    echo "   ✅ android 目录: 已存在"
else
    echo "   ⚠️ android 目录: 缺失，需要运行 npx expo prebuild"
    ((WARNINGS++))
fi

# 8. TypeScript 类型检查
echo "8. TypeScript 类型检查..."
if [ -f "node_modules/.bin/tsc" ]; then
    TYPE_ERRORS=$(timeout 60 npx tsc --noEmit --skipLibCheck 2>&1 | grep -c "error TS" || echo "0")
    if [ "$TYPE_ERRORS" -gt 0 ]; then
        echo "   ⚠️ TypeScript 错误: $TYPE_ERRORS 个"
        ((WARNINGS++))
    else
        echo "   ✅ TypeScript: 无错误"
    fi
else
    echo "   ⚠️ tsc 不可用，跳过类型检查"
fi

# 9. 检查 app.json 配置
echo "9. 检查 app.json..."
if [ -f "app.json" ]; then
    APP_NAME=$(cat app.json | grep -o '"name"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | cut -d'"' -f4)
    APP_VERSION=$(cat app.json | grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | cut -d'"' -f4)
    echo "   ✅ App Name: $APP_NAME"
    echo "   ✅ Version: $APP_VERSION"
else
    echo "   ❌ app.json 不存在"
    ((ERRORS++))
fi

# 10. 检查签名配置
echo "10. 检查签名配置..."
if [ -f "android/app/build.gradle" ]; then
    if grep -q "signingConfigs" android/app/build.gradle; then
        echo "   ✅ 签名配置: 已配置"
    else
        echo "   ⚠️ 签名配置: 使用默认调试签名"
        ((WARNINGS++))
    fi
else
    echo "   ⚠️ build.gradle 不存在 (prebuild 后生成)"
fi

echo ""
echo "================================================"
echo "  检查结果"
echo "================================================"
echo "  错误: $ERRORS 个"
echo "  警告: $WARNINGS 个"
echo ""

if [ $ERRORS -gt 0 ]; then
    echo "❌ 构建前检查失败，请修复上述错误"
    exit 1
else
    echo "✅ 构建前检查通过"
    exit 0
fi
