# LangGraph Source Directory

此目录包含 LangGraph 官方源代码，通过 Git Submodule + Sparse Checkout 管理。

## 📦 目录结构

```
source/
├── README.md           # 本文件
├── QUICK_ACCESS.md     # 快速访问指南
└── langgraph/          # Git Submodule (sparse-checkout)
    ├── libs/           # 核心库代码
    ├── examples/       # 官方示例
    ├── docs/docs/      # 文档
    └── ...
```

## 🔧 管理方式

- **Git Submodule**: 源码作为子模块管理
- **Sparse Checkout**: 只检出必要的文件（~66MB vs 完整仓库 >500MB）

## 📋 常用操作

### 更新源码

```bash
cd langgraph
git pull origin main
```

### 查看配置

```bash
cd langgraph
git sparse-checkout list
```

### 初始化（首次克隆后）

```bash
# 在项目根目录
git submodule update --init --recursive

# 配置 sparse-checkout
cd langgraph-python-expert/source/langgraph
git sparse-checkout init --no-cone
git sparse-checkout set \
    /README.md /CLAUDE.md /AGENTS.md /LICENSE \
    /libs/langgraph/ /libs/prebuilt/ \
    /libs/checkpoint/ /libs/checkpoint-sqlite/ /libs/checkpoint-postgres/ \
    /docs/docs/ /examples/
```

## 📚 详细文档

- [QUICK_ACCESS.md](QUICK_ACCESS.md) - 快速访问指南
- [../SOURCE_STRUCTURE.md](../SOURCE_STRUCTURE.md) - 完整结构文档

