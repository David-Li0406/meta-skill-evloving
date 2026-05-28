---
name: plan-revision
description: 规划修订导航。触发：用户通知"analysis-agent已分析完成"或需要plan-agent查看analysis-agent复审结果并修订预定清单时使用；评估analysis-agent分析结果并修订draft-plan.md。
metadata:
  short-description: plan-agent查看analysis-agent分析并修订规划
  access: plan-agent-internal
  tags: [workflow, planning, revision]
---

# plan-revision

> **访问控制**：此 skill 仅限 plan-agent 内部调用，Claude 主对话和其他子代理不可直接调用。

规划修订，plan-agent查看analysis-agent的复审分析结果，进行评估与修订，形成可供用户确认的最终规划。

## When to Use This Skill

- 用户通知"analysis-agent已分析完成"
- 需要plan-agent查看analysis-agent复审结果
- 循环A规划阶段的修订环节

## Not For / Boundaries

**不做**：
- 不创建Record结构（由 project-bootstrap 负责）
- 不执行Claude的复审（由 draft-plan-review 负责）
- 不定稿方案（由 plan-finalize 负责）

**必需输入**：
- `Record/plan/draft-plan.md` 存在且包含"Claude复审补充"章节
- 项目根目录已确认

缺少输入时询问用户。

## Quick Reference

### 硬性规则

```
- 必须先读取 draft-plan.md 的"Claude复审补充"章节
- 对Claude每项分析必须明确表态：认可/不认可/部分认可
- 不认可的点必须说明理由（中文）
- 修订后必须更新 draft-plan.md
- 项目根目录不明确时必须先询问用户
```

### 独立思考原则

```
- 【必须独立判断】对 Claude 分析和用户决策进行独立技术评估
- 【可以否定用户】发现技术问题时必须明确指出，即使是用户的决定
- 【可以否定 analysis-agent】对 analysis-agent 的分析结论可以提出异议
- 【可以否定 neutral-agent】对 neutral-agent 的仲裁意见可以提出异议
- 【写明理由】所有否定意见必须写明具体原因和潜在风险
- 【不盲从】不因"用户说的"/"analysis-agent 分析的"/"neutral-agent 仲裁的"就无条件接受
- 【建设性】否定时应提供替代方案或改进建议
- 【坚持原则】技术上有严重问题时，即使三方都催促也要坚持异议
```

### 执行步骤

```
1. 读取 draft-plan.md 的"Claude复审补充"章节
2. 逐项评估Claude的分析结果
3. 对不认可的点说明理由
4. 回写修订结果到 draft-plan.md 的"plan-agent修订意见"章节
5. 更新 record.md + Memory/plan-agent.md
6. 告知用户修订完成，引导进入 revision-confirm
```

## Examples

### Example 1: 全部认可

- **输入**: Claude分析结果合理
- **步骤**: 读取分析 → 逐项评估(全部认可) → 回写"全部认可" → 告知用户
- **验收**: draft-plan.md 包含"plan-agent修订意见：全部认可"

### Example 2: 部分不认可

- **输入**: Claude某项分析有问题
- **步骤**: 读取分析 → 逐项评估 → 对不认可项说明理由 → 回写修订意见
- **验收**: draft-plan.md 包含具体不认可理由和修订建议

### Example 3: 需要补充信息

- **输入**: Claude分析缺少关键信息
- **步骤**: 读取分析 → 发现信息不足 → 回写"需补充xxx信息" → 告知用户
- **验收**: draft-plan.md 标注需补充的信息，用户知道下一步

## References

- `references/revision-workflow.md` - 评估与修订流程
- `references/writeback-template.md` - 回写修订结果模板

## Maintenance

- 来源：双AI协同开发方案
- 最后更新：2026-01-05
- 已知限制：仅修订规划，不执行代码
