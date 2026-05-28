---
name: odin-plan
description: |
  根据用户需求，执行详细的需求分析并生成结构化的计划任务文档。
  当用户需要创建新的开发计划时使用该 skill。
allowed-tools: AskUserQuestion, Read, Glob, Grep, WebSearch, Edit, Write
---

## 工作流程

### 1. 信息收集阶段

通过以下方式获取足够的信息：

- 读取与需求相关的所有关键代码文件
- 查阅在线文档、网络搜索相关技术信息
- 使用 AskUserQuestion 工具向用户提问以获取更清晰的需求（可多次提问直到需求清晰）

### 2. 需求分析阶段

获取到足够的信息后，分析需求是否成立：

- **若需求不成立**：向用户说明原因，并提供替代建议或修改意见
- **若需求成立**：继续生成计划任务文档

### 3. 文档生成阶段

生成一系列计划任务文档，保存到 `项目路径/.claude/odin/{yyyyMMdd}-{kebab-case-计划名称}/` 文件夹中。

**目录命名示例**：
- `20250121-refactor-auth-system/`
- `20250121-add-user-pagination/`
- `20250121-fix-payment-bug/`

## 必需文档

### 1. description.md

详细的现状分析和总体任务概述，应包含以下章节：

```markdown
# {计划标题}

## 现状分析
{描述当前系统状态，存在的问题或需要改进的点}

## 需求概述
{清晰描述用户需求，包括目标、范围和约束条件}

## 总体方案
{概述实现方案，包括技术选型、架构设计等}

## 预期成果
{描述完成后的预期效果和收益}

## 风险评估
{列出可能的风险点和应对措施}
```

### 2. plan.yml

计划任务状态文档，严格按以下格式生成，不可添加未出现的字段：

```yaml
description: ./description.md
created_at: 2025-01-21
updated_at: 2025-01-21

tasks:
  01-task-name:
    finished: false
    detail: ./01-task-name.md
    files:
      add:
        - path/to/new/file.ext
      modify:
        - path/to/existing/file.ext
      delete:
        - path/to/old/file.ext

  02-another-task:
    finished: false
    detail: ./02-another-task.md
    files:
      add: []
      modify:
        - path/to/file.ext
      delete: []
```

**字段说明**：
- `finished`：布尔值，表示任务是否完成
- `files`：文件变更列表（可选，若无变更可省略该字段）
  - `add`：新增文件列表
  - `modify`：修改文件列表
  - `delete`：删除文件列表

### 3. {no}-{task-name}.md

详细步骤文档，文件命名规范：
- `{no}`：两位数字编号（01、02、03...）
- `{task-name}`：kebab-case 命名（小写字母，单词间用连字符分隔）

每个任务文档应包含以下内容：

```markdown
# {任务标题}

## 任务目标
{清晰描述本任务要达成的目标}

## 前置条件
{列出执行本任务需要满足的条件}

## 详细步骤

### 步骤 1：{步骤标题}
{具体操作说明、代码示例等}

### 步骤 2：{步骤标题}
{...}

## 验证标准
{列出判断任务完成的验收标准}

## 注意事项
{重要的注意事项、潜在问题等}
```

## 任务拆分原则

1. **原子性**：每个任务应该是独立的、可验证的工作单元
2. **按序执行**：任务按序号从上往下依次执行，确保序号顺序合理
3. **粒度适中**：单个任务的工作量应该适中（通常 1-4 小时完成）
4. **可追溯**：每个任务应该有明确的输入和可验证的输出

## 最少任务要求

- 至少包含 1 个任务文档
- 建议复杂任务拆分为 3-7 个子任务
- 避免单个任务过于庞大或过于琐碎
