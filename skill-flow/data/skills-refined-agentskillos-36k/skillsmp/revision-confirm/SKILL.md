---
name: revision-confirm
description: 修订确认导航。触发：您通知"plan-agent已修订完成"或需要analysis-agent查看plan-agent修订意见时使用；读取 draft-plan.md 的"plan-agent修订意见"章节，分析后引导下一步。
metadata:
  short-description: analysis-agent确认plan-agent修订（引导至analysis-agent）
  tags: [workflow, planning, confirm, redirect]
---

# revision-confirm

> **重要**：此功能已迁移至 `analysis-agent` 子代理。

## 如何使用

请启动 **analysis-agent** 来执行修订确认：

```
启动分析
```

或

```
analysis-agent 确认修订
```

## 迁移说明

- 原 skill 功能已完整迁移至 `~/.claude/agents/analysis-agent/skills/revision-confirm/`
- analysis-agent 提供更完整的确认流程和访问控制
- 支持与 plan-agent 的自动化协作

## 相关文件

- 子代理主文件：`~/.claude/agents/analysis-agent/analysis-agent.md`
- 内部 skill：`~/.claude/agents/analysis-agent/skills/revision-confirm/SKILL.md`
