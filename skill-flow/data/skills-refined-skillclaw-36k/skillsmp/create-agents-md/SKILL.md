---
name: create-agents-md
description: 创建或更新 AGENTS.md 文件，为 AI coding agents 提供项目上下文和指令。当用户要求创建 AGENTS.md、设置 agent 指南、或添加项目特定的 agent 指令时使用此技能。
---

# Create AGENTS.md

为 AI coding agents 创建项目指导文档。AGENTS.md 是一个开放格式，被超过 60k 开源项目使用。

## 前置要求

**在应用此技能前，必须先阅读以下技能以了解基础编写规范**：

1. 内置的 `create-skill` 技能（提供文档结构和组织原则）
2. [create-skill-overrides](./../create-skill-overrides/SKILL.md) 技能（提供编写风格、命令格式、跨平台兼容性等核心规范）

本技能专注于 AGENTS.md 的特定内容和用途，通用的编写规范请参考上述技能。

## 何时创建 AGENTS.md

为每个需要 agent 特定上下文的项目创建：

- 项目根目录：整体项目指南
- 子目录/包：特定包的覆盖指南（monorepo 场景）

**优先级规则**：最近的 AGENTS.md（相对于正在编辑的文件）优先级更高

## 核心内容

AGENTS.md 使用标准 Markdown，无必需字段。只包含 agent 需要但无法轻易推断的信息。

### 标题规则

使用 `# 此目录及其子目录的 AGENTS 指南` 作为一级标题

**必须**遵循此标题格式以保持整个项目的一致性。

### 推荐章节

```markdown
# 此目录及其子目录的 AGENTS 指南

## 设置命令

安装依赖: `pnpm install`
启动开发服务器: `pnpm dev`
运行测试: `pnpm test`

## 代码风格

- TypeScript strict 模式
- 单引号，无分号
- 优先使用函数式模式

## 开发环境提示

- 使用 `pnpm dlx turbo run where <project_name>` 快速跳转到包
- 检查每个包的 `package.json` 中的 `name` 字段确认正确的包名

## 测试指令

- 运行所有测试: `pnpm turbo run test --filter <project_name>`
- 运行特定测试: `pnpm vitest run -t "<test name>"`
- **必须**：提交前所有测试通过

## PR 指令

- 标题格式: `[<project_name>] <Title>`
- 提交前运行 `pnpm lint` 和 `pnpm test`
```

### 常见章节模板

根据项目需求选择相关章节：

**项目概览**

```markdown
## 项目概览

这是一个 [技术栈] 项目，使用 [主要框架/工具]
```

**构建和测试**

```markdown
## 构建

构建生产版本: `npm run build`
验证构建: `npm run validate:build`

## 测试

运行单元测试: `npm test`
运行集成测试: `npm run test:integration`
```

**安全考虑**

```markdown
## 安全

- **必须**：所有用户输入经过验证和清理
- API 密钥存储在 `.env` 文件中（不提交）
- 使用 `npm audit` 检查依赖漏洞
```

**部署**

```markdown
## 部署

### 准备

- 确保测试通过: `npm test`
- 更新版本: `npm version patch`

### 发布

- 构建: `npm run build`
- 部署: `npm run deploy`
```

## Monorepo 支持

大型 monorepo 可在子包中放置独立的 AGENTS.md：

```
project/
├── AGENTS.md              # 根目录及其子目录的整体指南
├── packages/
│   ├── frontend/
│   │   └── AGENTS.md      # frontend 目录及其子目录的特定指南
│   └── backend/
│       └── AGENTS.md      # backend 目录及其子目录的特定指南
```

最近的文件优先级更高，允许包级别覆盖根级别指令。

## 示例

完整示例：

```markdown
# 此目录及其子目录的 AGENTS 指南

## 设置命令

安装依赖: `pnpm install`
启动开发服务器: `pnpm dev --port 3000`
运行测试: `pnpm test`

## 代码风格

- TypeScript strict 模式
- 单引号，无分号
- 优先使用函数式模式

## 开发环境提示

- 使用 `pnpm dlx turbo run where <project_name>` 跳转到包
- 运行 `pnpm install --filter <project_name>` 添加包到工作区
- 检查每个 `package.json` 的 `name` 字段确认包名

## 测试指令

- CI 配置在 [.github/workflows](./.github/workflows) 文件夹
- 运行包测试: `pnpm turbo run test --filter <project_name>`
- 修复所有测试和类型错误
- 更改代码时添加或更新测试

## PR 指令

- 标题格式: `[<project_name>] <Title>`
- **必须**：提交前运行 `pnpm lint` 和 `pnpm test`
```

## 验证清单

创建 AGENTS.md 后验证（通用格式规范参见 [create-skill-overrides](../create-skill-overrides/SKILL.md)）：

- [ ] 使用正确的标题格式：`# 此目录及其子目录的 AGENTS 指南`
- [ ] 包含项目设置命令
- [ ] 说明代码风格约定
- [ ] 提供测试运行指令
- [ ] 如果是 monorepo，说明包导航方式
- [ ] 只包含 agent 需要但无法从代码推断的信息

## 总结

AGENTS.md 是为 AI agents 提供的项目 README：

- **项目特定** - 聚焦于项目独有的知识和约定
- **开发导向** - 提供设置、测试、构建等开发命令
- **分层支持** - monorepo 可在子包中提供覆盖指令
- **持续更新** - 随项目演进保持同步

编写规范遵循 [create-skill-overrides](../create-skill-overrides/SKILL.md) 中的通用原则。
