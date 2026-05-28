---
name: env-update
description: "环境更新触发：安装环境后调用 env-agent 更新文档。触发条件：执行了任何环境安装命令。"
---

# env-update

环境安装后自动触发 env-agent 更新 ~/environment.md。

## When to Use This Skill

触发条件（满足任一）：
- 执行了 `apt install`、`npm install -g`、`pip install`、`cargo install` 等安装命令
- 用户手动执行安装命令并确认完成
- 安装了新的开发工具、运行时、库或依赖

## Not For / Boundaries

**不做**：
- Claude 主对话不直接修改 ~/environment.md
- 不跳过 env-agent 直接记录环境变更

## Quick Reference

### 调用方式

```
Task: env-agent
prompt: "更新环境文档。刚安装了：[工具名称]。验证安装并更新 ~/environment.md"
```

### 执行流程

```
1. 检测到安装命令执行完成
2. 调用 env-agent（传入安装的工具名称）
3. env-agent 验证安装并更新 ~/environment.md
```

## Examples

### Example 1: npm 全局安装

- **输入**: `sudo npm install -g @gitee/mcp-gitee`
- **触发**: 安装完成后
- **调用**: `Task: env-agent, prompt: "更新环境文档。刚安装了：@gitee/mcp-gitee。验证安装并更新 ~/environment.md"`

### Example 2: apt 安装

- **输入**: `sudo apt install libssl-dev`
- **触发**: 用户确认安装完成后
- **调用**: `Task: env-agent, prompt: "更新环境文档。刚安装了：libssl-dev。验证安装并更新 ~/environment.md"`

## Maintenance

- 最后更新：2026-01-11
