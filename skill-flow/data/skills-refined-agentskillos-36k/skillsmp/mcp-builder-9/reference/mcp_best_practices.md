# MCP 服务器最佳实践

## 快速参考

### 服务器命名
- **Python**：`{service}_mcp`（例如 `slack_mcp`）
- **Node/TypeScript**：`{service}-mcp-server`（例如 `slack-mcp-server`）

### 工具命名
- 使用 snake_case 加服务前缀
- 格式：`{service}_{action}_{resource}`
- 示例：`slack_send_message`、`github_create_issue`

### 响应格式
- 同时支持 JSON 和 Markdown 格式
- JSON 用于程序化处理
- Markdown 用于人类可读性

### 分页
- 始终尊重 `limit` 参数
- 返回 `has_more`、`next_offset`、`total_count`
- 默认为 20-50 项

### 传输
- **可流式 HTTP**：用于远程服务器、多客户端场景
- **stdio**：用于本地集成、命令行工具
- 避免 SSE（已弃用，改用可流式 HTTP）

---

## 服务器命名约定

遵循这些标准化的命名模式：

**Python**：使用格式 `{service}_mcp`（小写加下划线）
- 示例：`slack_mcp`、`github_mcp`、`jira_mcp`

**Node/TypeScript**：使用格式 `{service}-mcp-server`（小写加连字符）
- 示例：`slack-mcp-server`、`github-mcp-server`、`jira-mcp-server`

名称应该是：
- 通用的，描述被集成的服务
- 容易从任务描述推断出来
- 不包含版本号

---

## 工具命名和设计

### 工具命名

1. **使用 snake_case**：`search_users`、`create_project`、`get_channel_info`
2. **包含服务前缀**：预期你的 MCP 服务器可能与其他 MCP 服务器一起使用
   - 使用 `slack_send_message` 而不仅仅是 `send_message`
   - 使用 `github_create_issue` 而不仅仅是 `create_issue`
3. **以行动为导向**：以动词开头（get、list、search、create 等）
4. **具体化**：避免可能与其它服务器冲突的通用名称

### 工具设计

- 工具描述必须精确且无歧义地描述功能
- 描述必须与实际功能精确匹配
- 提供工具注释（readOnlyHint、destructiveHint、idempotentHint、openWorldHint）
- 保持工具操作专注和原子化

---

## 响应格式

所有返回数据的工具都应该支持多种格式：

### JSON 格式（`response_format="json"`）
- 机器可读的结构化数据
- 包含所有可用字段和元数据
- 一致的字段名称和类型
- 用于程序化处理

### Markdown 格式（`response_format="markdown"`，通常为默认）
- 人类可读的格式化文本
- 使用标题、列表和格式化以清晰显示
- 将时间戳转换为人类可读格式
- 在括号中显示 ID 的显示名称
- 省略详细的元数据

---

## 分页

对于列出资源的工具：

- **始终尊重 `limit` 参数**
- **实现分页**：使用 `offset` 或基于游标的分页
- **返回分页元数据**：包含 `has_more`、`next_offset`/`next_cursor`、`total_count`
- **永远不要将所有结果加载到内存中**：对于大数据集尤其重要
- **默认为合理的限制**：通常 20-50 项

示例分页响应：
```json
{
  "total": 150,
  "count": 20,
  "offset": 0,
  "items": [...],
  "has_more": true,
  "next_offset": 20
}
```

---

## 传输选项

### 可流式 HTTP

**最适合**：远程服务器、Web 服务、多客户端场景

**特性**：
- 通过 HTTP 的双向通信
- 支持多个同时客户端
- 可部署为 Web 服务
- 启用服务器到客户端通知

**在以下情况使用**：
- 同时为多个客户端提供服务
- 部署为云服务
- 与 Web 应用程序集成

### stdio

**最适合**：本地集成、命令行工具

**特性**：
- 标准输入/输出流通信
- 设置简单，不需要网络配置
- 作为客户端的子进程运行

**在以下情况使用**：
- 为本地开发环境构建工具
- 与桌面应用程序集成
- 单用户、单会话场景

**注意**：stdio 服务器不应记录到 stdout（使用 stderr 进行记录）

### 传输选择

| 标准 | stdio | 可流式 HTTP |
|-----------|-------|-----------------|
| **部署** | 本地 | 远程 |
| **客户端** | 单个 | 多个 |
| **复杂性** | 低 | 中等 |
| **实时性** | 否 | 是 |

---

## 安全最佳实践

### 认证和授权

**OAuth 2.1**：
- 使用来自受认可机构的证书进行安全 OAuth 2.1
- 在处理请求之前验证访问令牌
- 只接受专门为你的服务器指定的令牌

**API 密钥**：
- 将 API 密钥存储在环境变量中，绝不在代码中存储
- 在服务器启动时验证密钥
- 当认证失败时提供清晰的错误消息

### 输入验证

- 清理文件路径以防止目录遍历
- 验证 URL 和外部标识符
- 检查参数大小和范围
- 在系统调用中防止命令注入
- 对所有输入使用模式验证（Pydantic/Zod）

### 错误处理

- 不要向客户端暴露内部错误
- 在服务器端记录安全相关错误
- 提供有帮助但不揭示信息的错误消息
- 在错误后清理资源

### DNS 重新绑定保护

对于本地运行的可流式 HTTP 服务器：
- 启用 DNS 重新绑定保护
- 验证所有传入连接上的 `Origin` 头
- 绑定到 `127.0.0.1` 而不是 `0.0.0.0`

---

## 工具注释

提供注释以帮助客户端理解工具行为：

| 注释 | 类型 | 默认 | 描述 |
|-----------|------|---------|-------------|
| `readOnlyHint` | boolean | false | 工具不修改其环境 |
| `destructiveHint` | boolean | true | 工具可能执行破坏性更新 |
| `idempotentHint` | boolean | false | 使用相同参数重复调用没有额外效果 |
| `openWorldHint` | boolean | true | 工具与外部实体交互 |

**重要**：注释是提示，不是安全保证。客户端不应仅基于注释做出安全关键决策。

---

## 错误处理

- 使用标准 JSON-RPC 错误代码
- 在结果对象中报告工具错误（而不是协议级错误）
- 提供有用的、具体的错误消息并建议后续步骤
- 不要暴露内部实现细节
- 在错误时正确清理资源

示例错误处理：
```typescript
try {
  const result = performOperation();
  return { content: [{ type: "text", text: result }] };
} catch (error) {
  return {
    isError: true,
    content: [{
      type: "text",
      text: `错误：${error.message}。尝试使用 filter='active_only' 来减少结果。`
    }]
  };
}
```

---

## 测试要求

全面的测试应该覆盖：

- **功能测试**：使用有效/无效输入验证正确执行
- **集成测试**：与外部系统的交互测试
- **安全测试**：验证认证、输入清理、速率限制
- **性能测试**：负载下的行为、超时检查
- **错误处理**：确保正确的错误报告和清理

---

## 文档要求

- 提供所有工具和功能的清晰文档
- 包含工作示例（每个主要功能至少 3 个）
- 记录安全注意事项
- 指定所需权限和访问级别
- 记录速率限制和性能特征