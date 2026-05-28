---
name: branch
description: 智能分支管理技能 - 策略、操作自动化和冲突解决。用于创建分支、合并分支、检查冲突 or 清理分支。
disable-model-invocation: false
argument-hint: [create|merge|check-conflicts|cleanup] [args...]
---

# Skill: Branch

智能分支管理技能 - 策略、操作自动化和冲突解决。

## 核心功能

- 🌳 **分支策略** - GitFlow、GitHub Flow 等
- 📝 **智能命名** - 自动生成规范的分支名
- 🔄 **操作自动化** - 创建、合并、清理
- ⚔️ **冲突解决** - 预测和自动解决冲突
- 🛡️ **分支保护** - 规则验证和合规检查

## 快速使用

```bash
# 创建功能分支
/branch create feature PROJ-123 "添加用户认证"

# 合并分支
/branch merge feature/auth into develop

# 检查冲突
/branch check-conflicts feature/auth develop

# 清理分支
/branch cleanup
```

## 配置

```json
{
  "branch": {
    "strategy": "gitflow",
    "autoNaming": true,
    "protection": true,
    "autoCleanup": true
  }
}
```

## 详细信息

- 🔗 [分支策略配置](../../references/config/branch-strategies.md)
- 🔗 [Git 工具函数](../../references/utils/git-helpers.md)
- 🔗 [错误处理](../../references/errors/error-types.md)
