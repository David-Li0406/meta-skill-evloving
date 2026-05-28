# Chain Prompts（链式提示）

来源：
- https://platform.claude.com/docs/zh-CN/build-with-claude/prompt-engineering/chain-prompts

要点
- 将复杂任务拆为多个子任务，逐步传递中间结果。
- 可加入“自检/评审/对照标准”的中间步骤。
- 每一步输出都要结构化，便于下一步消费。

示例流程
1. 需求抽取 -> 2. 结构化草案 -> 3. 校验与修订 -> 4. 最终输出
