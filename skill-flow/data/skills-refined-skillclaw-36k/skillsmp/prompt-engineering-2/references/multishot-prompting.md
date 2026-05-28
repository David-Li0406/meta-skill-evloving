# Few-shot / Multishot Prompting

来源：
- https://platform.claude.com/docs/zh-CN/build-with-claude/prompt-engineering/multishot-prompting

要点
- 通过 3-5 个多样且一致格式的示例建立模式。
- 示例需覆盖典型与边界情况，减少模型误解。
- 建议用 XML 结构示例区块，保持可解析性。

示例结构
<examples>
  <example>
    <input>...</input>
    <output>...</output>
  </example>
</examples>
