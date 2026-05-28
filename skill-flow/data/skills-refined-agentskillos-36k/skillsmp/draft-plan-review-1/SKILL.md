---
name: draft-plan-review
description: 复审 plan-agent 生成的"预定清单（草案）"。触发：用户让你复审/分析/补全 plan-agent 的项目规划草案时使用；读取 draft-plan.md 并回写分析结果。
metadata:
  short-description: analysis-agent复审plan-agent草案（引导至analysis-agent）
  tags: [workflow, planning, review, redirect]
---

# draft-plan-review

> **重要**：此功能已迁移至 `analysis-agent` 子代理。

## 如何使用

请启动 **analysis-agent** 来执行草案复审：

```
启动分析
```

或

```
analysis-agent 复审草案
```

## 迁移说明

- 原 skill 功能已完整迁移至 `~/.claude/agents/analysis-agent/skills/draft-plan-review/`
- analysis-agent 提供更完整的分析流程和访问控制
- 支持与 plan-agent 的自动化协作

## 相关文件

- 子代理主文件：`~/.claude/agents/analysis-agent/analysis-agent.md`
- 内部 skill：`~/.claude/agents/analysis-agent/skills/draft-plan-review/SKILL.md`
