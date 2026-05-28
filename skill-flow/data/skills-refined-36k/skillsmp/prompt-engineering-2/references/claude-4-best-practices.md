# 通用最佳实践（来源：Claude 4 文档）

来源：
- https://platform.claude.com/docs/zh-CN/build-with-claude/prompt-engineering/claude-4-best-practices

要点
- 明确角色、任务范围与输出格式；对不确定信息要求先澄清。
- 对复杂任务使用结构化输入（XML/分段）与分步流程。
- 通过示例约束风格与结构，避免“只说目标不说方法”。
- 需要高准确或复杂推理时，考虑更强推理/扩展思考策略，但评估成本与时延。
- 长任务优先拆分与链式处理，加入自检/复核步骤。
