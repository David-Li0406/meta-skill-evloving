#!/bin/bash
# install-device.sh - 安装 APK 到连接的设备
# 支持真机和模拟器

set -e

PROJECT_ROOT="${1:-/Users/jietaoxie/my-prototype-logistics/frontend/CretasFoodTrace}"
BUILD_TYPE="${2:-release}"  # debug 或 release

echo "================================================"
echo "  安装 APK 到设备"
echo "================================================"
echo ""

# 设置 Android SDK
export ANDROID_HOME="${ANDROID_HOME:-$HOME/Library/Android/sdk}"
ADB="$ANDROID_HOME/platform-tools/adb"

# 检查 adb
if [ ! -f "$ADB" ]; then
    echo "❌ adb 未找到: $ADB"
    exit 1
fi

# 检查设备连接
echo "检查连接的设备..."
DEVICES=$("$ADB" devices | grep -v "List" | grep -v "^$" | wc -l)

if [ "$DEVICES" -eq 0 ]; then
    echo "❌ 没有连接的设备"
    echo ""
    echo "请确保:"
    echo "  1. USB 调试已启用"
    echo "  2. 设备已通过 USB 连接"
    echo "  3. 或 Android 模拟器正在运行"
    exit 1
fi

echo "找到 $DEVICES 个设备:"
"$ADB" devices -l | grep -v "List"
echo ""

# 确定 APK 路径
if [ "$BUILD_TYPE" = "release" ]; then
    APK_PATH="$PROJECT_ROOT/android/app/build/outputs/apk/release/app-release.apk"
else
    APK_PATH="$PROJECT_ROOT/android/app/build/outputs/apk/debug/app-debug.apk"
fi

# 检查 APK 是否存在
if [ ! -f "$APK_PATH" ]; then
    echo "❌ APK 文件不存在: $APK_PATH"
    echo "   请先运行 build-apk.sh"
    exit 1
fi

APK_SIZE=$(du -h "$APK_PATH" | cut -f1)
echo "APK: $APK_PATH ($APK_SIZE)"
echo ""

# 安装 APK
echo "安装 APK..."
"$ADB" install -r "$APK_PATH"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 安装成功!"
    echo ""

    # 启动应用
    echo "启动应用..."
    PACKAGE_NAME="com.cretas.foodtrace"
    "$ADB" shell am start -n "$PACKAGE_NAME/.MainActivity" 2>/dev/null || \
    "$ADB" shell monkey -p "$PACKAGE_NAME" -c android.intent.category.LAUNCHER 1 2>/dev/null || \
    echo "⚠️ 无法自动启动应用，请手动打开"

    echo ""
    echo "================================================"
    echo "  安装完成!"
    echo "================================================"
else
    echo ""
    echo "❌ 安装失败"
    exit 1
fi
