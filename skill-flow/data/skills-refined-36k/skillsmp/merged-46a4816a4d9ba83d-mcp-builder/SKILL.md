---
name: mcp-builder
description: Use this skill to create high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools, applicable for integrating external APIs or services using Python (FastMCP) or Node/TypeScript (MCP SDK).
---

# MCP 服务器开发指南

## 概述

创建高质量的 MCP（模型上下文协议）服务器，使 LLM 能够通过精心设计的工具与外部服务交互。MCP 服务器的质量衡量标准是它能在多大程度上帮助 LLM 完成现实世界的任务。

---

## 开发流程

### 🚀 高级工作流程

建立高质量的 MCP 服务器涉及四个主要阶段：

### 第一阶段：深入研究与规划

#### 1.1 理解以代理为中心的设计原则

- **为工作流程而非仅为 API 端点建立**：创建深思熟虑、高影响力的工作流程工具，整合相关操作。
- **针对有限的上下文进行优化**：确保每个 token 都有价值，提供高信号信息。
- **设计可操作的错误消息**：错误消息应引导代理朝向正确的使用模式。
- **遵循自然任务细分**：工具名称应反映人类对任务的思考方式。
- **使用评估驱动开发**：及早建立实际的评估场景，快速原型制作并根据代理效能进行迭代。

#### 1.2 研究 MCP 协议文档

- 从 `https://modelcontextprotocol.io/sitemap.xml` 开始查找相关页面，获取最新的 MCP 协议文件。

#### 1.3 研究框架文档

- **推荐技术栈**：
  - **TypeScript**：高质量的 SDK 支持和良好的兼容性。
  - **Python**：生态丰富、易于上手。

#### 1.4 建立全面的实施计划

- 列出要实现的最有价值的端点/操作，优先考虑常见和重要用例。

---

### 第二阶段：实现

#### 2.1 设置项目结构

- **Python**：建立单一 `.py` 文件或组织成模块。
- **Node/TypeScript**：建立适当的项目结构，设置 `package.json` 和 `tsconfig.json`。

#### 2.2 实现核心基础设施

- 创建共享工具，如 API 请求辅助函数、错误处理工具和响应格式化函数。

#### 2.3 系统化地实现工具

- 定义输入架构，使用 Pydantic（Python）或 Zod（TypeScript）进行验证。
- 撰写全面的文档字符串/说明，确保工具功能的清晰描述。

---

### 第三阶段：审查和优化

#### 3.1 代码质量

审查以下方面：
- 没有重复代码（DRY 原则）。
- 一致的错误处理。
- 完整的类型覆盖。

#### 3.2 测试和构建

- 使用 MCP Inspector 进行交互式测试，确保服务器正常运行。

---

### 第四阶段：创建评估

#### 4.1 理解评估目的

使用评估来测试 LLM 是否能有效使用你的 MCP 服务器来回答现实、复杂的问题。

#### 4.2 创建 10 个评估问题

遵循评估指南中概述的流程，确保每个问题都满足独立性、复杂性和可验证性。

---

# 参考文件

## 📚 文档库

在开发过程中根据需要加载这些资源：

- **MCP 协议**：从 `https://modelcontextprotocol.io/sitemap.xml` 获取。
- [📋 MCP 最佳实践](./reference/mcp_best_practices.md) - 通用 MCP 指导原则。
- **Python SDK**：从 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md` 获取。
- **TypeScript SDK**：从 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md` 获取。