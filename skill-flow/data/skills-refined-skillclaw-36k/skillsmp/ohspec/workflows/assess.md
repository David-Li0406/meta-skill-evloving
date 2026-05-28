# ASSESS 阶段 - 代码库规模评估

## 目录
- [概述](#概述)
- [执行时机](#执行时机)
- [评估步骤](#评估步骤)
- [策略决策](#策略决策)
- [输出格式](#输出格式)
- [示例](#示例)

---

## 概述

**目标**：在执行代码扫描前，快速评估代码库规模，选择最优扫描策略，避免上下文爆炸。

**执行者**：编排器（自动执行，无需子代理）

## 硬约束（强制）

ASSESS 的定位是“**选择策略**”，不是“**开始扫描内容**”。为了避免 Codex 单代理模式下跑飞：

- **时间预算**：ASSESS 应在 **30 秒内**完成；超出则直接选择“保守策略（Grep 预过滤 + 小批 Read）”并进入 Dispatcher。
- **命令预算**：最多执行 **3 次**关键词统计类搜索（`--count`/`-l`），禁止跑“十几组 pattern 循环”。
- **禁止 Read**：ASSESS 阶段**不得 Read 代码文件内容**（否则等于扫描做两遍）。
- **必须落盘**：ASSESS 结束时必须写入 `progress.json`：
  - `tooling.search_tool / fallback_used / scan_scope / metrics`
  - `phases.assess.status/started_at/completed_at`
  - `audit_log` 追加一条 `assess_completed`
  若未写入，视为失败，禁止进入 Dispatcher。
- **固定 scan_scope**：所有搜索命令必须显式限定在 repo root（例如 `$ROOT`），并排除 `.claude/**` 等生成物目录（避免把历史 RFC 当成“代码证据”）。

**预期收益**：
- 大型项目性能提升 3-5 倍
- 节省 30-50% token
- 避免盲目扫描导致的超时或内存问题

---

## 执行时机

在初始化三文件之后、启动 Dispatcher 之前执行：

```
用户需求 → 初始化三文件 → ASSESS → Dispatcher → analyze → design → precheck → audit
```

---

## 评估步骤

### 步骤 0：选择搜索工具（性能优先）

优先级：`ripgrep (rg)` → `ag` → `Grep` → `bash grep` → `find + cat`

记录到 `progress.json.tooling`：
```json
{
  "tooling": {
    "search_tool": "ripgrep",
    "fallback_used": "none",
    "version": "15.1.0"
  }
}
```

> Codex/单代理建议：优先用 Bash `rg`，并且**每条命令都带显式路径**（`rg ... "$ROOT"`），不要依赖当前工作目录。

### 统一排除规则（强制，性能优先）

为了避免把生成物/依赖目录当作“代码证据”，并减少 I/O 成本，所有搜索默认排除：

```
.git/ .claude/ .ohspec/ node_modules/ dist/ build/ vendor/ .venv/ target/
```

> 建议将排除规则固化到 `.rgignore`/`.ignore`，避免每条命令重复维护。

### 步骤 1：统计文件数量

优先使用“文件列表 + 计数”，不要 Read 内容。

**推荐（优先 git ls-files，fallback 到 rg）**：

```bash
# 显式限定 ROOT，并排除 .claude 生成物
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
if git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git -C "$ROOT" ls-files | wc -l
else
  rg --files --hidden \
    --glob '!**/.git/**' \
    --glob '!**/.claude/**' \
    --glob '!**/.ohspec/**' \
    --glob '!**/node_modules/**' \
    --glob '!**/dist/**' \
    --glob '!**/build/**' \
    --glob '!**/vendor/**' \
    --glob '!**/.venv/**' \
    --glob '!**/target/**' \
    "$ROOT" | wc -l
fi
```

**记录**：
- 总文件数
- 各类型文件数量（.js, .ts, .py 等）

### 步骤 2：预览关键词匹配

使用上一步选择的搜索工具预览关键词匹配数量（不读取完整内容）：

```bash
# 预览关键词匹配数量
rg -l "关键词" "$ROOT" --hidden \
  --glob '!**/.git/**' \
  --glob '!**/.claude/**' \
  --glob '!**/.ohspec/**' \
  --glob '!**/node_modules/**' \
  --glob '!**/dist/**' \
  --glob '!**/build/**' \
  --glob '!**/vendor/**' \
  --glob '!**/.venv/**' \
  --glob '!**/target/**' | wc -l
```

**记录**：
- 匹配文件数量
- 预估相关文件占比

> **强制**：本步骤最多做 1-3 个关键词（通常来自需求关键词），禁止跑长列表循环。

### 快速路径（优先）

满足以下任一条件，可跳过或收缩关键词预览（仍需落盘）：
- `total_files <= 10`（小仓库）→ 可直接进入策略决策
- 用户已明确给出入口/配置/依赖的路径 → 仅做 1 个高信号关键词或直接进入策略决策

### 结果复用（可选）

若 `git HEAD` 未变化，可复用上次 ASSESS 的文件数量与关键词匹配结果（减少重复 I/O）：
- 以 `repo_root + HEAD` 为 key 缓存结果到 `.ohspec/cache/`
- 复用需记录到 `audit_log`（例如 `assess_cache_hit`）
- 一旦证据不足（key_files/facts 不达标）立即回退实时扫描

### 步骤 3：估算上下文大小

根据统计数据估算上下文消耗：

```
预估 tokens = 文件数 × 平均行数 × 4 (字符到token比例)
```

**假设**：
- 平均每个文件 200 行
- 平均每行 50 字符
- 1 token ≈ 4 字符

**示例**：
- 10 文件：10 × 200 × 50 ÷ 4 = 25,000 tokens
- 50 文件：50 × 200 × 50 ÷ 4 = 125,000 tokens
- 100 文件：100 × 200 × 50 ÷ 4 = 250,000 tokens

---

## 策略决策

根据评估结果选择扫描策略：

| 文件数 | 预估上下文 | 策略 | 说明 |
|--------|-----------|------|------|
| ≤ 10 | < 30K tokens | **直接扫描** | 直接读取所有相关文件 |
| 10-50 | 30K-150K tokens | **Grep 预过滤** | 先 Grep 定位，再读取匹配文件 |
| 50-100 | 150K-300K tokens | **分区并行扫描** | 按模块分区，并行扫描（最多 5 个子代理） |
| > 100 | > 300K tokens | **摘要模式** | 只读取关键文件，其他生成摘要 |

### 策略详细说明

#### 1. 直接扫描（≤ 10 文件）

```
Glob 找到文件 → Read 全部文件 → 分析
```

**适用**：小型项目、单模块修改

#### 2. Grep 预过滤（10-50 文件）

```
Grep 关键词 → 获取匹配文件列表 → Read 匹配文件 → 分析
```

**适用**：中型项目、关键词明确

#### 3. 分区并行扫描（50-100 文件）

```
按模块分区 → 并行启动子代理（最多 5 个）→ 各自扫描 → 汇总结果
```

**适用**：大型项目、多模块

**限制**：最多 5 个并行子代理，避免资源耗尽

#### 4. 摘要模式（> 100 文件）

```
识别核心文件（≤ 20 个）→ Read 核心文件 → 其他文件生成摘要 → 分析
```

**适用**：超大型项目

**核心文件识别**：
- Grep 匹配度最高的文件
- 入口文件（main, index, app）
- 配置文件

---

## 输出格式

评估结果写入 `progress.json`（推荐落点：`tooling` + `phases.assess` + `audit_log`）：

```json
{
  "tooling": {
    "search_tool": "ripgrep",
    "fallback_used": "none",
    "scan_scope": "/repo/root",
    "metrics": {
      "total_searches": 2,
      "total_time_sec": 1.2,
      "avg_time_sec": 0.6
    }
  },
  "phases": {
    "assess": {
      "status": "complete",
      "started_at": "2026-01-19T10:29:59Z",
      "completed_at": "2026-01-19T10:30:00Z",
      "summary": {
        "total_files": 45,
        "keyword_matches": 12,
        "selected_strategy": "grep_prefilter",
        "max_files_to_read": 15
      }
    }
  },
  "audit_log": [
    {"time": "2026-01-19T10:30:00Z", "action": "assess_completed", "detail": "files=45, matches=12, strategy=grep_prefilter"}
  ]
}
```

---

## 示例

### 示例 1：小型项目（直接扫描）

**输入**：用户需求 "为 audio.js 添加音量控制"

**评估**：
- Glob 找到 5 个 .js 文件
- Grep "audio" 匹配 2 个文件
- 预估：5 × 200 × 50 ÷ 4 = 12,500 tokens

**策略**：直接扫描
```json
{
  "strategy": {
    "selected": "direct_scan",
    "reason": "文件数 5，预估 12.5K tokens，直接扫描最高效"
  }
}
```

### 示例 2：中型项目（Grep 预过滤）

**输入**：用户需求 "重构用户认证模块"

**评估**：
- Glob 找到 35 个 .ts 文件
- Grep "auth" 匹配 8 个文件
- 预估：35 × 200 × 50 ÷ 4 = 87,500 tokens

**策略**：Grep 预过滤
```json
{
  "strategy": {
    "selected": "grep_prefilter",
    "reason": "文件数 35，Grep 匹配 8 个，只读取匹配文件可节省 77% token",
    "parameters": {
      "max_files_to_read": 10
    }
  }
}
```

### 示例 3：大型项目（分区并行扫描）

**输入**：用户需求 "跨模块重构日志系统"

**评估**：
- Glob 找到 80 个代码文件
- Grep "log" 匹配 25 个文件，分布在 5 个模块
- 预估：80 × 200 × 50 ÷ 4 = 200,000 tokens

**策略**：分区并行扫描
```json
{
  "strategy": {
    "selected": "parallel_scan",
    "reason": "文件数 80，跨 5 个模块，并行扫描可提升 3 倍速度",
    "parameters": {
      "partitions": ["auth", "api", "storage", "ui", "core"],
      "max_parallel": 5
    }
  }
}
```

### 示例 4：超大型项目（摘要模式）

**输入**：用户需求 "架构级重构"

**评估**：
- Glob 找到 150 个代码文件
- 预估：150 × 200 × 50 ÷ 4 = 375,000 tokens

**策略**：摘要模式
```json
{
  "strategy": {
    "selected": "summary_mode",
    "reason": "文件数 150，预估 375K tokens，超出预算，启用摘要模式",
    "parameters": {
      "core_files": 15,
      "summary_files": 135
    }
  }
}
```

---

## 集成到主工作流

编排器在启动 Dispatcher 之前执行 ASSESS（仅做规模/工具/分区决策，不做内容级扫描）：

```python
# 伪代码
def orchestrate(user_requirement):
    # 0. 初始化目录与三文件（早落盘）
    rfc_dir = init_rfc_dir(user_requirement)

    # 1. ASSESS（工具/规模/分区决策）
    assess_result = run_assess(project_root, user_requirement)

    # 2. Dispatcher 基线扫描（scan-of-record，写 findings.json）
    dispatcher_result = run_dispatcher(user_requirement, assess_result)

    # 3. analyze/design 默认不再全量扫描，仅在缺口触发时补扫
    analyze_result = run_analyze(dispatcher_result, assess_result)
    ...
```

---

## 注意事项

1. **快速执行**：ASSESS 阶段应在 10 秒内完成，避免成为瓶颈
2. **保守估算**：预估 token 时使用保守值，避免低估
3. **动态调整**：如果实际扫描发现文件更多，可中途切换策略
4. **记录决策**：所有决策必须记录到 progress.json，便于审计和优化
