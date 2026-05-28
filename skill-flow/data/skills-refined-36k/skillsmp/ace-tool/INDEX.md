# Ace Tool 文档索引

## 文档结构

```
~/.pi/agent/skills/ace-tool/
├── SKILL.md          # 完整技能文档（主文档）
├── WRAPPER.md        # ace 包装器说明（原理与安装）
├── COMPARISON.md     # 包装器使用对比
├── README.md         # 项目说明
└── client.ts         # 主脚本实现
```

## 快速导航

### 主文档
📖 **[SKILL.md](./SKILL.md)** - 完整的技能文档和使用指南

### 包装器
📦 **[WRAPPER.md](./WRAPPER.md)** - `ace` 命令包装器的原理、位置和安装说明
🔄 **[COMPARISON.md](./COMPARISON.md)** - 包装器 vs 直接调用的对比

### 项目说明
📚 **[README.md](./README.md)** - 项目原始说明文档

## 快速开始

### 1. 使用包装器（推荐）

```bash
# 语义搜索
ace search "Where is authentication?"

# 提示增强
ace enhance "Add login page"

# 查看帮助
ace
```

### 2. 直接调用（绕过包装器）

```bash
# 语义搜索
bun ~/.pi/agent/skills/ace-tool/client.ts search "query"

# 提示增强
bun ~/.pi/agent/skills/ace-tool/client.ts enhance "prompt"
```

## 常见问题

**Q: `ace` 命令不可用？**
A: 按照 [WRAPPER.md#安装/更新](./WRAPPER.md#安装更新) 创建包装器

**Q: 包装器和直接调用有什么区别？**
A: 参考 [COMPARISON.md](./COMPARISON.md) 了解差异和优势

**Q: 如何查看日志？**
A: 检查项目根目录的 `.ace-tool/ace-tool.log`

## 技术栈

- **运行时**: Bun
- **语言**: TypeScript
- **通信**: TCP Socket (daemon + client)
- **索引**: AugmentCode
