# OpenAI Prompt Engineering（通用要点）

来源：
- https://platform.openai.com/docs/guides/prompt-engineering

要点
- 指令层级：developer 指令优先于 user；instructions 参数优先于 input。
- 可复用提示词：在 Dashboard 维护 prompts，支持 id/version/variables 注入。
- 推荐用 Markdown 标题/列表 + XML 标签组织消息与边界。
- Few-shot 示例通常放在 developer 消息中，输入输出保持一致格式。
- 补充上下文可使用检索/文件搜索；注意上下文窗口与 token 预算。
- 模型版本建议固定快照并配套评估（evals）以控制漂移。
- GPT 与推理模型差异：GPT 需更明确步骤；推理模型可给更高层目标。
