---
name: sa-peer_review
description: 当完成任务、撰写主要章节，或在定稿前验证工作是否符合要求时使用
---

# 请求同行评审

分派 superpowers:code-reviewer 子智能体，在问题扩散之前捕捉它们。

**核心原则：** 尽早评审，频繁评审。

## 何时请求评审

**强制性：**
- 在子智能体驱动写作的每个任务之后
- 完成主要章节之后
- 在合并到主草稿之前

**可选但有价值：**
- 当卡住时（全新的视角）
- 在重写之前（基线检查）
- 在修复复杂的逻辑漏洞之后

## 如何请求

**1. 获取版本记录 (Git SHAs):**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # 或 origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. 分派审稿子智能体:**

使用 Task 工具调用 superpowers:code-reviewer 类型，填写 `code-reviewer_zh.md` 中的模板

**占位符：**
- `{WHAT_WAS_WRITTEN}` - 你刚刚写了什么
- `{PLAN_OR_REQUIREMENTS}` - 它应该包含什么论点
- `{BASE_SHA}` - 起始提交
- `{HEAD_SHA}` - 结束提交
- `{DESCRIPTION}` - 简要总结

**3. 根据反馈行动:**
- 立即修复 **严重 (Critical)** 问题
- 在继续之前修复 **重要 (Important)** 问题
- 记录 **次要 (Minor)** 问题以备后用
- 如果审稿人错了，进行反驳（附带理由）

## 示例

```
[刚刚完成任务 2: 添加验证论据]

你: 让我在继续之前请求同行评审。

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[分派 superpowers:code-reviewer 子智能体]
  WHAT_WAS_WRITTEN: 关于会话索引验证和修复的论证段落
  PLAN_OR_REQUIREMENTS: docs/plans/deployment-plan.md 中的任务 2
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  DESCRIPTION: 增加了 verifyIndex() 和 repairIndex() 的理论依据和 4 种问题类型
  
[子智能体返回]:
  优势: 架构清晰，论据真实
  问题:
    重要: 缺少进度指标的论述
    次要: 报告间隔 (100) 的依据不明确
  评估: 准备好继续

你: [添加进度指标论述]
[继续任务 3]
```

## 与工作流集成

**子智能体驱动写作:**
- 在每个任务后评审
- 在问题复合之前捕捉它们
- 在移动到下一个任务之前修复

**执行计划:**
- 在每个批次（3 个任务）后评审
- 获取反馈，应用，继续

**临时写作:**
- 在合并前评审
- 卡住时评审

## 危险信号

**绝不：**
- 因为“很简单”而跳过评审
- 忽略 **严重** 问题
- 在未修复 **重要** 问题的情况下继续
- 对有效的学术反馈进行无理争辩

**如果审稿人错了：**
- 用学术理由反驳
- 展示证明其成立的证据/引用
- 请求澄清

参见模板：peer_review/code-reviewer_zh.md
