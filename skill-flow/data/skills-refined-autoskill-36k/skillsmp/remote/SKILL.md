---
name: remote
description: 远程仓库管理技能 - 智能推送、拉取和多仓库同步。用于安全推送、智能拉取、同步分支或管理多个远程仓库。
disable-model-invocation: false
argument-hint: [push|pull|sync|push-all] [args...]
---

# Skill: Remote

远程仓库管理技能 - 智能推送、拉取和多仓库同步。

## 核心功能

- 🚀 **智能推送** - 安全检查和分批推送
- 📥 **智能拉取** - 冲突预防和策略选择
- 🔗 **多仓库管理** - 同步多个远程仓库
- 🌐 **分支同步** - 自动同步远程分支
- 📊 **状态监控** - 实时同步状态监控

## 快速使用

```bash
# 安全推送
/remote push main --safe

# 智能拉取
/remote pull --auto

# 同步分支
/remote sync --all

# 多仓库推送
/remote push-all --remotes origin,backup
```

## 配置

```json
{
  "remote": {
    "safetyChecks": true,
    "autoSync": false,
    "multiRemote": true
  }
}
```

## 详细信息

- 🔗 [Git 工具函数](../../references/utils/git-helpers.md)
- 🔗 [错误处理](../../references/errors/error-types.md)
- 🔗 [通用类型定义](../../references/types/common-types.md)
