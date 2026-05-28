# 修订确认工作流（revision-confirm）

> **注意**：此文件为旧版引导文件，实际功能已迁移至 analysis-agent。

## 硬性禁止（必须遵守）

- **禁止修改草案的 status 字段**
- **禁止写入"用户最终确认"或类似确认结果**
- **禁止代替 plan-agent 执行 plan-finalize 的任何操作**

## 迁移说明

此功能已迁移至 `~/.claude/agents/analysis-agent/skills/revision-confirm/`

请参考：
- 子代理主文件：`~/.claude/agents/analysis-agent/analysis-agent.md`
- 内部 skill：`~/.claude/agents/analysis-agent/skills/revision-confirm/SKILL.md`
- 确认流程：`~/.claude/agents/analysis-agent/skills/revision-confirm/references/confirm-workflow.md`
