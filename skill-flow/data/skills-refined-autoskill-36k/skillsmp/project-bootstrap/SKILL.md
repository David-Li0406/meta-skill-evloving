---
name: project-bootstrap
description: 项目启动与落盘导航。触发：用户开始新项目/首次提出需求时，确认项目根目录并创建 Record/ 目录结构。
metadata:
  short-description: 项目启动落盘与 Record 结构
  tags: [workflow, record, planning]
  access: plan-agent-internal
---

# project-bootstrap

> **访问控制**：此 skill 仅限 plan-agent 内部调用，Claude 主对话和其他子代理不可直接调用。

项目启动标准化，确保规划可落盘、可追溯。

## When to Use This Skill

- 用户说"开始一个项目"/"我的需求是..."
- 首次提出需求需要进入循环A规划
- 项目目录下没有 `Record/` 结构

## Not For / Boundaries

**不做**：
- 不分析需求（由 draft-plan-review 负责）
- 不生成提案（由 plan-finalize 负责）
- 不写入 `~/ai-synergy/`（那是全局配置）

**必需输入**：项目需求描述。缺少时询问用户。

## Quick Reference

### 硬性规则

```
- 产物写入项目根目录的 Record/（禁止写入 ~/ai-synergy/）
- 未确认项目根目录前，不得创建任何文件
- 默认项目根目录 = CWD
```

### Record 目录结构

```
项目根目录/
└── Record/
    ├── plan/draft-plan.md   # 预定清单草案
    ├── Memory/              # 子代理记忆目录
    │   ├── plan-agent.md    # 规划子代理记忆
    │   └── ...              # 其他子代理记忆
    ├── state.json           # 项目状态机
    └── record.md            # 事件日志
```

### 执行步骤

```
1. 确认项目根目录（询问用户）
2. 创建 Record/plan/ 和 Record/Memory/
3. 生成 draft-plan.md（需求+待澄清问题）
4. 初始化 state.json
5. 创建 record.md + Memory/plan-agent.md
6. 输出下一步指令
```

## Examples

### Example 1: 新项目启动

- **输入**: "我想做一个命令行工具"
- **步骤**: 确认CWD → 创建Record/ → 写入draft-plan.md
- **验收**: Record/目录存在，draft-plan.md包含需求描述

### Example 2: 已有项目补建Record

- **输入**: "这个项目还没有Record目录"
- **步骤**: 确认项目根目录 → 创建Record/ → 初始化所有文件
- **验收**: Record/结构完整

### Example 3: 需求不明确

- **输入**: "帮我做个东西"
- **步骤**: AskUserQuestion询问具体需求 → 确认后创建Record/
- **验收**: draft-plan.md的"待澄清问题"章节列出需确认项

## References

- `references/bootstrap.md` - 详细执行步骤
- `references/templates.md` - 文件模板

## Maintenance

- 来源：双AI协同开发方案
- 最后更新：2026-01-05
- 已知限制：仅创建结构，不分析需求
