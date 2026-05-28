#!/bin/bash
# build-apk.sh - 构建 Android APK
# 支持 Debug 和 Release 两种模式

set -e

PROJECT_ROOT="${1:-/Users/jietaoxie/my-prototype-logistics/frontend/CretasFoodTrace}"
BUILD_TYPE="${2:-release}"  # debug 或 release

echo "================================================"
echo "  构建 Android APK"
echo "  模式: $BUILD_TYPE"
echo "================================================"
echo ""

cd "$PROJECT_ROOT"

# 设置 Java 环境
if [ -d "/Library/Java/JavaVirtualMachines/jdk-17.0.1.jdk/Contents/Home" ]; then
    export JAVA_HOME="/Library/Java/JavaVirtualMachines/jdk-17.0.1.jdk/Contents/Home"
elif [ -d "/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home" ]; then
    export JAVA_HOME="/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home"
fi
echo "JAVA_HOME: $JAVA_HOME"

# 设置 Android SDK
export ANDROID_HOME="${ANDROID_HOME:-$HOME/Library/Android/sdk}"
export PATH="$PATH:$ANDROID_HOME/platform-tools"
echo "ANDROID_HOME: $ANDROID_HOME"
echo ""

# 1. 检查并安装依赖
if [ ! -d "node_modules" ]; then
    echo "安装 npm 依赖..."
    npm install
fi

# 2. 执行 Expo prebuild (如果需要)
if [ ! -d "android" ]; then
    echo "执行 Expo prebuild..."
    npx expo prebuild --platform android
fi

# 3. 进入 android 目录构建
cd android

# 4. 清理之前的构建
echo "清理之前的构建..."
./gradlew clean --quiet

# 5. 执行构建
if [ "$BUILD_TYPE" = "release" ]; then
    echo "构建 Release APK..."
    ./gradlew assembleRelease --no-daemon --console=plain

    APK_PATH="app/build/outputs/apk/release/app-release.apk"
else
    echo "构建 Debug APK..."
    ./gradlew assembleDebug --no-daemon --console=plain

    APK_PATH="app/build/outputs/apk/debug/app-debug.apk"
fi

# 6. 检查构建结果
if [ -f "$APK_PATH" ]; then
    APK_SIZE=$(du -h "$APK_PATH" | cut -f1)
    echo ""
    echo "================================================"
    echo "  构建成功!"
    echo "================================================"
    echo "  APK 路径: $PROJECT_ROOT/android/$APK_PATH"
    echo "  APK 大小: $APK_SIZE"
    echo ""

    # 复制到项目根目录
    VERSION=$(grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' "$PROJECT_ROOT/app.json" | head -1 | cut -d'"' -f4)
    DATE=$(date +%Y%m%d)
    OUTPUT_NAME="CretasFoodTrace-${BUILD_TYPE}-v${VERSION}-${DATE}.apk"

    cp "$APK_PATH" "$PROJECT_ROOT/../../../$OUTPUT_NAME"
    echo "  已复制到: $OUTPUT_NAME"

    exit 0
else
    echo ""
    echo "❌ 构建失败，APK 文件未生成"
    exit 1
fi
