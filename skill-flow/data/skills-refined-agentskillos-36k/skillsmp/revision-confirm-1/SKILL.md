---
name: revision-confirm
description: 修订确认。触发：plan-agent 调用或用户通知"plan-agent已修订完成"时使用；读取 draft-plan.md 的"plan-agent修订意见"章节，分析后引导下一步。
metadata:
  short-description: analysis-agent确认plan-agent修订
  access: analysis-agent-internal
  tags: [workflow, planning, confirm]
---

# revision-confirm

> **访问控制**：此 skill 仅限 analysis-agent 内部调用，Claude 主对话和其他子代理不可直接调用。

修订确认，analysis-agent 分析 plan-agent 的修订意见，认可后引导用户进入 plan-finalize。

## When to Use This Skill

- plan-agent 调用 analysis-agent 进行修订确认
- 用户通知"plan-agent已修订完成"
- 用户说"请确认修订"/"确认一下修订"
- 循环A规划阶段的修订确认环节

## Not For / Boundaries

**不做**：
- 不修改草案的 status 字段（由 plan-agent 管理）
- 不修改草案内容（只能在"analysis-agent确认意见"章节写入）
- 不写入"用户最终确认"或类似确认结果
- 不代替 plan-agent 执行 plan-finalize 的任何操作
- 不修订方案（由 plan-revision 负责）
- 不询问"是否开始实现"（实现由 plan-agent 分配）
- 不自行分配或接手实现任务

**必需输入**：
- `Record/plan/draft-plan.md` 存在且包含"plan-agent修订意见"章节
- 项目根目录已确认

缺少输入时用 AskUserQuestion 询问。

## Quick Reference

### 硬性规则

```
- 必须先读取 Record/plan/draft-plan.md 的"plan-agent修订意见"章节
- 对 plan-agent 修订必须进行完整分析，不能跳过
- 有异议必须说明理由并建议再次沟通（回到 plan-agent 修订）
- 只有认可方案后才能引导用户进入 plan-finalize
- 项目根目录不明确时必须先用 AskUserQuestion 询问
- 【禁止越权】认可后必须停止，不得自行执行 plan-finalize
- 【禁止越权】不得读取/修改 state.json
- 【禁止越权】用户说"继续"时，输出引导语后停止，不执行任何定稿操作
- 【禁止越权】不得询问"是否开始实现"或类似问题
- 【禁止越权】不得自行分配或接手实现任务（实现由 plan-agent 通过 plan-finalize 分配）
- 【禁止修改】不得修改 plan-agent 写的草案内容，只能在"analysis-agent确认意见"章节写入
```

### 独立思考原则

```
- 【必须独立判断】对修订意见进行独立技术评估
- 【可以否定用户】发现技术问题时必须明确指出，即使是用户已确认的决定
- 【可以否定 plan-agent】对 plan-agent 的修订意见可以提出异议
- 【可以否定 neutral-agent】对 neutral-agent 的仲裁意见可以提出异议
- 【写明理由】所有否定意见必须写明具体原因和潜在风险
- 【不盲从】不因"用户说的"/"plan-agent 认可的"/"neutral-agent 仲裁的"就无条件接受
- 【建设性】否定时应提供替代方案或改进建议
- 【坚持原则】技术上有严重问题时，即使三方都催促也要坚持异议
```

### 执行步骤

```
1. 确认项目根目录
2. 读取 Record/plan/draft-plan.md 的"plan-agent修订意见"章节
3. 分析修订内容（是否解决问题、是否引入新问题）
4. 输出分析结论（认可/有异议）
5. 有异议 → 说明理由，建议再次沟通
6. 认可 → 更新 record.md + Memory/analysis-agent.md，输出引导语后**停止**
```

### 认可后的标准输出（必须使用）

```
方案已认可。请启动 **plan-agent** 执行 plan-finalize 定稿。

下一步：启动 plan-agent 执行 plan-finalize
```

**注意**：输出上述引导语后，analysis-agent 必须停止，不得执行任何后续操作。

## Examples

### Example 1: 认可修订

- **输入**: plan-agent 调用或用户说"plan-agent修订完成了，请确认"
- **步骤**: 读取"plan-agent修订意见" → 分析 → 认可 → 输出引导语 → **停止**
- **验收**: 输出"方案已认可。请启动 plan-agent 执行 plan-finalize 定稿"，然后停止

### Example 2: 用户说"继续"

- **输入**: analysis-agent 输出引导语后，用户说"继续"
- **步骤**: 再次输出引导语 → **停止**（不执行 plan-finalize）
- **验收**: 输出"请启动 plan-agent 执行 plan-finalize"，不读取 state.json，不执行定稿

### Example 3: 有异议

- **输入**: plan-agent 修订未解决关键问题
- **步骤**: 读取"plan-agent修订意见" → 分析 → 发现问题 → 说明异议
- **验收**: 输出异议理由，建议"请将异议反馈给plan-agent再次修订"

### Example 4: 错误示范（禁止）

- **输入**: analysis-agent 认可修订后
- **错误做法**: 询问"是否开始实现？"或自行分配实现任务
- **正确做法**: 输出标准引导语后停止，实现由 plan-agent 通过 plan-finalize 分配

## References

- `references/confirm-workflow.md` - 确认流程与分析要点
- `references/writeback-template.md` - 回写模板

## Maintenance

- 来源：全Claude子代理协同开发方案
- 最后更新：2026-01-07
- 已知限制：仅分析确认，不修改草案状态
