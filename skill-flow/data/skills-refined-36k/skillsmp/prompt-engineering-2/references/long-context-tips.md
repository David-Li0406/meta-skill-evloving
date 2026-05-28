# 长上下文提示

来源：
- https://platform.claude.com/docs/zh-CN/build-with-claude/prompt-engineering/long-context-tips

要点
- 把长文档放在前面，把问题放在最后，提升定位准确性。
- 用 <document> 标签区分多文档，并标记来源/标题。
- 要求回答引用证据，必要时先做摘要再回答问题。

示例结构
<documents>
  <document>
    <source>doc-a</source>
    <content>...</content>
  </document>
</documents>
<question>...</question>
