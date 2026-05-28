---
name: odin-task-executor
description: |
  执行 ODIN 任务流程。用户选中 plan.yml 文件后，分两次调用 odin-subagent：先加载 odin-executor skill 执行任务，再加载 odin-reviewer skill 审核代码。
  当用户需要执行项目路径 .claude/odin/ 中的计划任务时使用该 skill。
allowed-tools: Task, AskUserQuestion
---

## 执行流程

### 1. 确认计划文件

用户通过选中 `plan.yml` 文件触发该 skill。从输入中获取计划文件路径。

### 2. 启动 odin-subagent 执行任务

使用 Task 工具调用 odin-subagent 子代理，让 subagent 加载 odin-executor skill：

```
计划文件: <plan.yml 路径>

请使用 Skill 工具加载 odin-executor skill，然后按照 skill 的指令读取并执行下一个任务。
```

odin-subagent 会：
1. 使用 Skill 工具加载 odin-executor
2. 按照 odin-executor skill 的指令执行任务
3. 返回执行结果（包括任务 ID）

### 3. 启动 odin-subagent 审核代码

任务执行完成后，再次使用 Task 工具启动一个新的 odin-subagent 子代理，让 subagent 加载 odin-reviewer skill：

```
计划文件: <plan.yml 路径>
任务 ID: <odin-executor 返回的任务 ID>

请使用 Skill 工具加载 odin-reviewer skill，然后按照 skill 的指令审核刚才完成的任务代码质量。
```

odin-subagent 会：
1. 使用 Skill 工具加载 odin-reviewer
2. 按照 odin-reviewer skill 的指令审核代码
3. 返回审核结果

### 4. 处理审核结果

根据审核结果：

- **审核发现问题**：询问用户是否需要修正
  - 如果确认修正，修正后重新执行步骤 3
  - 如果用户选择跳过，继续下一步

- **审核通过**：询问用户是否继续执行下一个任务
  - 如果继续，重复步骤 2-3
  - 如果结束或没有更多任务，完成流程

## 任务状态说明

- **finished: false**: 未完成的任务
- **finished: true**: 已完成的任务

## 注意事项

- 按序号从上往下依次执行任务
- 每个任务完成后都应进行代码审核
- 及时向用户报告进度和遇到的问题
- 根据任务文档中的验证标准确认任务已完成

## 架构说明

该 skill 采用薄壳子代理模式：
- **odin-subagent**: 薄壳子代理，仅负责加载和执行 skills
- **odin-executor**: 任务执行 skill，包含任务执行逻辑和 Python 脚本
- **odin-reviewer**: 代码审核 skill，包含审核标准和流程

这种设计实现了关注点分离：
- 主协调 skill (odin-task-executor) 负责流程编排
- 薄壳 subagent (odin-subagent) 提供技能加载环境
- 具体 skills (odin-executor/odin-reviewer) 负责具体业务逻辑
