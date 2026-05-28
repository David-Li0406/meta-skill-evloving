#!/bin/bash

# Add Source Submodule Script
# 为 Claude Code Skill 添加源码引用（Git Submodule + Sparse Checkout）
#
# 用法: ./add_source_submodule.sh <skill-name> <repo-url> [repo-name]
#
# 示例:
#   ./add_source_submodule.sh langgraph-python-expert https://github.com/langchain-ai/langgraph.git
#   ./add_source_submodule.sh my-skill https://github.com/org/repo.git custom-name

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印函数
info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; exit 1; }

# 检查参数
if [ $# -lt 2 ]; then
    echo "用法: $0 <skill-name> <repo-url> [repo-name]"
    echo ""
    echo "参数:"
    echo "  skill-name  技能目录名称"
    echo "  repo-url    Git 仓库 URL"
    echo "  repo-name   可选，submodule 目录名（默认从 URL 提取）"
    echo ""
    echo "示例:"
    echo "  $0 langgraph-python-expert https://github.com/langchain-ai/langgraph.git"
    exit 1
fi

SKILL_NAME="$1"
REPO_URL="$2"
REPO_NAME="${3:-$(basename "$REPO_URL" .git)}"

# 获取 skills 目录
SKILLS_DIR="$HOME/.claude/skills"
SKILL_DIR="$SKILLS_DIR/$SKILL_NAME"
SOURCE_DIR="$SKILL_DIR/source"
SUBMODULE_PATH="$SKILL_NAME/source/$REPO_NAME"

# 检查技能目录是否存在
if [ ! -d "$SKILL_DIR" ]; then
    error "技能目录不存在: $SKILL_DIR"
fi

# 检查是否已存在 submodule
if [ -d "$SOURCE_DIR/$REPO_NAME" ]; then
    warning "目录已存在: $SOURCE_DIR/$REPO_NAME"
    read -p "是否删除并重新添加? (y/n): " confirm
    if [ "$confirm" = "y" ]; then
        info "清理现有目录..."
        cd "$SKILLS_DIR"
        git submodule deinit -f "$SUBMODULE_PATH" 2>/dev/null || true
        rm -rf ".git/modules/$SUBMODULE_PATH" 2>/dev/null || true
        rm -rf "$SOURCE_DIR/$REPO_NAME"
    else
        error "操作已取消"
    fi
fi

# 创建 source 目录
mkdir -p "$SOURCE_DIR"

# 添加 submodule
info "添加 Git Submodule: $REPO_URL"
cd "$SKILLS_DIR"
git submodule add "$REPO_URL" "$SUBMODULE_PATH"

success "Submodule 添加成功!"
echo ""
echo "📋 下一步操作:"
echo ""
echo "1. 配置 Sparse Checkout:"
echo "   cd $SOURCE_DIR/$REPO_NAME"
echo "   git sparse-checkout init --no-cone"
echo "   git sparse-checkout set /README.md /src/ /docs/ /examples/"
echo ""
echo "2. 验证配置:"
echo "   git sparse-checkout list"
echo "   du -sh ."
echo ""
echo "3. 创建 SOURCE_STRUCTURE.md 文档"
echo ""
echo "4. 更新 SKILL.md 中的源码访问说明"
echo ""
echo "5. 提交更改:"
echo "   cd $SKILLS_DIR"
echo "   git add .gitmodules $SUBMODULE_PATH"
echo "   git commit -m 'Add $REPO_NAME as submodule for $SKILL_NAME'"

