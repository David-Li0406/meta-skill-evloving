#!/bin/bash
# 检查前端日志和状态
# Usage: ./check-frontend-logs.sh [check|clear|start]

set -e

ACTION="${1:-check}"
FRONTEND_DIR="/Users/jietaoxie/my-prototype-logistics/frontend/CretasFoodTrace"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${YELLOW}=== React Native 前端检查 ===${NC}"
echo ""

check_environment() {
    echo -e "${CYAN}环境检查...${NC}"

    # Node.js
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        echo -e "${GREEN}✓ Node.js: $NODE_VERSION${NC}"
    else
        echo -e "${RED}✗ Node.js 未安装${NC}"
    fi

    # npm
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        echo -e "${GREEN}✓ npm: $NPM_VERSION${NC}"
    else
        echo -e "${RED}✗ npm 未安装${NC}"
    fi

    # Expo CLI
    if command -v expo &> /dev/null || npx expo --version &> /dev/null; then
        EXPO_VERSION=$(npx expo --version 2>/dev/null || echo "已安装")
        echo -e "${GREEN}✓ Expo CLI: $EXPO_VERSION${NC}"
    else
        echo -e "${YELLOW}⚠ Expo CLI 需要安装${NC}"
    fi

    echo ""
}

check_metro() {
    echo -e "${CYAN}Metro Bundler 状态...${NC}"

    # 检查端口 3010
    if lsof -i:3010 2>/dev/null | grep -q LISTEN; then
        echo -e "${GREEN}✓ Metro 运行中 (端口 3010)${NC}"
        lsof -i:3010 | grep LISTEN | head -1
    else
        echo -e "${YELLOW}⚠ Metro 未运行${NC}"
    fi

    # 检查端口 8081 (默认)
    if lsof -i:8081 2>/dev/null | grep -q LISTEN; then
        echo -e "${GREEN}✓ Metro 运行中 (端口 8081)${NC}"
    fi

    echo ""
}

check_node_modules() {
    echo -e "${CYAN}依赖检查...${NC}"

    if [ -d "$FRONTEND_DIR/node_modules" ]; then
        MODULE_COUNT=$(ls "$FRONTEND_DIR/node_modules" 2>/dev/null | wc -l | tr -d ' ')
        echo -e "${GREEN}✓ node_modules 存在 ($MODULE_COUNT 个包)${NC}"
    else
        echo -e "${RED}✗ node_modules 不存在${NC}"
        echo "  运行: cd $FRONTEND_DIR && npm install"
    fi

    echo ""
}

check_typescript() {
    echo -e "${CYAN}TypeScript 检查...${NC}"

    cd "$FRONTEND_DIR" 2>/dev/null || {
        echo -e "${RED}✗ 无法进入前端目录${NC}"
        return 1
    }

    # 快速类型检查
    if timeout 30 npx tsc --noEmit --skipLibCheck 2>&1 | head -20; then
        echo -e "${GREEN}✓ TypeScript 编译通过${NC}"
    else
        echo -e "${YELLOW}⚠ TypeScript 有错误 (仅显示前 20 行)${NC}"
    fi

    echo ""
}

clear_cache() {
    echo -e "${CYAN}清除缓存...${NC}"

    cd "$FRONTEND_DIR" 2>/dev/null || {
        echo -e "${RED}✗ 无法进入前端目录${NC}"
        return 1
    }

    # 清除 Expo 缓存
    echo "清除 Expo 缓存..."
    npx expo start --clear --help > /dev/null 2>&1 || true

    # 清除 Metro 缓存
    echo "清除 Metro 缓存..."
    rm -rf "$TMPDIR/metro-*" 2>/dev/null || true
    rm -rf "$TMPDIR/haste-*" 2>/dev/null || true

    # 清除 watchman
    if command -v watchman &> /dev/null; then
        echo "清除 Watchman..."
        watchman watch-del-all 2>/dev/null || true
    fi

    echo -e "${GREEN}✓ 缓存已清除${NC}"
    echo ""
}

start_frontend() {
    echo -e "${CYAN}启动前端...${NC}"

    cd "$FRONTEND_DIR" 2>/dev/null || {
        echo -e "${RED}✗ 无法进入前端目录${NC}"
        return 1
    }

    echo "启动 Expo 开发服务器 (端口 3010)..."
    echo "按 Ctrl+C 停止"
    echo ""

    npx expo start --clear --port 3010
}

# 主逻辑
case $ACTION in
    check)
        check_environment
        check_node_modules
        check_metro
        ;;
    ts|typescript)
        check_typescript
        ;;
    clear)
        clear_cache
        ;;
    start)
        start_frontend
        ;;
    *)
        echo "Usage: $0 [check|typescript|clear|start]"
        echo ""
        echo "Commands:"
        echo "  check      - 检查环境和依赖"
        echo "  typescript - 运行 TypeScript 类型检查"
        echo "  clear      - 清除缓存"
        echo "  start      - 启动开发服务器"
        exit 1
        ;;
esac
