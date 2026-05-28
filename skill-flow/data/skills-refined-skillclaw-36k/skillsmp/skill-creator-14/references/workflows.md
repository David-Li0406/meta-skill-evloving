# 工作流模式 (Workflow Patterns)

## 顺序工作流 (Sequential Workflows)

对于复杂的任务，将操作分解为清晰的顺序步骤。在 `SKILL.md` 的开头附近向 Agent 提供流程概览通常很有帮助：

```markdown
填充 PDF 表单涉及以下步骤：

1. 分析表单（运行 analyze_form.py）
2. 创建字段映射（编辑 fields.json）
3. 验证映射（运行 validate_fields.py）
4. 填充表单（运行 fill_form.py）
5. 验证输出（运行 verify_output.py）
```

## 条件工作流 (Conditional Workflows)

对于具有分支逻辑的任务，引导 Agent 通过决策点：

```markdown
1. 确定修改类型：
   **创建新内容？** → 遵循下方的“创建工作流”
   **编辑现有内容？** → 遵循下方的“编辑工作流”

2. 创建工作流：[步骤]
3. 编辑工作流：[步骤]
```