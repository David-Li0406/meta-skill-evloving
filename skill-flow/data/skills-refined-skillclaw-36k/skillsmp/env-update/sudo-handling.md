---
name: sudo-handling
description: "sudo 命令处理规范：env-agent 处理需要 sudo 权限的安装命令时的详细流程。"
---

# sudo 命令处理规范

env-agent 处理需要 sudo 权限的安装命令时必须遵守的详细流程。

## When to Use This Skill

当 env-agent 检测到需要 sudo 权限的安装命令时（如 apt install、npm install -g 等系统级安装）。

## 核心原则

**禁止直接输出命令后结束**：必须通过 AskUserQuestion 与用户交互，获取执行结果后再继续。

## 处理流程

```
检测到需要 sudo 的命令
        │
        ▼
使用 AskUserQuestion 询问用户
        │
        ▼
等待用户回复
        │
        ├─→ 已执行成功 → 验证安装 → 更新文档 → 继续下一项
        │
        ├─→ 执行失败 → 记录失败原因 → 继续下一项
        │
        └─→ 暂不执行 → 跳过该项 → 继续下一项
```

## AskUserQuestion 格式

```
需要 sudo 权限安装依赖，请在终端执行以下命令：

{完整的 sudo 命令}

执行完成后请告知结果。

选项：
1. 已执行成功
2. 执行失败（请说明错误信息）
3. 暂不执行
```

## 用户回复处理

| 用户选择 | 处理动作 |
|---------|---------|
| 已执行成功 | 1. 执行版本检查验证安装 2. 更新 env.md 打钩 3. 更新 ~/environment.md 4. 继续下一项 |
| 执行失败 | 1. 记录失败原因到 failed_items 2. 继续下一项 |
| 暂不执行 | 1. 跳过该项 2. 继续下一项 |

## 禁止的行为

- 禁止直接输出命令让用户手动执行后就结束任务
- 禁止不等待用户确认就继续执行后续步骤
- 禁止跳过文档更新步骤
- 禁止在用户确认成功后不验证安装结果

## 安装后文档更新（必须执行）

用户确认安装成功后，必须：

1. **验证安装**：执行版本检查或相关命令确认安装成功
2. **更新 env.md**：在对应项目打钩标记完成
3. **更新 ~/environment.md**：记录新安装的工具和版本

## Examples

### Example 1: apt 安装开发库

```
AskUserQuestion:
需要 sudo 权限安装依赖，请在终端执行以下命令：

sudo apt install libssl-dev libffi-dev

执行完成后请告知结果。

选项：
1. 已执行成功
2. 执行失败（请说明错误信息）
3. 暂不执行
```

用户选择"已执行成功"后：
1. 执行 `dpkg -l | grep libssl-dev` 验证
2. 更新 Record/env.md 打钩
3. 更新 ~/environment.md 添加记录

### Example 2: npm 全局安装

```
AskUserQuestion:
需要 sudo 权限安装全局包，请在终端执行以下命令：

sudo npm install -g typescript

执行完成后请告知结果。

选项：
1. 已执行成功
2. 执行失败（请说明错误信息）
3. 暂不执行
```

用户选择"已执行成功"后：
1. 执行 `tsc --version` 验证
2. 更新 Record/env.md 打钩
3. 更新 ~/environment.md 添加 TypeScript 版本记录

## Maintenance

- 最后更新：2026-01-12
- 关联文件：`~/.claude/agents/env-agent.md`
