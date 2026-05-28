# RCI & Golden Path Criteria

> 什么该进全量，什么该成为 Golden Path

---

## Part 1: RCI Criteria (进入 Regression Contract)

### 必须满足的 4 个条件

| 条件 | 说明 | 反例 |
|------|------|------|
| **Must-never-break** | 坏了会导致开发/发布不可用 | UI 文案改动 |
| **Verifiable** | 可用日志/退出码/CI 状态验证 | "用户体验好" |
| **Stable Surface** | 属于稳定接口或机制 | 临时脚本 |
| **Minimal** | 只记录必须永远不坏的点 | 业务细节 |

### Priority 判定

| Priority | 标准 | 例子 |
|----------|------|------|
| **P0** | 一坏就停工 / 破坏安全边界 | main 禁写、PR Gate 拦截 |
| **P1** | 重要但可临时绕过 | CI 版本检查、Shell 语法检查 |
| **P2** | 辅助性能力 | 失败通知、统计报告 |

### Trigger 判定

| Trigger | 何时使用 |
|---------|----------|
| **PR** | P0 必须，P1 视情况 |
| **Release** | P0/P1 必须，P2 可选 |
| **Nightly** | 全部（通过"跑全部条目"实现） |

### 常见判定结果

**应该进 RC**：
- ✅ main/develop 禁写（安全边界）
- ✅ PR Gate 拦截（开发流程核心）
- ✅ Release Gate 规则（发布流程核心）
- ✅ CI 版本检查（质量门禁）
- ✅ CI test job（L1 自动化）

**不应进 RC**：
- ❌ 具体业务 UI 文案
- ❌ 某个按钮颜色
- ❌ 业务功能细节（除非是业务 repo 自己的 RC）
- ❌ 临时脚本、一次性工具

---

## Part 2: Golden Path Criteria (E2E 关键链路)

### 必须满足的 4 个条件

| 条件 | 说明 |
|------|------|
| **End-to-end** | 跨多个步骤/组件/RCI，不是单点断言 |
| **Critical** | 坏了 = 无法开发/无法发布/核心用户不可用 |
| **Representative** | 覆盖最大面/最典型路径 |
| **Minimal Set** | Golden Paths 只保留 3~8 条，避免爆炸 |

### Engine Repo 的 Golden Paths（流程链路）

> **注意**：以下 GP ID 和 RCI ID 是 `regression-contract.yaml` 中的实际定义。
> 新增 GP/RCI 时请参照此格式，并确保 ID 唯一。

| GP ID | 名称 | 验证的链路 | 涉及 RCI |
|-------|------|-----------|----------|
| GP-001 | 完整开发流程 | /dev → 分支 → DoD → PR → CI → 合并 | W1-001, W1-002, W1-003, H2-003, C1-001, C2-001 |
| GP-002 | 分支保护链路 | main 写 → 拦截 → cp-* 写 → 通过 | H1-001, H1-002 |
| GP-003 | PR Gate 链路 | L1 失败 → 阻止 / L1 通过 → 放行 | H2-001, H2-002, H2-003 |
| GP-004 | CI 链路 | PR → 版本检查 → 测试 → Shell 检查 | C1-001, C2-001, C3-001 |

### Business Repo 的 Golden Paths（用户链路）

典型模式（按业务类型）：

| 业务类型 | Golden Path 示例 |
|----------|------------------|
| **内容平台** | 登录 → 创建内容 → 保存 → 发布 → 可见 |
| **电商** | 登录 → 搜索 → 加购 → 下单 → 支付回调 |
| **SaaS 工具** | 登录 → 创建项目 → 操作 → 保存 → 导出 |
| **内部系统** | 登录 → 查询 → 操作 → 结果可见 |

### 判定流程

```
这个功能/链路要加到 Golden Path 吗？
    │
    ├─→ 是端到端链路吗？（跨多个组件）
    │     └─→ 否 → 不是 GP，考虑加为单条 RCI
    │
    ├─→ 坏了会导致核心不可用吗？
    │     └─→ 否 → 不是 GP，可选加为 P1/P2 RCI
    │
    ├─→ 是最典型/覆盖面最大的路径吗？
    │     └─→ 否 → 考虑是否能合并到现有 GP
    │
    └─→ 全部是 → 加入 Golden Paths
              建议 GP ID: GP-00X
              列出 rcis: [...]
```

---

## 快速判定表

| 问题 | RCI? | GP? |
|------|------|-----|
| Hook 拦截逻辑 | ✅ P0 | 组合进 GP-002/003 |
| CI job 通过 | ✅ P0/P1 | 组合进 GP-004 |
| /dev 流程可启动 | ✅ P0 | 组合进 GP-001 |
| 某个按钮文案 | ❌ | ❌ |
| 登录→操作→结果 | 各步骤可拆 RCI | ✅ GP |
| 临时调试脚本 | ❌ | ❌ |

---

## ID 命名规范

### RCI ID

```
{Scope}-{Feature}-{Sequence}

Scope:
  H = Hooks
  W = Workflow
  C = CI/Release
  B = Business
  E = Export (QA报告/会话摘要)

例：H1-001, H2-003, W1-002, C1-001, E1-001
```

### Golden Path ID

```
GP-{Sequence}

例：GP-001, GP-002, GP-003
```

---

## 输出模板

### 判定为"应该进 RCI"

```
Decision: MUST_ADD_RCI
Reason: [一句话，如"Hook 拦截是安全边界，必须永远不坏"]
Next Actions:
  - 在 regression-contract.yaml 新增 RCI
  - ID: H?-00X
  - Priority: P0
  - Trigger: [PR, Release]
  - steps: given/when/then
  - evidence: type/contains
Artifacts:
  - regression-contract.yaml
```

### 判定为"应该进 Golden Path"

```
Decision: MUST_ADD_GP
Reason: [一句话，如"端到端流程链路，坏了无法开发"]
Next Actions:
  - 在 regression-contract.yaml 的 golden_paths 新增条目
  - GP ID: GP-00X
  - rcis: [W1-001, H2-003, C1-001]
Artifacts:
  - regression-contract.yaml
```

---

## Part 3: QA Report 检查定义（qa-report.sh 的基准）

> **qa-report.sh 只做"测量"，不做"内容补全"**

### Meta "全" 的定义

| 检查项 | 通过条件 |
|--------|----------|
| Feature → RCI 覆盖 | 每个 Committed Feature 至少有 1 条 RCI |
| P0 触发规则 | 所有 P0 RCI 的 trigger 必须包含 PR |

**输出**：
- 覆盖率百分比
- 缺口列表（哪些 Feature 没有 RCI）
- P0 违规列表（哪些 P0 不在 PR 触发集合）

### Unit "全" 的定义

| 检查项 | 通过条件 |
|--------|----------|
| 真相命令 | `npm run qa`（typecheck + test + build）|
| 通过标准 | exit code = 0 |

**输出**：
- 通过/失败状态
- 测试数量
- 用时
- 失败时：前 N 行错误摘要

### E2E "全" 的定义

| 检查项 | 通过条件 |
|--------|----------|
| GP 存在 | golden_paths 部分存在且非空 |
| GP 结构完整 | 每个 GP 有 id, name, rcis 列表 |
| RCI 可解析 | GP.rcis 中的每个 ID 在 RC 中存在 |
| GP 允许 manual | GP-001 等流程类 GP 可以 method: manual |

**输出**：
- GP 数量
- 每个 GP 覆盖的 Feature 列表
- 哪些 Feature 不在任何 GP 中

### RCI 最小字段

一条 RCI 至少需要以下 6 个字段才算"合格"：

```yaml
- id: H1-001          # 必须
  feature: H1         # 必须
  name: "描述"        # 必须
  priority: P0        # 必须
  trigger: [PR]       # 必须
  evidence:           # 必须
    type: log
    contains: "xxx"
```

可选字段：`scope`, `method`, `tags`, `owner`, `steps`, `test`

### 报告输出格式

```json
{
  "meta": {
    "score": 91,
    "total_features": 11,
    "covered_features": 10,
    "gaps": ["W3"],
    "p0_violations": []
  },
  "unit": {
    "score": 100,
    "passed": true,
    "test_count": 99,
    "duration": "1.94s",
    "error_summary": null
  },
  "e2e": {
    "score": 100,
    "gp_count": 4,
    "gp_coverage": ["H1", "H2", "W1", "C1", "C2", "C3"],
    "uncovered_features": []
  },
  "overall": 97
}
```
