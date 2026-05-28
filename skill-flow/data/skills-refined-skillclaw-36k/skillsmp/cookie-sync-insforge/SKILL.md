---
name: cookie-sync-insforge
description: 动态访问 cookie-sync-insforge MCP 服务器 (1 个工具)
version: 1.0.0
---

# cookie-sync-insforge Skill

此 Skill 允许 Claude 动态调用 cookie-sync-insforge，无需预加载所有工具定义。

## 可用工具列表

- `example_tool`: 来自 Node.js MCP 服务器的示例工具

## 使用模式

当用户请求需要此 Skill 时：

1. **确定工具**：从上方列表中选择合适的工具。
2. **生成调用 JSON**：
```json
{
  "tool": "工具名",
  "arguments": { "参数名": "值" }
}
```

3. **执行命令**：
```bash
node $SKILL_DIR/executor.js --call 'JSON_STRING'
```

## 获取详细参数定义
如果不知道参数怎么传，执行：
```bash
node $SKILL_DIR/executor.js --describe 工具名
```
