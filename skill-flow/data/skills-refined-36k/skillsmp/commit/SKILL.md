---
name: commit
description: 智能代码提交技能 - 分析变更并生成规范提交信息。用于分析代码变更、生成符合规范的提交信息、执行质量检查或创建提交。
disable-model-invocation: false
argument-hint: [analyze|check|create]
---

# Skill: Commit

智能代码提交技能 - 分析变更并生成规范提交信息。用于分析代码变更、生成符合规范的提交信息、执行质量检查或创建提交。

## 核心功能

- 📊 **变更分析** - 识别文件类型和影响范围
- 🏷️ **类型检测** - 自动识别 feat/fix/docs 等类型
- 📍 **Scope识别** - 自动确定变更模块
- 📝 **信息生成** - 生成符合规范的提交信息
- ✅ **质量检查** - 检查敏感信息、TODO等
- 🚫 **纯净提交** - 绝不添加 AI 工具标识，保持提交历史专业

## 快速使用

```bash
# 分析并生成提交信息
/ct analyze

# 执行质量检查
/ct check

# 一键提交
/ct create
```

## 配置

```json
{
  "commit": {
    "messageFormat": "conventional",
    "qualityChecks": true,
    "autoScope": true
  }
}
```

## 详细信息

- 🔗 [提交类型配置](../../references/config/commit-types.md)
- 🔗 [Git 工具函数](../../references/utils/git-helpers.md)
- 🔗 [错误处理](../../references/errors/error-types.md)