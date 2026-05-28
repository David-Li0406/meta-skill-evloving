---
name: project-index
description: Use this skill for large project maintenance with layered CLAUDE.md index system. Triggers when users need to (1) analyze and document existing codebases, (2) generate hierarchical CLAUDE.md files for modules, (3) set up incremental update hooks after code changes, or (4) navigate large projects efficiently. Supports legacy project onboarding and automatic context management.
version: 1.0.0
triggers:
  - 分析项目
  - 生成文档
  - 代码审计
  - 测试修复
  - 测试生成
  - 检查过期
  - project index
  - CLAUDE.md
  - AUDIT.md
dependencies:
  required:
    - codeagent-wrapper
  optional:
    - kanban
ports:
  dashboard: 3008
  kanban: 3007
tags:
  - documentation
  - testing
  - audit
  - maintenance
---

# Project Index - Layered CLAUDE.md System

自动生成和维护大型项目的层次化 CLAUDE.md 索引系统。

## 功能清单

| 功能 | 脚本 | 说明 |
|------|------|------|
| **文档生成** | `generate.js` | 生成/更新 CLAUDE.md |
| **代码审计** | `code-audit.js` | 生成 AUDIT.md，检测安全问题 |
| **过期检测** | `check-stale.js` | 检测文档/审计/测试是否过期 |
| **测试映射** | `test-mapper.js` | 源码↔测试映射，生成 .test-map.json |
| **测试生成** | `test-generator.js` | 批量生成缺失测试 |
| **测试修复** | `test-fix.js` | 并发修复测试错误 |
| **审计修复** | `audit-fix.js` | 并发修复审计问题 |
| **Dashboard** | `dashboard.js` | Web UI (http://localhost:3008) |

## AI 交互指引

### 主动询问

完成批量任务后，应主动询问用户：

```
任务完成。是否打开 Dashboard 查看详细状态？
→ 运行: node scripts/dashboard.js --open
→ 访问: http://localhost:3008
```

### 任务前检查

执行文档/测试任务前，先检查状态：

```bash
node scripts/check-stale.js --stale-only --json
```

根据输出决定处理范围。

## 触发场景

1. **新项目入驻** — 用户说"帮我分析这个项目"、"生成文档"
2. **遗留项目理解** — 用户说"这个代码库怎么组织的"
3. **代码修改后** — 检测到核心模块变更，提醒更新文档
4. **测试维护** — 用户说"生成测试"、"修复测试"
5. **审计需求** — 用户说"检查安全问题"、"代码审计"

## 前置依赖

| 依赖 | 类型 | 用途 |
|------|------|------|
| **codeagent-wrapper** | 必需 | LLM 调用 |
| **kanban** | 可选 | 审计任务自动创建 |

## 核心概念

### 三层架构

```
project/CLAUDE.md           # Layer 1: 概览 + 模块索引
    ↓
src/modules/auth/CLAUDE.md  # Layer 2: 模块详情 + 子模块索引
    ↓
src/modules/auth/jwt/CLAUDE.md  # Layer 3: 实现细节
```

### 智能覆盖策略

不是每个目录都需要独立 CLAUDE.md：

- **大目录** (≥5 文件或 ≥200 行) → 必须有独立 CLAUDE.md
- **小目录** + 父目录有 CLAUDE.md → 由父目录覆盖
- **小目录** + 父目录无 CLAUDE.md → 孤儿，需关注

详见 [docs/coverage.md](docs/coverage.md)

### 层级依赖排序

批量生成时按目录深度从深到浅处理：

```
js/agents/core/sandbox/system  → 先生成
js/agents/core/sandbox         → 后生成
js/agents/core                 → 再后
js/agents                      → 最后
```

确保父目录生成时可引用子目录的 CLAUDE.md。

### AUDIT.md 同策略

代码审计 (`code-audit.js`) 采用相同策略：
- 大目录生成独立 AUDIT.md
- 小目录由父目录审计覆盖
- 审计提示词包含未独立审计的小子目录代码

## 快速开始

```bash
# 1. 扫描项目
node scripts/scan.js

# 2. 生成 CLAUDE.md
node scripts/generate.js --auto

# 3. 安装 hooks
node scripts/hook.js init

# 4. 启动 Dashboard
node scripts/dashboard.js --open
```

## 常用命令

详见 [docs/commands.md](docs/commands.md)

快速参考：

```bash
node scripts/module-analyzer.js          # 日常维护
node scripts/module-analyzer.js --all    # 全量处理
node scripts/check-stale.js --stale-only # 过期检测
node scripts/test-fix.js                 # 修复测试错误
node scripts/dashboard.js --open         # Web UI
```

## 工作流

### 新项目

1. `hook.js init` - 安装 hooks + 创建配置
2. `scan.js` - 分析结构
3. `generate.js --auto` - 生成文档
4. 开始开发

### 遗留项目

1. `scan.js` - 理解结构
2. `hook.js init` - 安装配置
3. `generate.js --auto` - 生成文档
4. `module-analyzer.js` - 初始审计
5. 按需调整

### 代码修改后

修改模块代码后，**必须**检查并更新对应的 `CLAUDE.md` 和 `AUDIT.md`：

1. **检查 CLAUDE.md**
   - 内容需要更新 → 修改文档内容
   - 内容仍然准确 → `touch CLAUDE.md` 更新时间戳

2. **检查 AUDIT.md**
   - 新增安全问题 → 补充到 Issues 列表
   - 问题已修复 → 使用 `audit-archive.js` 归档
   - 内容仍然准确 → `touch AUDIT.md` 更新时间戳

3. **验证状态**
   ```bash
   node scripts/check-stale.js <module-path> --stale-only
   node scripts/audit-status.js <module-path>
   ```

> **重要**：即使没有实质性改动，也必须 touch 文件以更新时间戳，否则 stale 检测会持续报告该模块过期。

## 详细文档

| 文档 | 内容 |
|------|------|
| [docs/commands.md](docs/commands.md) | 常用命令详解 |
| [docs/coverage.md](docs/coverage.md) | 智能覆盖率策略、批量任务发现 |
| [docs/dashboard.md](docs/dashboard.md) | Web UI 仪表盘详解 |
| [docs/scripts.md](docs/scripts.md) | 所有脚本参考 |
| [docs/config.md](docs/config.md) | 配置文件说明 |
| [docs/testing.md](docs/testing.md) | 测试工具链详解 |
| [docs/anti-patterns.md](docs/anti-patterns.md) | ⚠️ 禁止的错误模式 |

## 配置

创建 `.stale-config.json`：

```json
{
  "include": ["js/agents/**"],
  "ignore": ["tests/**", "docs/**"],
  "features": { "doc": true, "audit": true, "kanban": true, "testAnalysis": true },
  "concurrency": 6
}
```

## 测试追踪

测试状态与 CLAUDE.md/AUDIT.md 统一追踪：

```bash
# 检查测试覆盖状态
node scripts/check-stale.js --type=test --stale-only

# 检查所有类型（doc + audit + test）
node scripts/check-stale.js --type=all --stale-only

# 刷新测试映射
node scripts/test-mapper.js

# 查看模块测试详情
node scripts/test-view.js js/agents/core
```

测试状态类型：
- **missing** - 模块无测试覆盖
- **stale** - 源码已修改但测试未更新
- **fresh** - 测试与源码同步

详见 [docs/testing.md](docs/testing.md)

## 与 Codex 集成

更新父目录时注入小子目录上下文：

```bash
context=$(node generate.js --prompt-context --module js/agents/ingest)

codex-wrapper - <<EOF
更新 js/agents/ingest/CLAUDE.md

$context
EOF
```

## Kanban API

审计任务自动创建到 Kanban：

```bash
export KANBAN_URL=http://127.0.0.1:3007/api/v1
```

未运行 Kanban 服务时静默跳过。

## ⚠️ 禁止的错误模式

测试修复和代码生成时必须避免的反模式。

详见 [docs/anti-patterns.md](docs/anti-patterns.md)
