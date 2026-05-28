# Codex MCP 工具调用规范

## 工具概述

`mcp__codex__codex` 通过 MCP 协议调用，执行 AI 辅助编码任务。

## 参数

### 必选参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `PROMPT` | string | 任务指令 |
| `cd` | Path | 工作目录根路径 |

### 可选参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `sandbox` | string | "read-only" | 沙箱策略 |
| `SESSION_ID` | UUID | None | 会话 ID，用于多轮交互 |
| `skip_git_repo_check` | bool | False | 允许非 Git 仓库运行 |
| `return_all_messages` | bool | False | 返回所有消息（含推理、工具调用） |
| `image` | List[Path] | None | 附加图片文件 |
| `model` | string | None | 指定模型 |
| `yolo` | bool | False | 跳过审批和沙箱 |
| `profile` | string | None | 配置文件名称 |

### sandbox 策略

| 值 | 说明 |
|----|------|
| `read-only` | 只读模式（**推荐**） |
| `workspace-write` | 允许工作区写入 |
| `danger-full-access` | 完全访问权限 |

## 返回值

成功：
```json
{
  "success": true,
  "SESSION_ID": "uuid-string",
  "agent_messages": "回复内容",
  "all_messages": []  // 仅 return_all_messages=True
}
```

失败：
```json
{
  "success": false,
  "error": "错误信息"
}
```

## 会话管理

### 开启新会话
不传 `SESSION_ID`，工具返回新 ID

### 继续会话
传入之前的 `SESSION_ID`，上下文保留

## 调用规范

**必须遵守**：
- 保存返回的 `SESSION_ID` 以便后续复用
- `cd` 必须指向存在的目录
- 使用 `sandbox="read-only"` 避免意外修改
- 原型阶段只要求 unified diff patch

**推荐**：
- 需要追踪推理过程时设置 `return_all_messages=True`
- 精准定位、debug、快速原型优先使用 Codex
