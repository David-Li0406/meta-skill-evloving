#!/bin/bash
# 检查数据库连接
# Usage: ./check-db-connection.sh [local|remote]

set -e

TARGET="${1:-local}"
SERVER="root@139.196.165.140"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${YELLOW}=== 数据库连接检查 ===${NC}"
echo ""

check_local_mysql() {
    echo -e "${CYAN}检查本地 MySQL...${NC}"

    # 检查 MySQL 服务
    if command -v mysql &> /dev/null; then
        echo -e "${GREEN}✓ MySQL 客户端已安装${NC}"
    else
        echo -e "${RED}✗ MySQL 客户端未安装${NC}"
        return 1
    fi

    # 检查服务状态
    if mysql.server status 2>/dev/null | grep -q "running"; then
        echo -e "${GREEN}✓ MySQL 服务运行中${NC}"
    elif pgrep -x mysqld > /dev/null; then
        echo -e "${GREEN}✓ MySQL 进程运行中${NC}"
    else
        echo -e "${RED}✗ MySQL 服务未运行${NC}"
        echo "  启动命令: mysql.server start"
        return 1
    fi

    # 测试连接
    if mysql -u root -e "SELECT 1" 2>/dev/null | grep -q 1; then
        echo -e "${GREEN}✓ 数据库连接成功${NC}"

        # 检查数据库
        echo ""
        echo -e "${CYAN}可用数据库:${NC}"
        mysql -u root -e "SHOW DATABASES" 2>/dev/null | grep -E "cretas|mall|aims" || echo "  无相关数据库"

        # 检查 cretas 表
        if mysql -u root -e "USE cretas_db; SHOW TABLES" 2>/dev/null | head -10; then
            echo "  ... (更多表)"
        fi
    else
        echo -e "${RED}✗ 数据库连接失败${NC}"
        echo "  检查用户名密码或权限"
        return 1
    fi
}

check_remote_mysql() {
    echo -e "${CYAN}检查远程 MySQL (139.196.165.140)...${NC}"

    # 通过 SSH 检查
    if ssh $SERVER "systemctl status mysql 2>/dev/null || service mysql status 2>/dev/null" | grep -q "active\|running"; then
        echo -e "${GREEN}✓ 远程 MySQL 服务运行中${NC}"
    else
        echo -e "${YELLOW}⚠ 无法确认远程 MySQL 状态${NC}"
    fi

    # 检查端口
    if ssh $SERVER "netstat -tlnp 2>/dev/null | grep 3306"; then
        echo -e "${GREEN}✓ MySQL 端口 3306 监听中${NC}"
    else
        echo -e "${RED}✗ MySQL 端口未监听${NC}"
    fi

    # 检查数据库
    echo ""
    echo -e "${CYAN}检查数据库...${NC}"
    ssh $SERVER "mysql -u root -e 'SHOW DATABASES' 2>/dev/null" | grep -E "cretas|mall|aims" || echo "  需要密码或权限不足"
}

check_redis() {
    echo ""
    echo -e "${YELLOW}=== Redis 检查 ===${NC}"

    if [ "$TARGET" = "local" ]; then
        if redis-cli ping 2>/dev/null | grep -q PONG; then
            echo -e "${GREEN}✓ 本地 Redis 运行中${NC}"
        else
            echo -e "${YELLOW}⚠ 本地 Redis 未运行${NC}"
        fi
    else
        if ssh $SERVER "redis-cli ping 2>/dev/null" | grep -q PONG; then
            echo -e "${GREEN}✓ 远程 Redis 运行中${NC}"
        else
            echo -e "${YELLOW}⚠ 远程 Redis 未运行或未安装${NC}"
        fi
    fi
}

# 主逻辑
case $TARGET in
    local)
        check_local_mysql
        check_redis
        ;;
    remote)
        check_remote_mysql
        check_redis
        ;;
    *)
        echo "Usage: $0 [local|remote]"
        exit 1
        ;;
esac

echo ""
echo -e "${YELLOW}=== 完成 ===${NC}"
