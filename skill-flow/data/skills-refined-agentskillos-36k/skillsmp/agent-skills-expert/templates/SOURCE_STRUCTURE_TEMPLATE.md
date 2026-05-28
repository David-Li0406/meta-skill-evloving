# [Project Name] Source Structure

本文档描述了 `source/[repo-name]/` 目录的结构和导航指南。

## 📦 Submodule 配置

**仓库**: https://github.com/org/repo
**管理方式**: Git Submodule + Sparse Checkout
**当前大小**: ~XXM (原完整仓库 >XXXM)

### Sparse Checkout 配置

```
/README.md
/LICENSE
/src/
/docs/
/examples/
```

## 📂 目录结构

```
source/[repo-name]/
├── README.md              # 项目概述
├── LICENSE                # 许可证
│
├── src/                   # 核心源码
│   ├── module1/           # 模块1
│   │   ├── file1.py
│   │   └── file2.py
│   └── module2/           # 模块2
│       └── ...
│
├── docs/                  # 文档
│   ├── getting-started.md
│   ├── api-reference.md
│   └── ...
│
└── examples/              # 示例
    ├── basic/
    └── advanced/
```

## 🔍 关键文件导航

### 核心 API

| 功能 | 文件位置 |
|------|----------|
| 主要类 | `src/module/main.py` |
| 工具函数 | `src/utils/helpers.py` |

### 文档

| 类型 | 位置 |
|------|------|
| 入门指南 | `docs/getting-started.md` |
| API 参考 | `docs/api-reference.md` |

## 🛠️ 常用操作

### 更新源码

```bash
cd source/[repo-name]
git pull origin main
```

### 查看 Sparse Checkout 配置

```bash
cd source/[repo-name]
git sparse-checkout list
```

### 临时访问完整仓库

```bash
cd source/[repo-name]
git sparse-checkout disable
# ... 执行操作 ...
git sparse-checkout reapply
```

### 添加新目录到 Sparse Checkout

```bash
cd source/[repo-name]
git sparse-checkout add /新目录/
```

## 📚 学习路径

### 初学者
1. 阅读 `README.md`
2. 查看 `examples/basic/`
3. 阅读 `docs/getting-started.md`

### 中级
1. 研究 `src/` 源码
2. 查看高级示例
3. 阅读 API 文档

### 高级
1. 深入核心实现
2. 研究测试用例
3. 查看贡献指南

## 🔧 维护指南

### Sparse Checkout 配置位置

```
.git/modules/[skill-name]/source/[repo-name]/info/sparse-checkout
```

### 重新配置 Sparse Checkout

```bash
cd source/[repo-name]
git sparse-checkout init --no-cone
git sparse-checkout set \
    /README.md \
    /LICENSE \
    /src/ \
    /docs/ \
    /examples/
```

---

*最后更新: YYYY-MM-DD*

