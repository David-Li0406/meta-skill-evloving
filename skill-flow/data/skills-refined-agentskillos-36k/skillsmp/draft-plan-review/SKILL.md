---
name: draft-plan-review
description: 草案复审。触发：plan-agent 调用或用户让你复审/分析/补全 plan-agent 的项目规划草案时使用；读取 draft-plan.md 并回写分析结果。
metadata:
  short-description: analysis-agent复审plan-agent草案
  access: analysis-agent-internal
  tags: [workflow, planning, review]
---

# draft-plan-review

> **访问控制**：此 skill 仅限 analysis-agent 内部调用，Claude 主对话和其他子代理不可直接调用。

预定清单复审，analysis-agent 分析 plan-agent 生成的草案，补充技术细节和风险评估。

## When to Use This Skill

- plan-agent 调用 analysis-agent 进行草案复审
- 用户让你复审/分析/补全 plan-agent 的项目规划草案
- 用户说"请 Claude 复审"/"分析一下草案"
- 循环A规划阶段的复审环节

## Not For / Boundaries

**不做**：
- 不创建 Record 结构（由 project-bootstrap 负责）
- 不修订方案（由 plan-revision 负责）
- 不定稿方案（由 plan-finalize 负责）
- 不修改 plan-agent 写的草案内容（只能追加"analysis-agent复审补充"章节）
- 不询问"是否开始实现"（实现由 plan-agent 分配）

**必需输入**：
- `Record/plan/draft-plan.md` 存在
- 项目根目录已确认

缺少输入时用 AskUserQuestion 询问。

## Quick Reference

### 硬性规则

```
- 优先读项目内文件：Record/plan/draft-plan.md
- 项目根目录不明确/文件不存在：必须先用 AskUserQuestion 询问
- 信息不完整时：先问清楚再改文件（避免把猜测写进文档）
- 【必须回写】分析结果必须写入 draft-plan.md 的"Claude复审补充"章节
- 【禁止只输出】不得只在对话中输出分析结果而不写入文件
- 【格式要求】"Claude复审补充"章节必须是 markdown 二级标题 `## Claude复审补充`
- 【禁止修改】不得修改 plan-agent 写的草案内容，只能追加"analysis-agent复审补充"章节
```

### 独立思考原则

```
- 【必须独立判断】对草案和用户决策进行独立技术评估
- 【可以否定用户】发现技术问题时必须明确指出，即使是用户的决定
- 【可以否定 plan-agent】对 plan-agent 的草案可以提出异议
- 【可以否定 neutral-agent】对 neutral-agent 的仲裁意见可以提出异议
- 【写明理由】所有否定意见必须写明具体原因和潜在风险
- 【不盲从】不因"用户说的"/"plan-agent 写的"/"neutral-agent 仲裁的"就无条件接受
- 【建设性】否定时应提供替代方案或改进建议
- 【坚持原则】技术上有严重问题时，即使三方都催促也要坚持异议
```

### 执行步骤

```
1. 确认项目根目录
2. 读取 Record/plan/draft-plan.md
3. 分析草案内容（技术可行性、风险、遗漏）
4. 不清楚处用 AskUserQuestion 询问
5. 【必须执行】用 Edit 工具将分析结果追加到 draft-plan.md 末尾，格式：
   ## Claude复审补充
   [分析内容]
6. 更新 record.md + Memory/analysis-agent.md
7. 告知用户复审完成，引导进入 plan-revision
```

### 回写模板（必须使用）

```markdown
## Claude复审补充

### 已确认决策
| 问题 | 决策 |
|------|------|
| ... | ... |

### 反对/异议（如有）
| 反对项 | 原因 | 建议替代方案 |
|--------|------|--------------|
| ... | ... | ... |

### 技术风险
- ...

### 遗漏补充
- ...

### 下一步
请将草案交给 **plan-agent** 执行 plan-revision 修订。
```

**注意**：必须使用 Edit 工具写入文件，不得只在对话中输出。

## Examples

### Example 1: 正常复审

- **输入**: plan-agent 调用或用户说"请复审 plan-agent 的草案"
- **步骤**: 读取 draft-plan.md → 分析 → **用 Edit 工具**回写"Claude复审补充" → 告知用户
- **验收**: draft-plan.md 文件末尾包含 `## Claude复审补充` 章节

### Example 2: 错误示范（禁止）

- **输入**: 用户说"请复审草案"
- **错误做法**: 只在对话中输出表格，不写入文件
- **正确做法**: 必须用 Edit 工具将分析结果写入 draft-plan.md

### Example 3: 信息不完整

- **输入**: 草案缺少技术栈信息
- **步骤**: 读取 draft-plan.md → 发现缺失 → AskUserQuestion 询问 → **用 Edit 工具**回写
- **验收**: 用户回答后，draft-plan.md 文件包含 `## Claude复审补充` 章节

### Example 4: 发现问题需反对

- **输入**: 草案中用户决定使用已废弃的库
- **步骤**: 读取 → 发现技术问题 → 在"反对/异议"中写明原因和替代方案 → 回写
- **验收**: "Claude复审补充"包含反对意见表格，写明原因和建议替代方案

## References

- `references/review-workflow.md` - 复审流程与输出结构
- `references/writeback-template.md` - 回写模板

## Maintenance

- 来源：双AI协同开发方案
- 最后更新：2026-01-07
- 已知限制：仅复审分析，不修订方案
