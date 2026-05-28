---
name: code-review
description: 代码审核导航。触发：用户通知"编译通过"或"请审核代码"时使用；对子代理产出的代码进行质量审核、规范检查、越界检查，输出审核报告。
metadata:
  short-description: 编译通过后进行代码审核
  access: plan-agent-internal
  tags: [workflow, review, quality]
---

# code-review

> **访问控制**：此 skill 仅限 plan-agent 内部调用，Claude 主对话和其他子代理不可直接调用。

代码审核，对所有子代理产出的代码进行质量审核，输出审核报告供用户确认。

## When to Use This Skill

- 用户通知"编译通过"/"请审核代码"
- 编译提案状态为 `accepted`
- 所有功能实现提案状态为 `accepted`

## Not For / Boundaries

**不做**：
- 不执行编译（由 build-agent 负责）
- 不修复代码（由子代理根据修复提案负责）
- 不完成项目（由 project-complete 负责）

**必需输入**：
- 编译提案（`build-all-build-agent`）状态为 `accepted`
- 所有功能实现提案状态为 `accepted`

缺少输入时阻塞并告知用户。

## Quick Reference

### 硬性规则

```
- 必须按顺序执行：确认状态 → 归档 → 收集范围 → 执行审核 → 生成报告
- 发现问题必须创建修复提案
- 修复后必须重新审核
- 越界修改必须标记为严重问题
```

### 审核维度

```
- 代码质量：屎山代码、重复代码、过度复杂
- 规范检查：是否符合项目编码规范
- 越界检查：对照 scope 检查是否有越界修改
- 风险识别：安全问题、性能问题、维护性问题
```

### 执行步骤

```
1. 确认前置状态 → 检查编译提案和功能提案状态
2. 归档提案执行记录 → 记录已完成的提案
3. 收集审核范围 → 确定需要审核的文件
4. 执行审核 → 按审核维度检查代码
5. 生成审核报告 → 输出问题清单和建议
6. 创建修复提案 → 对发现的问题创建修复提案
7. 修复后重新审核 → 确认问题已修复
```

## Examples

### Example 1: 审核通过

- **输入**: 用户说"编译通过，请审核"
- **步骤**: 确认状态 → 收集范围 → 执行审核(无问题) → 生成报告
- **验收**: 审核报告显示"通过"，无修复提案

### Example 2: 发现问题

- **输入**: 代码存在重复和越界
- **步骤**: 执行审核 → 发现问题 → 生成报告 → 创建修复提案
- **验收**: 审核报告列出问题，修复提案已创建

### Example 3: 修复后重审

- **输入**: 修复提案已完成
- **步骤**: 重新审核 → 确认问题已修复 → 更新报告
- **验收**: 审核报告更新为"通过"

## References

- `references/step1-check-state.md` - 确认前置状态
- `references/step2-archive-impl.md` - 归档提案执行记录
- `references/step3-collect-scope.md` - 收集审核范围
- `references/step4-execute-review.md` - 执行审核
- `references/step5-generate-report.md` - 生成审核报告
- `references/step6-create-fix-proposal.md` - 创建修复提案
- `references/step7-re-review.md` - 修复后重新审核
- `references/review-checklist.md` - 审核检查清单
- `references/review-report-template.md` - 审核报告模板

## Maintenance

- 来源：双AI协同开发方案
- 最后更新：2026-01-05
- 已知限制：仅审核代码，不修复代码
