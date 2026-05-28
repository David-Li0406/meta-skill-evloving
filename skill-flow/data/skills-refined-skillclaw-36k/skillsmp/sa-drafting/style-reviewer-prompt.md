# 行文质量审查助手提示词模板 (Style Checker Prompt Template)

Use this template when dispatching a style quality reviewer subagent.

**目的：** 验证草稿质量良好（清晰、严谨、可读）

**仅在论证合规审查通过后分派。**

```
Task tool (superpowers:style-reviewer):
  Use template at peer_review/manuscript-reviewer.md

  WHAT_WAS_WRITTEN: [来自撰写者的报告]
  PLAN_OR_REQUIREMENTS: 任务 N 来自 [plan-file]
  BASE_SHA: [任务前提交]
  HEAD_SHA: [当前提交]
  DESCRIPTION: [任务摘要]
```

**行文审查员返回：** 优势，问题（严重/重要/次要），评估
