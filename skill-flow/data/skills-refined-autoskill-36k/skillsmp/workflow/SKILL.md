---
name: workflow
description: 团队工作流管理技能 - 协作规范、自动化流程和最佳实践。用于初始化工作流、创建功能分支、分配代码审查或发布版本。
disable-model-invocation: false
argument-hint: [init|start-feature|assign-review|release] [args...]
---

# Skill: Workflow

团队工作流管理技能 - 协作规范、自动化流程和最佳实践。

## 核心功能

- 🏗️ **工作流模板** - GitFlow、GitHub Flow 等
- 👥 **代码审查** - 自动分配和管理
- 🚀 **发布管理** - 版本控制和自动化发布
- 📋 **团队规范** - 提交规范执行
- 🔗 **工具集成** - JIRA、Slack 等

## 快速使用

```bash
# 初始化工作流
/workflow init --template gitflow

# 创建功能分支
/workflow start-feature PROJ-123 "用户认证"

# 分配审查
/workflow assign-review

# 发布版本
/workflow release --type minor
```

## 配置

```json
{
  "workflow": {
    "template": "gitflow",
    "autoReview": true,
    "autoRelease": false,
    "integrations": ["slack", "jira"]
  }
}
```

## 详细信息

- 🔗 [分支策略配置](../../references/config/branch-strategies.md)
- 🔗 [提交类型配置](../../references/config/commit-types.md)
- 🔗 [错误处理](../../references/errors/error-types.md)
