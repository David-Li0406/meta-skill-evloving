# 子代理可用工具

子代理可以被授予访问 Claude Code 任何内部工具的权限。如果省略 `tools` 字段，子代理将继承主线程的所有工具。

## 核心工具

| 工具 | 描述 |
|------|-------------|
| `Read` | 读取文件内容 |
| `Write` | 创建或覆盖文件 |
| `Edit` | 对现有文件进行精确编辑 |
| `Glob` | 通过模式匹配查找文件 |
| `Grep` | 使用正则表达式搜索文件内容 |
| `Bash` | 执行 Shell 命令 |
| `Task` | 生成子代理（不推荐子代理使用） |

## 交互工具

| 工具 | 描述 |
|------|-------------|
| `AskUser` | 向用户提问以澄清问题 |
| `TodoWrite` | 管理任务列表 |

## Web 工具

| 工具 | 描述 |
|------|-------------|
| `WebFetch` | 获取和处理 Web 内容 |
| `WebSearch` | 搜索 Web |

## IDE 工具（可用时）

| 工具 | 描述 |
|------|-------------|
| `mcp__ide__getDiagnostics` | 从 VS Code 获取语言诊断 |
| `mcp__ide__executeCode` | 在 Jupyter 内核中执行代码 |

## MCP 工具

子代理还可以访问已配置的 MCP 服务器的工具。MCP 工具名称遵循模式 `mcp__<server>__<tool>`。

## 常见工具组合

### 只读研究
```
tools: Read, Grep, Glob, Bash
```
最适用于：代码分析、文档审查、代码库探索

### 代码修改
```
tools: Read, Write, Edit, Grep, Glob, Bash
```
最适用于：实现功能、修复错误、重构

### 最小写入权限
```
tools: Read, Grep, Glob
```
最适用于：安全审计、代码审查（仅报告）

### 完全访问
省略 `tools` 字段以继承所有可用工具。
