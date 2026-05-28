---
name: writing-plans
description: 使用此技能当你有多步骤写作任务的规范或要求时，在开始撰写正文之前。
---

# 制定写作计划

## 概述

编写详尽的撰写实施计划，假设执行该计划的研究助理对我们的文献库毫无背景知识，且学术品味存疑。记录他们需要知道的一切：每个任务涉及哪些章节文件、核心论点、需要查阅的证据、如何验证逻辑。将整个计划分解为一口大小的任务，避免重复 (DRY)，不需要的不写 (YAGNI)，论证驱动写作 (ADW)，并频繁提交。

**开始时声明：** “我正在使用 writing-plans 技能来创建撰写实施计划。”

**上下文：** 这应该在一个专门的工作树中运行。

**保存计划至：** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## 任务粒度

**每个步骤是一个动作（2-5分钟）：**
- “写出缺失证据的主张（失败的测试）” - 步骤
- “阅读它以确保它缺乏支持” - 步骤
- “撰写最简内容以提供证据支持” - 步骤
- “检查逻辑并确保论证成立” - 步骤
- “提交” - 步骤

## 计划文档标头

**每个计划必须以从以下标头开始：**

```markdown
# [章节/论题名称] 撰写实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:sa-execution to implement this plan task-by-task.

**目标：** [一句话描述本部分旨在论证什么]

**逻辑架构：** [2-3 句话描述论证方法]

**理论框架/工具：** [关键理论/引用来源]

---
```

## 任务结构

```markdown
### 任务 N: [小节名称]

**文件：**
- 创建：`exact/path/to/section.tex` (或 .md)
- 修改：`exact/path/to/existing.tex:123-145`
- 验证：`tests/exact/path/to/validation_checklist.md`

**步骤 1: 提出待验证的主张 (Write the failing test)**

```markdown
<!-- 预期论点 -->
主张：X 变量对 Y 变量有显著正向影响。
现状：文中尚无此主张的实证支持。
```

**步骤 2: 验证主张缺乏支持 (Run test to verify it fails)**

检查：阅读当前草稿
预期：未找到支持该主张的段落或数据引用。

**步骤 3: 撰写最简内容 (Write minimal implementation)**

```markdown
根据 Z 研究 (2023)，X 的增加通常伴随着 Y 的改善...
```

**步骤 4: 验证论证成立 (Run test to verify it passes)**

检查：阅读新撰写的段落
预期：主张现在有明确的证据支持，且逻辑连贯。

**步骤 5: 提交 (Commit)**

```bash
git add tests/path/validation.md src/path/section.tex
git commit -m "feat: add specific argument about X and Y"
```
```

## 记住
- 始终使用确切的文件路径
- 计划中包含完整的文本草稿（不仅仅是“添加论证”）
- 包含确切的验证指令和预期结果
- 使用 @ 语法引用相关技能
- DRY (不要重复), YAGNI (你不需要它), ADW (论证驱动写作), 频繁提交

## 执行移交

保存计划后，提供执行选项：

**“计划已完成并保存至 `docs/plans/<filename>.md`。两个执行选项：**

**1. 子智能体驱动 (本会话)** - 我为每个任务分派一个新的子智能体，并在任务之间进行审阅，快速迭代

**2. 并行会话 (独立)** - 使用 execution 打开新会话，带检查点的批量执行

**选择哪种方法？”**

**如果选择子智能体驱动：**
- **REQUIRED SUB-SKILL:** Use superpowers:sa-drafting
- 留在这个会话中
- 每个任务使用新的子智能体 + 同行评审

**如果选择并行会话：**
- 引导他们在工作树中打开新会话
- **REQUIRED SUB-SKILL:** 新会话使用 superpowers:sa-execution