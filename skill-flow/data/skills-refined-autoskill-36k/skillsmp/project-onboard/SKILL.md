---
name: project-onboard
description: Use this skill when entering a new or legacy project for the first time, to scan and localize global skills for project-specific conventions. Triggers on "onboard", "init skills", "localize skills", "project setup", or when Claude detects an unfamiliar codebase that would benefit from adapted workflows.
---

# Project Onboarding

分析项目，把全局 skills 本地化到 `.skills/`。

## 流程

1. **探索项目** — 用 Glob/Read 看目录结构、配置文件、代码样本
2. **理解规范** — 从代码推断项目的测试、lint、commit 等规范
3. **扫描全局 skills** — `ls ~/.claude/skills/`
4. **对比分析** — 哪些 skill 需要适配？哪些直接可用？
5. **交互确认** — 列出建议，让用户选择
6. **生成 .skills/** — 写入本地化版本

## 排除列表（不参与本地化）

以下元 skills 默认跳过，除非用户明确要求：

```
project-onboard    # 本 skill
skill-cleanup      # 清理工具
skill-builder      # 创建工具
skill-creator      # 创建工具
skill-install      # 安装工具
skill-sync         # 同步工具
workflow-analyze   # 分析工具
```

这些是管理 skills 的工具，不是项目工作流的一部分。

## 探索时重点看

```
配置文件: package.json, pyproject.toml, Makefile, tsconfig.json
CI/CD: .github/workflows/, .gitlab-ci.yml
规范: .eslintrc, .prettierrc, commitlint.config.js
测试: jest.config.js, pytest.ini, *_test.go
现有 Claude 配置: CLAUDE.md, .claude/
```

## 输出格式

```
.skills/
├── MANIFEST.json      # 简单记录：哪些被本地化了
├── test/
│   └── SKILL.md       # 适配后的 test skill
└── commit/
    └── SKILL.md       # 适配后的 commit skill
```

## MANIFEST.json 示例

```json
{
  "project": "my-app",
  "localized": ["test", "commit"],
  "skipped": ["code"],
  "created": "2024-01-12"
}
```

## 本地化适配示例

全局 skill 写的是 `npm test`，但项目用 jest:

```markdown
## Pre-flight Checklist
- [ ] Run `jest --coverage`
- [ ] Ensure coverage > 80%
```

## ephemeral 标记

如果是临时任务相关的 skill，在 SKILL.md 开头加注释:

```markdown
<!-- ephemeral: pr_merged:#123 -->
```

这样 `/skill-cleanup` 知道什么时候可以清理。
