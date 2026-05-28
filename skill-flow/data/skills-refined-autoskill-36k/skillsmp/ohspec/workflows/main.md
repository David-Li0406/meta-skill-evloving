# OHSpec 主工作流程

## 目录
- [编排模式](#编排模式)
- [执行序列](#执行序列)
- [复杂度路由](#复杂度路由)
- [路由信号](#路由信号)
- [Resume 模式](#resume-模式)
- [快速填充机制](#快速填充机制)
- [子代理委托原则](#子代理委托原则)
- [并行执行](#并行执行)
- [错误处理](#错误处理)

---

## 编排模式

```
用户需求 → 初始化三文件 → ASSESS评估（工具/规模/分区）→ Dispatcher基线扫描 → 复杂度路由 → 阶段执行 → RFC输出
```

## 执行序列

### -1. 初始化 RFC 目录（强制）
- 初始化项目级 OHSpec 工具目录（强制，落盘一致性）
  - 确保项目内存在：
    - `.ohspec/templates/`（放置 rfc/findings/progress 模板）
    - `.ohspec/scripts/`（放置可执行脚本：precheck/export 等）
  - 若不存在，则从 skill 自带的 `templates/`、`scripts/` **复制**到项目目录（避免依赖安装路径，保证跨仓/跨环境一致）
  - 最少需要落盘到项目目录的文件：
    - `.ohspec/templates/rfc.md`
    - `.ohspec/templates/findings.json`
    - `.ohspec/templates/progress.json`
    - `.ohspec/scripts/precheck_rfc.py`
    - `.ohspec/scripts/export_digest.py`

  - **兼容（历史）**：若项目已存在 `.claude/ohspec/`，允许继续读取；但新生成物默认写入 `.ohspec/`（工具无关，便于多模型共用与查看）

- 创建 RFC 目录与三文件（`.ohspec/rfcs/{RFC-ID}/rfc.md|findings.json|progress.json`）
- **必须在任何扫描/分析前完成**，确保早落盘
- **模板锁定（强制）**：三文件必须从 `templates/` 生成，**禁止自造结构/章节/目录**（否则后续 precheck/audit 必然失败）
  - `rfc.md`：必须以 `templates/rfc.md` 为骨架（只允许“填空/增量更新”，不得重排章节、不得另起“§1~§8”自定义结构）
  - `findings.json`：优先使用 `templates/findings.json`（纯 JSON，无注释，避免 JSONC 去注释失误导致 schema 漂移）
  - `progress.json`：优先使用 `templates/progress.json`（纯 JSON，无注释，避免 schema 漂移）

- **目录隔离（强制）**：每个 RFC 必须独立目录，避免不同模型/不同轮次互相污染
  - ✅ 正确：`.ohspec/rfcs/RFC-.../rfc.md`
  - ❌ 错误：`.ohspec/rfc.md` 或 `.ohspec/findings.json`（这会导致 list/resume/precheck/export 失效）
- **禁止空壳**：初始化时至少写入：
  - `findings.requirement.original`（用户原始需求）
  - `findings.meta.repos[0].root`（Repo Manifest main.root）
  - `progress.meta.created_at/updated_at`（ISO8601）
  - `progress.state_machine.current_state = INIT`

### 0. ASSESS 阶段（新增）
- 评估代码库规模（Glob 统计文件数）
- 预览关键词匹配（Grep 预览）
- 决策扫描策略（直接/过滤/并行/摘要）
- **仅做决策，不做内容级扫描（不 Read 代码）**
- **强制落盘**：必须更新 `progress.json.tooling` + `progress.json.phases.assess` + `progress.json.audit_log`（未落盘则禁止进入 Dispatcher）

详见：[assess.md](assess.md)

### 1. 启动 Dispatcher（Task工具，Explore子代理）
- 按 ASSESS 策略执行**基线扫描（scan-of-record）**：Grep/Glob/Read
- 接收 JSON 摘要（~2k tokens）：意图、复杂度、范围、专家、模式
- **禁止**：编排器直接扫描代码
- **默认不重复扫描**：后续 analyze/design 仅在“缺口触发”时补扫

### 2. Gate-1：范围/事实对齐确认（强制，分析前但不冻结需求）
在进入需求分析（analyze）前，必须先把“基线扫描结果”对齐给用户（避免先写再发现跑偏）。

展示给用户（摘要即可）：
- 意图理解（≤50字）
- 初步范围（会改哪些层/模块）
- scan-of-record：key_files（≥3，含角色）+ facts（≥3）
- 仍不确定的关键点（≤5条）

然后用 **选项式** 询问（COMPLEX 必须；MEDIUM 建议；SIMPLE 可跳过）：
1) 继续进入需求分析（范围=当前）
2) 调整范围（你补充/删减模块，我更新范围后再分析）
3) 先补齐证据（触发定向补扫：补 key_files/facts）

**落盘（强制）**：
- 写入 `progress.json.phases.dispatcher.gate`（type/decision/confirmed_at/passed）
- 追加 `progress.json.audit_log`（记录用户选择与理由）

### 3. 执行阶段
- 启动专家子代理（需求分析师、架构设计师、质量审查员）
- 管理阶段转换和用户门禁
- 收集输出到 RFC 结构
- **门禁记录**：必须写入 progress.json（gate 类型/是否通过/用户确认）
- **澄清优先**：如 findings 存在 pending_questions/pending_options，必须停止并向用户澄清

### 3.5 Gate-2：需求冻结确认（强制，进入设计前）
analyze 输出 RFC §1-§2 后，必须做“澄清完成/需求冻结”确认（避免“写完设计才澄清”）。

展示给用户（摘要即可）：
- REQ 列表 + 验收标准
- 排除项/兼容范围/默认行为
- 场景概览（SCN 列表）+ 关键边界/异常清单

然后用 **选项式** 询问（COMPLEX 必须；MEDIUM 可选（默认自动）；SIMPLE 可跳过）：
1) 澄清完成，冻结需求并进入方案设计
2) 继续澄清（我补充缺失信息/选择未决项）
3) 回到证据补扫（扩大 scan-of-record，再进入澄清）

**落盘（强制）**：
- 写入 `progress.json.phases.analyze.gate`（type/decision/confirmed_at/passed）
- 追加 `progress.json.audit_log`

### 4. 质量门禁（自动）
- 验证 RFC 结构完整性
- 检查 DFX 8维度覆盖
- 验证场景覆盖（正常/异常/边界/不支持）

### 5. 自动流转（默认）
- 默认自动进入 precheck → audit
- 仅当存在需人工决策/澄清时才向用户提问

## 复杂度路由

| 复杂度 | 特征 | 执行模式 | 用户门禁 |
|--------|------|----------|----------|
| SIMPLE | 单文件，<50行 | 快速通道（分析+设计合并） | 仅最终审批 |
| MEDIUM | 多文件，单子系统，<200行 | 标准流程 | 每阶段审批 |
| COMPLEX | 跨子系统，架构级，>200行 | 完整流程+spike验证 | 每阶段+spike审批（强制） |

## 路由信号

详见 [routing-signals.md](../docs/routing-signals.md)

根据需求特征动态调整执行路径：

| 信号 | 检测条件 | 动作 |
|------|----------|------|
| `SKIP_ANALYZE` | 需求明确、单文件影响 | 跳过 analyze 阶段 |
| `LOAD_DIPLOMAT` | 跨子系统依赖 | 加载 Diplomat 专家 |
| `TRIGGER_SPIKE` | 技术不确定 | 触发 Spike 验证 |
| `SIMPLIFY_CLARIFY` | 用户已提供详细需求 | 简化澄清阶段 |

## Resume 模式

**适用场景**：
- SIMPLE 任务：合并分析+设计阶段
- MEDIUM 任务：无需用户确认的自动流转
- Token 节省：~7,400 tokens

**不适用场景**：
- COMPLEX 任务：需要每阶段用户确认
- 需要用户决策或补充信息的阶段

详见 [resume-mode.md](../docs/resume-mode.md)

## 快速填充机制

当触发 `SKIP_ANALYZE` 信号时，自动填充 RFC §1-§2 章节。

### 触发条件

全部满足时启用：
- 用户已提供详细需求文档（≥100字）
- 需求明确、单文件影响、无歧义
- Dispatcher 返回 `signals` 包含 `SKIP_ANALYZE`

### 填充规则

| 章节 | 填充来源 | 填充方式 |
|------|----------|----------|
| §1.1 元数据 | Dispatcher 分析结果 | `complexity` → complexity，`intent` → title |
| §1.2 背景 | 用户原始需求 | 直接提取现状/问题/目标 |
| §2.1 功能需求 | 用户原始需求 | 结构化为 SHALL/MUST 语句 |
| §2.2 约束条件 | Dispatcher 扫描 | `scope.dependencies` → 技术约束 |

### 验证标准

快速填充后必须验证：
- [ ] §1.1 metadata 字段完整（title、complexity、needs_spike）
- [ ] §1.2 背景三要素齐全（现状、问题、目标）
- [ ] §2.1 至少 1 条功能需求
- [ ] §2.2 约束条件已从 Dispatcher 提取

### 使用模板

快速填充使用最小化模板：[templates/rfc-minimal.md](../templates/rfc-minimal.md)

## 子代理委托原则

**必须委托**：
- 代码扫描（Grep/Glob/Read）→ Dispatcher
- 需求分析 → 需求分析师
- 方案设计 → 架构设计师
- 质量审查 → 质量审查员

**禁止直接执行**：
- 编排器不使用 Grep/Glob/Read
- 编排器不分析代码
- 编排器不生成 RFC 章节

**例外（Codex 兼容模式）**：
- 当 Task 子代理不可用时，允许编排器执行**最小化扫描回退**：
  - 必须记录 `progress.json.tooling` 与 `audit_log`
  - 必须满足 key_files ≥ 3 且覆盖面达标，并补齐 facts ≥3（事实+锚点），否则停在澄清阶段
  - 默认展示候选锚点/模块供确认，仅在最后才请求人工锚点

**原因**：避免主上下文消耗（节省 19k-59k tokens）

## 并行执行

### 可并行组合

| 组合 | 条件 | 预期收益 | 依赖关系 |
|------|------|----------|----------|
| Dispatcher + 项目上下文加载 | 首次运行 | ~30s | 无数据依赖，可完全并行 |
| 代码扫描 + 竞品分析 | COMPLEX 任务 | ~60s | 无数据依赖，结果独立合并 |
| 多模块扫描 | 跨子系统任务 | ~40s | 各模块独立扫描 |

### 并行条件

启用并行执行必须满足：
1. **无数据依赖**：任务 A 的输出不是任务 B 的输入
2. **无资源冲突**：不同时写入同一文件
3. **可独立合并**：结果可在完成后合并到 findings.json

### 执行模式

```
串行模式（默认）:
  Dispatcher → 用户确认 → 分析 → 设计 → 审查

并行模式（优化）:
  ┌─ Dispatcher ────────┐
  │                     ├─→ 合并结果 → 用户确认 → ...
  └─ 项目上下文加载 ────┘

  ┌─ 代码扫描 ──────────┐
  │                     ├─→ 合并到 findings.json
  └─ 竞品分析 ──────────┘
```

### 结果合并规则

| 来源 | 合并目标 | 冲突处理 |
|------|----------|----------|
| Dispatcher | `findings.json` | 主数据源 |
| 项目上下文 | `findings.confirmed.context` | 补充合并 |
| 竞品分析 | `findings.confirmed.competitive` | 独立分区 |

## 错误处理

详见 [error-handling.md](../docs/error-handling.md)

**核心规则**：
- L1-L4 四级错误分类
- 3-Strike 规则：连续3次相同错误必须升级处理策略
- 各阶段有特定的错误处理策略
