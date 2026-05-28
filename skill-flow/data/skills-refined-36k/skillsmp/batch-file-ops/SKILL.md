---
name: batch-file-ops
description: 安全的批量文件处理，包含三重验证协议、基准清单和原子操作。
当重构、迁移或批量重命名文件时使用。
Use when refactoring, migrating, or bulk renaming files. Also triggers for glob patterns like "find all *.js files" or "move src/ to lib/".
allowed-tools: "Bash,Glob,Read,Write,Edit"
---

# Batch File Operations - 批量文件操作

安全的批量文件处理，包含三重验证协议和原子操作。

## 使用场景

- 项目重构
- 代码迁移
- 批量文件重命名
- 项目整理
- 多文件合并

## 核心协议

### 1. 基准清单

初次扫描后生成"处理清单"，严格按清单执行。
❌ **严禁**中途重新评估（导致范围扩散）

### 2. 三重验证

任何删除/修改操作前，必须确认：
1. `Read` 工具确认源文件中引用确实存在
2. 目标位置文件确认缺失
3. 源位置文件确认存在

### 3. 分阶段执行

- **阶段一**：完成所有"复制"操作
- **阶段二**：然后处理所有"删除"操作
❌ **严禁**混合检查和修改

### 4. Bash 不可信

批量判断时：
- Bash 输出**仅供参考**
- 必须用 `Read` 工具逐个验证关键文件

### 5. 一致性原则

建立基准后：
- 任何矛盾发现 → 立即停止
- 重新读取原始状态
- ❌ **严禁**"凭印象修正"

## 示例工作流

```bash
# 步骤 1：生成基准
find . -name "*.js" -type f > files_to_migrate.txt

# 步骤 2：用 Read 工具验证每个文件
# 步骤 3：复制所有到新位置
# 步骤 4：确认复制成功
# 步骤 5：只有这时才删除原文件
```

## 文件编辑规范

### 单次修改

- 修改 <50 行：使用 `Edit` 工具
- `old_str` 必须含唯一锚点，严禁仅用 `}` 或 `return` 作为锚点

### 大规模替换

- 修改 >3 处：使用 `mcp__filesystem__edit_file` 或重写整个文件

## 安全检查清单

- [ ] 基准清单已生成
- [ ] 每个操作都三重验证
- [ ] 复制完成后再删除
- [ ] 关键文件用 Read 工具验证
- [ ] 每批操作后确认状态

## 常见触发场景

使用此技能时，你会听到：
- "批量重命名这些文件"
- "重构这个项目"
- "整理项目结构"
- "迁移代码到新目录"
- "找出所有 *.js 文件"
- "把 src/ 的内容移到 lib/"
- "将 components/ 重命名为 widgets/"
- "Bulk rename files"
- "Refactor this project"
- "Migrate src to lib"
- "Find all *.ts files"
