#!/bin/bash

# Configure Sparse Checkout Script
# 为 Skill 源码配置 Sparse Checkout
#
# 用法: ./configure_sparse_checkout.sh <submodule-path> <paths...>
#
# 示例:
#   ./configure_sparse_checkout.sh langgraph-python-expert/source/langgraph \
#       /README.md /libs/langgraph/ /docs/docs/ /examples/

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; exit 1; }

# 检查参数
if [ $# -lt 2 ]; then
    echo "用法: $0 <submodule-path> <paths...>"
    echo ""
    echo "参数:"
    echo "  submodule-path  Submodule 相对路径（相对于 skills 目录）"
    echo "  paths...        要保留的路径（以 / 开头）"
    echo ""
    echo "示例:"
    echo "  $0 langgraph-python-expert/source/langgraph /README.md /src/ /docs/"
    exit 1
fi

SUBMODULE_PATH="$1"
shift
PATHS=("$@")

SKILLS_DIR="$HOME/.claude/skills"
FULL_PATH="$SKILLS_DIR/$SUBMODULE_PATH"

# 检查目录是否存在
if [ ! -d "$FULL_PATH" ]; then
    error "目录不存在: $FULL_PATH"
fi

# 检查是否是 git 仓库
if [ ! -e "$FULL_PATH/.git" ]; then
    error "不是 Git 仓库: $FULL_PATH"
fi

cd "$FULL_PATH"

# 获取当前大小（配置前）
SIZE_BEFORE=$(du -sh . 2>/dev/null | cut -f1)
info "配置前大小: $SIZE_BEFORE"

# 初始化 sparse-checkout
info "初始化 Sparse Checkout..."
git sparse-checkout init --no-cone

# 设置要保留的路径
info "设置保留路径..."
git sparse-checkout set "${PATHS[@]}"

# 获取配置后大小
SIZE_AFTER=$(du -sh . 2>/dev/null | cut -f1)

success "Sparse Checkout 配置完成!"
echo ""
echo "📊 配置结果:"
echo "   配置前: $SIZE_BEFORE"
echo "   配置后: $SIZE_AFTER"
echo ""
echo "📋 保留的路径:"
git sparse-checkout list | while read line; do
    echo "   • $line"
done
echo ""
echo "📁 目录结构:"
ls -la

