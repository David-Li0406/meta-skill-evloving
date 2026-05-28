---
name: history
description: Git 历史管理技能 - 重写、优化和分析历史。用于分析提交历史质量、执行 rebase、搜索提交或创建历史快照。
disable-model-invocation: false
argument-hint: [analyze|rebase|search|snapshot] [args...]
---

# Skill: History

Git 历史管理技能 - 重写、优化和分析历史。

## 核心功能

- 📊 **历史分析** - 提交质量评分和问题检测
- ✏️ **历史重写** - 安全的 interactive rebase
- 🔍 **智能搜索** - 多维度提交搜索
- 📸 **历史快照** - 创建和恢复历史状态
- ⚠️ **异常检测** - 识别历史问题模式

## 快速使用

```bash
# 分析历史质量
/history analyze --depth 100

# Interactive rebase
/history rebase HEAD~10

# 搜索提交
/history search --author "john"

# 创建快照
/history snapshot pre-release
```

## 配置

```json
{
  "history": {
    "autoAnalysis": true,
    "rebaseSafety": true,
    "snapshotRetention": 30
  }
}
```

## 详细信息

- 🔗 [Git 工具函数](../../references/utils/git-helpers.md)
- 🔗 [错误处理](../../references/errors/error-types.md)
- 🔗 [通用类型定义](../../references/types/common-types.md)
