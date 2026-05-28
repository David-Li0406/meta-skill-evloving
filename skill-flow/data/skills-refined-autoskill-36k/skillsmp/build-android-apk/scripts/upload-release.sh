#!/bin/bash
# upload-release.sh - 上传 APK 到发布渠道
# 支持阿里云 OSS 存储

set -e

PROJECT_ROOT="${1:-/Users/jietaoxie/my-prototype-logistics/frontend/CretasFoodTrace}"
APK_PATH="$2"

echo "================================================"
echo "  上传 APK 到发布渠道"
echo "================================================"
echo ""

# 如果未指定 APK 路径，查找最新的
if [ -z "$APK_PATH" ]; then
    APK_PATH="$PROJECT_ROOT/android/app/build/outputs/apk/release/app-release.apk"
fi

# 检查 APK
if [ ! -f "$APK_PATH" ]; then
    echo "❌ APK 文件不存在: $APK_PATH"
    exit 1
fi

APK_NAME=$(basename "$APK_PATH")
APK_SIZE=$(du -h "$APK_PATH" | cut -f1)
echo "APK: $APK_NAME ($APK_SIZE)"

# 获取版本信息
VERSION=$(grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' "$PROJECT_ROOT/app.json" | head -1 | cut -d'"' -f4)
DATE=$(date +%Y%m%d-%H%M%S)
RELEASE_NAME="CretasFoodTrace-v${VERSION}-${DATE}.apk"

echo "版本: $VERSION"
echo "发布名称: $RELEASE_NAME"
echo ""

# 检查阿里云 CLI
if ! command -v aliyun &> /dev/null; then
    echo "⚠️ 阿里云 CLI 未安装，跳过 OSS 上传"
    echo ""
    echo "手动上传步骤:"
    echo "  1. 登录阿里云 OSS 控制台"
    echo "  2. 上传文件: $APK_PATH"
    echo "  3. 设置公开访问权限"
    echo ""
    exit 0
fi

# 检查环境变量
if [ -z "$OSS_BUCKET" ]; then
    OSS_BUCKET="cretas-releases"
    echo "⚠️ OSS_BUCKET 未设置，使用默认: $OSS_BUCKET"
fi

if [ -z "$OSS_ENDPOINT" ]; then
    OSS_ENDPOINT="oss-cn-shanghai.aliyuncs.com"
    echo "⚠️ OSS_ENDPOINT 未设置，使用默认: $OSS_ENDPOINT"
fi

echo ""
echo "上传到 OSS..."
echo "  Bucket: $OSS_BUCKET"
echo "  Endpoint: $OSS_ENDPOINT"
echo "  目标路径: apk/$RELEASE_NAME"
echo ""

# 上传到 OSS
aliyun oss cp "$APK_PATH" "oss://$OSS_BUCKET/apk/$RELEASE_NAME" \
    --endpoint "$OSS_ENDPOINT" \
    --acl public-read

if [ $? -eq 0 ]; then
    DOWNLOAD_URL="https://$OSS_BUCKET.$OSS_ENDPOINT/apk/$RELEASE_NAME"
    echo ""
    echo "================================================"
    echo "  上传成功!"
    echo "================================================"
    echo ""
    echo "下载链接: $DOWNLOAD_URL"
    echo ""

    # 生成二维码 (如果有 qrencode)
    if command -v qrencode &> /dev/null; then
        echo "扫码下载:"
        qrencode -t ANSI256 "$DOWNLOAD_URL"
    fi
else
    echo ""
    echo "❌ 上传失败"
    exit 1
fi
