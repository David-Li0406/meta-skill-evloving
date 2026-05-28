---
name: plan-confirm
description: 方案确认导航。触发：用户查看确定方案后通知"确认方案"或"开始执行"时使用；初始化openspec、创建提案、输出子代理任务清单与分工。
metadata:
  short-description: 确认方案后初始化openspec并创建提案
  access: plan-agent-internal
  tags: [workflow, planning, openspec, execution]
---

# plan-confirm

> **访问控制**：此 skill 仅限 plan-agent 内部调用，Claude 主对话和其他子代理不可直接调用。

方案确认，初始化openspec、创建提案、输出子代理任务清单，正式进入循环B执行阶段。

## When to Use This Skill

- 用户通知"确认方案"/"开始执行"
- `plan-finalize` 已完成，确定方案已生成
- 准备从循环A规划进入循环B执行

## Not For / Boundaries

**不做**：
- 不定稿方案（由 plan-finalize 负责）
- 不执行代码（由子代理负责）
- 不审核代码（由 code-review 负责）

**必需输入**：
- `Record/state.json` 中 `active_plan_version` 已冻结
- 确定方案文件 `Record/plan/{plan_version}-final.md` 存在

缺少输入时阻塞并告知用户先完成 plan-finalize。

## Quick Reference

### 硬性规则

```
- 必须按顺序执行：确认状态 → 初始化openspec → 创建提案 → 输出任务清单
- 提案必须包含 allowed_paths 确保文件排他
- 提案必须包含 depends_on 确保串行依赖
- 每个提案对应一个子代理执行
```

### 执行步骤

```
1. 确认前置状态 → 读取 state.json 确认 active_plan_version 存在
2. 初始化 OpenSpec → openspec init --tools none
3. 创建提案 → 按确定方案任务拆分，写入 openspec/proposals/
4. 输出任务清单 → 告知用户需启动哪些子代理、各做什么
5. 处理用户问题 → 回答关于分工的疑问
```

## Examples

### Example 1: 正常确认

- **输入**: 用户说"开始执行"
- **步骤**: 确认状态(通过) → 初始化openspec → 创建3个提案 → 输出任务清单
- **验收**: `openspec/proposals/` 下有3个提案文件，用户知道启动哪些子代理

### Example 2: 前置状态缺失

- **输入**: 用户说"开始执行"但未完成plan-finalize
- **步骤**: 确认状态(失败) → 阻塞
- **验收**: 输出"请先完成plan-finalize定稿方案"

### Example 3: 复杂项目多提案

- **输入**: 确定方案包含5个模块
- **步骤**: 确认状态 → 初始化openspec → 创建5个提案(含依赖关系) → 输出任务清单
- **验收**: 提案间 depends_on 正确设置，allowed_paths 无冲突

## References

- `references/step1-check-state.md` - 确认前置状态
- `references/step2-init-openspec.md` - 初始化 OpenSpec 和 Git
- `references/step3-create-proposal.md` - 创建提案
- `references/step4-output-tasklist.md` - 输出任务清单
- `references/step5-handle-questions.md` - 用户问题处理
- `references/proposal-template.md` - 提案模板
- `references/build-proposal-template.md` - 编译提案模板
- `references/security-scan-proposal-template.md` - 安全扫描提案模板

## Maintenance

- 来源：双AI协同开发方案
- 最后更新：2026-01-05
- 已知限制：仅创建提案，不执行代码
