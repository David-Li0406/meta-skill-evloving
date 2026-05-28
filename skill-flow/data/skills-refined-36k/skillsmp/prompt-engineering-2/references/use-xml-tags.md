# 使用 XML 标签结构化

来源：
- https://platform.claude.com/docs/zh-CN/build-with-claude/prompt-engineering/use-xml-tags

要点
- 用标签分隔指令、上下文、示例与输出要求。
- 保持标签一致、层级清晰、成对闭合。
- 适合长文本、多段输入、自动化解析输出。

推荐标签
<instructions>...</instructions>
<context>...</context>
<examples>...</examples>
<output_format>...</output_format>
