---
name: mcp-builder
description: Use this skill to create high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools, applicable for both Python (FastMCP) and Node/TypeScript (MCP SDK).
---

# MCP 服务器开发指南

## 概述

创建高质量的 MCP（模型上下文协议）服务器，使 LLM 能够通过精心设计的工具与外部服务交互。MCP 服务器的质量衡量标准是它能在多大程度上帮助 LLM 完成现实世界的任务。

---

# 流程

## 🚀 高级工作流程

建立高质量的 MCP 服务器涉及四个主要阶段：

### 第一阶段：深入研究与规划

#### 1.1 理解以代理为中心的设计原则

- **为工作流程而非仅为 API 端点建立**：创建深思熟虑、高影响力的工作流程工具，整合相关操作。
- **针对有限的上下文进行优化**：确保每个 token 都有价值，提供高信号信息。
- **设计可操作的错误消息**：错误消息应引导代理朝向正确的使用模式。
- **遵循自然任务细分**：工具名称应反映人类对任务的思考方式。
- **使用评估驱动开发**：及早建立实际的评估场景，快速原型并根据代理反馈进行迭代。

#### 1.2 研究 MCP 协议文档

使用 WebFetch 加载最新的 MCP 协议文件：`https://modelcontextprotocol.io/llms-full.txt`。

#### 1.3 研究框架文档

- **MCP 最佳实践**：[📋 查看最佳实践](./reference/mcp_best_practices.md) - 核心指导原则。

#### 1.4 详细研究 API 文件

审查服务的 API 文档以识别关键端点、认证要求和数据模型。

#### 1.5 建立全面的实施计划

根据研究，建立包含工具选择、共用工具、输入/输出设计和错误处理策略的详细计划。

---

### 第二阶段：实现

#### 2.1 设置项目结构

- **Python**：建立单一 `.py` 文件或组织成模块，使用 MCP Python SDK 进行工具注册。
- **Node/TypeScript**：建立适当的项目结构，设置 `package.json` 和 `tsconfig.json`，使用 MCP TypeScript SDK。

#### 2.2 实现核心基础设施

创建共享实用程序，包括 API 请求助手、错误处理工具和响应格式化函数。

#### 2.3 系统化地实现工具

对每个工具定义输入架构，撰写全面的文档字符串，实施工具逻辑并支持多种响应格式。

---

### 第三阶段：审查和优化

#### 3.1 代码质量检查

确保代码遵循 DRY 原则，具有一致的错误处理和完整的类型覆盖。

#### 3.2 测试和构建

使用评估测试工具进行测试，确保服务器在主进程中安全运行。

---

### 第四阶段：创建评估

实现 MCP 服务器后，建立全面的评估以测试其有效性。

#### 4.1 理解评估目的

评估测试 LLM 是否能有效使用您的 MCP 服务器来回答实际的复杂问题。

#### 4.2 创建评估问题

遵循评估指南中概述的流程，创建 10 个复杂的、现实的问题。

---

# 参考文件

## 📚 文档库

在开发过程中根据需要加载这些资源：

### 核心 MCP 文档
- **MCP 协定**：从 `https://modelcontextprotocol.io/llms-full.txt` 获取 - 完整的 MCP 规范。
- [📋 MCP 最佳实践](./reference/mcp_best_practices.md) - 通用 MCP 指导原则。

### SDK 文档
- **Python SDK**：从 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md` 获取。
- **TypeScript SDK**：从 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md` 获取。

### 特定语言实现指南
- [🐍 Python 实现指南](./reference/python_mcp_server.md) - 完整的 Python/FastMCP 指南。
- [⚡ TypeScript 实现指南](./reference/node_mcp_server.md) - 完整的 TypeScript 指南。

### 评估指南
- [✅ 评估指南](./reference/evaluation.md) - 完整的评估创建指南。