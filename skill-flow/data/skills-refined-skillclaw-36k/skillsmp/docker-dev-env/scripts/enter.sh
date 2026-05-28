#!/bin/bash
# 进入开发容器
# 用法: ./enter.sh [容器名称] [shell]

set -e

# 默认值
DEFAULT_SHELL="/bin/bash"
CONTAINER_NAME="${1:-dev}"
SHELL_CMD="${2:-$DEFAULT_SHELL}"

# 检查容器是否运行
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "❌ 容器 '${CONTAINER_NAME}' 未运行"
    echo ""
    echo "可用的运行中容器:"
    docker ps --format '  - {{.Names}}'
    echo ""
    echo "用法: $0 [容器名称] [shell]"
    exit 1
fi

# 进入容器
echo "🚀 进入容器: ${CONTAINER_NAME}"
docker exec -it "${CONTAINER_NAME}" "${SHELL_CMD}"
