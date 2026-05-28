# 模板（最小可用）

> 说明：只提供最小骨架，避免把冗长模板灌入上下文；需要时再扩展。

## `Record/plan/draft-plan.md`（最小骨架）

```markdown
---
doc_type: plan
plan_version: ""
status: draft
created_at: ISO8601
project_root: "<确认的项目根目录>"
---

# 预定清单（草案）

## 详细需求描述

<!-- 完整记录需求，供 Claude 分析用 -->

## 待澄清问题

<!-- 需要进一步确认的点 -->
- 技术栈选择：...
- 部署方式：...
- 其他：...
```

## `Record/state.json`（最小骨架）

```json
{
  "active_plan_version": "",
  "agents_registry_path": "~/.claude/agents/plan-agent/skills/agents-registry/references/registry.yaml",
  "environment_path": "~/environment.md",
  "proposals": {}
}
```

## `Record/record.md`（项目记录）

```markdown
# 项目记录

> 记录项目重大事件，便于回溯。git相关记录包含commit hash。

<!-- 由各阶段自动追加，勿手动编辑格式 -->
```

### 记录格式

```markdown
## YYYY-MM-DD HH:MM 事件类型
内容...
```

### 事件类型

| 类型 | 触发时机 | 记录内容 |
|------|---------|---------|
| 需求提出 | project-bootstrap | 需求摘要 |
| 方案确定 | plan-finalize | 方案版本、任务数 |
| 子代理完成 | 子代理提交后 | commit hash、提交信息 |
| 编译结果 | build-agent完成 | 成功/失败、产出/错误摘要 |
| 代码审核 | code-review完成 | 通过/问题数 |
| 提案修改 | plan-agent修改提案 | 修改原因、影响范围 |
| 归档完成 | project-complete步骤2 | commit hash、归档提案数 |
| 推送远程 | project-complete步骤4 | commit hash、远程分支 |
| 阻塞事件 | 环境/子代理缺失 | 阻塞原因、解决方式 |

## `Record/Memory/`（子代理记忆目录）

子代理记忆文件存放在 `Record/Memory/` 目录下，由各子代理启动时自动创建和管理。

### 命名规则

| 类型 | 命名 | 示例 |
|------|------|------|
| 唯一实例子代理 | `{agent-name}.md` | `plan-agent.md`、`build-agent.md` |
| 多实例子代理 | `{agent-name}-{nn}.md` | `python-agent-01.md`、`rust-agent-02.md` |

### 目录结构示例

```
Record/Memory/
├── plan-agent.md           # 规划子代理记忆
├── analysis-agent.md       # 分析子代理记忆
├── neutral-agent.md        # 仲裁子代理记忆
├── build-agent.md          # 构建子代理记忆
├── python-agent-01.md      # Python实现子代理01
├── python-agent-02.md      # Python实现子代理02
└── rust-agent-01.md        # Rust实现子代理01
```

### 记忆文件模板

参见 `~/.claude/agents/plan-agent/references/memory-template.md`
