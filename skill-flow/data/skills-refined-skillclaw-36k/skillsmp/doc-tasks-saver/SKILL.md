---
name: doc-tasks-saver
description: 当需要保存 AI 生成的 plan、task list、walkthrough、architecture decision、design doc、meeting notes 等结构化文档时，使用此 skill。将内容规范保存到项目 docs/tasks/ 目录下，文件名自动按顺序编号：001-plan-login-flow.md、002-task-refactor-payment.md 等。会帮你决定合适的文件名、添加序号、写 yaml frontmatter，并给出保存指令。
---

# Doc Tasks Saver Skill

## 核心目的
把 Claude 自己（或其他 AI）生成的各种规划类、任务类、步骤类文档，**有序、永久地**保存在项目的 `docs/tasks/` 目录中，避免散落在聊天记录里。

## 触发条件
- 用户说“保存这个 plan/task/walkthrough/design/meeting notes/adr/...”
- Claude （或其他 AI）自己生成了一个完整的规划/任务/步骤文档，想持久化
- 需要给文档编号存档，避免覆盖

## 使用规范与文件名约定

文件保存路径：始终使用相对路径 `docs/tasks/`

文件名规则（严格遵守）：
1. 必须是三位数字序号 + 短横线 + 描述性 kebab-case 英文标题
   - 001-initial-project-setup.md
   - 002-user-authentication-flow.md
   - 003-refactor-payment-service-tasks.md
   - 015-api-rate-limiting-decision.md
2. 序号从 001 开始递增
3. 如果不确定下一个序号是多少，优先检查已存在的文件，找到最大序号后 +1
4. 描述部分用 kebab-case，长度建议 8–40 个字符，清晰反映主要内容
5. 扩展名统一用 `.md`


## 文档内容格式要求（输出时必须包含）

内容使用简体中文，每个保存的文档开头**必须**有 YAML frontmatter：

```yaml
---
title:      "用户登录与注册流程规划"
created:    "2026-01-20"
author:     "Claude + Gangyi"
version:    1
status:     "active"       # 可选值：draft, active, superseded, archived
related:    []             # 可选，填相关文档序号
tags:       [auth, plan]
---