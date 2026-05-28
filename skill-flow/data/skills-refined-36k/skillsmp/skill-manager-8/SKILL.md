---
name: skill-manager
description: Skill 生命周期管理器。用于批量扫描 Skills 目录、检查 GitHub 更新、执行版本升级、管理 Skills 库存。当用户需要"检查更新"、"列出 Skills"、"删除 Skill"或"管理 Skills"时使用此工具。
---

# Skill Manager

管理 Skills 的完整生命周期：扫描、检查更新、升级、删除。

## 核心功能

1. **扫描审计**: 扫描 Skills 目录，解析所有 SKILL.md 的 frontmatter 元数据
2. **版本检查**: 并发查询 GitHub（通过 `git ls-remote`）比较本地和远程 hash
3. **状态报告**: 生成状态报告，标识 outdated/current/unmanaged/error
4. **更新工作流**: 引导 Agent 执行 Skill 升级
5. **库存管理**: 列出、删除 Skills

## 使用场景

### 检查更新

**触发方式**:
- `/skill-manager check`
- "检查我的 Skills 是否有更新"
- "扫描 Skills 更新"

**工作流**:
1. Agent 运行 `scripts/scan_and_check.py <skills_dir>`
2. 脚本并发检查所有带有 `source_url` 的 Skills
3. 输出 JSON 格式的状态报告
4. Agent 向用户呈现结果

**示例输出**:
```
Skills 状态摘要
========================================
总计: 12 个 Skills
  - 最新: 8
  - 需更新: 2
  - 非托管: 1
  - 错误: 1

需要更新的 Skills:
  - yt-dlp: New commits available
    本地: abc123...
    远程: def456...
```

### 列出 Skills

**触发方式**:
- `/skill-manager list`
- "列出我的 Skills"
- "显示所有 Skills"

**工作流**:
1. Agent 运行 `scripts/list_skills.py <skills_dir>`
2. 输出表格或 JSON 格式的 Skills 列表

**示例输出**:
```
Name                   | Type     | Ver      | Description
-----------------------|----------|----------|------------------------------------------
md-to-pptx             | Standard | 1.0.0    | Markdown 转 PowerPoint 工具...
n8n-workflow-patterns  | Standard | 1.0.0    | n8n 工作流模式专家...
yt-dlp                 | GitHub   | 0.1.0    | YouTube 视频下载工具封装...
-----------------------|----------|----------|------------------------------------------
Total: 12 skills
```

### 更新 Skill

**触发方式**:
- "更新 [Skill 名称]"（在检查更新后）
- `/skill-manager update <skill_name>`

**工作流**:
1. Agent 从远程仓库获取新的 README
2. 对比新旧 README，识别变化（新功能、废弃参数等）
3. 重写 SKILL.md 反映新功能
4. 更新 `source_hash` 字段
5. 可选：更新 wrapper.py
6. 运行 `skill-evolution` 的 `align_all.py` 恢复用户经验

### 删除 Skill

**触发方式**:
- `/skill-manager delete <skill_name>`
- "删除 Skill: <skill_name>"

**工作流**:
1. Agent 运行 `scripts/delete_skill.py <skill_name> <skills_dir>`
2. 脚本显示 Skill 信息并请求确认
3. 可选：备份到 `.skill-backup` 目录
4. 执行删除

## 脚本说明

| 脚本 | 功能 | 参数 |
|------|------|------|
| `scan_and_check.py` | 扫描并检查更新 | `<skills_dir> [--json\|--summary\|--table]` |
| `list_skills.py` | 列出所有 Skills | `<skills_dir> [--json] [--verbose]` |
| `delete_skill.py` | 删除 Skill | `<skill_name> <skills_dir> [--backup] [--force]` |

## 元数据依赖

此管理器依赖以下元数据字段：

| 字段 | 用途 |
|------|------|
| `source_url` | 远程仓库 URL（用于检查更新） |
| `source_hash` | 本地记录的 commit hash |
| `version` | 语义化版本号 |
| `evolution_enabled` | 是否启用经验进化 |

**兼容性**: 同时支持旧格式的 `github_url` 和 `github_hash` 字段。

## 状态说明

| 状态 | 含义 |
|------|------|
| `current` | 本地 hash 与远程相同，无需更新 |
| `outdated` | 远程有新的 commits |
| `unmanaged` | 没有配置 `source_url`，无法检查更新 |
| `error` | 无法访问远程仓库 |
| `unknown` | 本地没有记录 hash |

## 最佳实践

1. **定期检查**: 建议每周运行一次 `/skill-manager check`
2. **备份删除**: 删除重要 Skill 前使用 `--backup` 选项
3. **更新后对齐**: 更新 Skill 后运行 `skill-evolution` 的 `align_all.py` 恢复经验
4. **版本控制**: 使用 Git 管理 Skills 目录，便于回滚

## 与其他 Skill 的协作

- **skill-factory**: 创建的 Skills 自动包含生命周期管理所需的元数据
- **skill-evolution**: 更新后调用 `align_all.py` 恢复用户经验
- **skill-creator**: 遵循相同的元数据规范
