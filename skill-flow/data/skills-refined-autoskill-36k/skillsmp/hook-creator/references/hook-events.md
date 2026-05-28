# Hook 钩子事件参考

## 事件概览

| 事件 | 触发时机 | 可阻塞 | 典型用途 |
|-------|---------|-----------|-------------|
| PreToolUse | 工具执行前 | 是（退出代码 2） | 验证、阻塞 |
| PostToolUse | 工具完成后 | 否 | 格式化、日志记录 |
| PermissionRequest | 显示权限对话框时 | 是 | 自动允许/拒绝 |
| UserPromptSubmit | 用户提交提示时 | 否 | 预处理 |
| Notification | Claude 发送通知时 | 否 | 自定义提醒 |
| Stop | Claude 完成响应时 | 否 | 后处理 |
| SubagentStop | 子代理任务完成时 | 否 | 子代理清理 |
| PreCompact | 压缩操作前 | 否 | 压缩前操作 |
| SessionStart | 会话开始/恢复时 | 否 | 初始化 |
| SessionEnd | 会话结束时 | 否 | 清理 |

## PreToolUse

在工具调用前运行。可以阻塞执行。

**输入架构：**
```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "ls -la",
    "description": "列出文件"
  }
}
```

**退出代码：**
- `0` - 允许工具继续执行
- `2` - 阻塞工具，stdout 作为反馈发送给 Claude

**各工具的常见 tool_input 字段：**
- `Bash`: `command`, `description`
- `Edit`: `file_path`, `old_string`, `new_string`
- `Write`: `file_path`, `content`
- `Read`: `file_path`
- `Glob`: `pattern`, `path`
- `Grep`: `pattern`, `path`

## PostToolUse

在工具调用完成后运行。

**输入架构：**
```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/file.ts"
  },
  "tool_response": "文件编辑成功"
}
```

**使用场景：**
- 自动格式化编辑的文件
- 记录工具结果
- 触发相关操作

## PermissionRequest

显示权限对话框时运行。

**输入架构：**
```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm install"
  },
  "permission_type": "execute"
}
```

**退出代码：**
- `0` - 让用户决定
- `1` - 自动拒绝
- `2` - 自动允许

## Notification

Claude 发送通知时运行。

**输入架构：**
```json
{
  "message": "等待您的输入",
  "type": "input_required"
}
```

**使用场景：**
- 自定义桌面通知
- Slack/Discord 警报
- 声音通知

## UserPromptSubmit

用户提交提示时运行，Claude 处理之前。

**输入架构：**
```json
{
  "prompt": "帮我修复这个 bug",
  "session_id": "abc123"
}
```

**使用场景：**
- 提示日志记录
- 预处理
- 上下文注入

## Stop

Claude 完成响应时运行。

**输入架构：**
```json
{
  "stop_reason": "end_turn",
  "session_id": "abc123"
}
```

**使用场景：**
- 会话日志记录
- 清理任务
- 指标收集

## SubagentStop

子代理（Task 工具）任务完成时运行。

**输入架构：**
```json
{
  "subagent_type": "Explore",
  "result": "找到 5 个匹配文件"
}
```

## PreCompact

Claude 压缩对话上下文之前运行。

**输入架构：**
```json
{
  "reason": "context_limit",
  "current_tokens": 50000
}
```

## SessionStart

Claude Code 开始或恢复会话时运行。

**输入架构：**
```json
{
  "session_id": "abc123",
  "is_resume": false,
  "project_dir": "/path/to/project"
}
```

**使用场景：**
- 环境设置
- 加载项目配置
- 启动后台服务

## SessionEnd

Claude Code 会话结束时运行。

**输入架构：**
```json
{
  "session_id": "abc123",
  "end_reason": "user_exit"
}
```

**使用场景：**
- 清理资源
- 保存会话状态
- 停止后台服务