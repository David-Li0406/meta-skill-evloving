---
name: mcp-builder
description: MCP（Model Context Protocol）服务器开发指南。当用户需要开发 MCP 服务器、创建 LLM 工具集成、或构建 AI 代理与外部服务交互的接口时使用。
---

# MCP Builder - MCP 服务器开发指南

## 概述

MCP 服务器使 LLM 能够通过设计良好的工具与外部服务交互。

---

## 技术栈选择

| 技术栈 | 推荐度 | 理由 |
|--------|--------|------|
| **TypeScript** | ⭐⭐⭐⭐⭐ | SDK 支持好、类型安全 |
| **Python** | ⭐⭐⭐⭐ | 生态丰富、易于上手 |

**传输协议**：
- **Streamable HTTP**：推荐用于远程服务器
- **stdio**：适用于本地工具

---

## 开发流程

### 阶段1：研究与规划

```
规划清单：
1. 目标服务的 API 文档在哪里？
2. 需要实现哪些核心功能？
3. 哪些是只读操作？哪些是写操作？
4. 需要什么认证方式？
```

### 阶段2：实现

**TypeScript 项目结构**：
```
my-mcp-server/
├── src/
│   ├── index.ts
│   ├── server.ts
│   ├── tools/
│   └── utils/
├── package.json
└── tsconfig.json
```

**Python 项目结构**：
```
my-mcp-server/
├── src/my_mcp_server/
│   ├── __init__.py
│   ├── server.py
│   ├── tools/
│   └── utils/
└── pyproject.toml
```

### 阶段3：测试

使用 MCP Inspector 进行交互式测试：
```bash
npx @anthropic-ai/mcp-inspector
```

---

## 工具注解

| 注解 | 说明 |
|------|------|
| `readOnlyHint` | 只读操作 |
| `destructiveHint` | 破坏性操作 |
| `idempotentHint` | 幂等操作 |

---

## 最佳实践

- **单一职责**：每个工具只做一件事
- **清晰命名**：使用动词+名词格式
- **完整描述**：包含用途、参数、返回值说明
- **统一错误处理**：所有错误使用相同格式
- **分页支持**：大数据集必须支持分页

---

## 参考资源

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
