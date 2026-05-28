# memex-cli Quick Decision Guide

快速决策指南，用于工作流快速选择并行模式和文件引用策略，**无需脚本计算**。

---

## 🚀 并行执行决策表

### 规则 1: 任务关系矩阵

| 任务类型 | 是否并行 | dependencies 参数 | 执行模式 |
|---------|---------|------------------|---------|
| 前端开发 + 后端开发 | ✅ YES | 无 | 并行 |
| 前端开发 + 后端开发 + 测试 | ⚠️ 部分 | 测试依赖前两者 | 2 波次 |
| 设计 + 实现 + 测试 | ❌ NO | 链式依赖 | 3 波次 |
| 多个独立组件 | ✅ YES | 无 | 全并行 |
| 数据库 + API + 前端 | ⚠️ 部分 | API 依赖数据库 | 2 波次 |

### 规则 2: 按任务类型快速匹配

**直接并行（无依赖）：**
```bash
✅ 前端 UI 组件 + 后端 API 端点
✅ 文档生成（架构 + API + UX）
✅ 多个独立模块实现
✅ 并行探索（多个设计方案）
✅ 批量数据处理任务
```

**两波次执行：**
```bash
Wave 1: 基础设施任务
  - 数据库 schema
  - 配置文件
  - 项目脚手架

Wave 2: 业务逻辑 (dependencies: Wave 1 任务)
  - API 实现
  - 前端页面
  - 集成测试
```

**三波次执行：**
```bash
Wave 1: 设计阶段
  - 架构设计
  - API 规格

Wave 2: 实现阶段 (dependencies: Wave 1)
  - 后端实现
  - 前端实现

Wave 3: 验证阶段 (dependencies: Wave 2)
  - 集成测试
  - 性能测试
```

### 规则 3: 反模式识别

**❌ 避免过度并行：**
```bash
# 错误：50 个小任务全部并行
---TASK---
id: component-button
---TASK---
id: component-input
---TASK---
id: component-modal
... (47 more tasks)

# 正确：按功能分组为 3-5 个大任务
---TASK---
id: frontend-core-components
---CONTENT---
实现核心 UI 组件（按钮、输入框、模态框等）
---END---
```

**❌ 避免过度串行：**
```bash
# 错误：所有任务链式依赖
task-1 → task-2 → task-3 → task-4 → task-5 → task-6

# 正确：识别可并行的任务
task-1 ──┬─→ task-3 ─→ task-5
         └─→ task-4 ─→ task-6
```

---

## 📂 文件引用模式决策表

### 规则 1: 按文件类型快速匹配

| 文件模式 | files-mode | 理由 |
|---------|-----------|------|
| `*.md` (单个) | `embed` | 文档通常 < 50 KB |
| `*.json`, `*.yaml` | `embed` | 配置文件通常 < 10 KB |
| `src/*.py` (单个文件) | `embed` | 单个代码文件通常 < 50 KB |
| `src/**/*.py` (glob) | `ref` | 多文件，总大小未知 |
| `docs/**/*.md` (glob) | `ref` | 多文档，避免超上下文 |
| `data/*.json` | `ref` | 数据文件可能很大 |
| `*.sql`, `*.csv` | `ref` | 数据库文件通常 > 100 KB |
| `*.png`, `*.jpg` | `ref` | 二进制文件必须 ref |
| `./` (项目根目录) | `auto` | 混合文件类型 |

### 规则 2: 按任务阶段快速匹配

| 工作流阶段 | 典型文件 | files-mode | 示例 |
|-----------|---------|-----------|------|
| **需求澄清** | requirements_draft.md | `embed` | 单个小文档 |
| **架构设计** | requirements.md | `embed` | 单个需求文档 |
| **API 规格** | requirements.md, architecture.md | `embed` | 2-3 个设计文档 |
| **数据库设计** | requirements.md, architecture.md, api-spec.md | `embed` | 多个设计文档，但总量小 |
| **开发计划** | requirements.md, architecture.md | `embed` | 设计文档需完整上下文 |
| **代码实现** | `docs/**/*.md` | `ref` | 所有文档，按需加载 |
| **代码审查** | `src/**/*.py` | `ref` | 多个源文件 |
| **测试生成** | `src/**/*.py`, `docs/api-spec.md` | `ref` | 代码 + 文档混合 |

### 规则 3: 按文件数量快速决策

```
文件数量 = 1           → embed
文件数量 = 2-3         → embed (如果都是小文档)
文件数量 = 4-10        → ref
文件数量 > 10          → ref
使用 glob 模式 (**/)  → ref
```

### 规则 4: 文件模式速查表

**直接使用 `embed`：**
```bash
# ✅ 单个配置文件
files: config.json
files-mode: embed

# ✅ 单个需求文档
files: requirements.md
files-mode: embed

# ✅ 2-3 个设计文档（总量 < 100 KB）
files: architecture.md,api-spec.md
files-mode: embed

# ✅ 单个小代码文件
files: src/utils.py
files-mode: embed
```

**直接使用 `ref`：**
```bash
# ✅ Glob 模式（任何 glob）
files: src/**/*.py
files-mode: ref

files: docs/**/*.md
files-mode: ref

files: tests/**/*.js
files-mode: ref

# ✅ 数据文件
files: data/*.json
files-mode: ref

files: logs/*.log
files-mode: ref

# ✅ 二进制文件
files: mockups/*.png
files-mode: ref

# ✅ 大型文件
files: database_dump.sql
files-mode: ref
```

**直接使用 `auto`：**
```bash
# ✅ 项目根目录
files: ./
files-mode: auto

# ✅ 混合文件类型
files: config.json,data/*.csv,src/**/*.py
files-mode: auto

# ✅ 不确定文件大小
files: user_generated/*
files-mode: auto
```

---

## 🎯 工作流快速配置模板

### 模板 1: 需求分析阶段

```bash
---TASK---
id: analyze-requirements-$RUN_ID
backend: claude
workdir: .
files: requirements_draft.md
files-mode: embed    # 单个小文档
---CONTENT---
分析需求文档并生成结构化输出
---END---
```

**决策逻辑：** 需求文档 < 20 KB → embed

---

### 模板 2: 设计阶段（并行生成多个文档）

```bash
# 并行生成 3 个设计文档
---TASK---
id: design-architecture-$RUN_ID
backend: claude
workdir: .
files: requirements.md
files-mode: embed    # 单个需求文档
---CONTENT---
生成架构设计文档
Save to: docs/architecture.md
---END---

---TASK---
id: design-api-$RUN_ID
backend: claude
workdir: .
files: requirements.md
files-mode: embed    # 同一份需求文档
---CONTENT---
生成 API 规格文档
Save to: docs/api-spec.md
---END---

---TASK---
id: design-database-$RUN_ID
backend: claude
workdir: .
files: requirements.md
files-mode: embed    # 同一份需求文档
---CONTENT---
生成数据库设计文档
Save to: docs/database-schema.md
---END---
```

**决策逻辑：**
- 3 个任务无依赖关系 → 并行执行
- 每个任务仅读取 requirements.md → embed

---

### 模板 3: 实现阶段（引用所有文档）

```bash
---TASK---
id: implement-backend-$RUN_ID
backend: codex
workdir: .
files: docs/**/*.md    # 引用所有设计文档
files-mode: ref        # 多文档，按需加载
---CONTENT---
根据设计文档实现后端代码
参考：
- architecture.md
- api-spec.md
- database-schema.md
---END---
```

**决策逻辑：**
- 多个文档（glob 模式） → ref
- Backend 按需读取相关部分

---

### 模板 4: 测试阶段（依赖实现）

```bash
---TASK---
id: implement-code-$RUN_ID
backend: codex
workdir: .
files: docs/**/*.md
files-mode: ref
---CONTENT---
实现代码
---END---

---TASK---
id: generate-tests-$RUN_ID
backend: codex
workdir: .
dependencies: implement-code-$RUN_ID    # 等待实现完成
files: src/**/*.py,docs/api-spec.md
files-mode: ref    # 源代码 + API 文档
---CONTENT---
为实现的代码生成测试用例
---END---
```

**决策逻辑：**
- 测试依赖代码实现 → dependencies
- 源代码 + 文档（glob） → ref

---

### 模板 5: 混合并行（2 波次）

```bash
# Wave 1: 基础设施（并行）
---TASK---
id: setup-database-$RUN_ID
backend: codex
workdir: .
files: docs/database-schema.md
files-mode: embed    # 单个设计文档
---CONTENT---
创建数据库 schema 和迁移脚本
---END---

---TASK---
id: setup-config-$RUN_ID
backend: codex
workdir: .
files: docs/architecture.md
files-mode: embed    # 单个架构文档
---CONTENT---
生成项目配置文件
---END---

# Wave 2: 业务逻辑（依赖 Wave 1）
---TASK---
id: implement-api-$RUN_ID
backend: codex
workdir: .
dependencies: setup-database-$RUN_ID    # 依赖数据库
files: docs/**/*.md
files-mode: ref    # 所有设计文档
---CONTENT---
实现 API 端点
---END---

---TASK---
id: implement-frontend-$RUN_ID
backend: codex
workdir: .
dependencies: setup-config-$RUN_ID    # 依赖配置
files: docs/ux-design.md,docs/api-spec.md
files-mode: embed    # 2 个设计文档
---CONTENT---
实现前端页面
---END---
```

**决策逻辑：**
- Wave 1: 2 个基础任务无依赖 → 并行
- Wave 2: 2 个业务任务各有依赖 → 等待后并行

---

## 🔍 快速决策流程图

### 并行决策（30 秒）

```
START
  ↓
任务之间有数据依赖?
  ↓ NO → 全部并行执行 (无 dependencies)
  ↓ YES
  ↓
能否分组为 2-3 波次?
  ↓ YES → 混合并行 (部分 dependencies)
  ↓ NO
  ↓
是否必须严格串行?
  ↓ YES → 链式依赖 (全部 dependencies)
  ↓
END
```

### 文件引用决策（20 秒）

```
START
  ↓
使用 glob 模式 (**/)?
  ↓ YES → files-mode: ref
  ↓ NO
  ↓
文件数量 > 3?
  ↓ YES → files-mode: ref
  ↓ NO
  ↓
确定都是小文件 (< 50 KB)?
  ↓ YES → files-mode: embed
  ↓ NO
  ↓
files-mode: auto
  ↓
END
```

---

## 📋 multcode 命令优化建议

### 当前问题

```bash
# Stage 3: 文档生成（5 个串行任务）
memex-cli run --stdin <<EOF
---TASK---
id: stage3-architecture-$RUN_ID
...
EOF

memex-cli run --stdin <<EOF
---TASK---
id: stage3-api-spec-$RUN_ID
...
EOF

memex-cli run --stdin <<EOF
---TASK---
id: stage3-ux-design-$RUN_ID
...
EOF

# 问题：5 次串行调用，总耗时 = 累加
```

### 优化方案：单次调用并行

```bash
# Stage 3: 文档生成（1 次调用，5 个并行任务）
memex-cli run --stdin <<EOF
---TASK---
id: stage3-architecture-$RUN_ID
backend: $STAGE3_BACKEND
workdir: .
files: .claude/$RUN_ID/requirements.md
files-mode: embed
---CONTENT---
生成架构设计文档
Save to: .claude/$RUN_ID/docs/architecture.md
---END---

---TASK---
id: stage3-api-spec-$RUN_ID
backend: $STAGE3_BACKEND
workdir: .
files: .claude/$RUN_ID/requirements.md
files-mode: embed
---CONTENT---
生成 API 规格文档
Save to: .claude/$RUN_ID/docs/api-spec.md
---END---

---TASK---
id: stage3-ux-design-$RUN_ID
backend: $STAGE3_BACKEND
workdir: .
files: .claude/$RUN_ID/requirements.md
files-mode: embed
---CONTENT---
生成 UX 设计文档
Save to: .claude/$RUN_ID/docs/ux-design.md
---END---

---TASK---
id: stage3-database-schema-$RUN_ID
backend: $STAGE3_BACKEND
workdir: .
files: .claude/$RUN_ID/requirements.md,.claude/$RUN_ID/docs/architecture.md
files-mode: embed
dependencies: stage3-architecture-$RUN_ID    # 依赖架构设计
---CONTENT---
生成数据库设计文档
Save to: .claude/$RUN_ID/docs/database-schema.md
---END---

---TASK---
id: stage3-development-plan-$RUN_ID
backend: $STAGE3_BACKEND
workdir: .
files: .claude/$RUN_ID/requirements.md,.claude/$RUN_ID/docs/architecture.md
files-mode: embed
dependencies: stage3-architecture-$RUN_ID    # 依赖架构设计
---CONTENT---
生成开发计划
Save to: .claude/$RUN_ID/docs/development-plan.md
---END---
EOF
```

**优化效果：**
- 原耗时：5 × 4s = 20s（串行）
- 优化后：Wave 1 (3 任务并行) + Wave 2 (2 任务并行) ≈ 8s
- 性能提升：**60% 时间节省**

---

## 💡 核心原则总结

### 并行执行原则

1. **默认并行** - 无依赖关系的任务应该并行
2. **波次分组** - 有依赖的任务按波次执行（2-3 层最佳）
3. **避免过度细分** - 3-10 个并行任务为最佳粒度
4. **单次调用** - 使用单个 memex-cli 调用定义所有任务

### 文件引用原则

1. **Glob 必用 ref** - 任何 `**/` glob 模式使用 ref
2. **单文档用 embed** - 单个小文档（< 50 KB）使用 embed
3. **不确定用 auto** - 无法判断时使用 auto
4. **多文档用 ref** - 超过 3 个文件使用 ref

### 决策时间目标

- **并行决策** < 30 秒（参考任务关系矩阵）
- **文件引用决策** < 20 秒（参考文件模式速查表）
- **无需脚本计算文件大小或依赖关系**

---

## 🚦 快速检查清单

**在编写 memex-cli 调用前，快速回答：**

**并行：**
- [ ] 任务之间有数据依赖吗？（有 → dependencies，无 → 并行）
- [ ] 能否分为 2-3 波次？（可以 → 混合模式）
- [ ] 任务数量 < 10？（是 → 合理，否 → 重新分组）

**文件引用：**
- [ ] 使用 glob 模式吗？（是 → ref）
- [ ] 文件数量 > 3？（是 → ref）
- [ ] 确定都是小文件吗？（是 → embed，否 → auto）

**检查全通过 → 开始编写配置**

---

## 📚 完整示例参考

参见 `examples/` 目录中的实际示例：
- `examples/parallel-tasks.md` - 完全并行示例
- `examples/dag-workflow.md` - 混合并行 + 依赖示例
- `examples/file-loading-patterns.md` - 文件引用模式示例
