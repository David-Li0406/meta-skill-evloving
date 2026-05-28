---
name: project-complete
description: 项目完成导航。触发：用户通知"项目完成"或"可以提交了"时使用；执行归档、生成changelog、git commit+push。
metadata:
  short-description: 项目完成与归档提交
  access: plan-agent-internal
  tags: [workflow, complete, git]
---

# project-complete

> **访问控制**：此 skill 仅限 plan-agent 内部调用，Claude 主对话和其他子代理不可直接调用。

项目完成，执行归档、生成changelog、git commit+push，更新项目状态。

## When to Use This Skill

- 用户通知"项目完成"/"可以提交了"
- 代码审核已通过
- 所有提案状态为 `accepted`

## Not For / Boundaries

**不做**：
- 不执行代码审核（由 code-review 负责）
- 不修复代码（由子代理负责）
- 不创建新功能（由循环A规划负责）

**必需输入**：
- 代码审核已通过
- 安全扫描已通过或用户明确跳过
- 所有提案状态为 `accepted`

缺少输入时阻塞并告知用户。

## Quick Reference

### 硬性规则

```
- 必须按顺序执行：前置检查 → 归档 → changelog → commit+push → 更新状态 → 通知
- 仅 project-complete 允许执行 git push
- 禁止 git commit 添加 AI 署名
- 必须更新 Record/Memory/plan-agent.md 的会话记录摘要
```

### 执行步骤

```
1. 前置状态确认 → 检查审核和提案状态
2. 归档 OpenSpec 提案 → 移动到 openspec/archive/
3. 生成变更清单 → 更新 CHANGELOG.md
4. 项目完成提交与推送 → git commit + push
5. 更新项目状态 → state.json 状态为 completed
6. 通知用户 → 输出完成摘要，更新 record.md + Memory/plan-agent.md
```

## Examples

### Example 1: 正常完成

- **输入**: 用户说"项目完成，可以提交了"
- **步骤**: 前置检查(通过) → 归档提案 → 生成changelog → commit+push → 更新状态 → 通知
- **验收**: 代码已推送，state.json 为 completed

### Example 2: 审核未通过

- **输入**: 用户说"提交"但审核未通过
- **步骤**: 前置检查(失败) → 阻塞
- **验收**: 输出"请先完成代码审核"

### Example 3: 跳过安全扫描

- **输入**: 用户明确跳过安全扫描
- **步骤**: 前置检查(用户确认跳过) → 继续后续步骤
- **验收**: 记录"用户跳过安全扫描"，正常完成

## References

- `references/step1-check-state.md` - 前置状态确认
- `references/step2-archive.md` - 归档 OpenSpec 提案
- `references/step3-changelog.md` - 生成变更清单
- `references/step4-commit-push.md` - 项目完成提交与推送
- `references/step5-update-state.md` - 更新项目状态
- `references/step6-notify.md` - 通知用户

## Maintenance

- 来源：双AI协同开发方案
- 最后更新：2026-01-05
- 已知限制：仅完成归档和提交，不执行新功能开发
