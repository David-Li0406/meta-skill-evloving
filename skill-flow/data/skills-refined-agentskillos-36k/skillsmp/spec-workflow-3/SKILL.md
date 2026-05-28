---
name: spec-workflow
description: 在使用 Spec Workflow MCP 进行开发时加载此 skill 以获取操作规范。
mcp:
  spec-workflow:
    command: pnpm
    args: [ "dlx", "@pimzino/spec-workflow-mcp@latest" ]
---

# Spec Workflow 操作指南

在使用 Spec Workflow 进行开发时，请严格遵守以下操作指南：

## 阅读 MCP 指南

- 确保通过 Spec Workflow MCP 提供的工具阅读过全部指南

## Workspace 工作模式

- 当用户要求时采用 `jj workspace` 或 `git worktree` 模式来物理隔离每个 Spec 的工作空间
- 具体 Workspace 的名称可以使用 Spec 的名称或其变体
- 如果 Spec 涉及多个仓库，要创建一个独立的目录来统一存放这些相关的 Workspace，以保持工作区整洁
- 如果 `.spec-workflow` 是一个仓库，则同样需要创建 Workspace

## 文档语言

- 所有 Spec Workflow 相关的文档必须全部使用**中文**编写

## 目录路径约束

- 必须且只能使用当前工作空间根目录下的 `.spec-workflow` 目录存放所有文档
