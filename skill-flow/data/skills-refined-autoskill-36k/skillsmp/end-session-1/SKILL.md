---
name: end-session
description: 结束当前对话
---

# End Session Skill

用户希望结束当前对话。

## 执行流程

1. **总结本次对话**
   - 简要回顾完成的工作
   - 列出关键成果或决策

2. **调用 cunzhi 脚本**
   - 正常调用 `python3 cunzhi.py {PORT}`
   - 用户在 GUI 中点击"结束"按钮

## 示例 output.md 格式

```markdown
## 会话总结

### 完成的工作
- ...

### 关键成果
- ...
```

## 注意事项

- 对话已实时记录到 `conversations/YYYY-MM-DD.md`，无需额外操作
- 结束对话只是让 `KeepGoing=false`
