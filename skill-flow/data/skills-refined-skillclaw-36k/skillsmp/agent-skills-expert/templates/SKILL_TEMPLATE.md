---
name: your-skill-name
description: Brief description of what this Skill does. Include when to use it and key terms for discovery. Use when [specific scenarios]. Requires [packages if any].
---

# Your Skill Name

简短的技能概述。

## 📚 Source Documentation

> 如果技能包含源码引用，添加此部分

This skill includes access to the official source code through `source/` directory (managed as git submodule with sparse-checkout):

- **Core Libraries**: `source/repo/src/`
- **Documentation**: `source/repo/docs/`
- **Examples**: `source/repo/examples/`

### Source Structure (~XXM with sparse-checkout)

```
source/repo/
├── src/           # 核心源码
├── docs/          # 文档
├── examples/      # 示例
└── README.md      # 项目说明
```

### Updating Source Code

```bash
cd source/repo
git pull origin main
```

For detailed structure, see [SOURCE_STRUCTURE.md](SOURCE_STRUCTURE.md).

## Quick Start

### Installation

```bash
# 安装命令
pip install package-name
```

### Basic Usage

```python
# 基础使用示例
from package import Something

result = Something.do_something()
```

## Core Concepts

### Concept 1

说明核心概念...

### Concept 2

说明核心概念...

## Examples

### Example 1: Basic Usage

```python
# 示例代码
```

### Example 2: Advanced Usage

```python
# 高级示例代码
```

## Best Practices

1. **Practice 1** - 说明
2. **Practice 2** - 说明
3. **Practice 3** - 说明

## Troubleshooting

### Common Issue 1

**Problem**: 描述问题
**Solution**: 解决方案

### Common Issue 2

**Problem**: 描述问题
**Solution**: 解决方案

## Requirements

```bash
pip install package1 package2
```

## Additional Resources

- [Official Documentation](https://example.com/docs)
- [GitHub Repository](https://github.com/org/repo)

---

*最后更新: YYYY-MM-DD*

