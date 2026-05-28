# Chain-of-Thought（复杂推理）

来源：
- https://platform.claude.com/docs/zh-CN/build-with-claude/prompt-engineering/chain-of-thought

要点
- 对复杂问题可要求逐步推理，但注意成本与时延。
- 可用 <thinking> 与 <answer> 分离推理与最终输出。
- 生产场景可要求“简要理由/关键依据”，避免暴露冗长思维过程。

示例结构
<thinking>
  ...
</thinking>
<answer>
  ...
</answer>
