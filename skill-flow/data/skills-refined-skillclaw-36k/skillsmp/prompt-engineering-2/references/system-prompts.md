# System / Developer 角色提示

来源：
- https://platform.claude.com/docs/zh-CN/build-with-claude/prompt-engineering/system-prompts

要点
- system/developer 用于稳定角色、风格与硬性规则；用户消息放具体任务。
- 避免在用户消息里重复系统规则，减少冲突。
- 系统提示应简洁、稳定、与业务约束一致。

示例结构
<system>
  你是...（角色/风格/限制）
</system>
<user>
  任务与输入...
</user>
