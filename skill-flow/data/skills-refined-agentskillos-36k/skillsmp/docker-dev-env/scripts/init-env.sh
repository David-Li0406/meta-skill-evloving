#!/bin/bash
# 初始化 Docker 开发环境
# 生成 .env 文件，包含宿主机用户信息

set -e

ENV_FILE=".env"

# 检查是否已存在 .env 文件
if [ -f "$ENV_FILE" ]; then
    read -p ".env 文件已存在，是否覆盖？[y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "保留现有 .env 文件"
        exit 0
    fi
fi

# 获取当前用户信息
HOST_UID=$(id -u)
HOST_GID=$(id -g)
HOST_USER=$(whoami)

# 生成 .env 文件
cat > "$ENV_FILE" << EOF
# Docker 开发环境配置
# 由 init-env.sh 自动生成于 $(date)

# 宿主机用户信息（用于容器内权限映射）
HOST_UID=${HOST_UID}
HOST_GID=${HOST_GID}
HOST_USER=${HOST_USER}

# 项目名称（用于容器命名）
COMPOSE_PROJECT_NAME=dev

# 可选配置
# MIRROR_SOURCE=tuna  # 可选: tuna, aliyun, ustc
EOF

echo "✅ .env 文件已生成"
echo "   HOST_UID: ${HOST_UID}"
echo "   HOST_GID: ${HOST_GID}"
echo "   HOST_USER: ${HOST_USER}"
echo ""
echo "现在可以运行 docker compose up 启动开发环境"
