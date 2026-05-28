#!/bin/bash

# Create Skill Script
# 创建新的 Claude Code Skill
#
# 用法: ./create_skill.sh <skill-name> "<description>"
#
# 示例:
#   ./create_skill.sh my-python-expert "Expert for Python development..."

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
    echo "用法: $0 <skill-name> \"<description>\""
    echo ""
    echo "参数:"
    echo "  skill-name    技能名称（小写字母、数字、连字符）"
    echo "  description   技能描述"
    echo ""
    echo "示例:"
    echo "  $0 my-python-expert \"Expert for Python development. Use when writing Python code.\""
    exit 1
fi

SKILL_NAME="$1"
DESCRIPTION="$2"

# 验证技能名称
if ! [[ "$SKILL_NAME" =~ ^[a-z0-9-]+$ ]]; then
    error "技能名称只能包含小写字母、数字和连字符"
fi

if [ ${#SKILL_NAME} -gt 64 ]; then
    error "技能名称不能超过64个字符"
fi

if [ ${#DESCRIPTION} -gt 1024 ]; then
    error "描述不能超过1024个字符"
fi

SKILLS_DIR="$HOME/.claude/skills"
SKILL_DIR="$SKILLS_DIR/$SKILL_NAME"

# 检查是否已存在
if [ -d "$SKILL_DIR" ]; then
    error "技能已存在: $SKILL_DIR"
fi

# 创建目录结构
info "创建技能目录..."
mkdir -p "$SKILL_DIR"
mkdir -p "$SKILL_DIR/source"

# 创建 SKILL.md
info "创建 SKILL.md..."
cat > "$SKILL_DIR/SKILL.md" << EOF
---
name: $SKILL_NAME
description: $DESCRIPTION
---

# ${SKILL_NAME//-/ } Expert

简短的技能概述。

## Quick Start

### Installation

\`\`\`bash
# 安装命令
\`\`\`

### Basic Usage

\`\`\`python
# 基础使用示例
\`\`\`

## Core Concepts

### Concept 1

说明核心概念...

## Examples

### Example 1

\`\`\`python
# 示例代码
\`\`\`

## Best Practices

1. **Practice 1** - 说明

## Requirements

\`\`\`bash
# 依赖安装
\`\`\`

---

*最后更新: $(date +%Y-%m-%d)*
EOF

# 创建 source/README.md
cat > "$SKILL_DIR/source/README.md" << EOF
# Source Directory

此目录用于存放源码引用（Git Submodule）。

## 添加源码引用

\`\`\`bash
cd $SKILLS_DIR
git submodule add https://github.com/org/repo.git $SKILL_NAME/source/repo-name

# 配置 sparse-checkout
cd $SKILL_NAME/source/repo-name
git sparse-checkout init --no-cone
git sparse-checkout set /README.md /src/ /docs/ /examples/
\`\`\`
EOF

success "技能创建成功: $SKILL_DIR"
echo ""
echo "📁 创建的文件:"
echo "   • $SKILL_DIR/SKILL.md"
echo "   • $SKILL_DIR/source/README.md"
echo ""
echo "📋 下一步操作:"
echo "   1. 编辑 SKILL.md 添加详细内容"
echo "   2. 如需源码引用，添加 git submodule"
echo "   3. 测试技能是否被 Claude 正确发现"

