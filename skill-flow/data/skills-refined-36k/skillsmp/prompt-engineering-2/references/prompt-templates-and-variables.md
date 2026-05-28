# Prompt 模板与变量

来源：
- https://platform.claude.com/docs/zh-CN/build-with-claude/prompt-engineering/prompt-templates-and-variables

要点
- 把固定指令与动态输入分离，使用占位符（如 {{variable}}）。
- 模板化能提升一致性、可测试性与复用性，适合批量或多场景。
- 明确变量类型与默认值，避免变量注入导致指令被覆盖。
- 将变量放入清晰的输入区块，配合 XML/标题分区。

示例片段
<task>
  目标：{{goal}}
  输入：{{input}}
  输出格式：{{format}}
</task>
