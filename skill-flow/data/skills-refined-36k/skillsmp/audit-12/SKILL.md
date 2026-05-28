---
name: audit
version: 1.2.0
updated: 2026-01-23
description: |
  有边界的代码审计与修复。分层标准：L1阻塞性/L2功能性/L3最佳实践/L4过度优化。
  默认目标L2，L1+L2清零即宣布完成，防止无限深挖。
---

# /audit - 代码审计与修复

> 有边界的代码审计，避免无限深挖。

---

## 分层标准

| Layer | 名称 | 描述 | 完成标准 |
|-------|------|------|----------|
| **L1** | 阻塞性 | 功能不工作、崩溃、数据丢失 | **必须修** |
| **L2** | 功能性 | 边界条件、错误处理、已知 edge case | **建议修** |
| **L3** | 最佳实践 | 代码风格、一致性、可读性 | 可选 |
| **L4** | 过度优化 | 理论边界、极端情况、性能微调 | **不修** |

---

## 严重性 → 优先级映射（v8.25.0+）

当审计发现问题时，**严重性关键字会自动映射为业务优先级**：

| 审计严重性 | 业务优先级 | 对应 Layer | RCI 要求 |
|-----------|-----------|-----------|----------|
| **CRITICAL** | **P0** | L1 阻塞性 | ✅ 必须更新 RCI |
| **HIGH** | **P1** | L2 功能性 | ✅ 必须更新 RCI |
| MEDIUM | P2 | L2/L3 | 可选 |
| LOW | P3 | L3/L4 | 可选 |

**触发规则**：
- PR title/commit 包含 `CRITICAL` → 触发 P0 检查
- PR title/commit 包含 `HIGH` → 触发 P1 检查
- PR title 以 `security:` 开头 → 触发 P0 检查

**影响**：
- P0/P1 修复必须在 `regression-contract.yaml` 添加 RCI 条目
- 检测由 `scripts/devgate/detect-priority.cjs` 执行
- 强制由 `scripts/devgate/require-rci-update-if-p0p1.sh` 检查

---

## 与质检分层的关系

**注意**：本 Skill 的 L1/L2/L3/L4 是 **问题严重性分类**，用于审计发现的问题。

这与 `/dev` 工作流的质检分层是不同概念：

| 质检层 | 名称 | 内容 | 与本 Skill 的关系 |
|--------|------|------|-------------------|
| L1 | 自动化测试 | npm run qa | 无关 |
| **L2A** | 代码审计 | **本 Skill 执行的工作** | Audit 是 L2A |
| L2B | Evidence 证据 | 截图/curl 验证 | 无关 |
| L3 | Acceptance 验收 | DoD 全勾 | 无关 |

**简单说**：
- 质检的 L2A = 调用 /audit 做代码审计
- /audit 内部用 L1/L2/L3/L4 对问题分级
- 质检的 L2B = 证据收集（与 /audit 无关）

---

## 默认目标

**L2 完成 = 稳定可用**（推荐停止点）

```
用户说"找 bug"  → 做到 L2
用户说"深度审计" → 做到 L3
用户说"极致优化" → 警告用户，确认后做 L3
```

---

## 执行流程

### Step 1: 确定范围

```bash
# 询问用户
- 审计哪些文件/目录？
- 目标层级？（默认 L2）
- 最大轮次？（默认 3 轮）
```

### Step 2: 分层审计

```
第 1 轮：只找 L1 问题（阻塞性）
第 2 轮：找 L2 问题（功能性）
第 3 轮：如果用户要求，找 L3 问题
```

### Step 3: 每轮结束检查

```
问自己：
1. 这个问题会导致功能失败吗？ → L1
2. 这个问题会在边界情况出错吗？ → L2
3. 这个问题只是"可以更好"吗？ → L3，停止

如果找到的都是 L3/L4 问题 → 宣布审计完成
```

### Step 4: 完成声明

```
当以下条件满足时，主动声明审计完成：

✅ L1 问题：0 个
✅ L2 问题：0 个（或已全部修复）
✅ 连续 2 轮未发现新的 L1/L2 问题

输出：
"审计完成。L1/L2 问题已清零，剩余 N 个 L3 建议（可选修复）。"
```

---

## 问题分类示例

### L1 阻塞性（必须修）

- 脚本语法错误，无法执行
- 命令不存在，功能完全失效
- 条件判断错误，导致错误分支
- 文件路径错误，找不到依赖

### L2 功能性（建议修）

- 网络超时无保护，可能挂起
- 空字符串未处理，边界出错
- 错误码未正确返回
- 分支/路径引用不一致

### L3 最佳实践（可选）

- shebang 不统一
- set options 风格不同
- 变量命名不规范
- 注释不够清晰
- 硬编码的 magic numbers

### L4 过度优化（不修）

- 理论上可能的 word splitting（实际不会发生）
- 极端边界条件（需要刻意构造）
- 性能微优化（毫秒级差异）
- 代码"可以更优雅"

---

## Audit Report 产物（/dev 流程必须产出）

当 /dev 流程调用 Audit Node 时，**必须**输出 `docs/AUDIT-REPORT.md`。

### 输出 Schema（固定格式）

```yaml
# Audit Report
Branch: cp-xxx
Date: YYYY-MM-DD
Scope: file1, file2, ...
Target Level: L2

Summary:
  L1: 0
  L2: 0
  L3: 0
  L4: 0

Decision: PASS | FAIL

Findings:
  - id: A1-001
    layer: L1 | L2 | L3 | L4
    file: path/to/file
    line: 123
    issue: 问题描述
    fix: 修复建议
    status: fixed | pending

Blockers: []  # L1 + L2 问题列表
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| Branch | ✅ | 当前分支名 |
| Date | ✅ | 审计日期 |
| Scope | ✅ | 审计范围（改动的文件） |
| Target Level | ✅ | 目标层级（默认 L2） |
| Summary | ✅ | 各层级问题数量 |
| Decision | ✅ | PASS=可继续 / FAIL=需修复 |
| Findings | ✅ | 发现的问题列表 |
| Blockers | ✅ | L1+L2 问题的 ID 列表 |

### Decision 判定规则

```
L1 > 0 OR L2 > 0  →  Decision: FAIL
L1 = 0 AND L2 = 0 →  Decision: PASS
```

### Gate 检查

PR Gate 会检查：
1. `docs/AUDIT-REPORT.md` 存在
2. `Decision: PASS`（FAIL 则 Gate 失败）

---

## 与 /dev 的关系

```
/dev 流程中的使用（必须）：

Step 5（写代码）完成后：
  - Audit Node 对新代码做 L1+L2 检查
  - 输出 docs/AUDIT-REPORT.md
  - Decision: FAIL 时必须修复后重新审计
  - Decision: PASS 后才能继续 PR 创建

Gate 强制检查：
  - PR Gate 检查 AUDIT-REPORT.md 存在
  - PR Gate 检查 Decision: PASS
```

---

## 关键原则

1. **有边界**：明确知道什么时候停
2. **分层次**：不同问题不同对待
3. **主动完成**：达标后主动宣布完成，不等用户问
4. **抵制完美主义**：L3/L4 的诱惑要抵抗

---

## 反模式警告

❌ "我再找找看还有没有问题" → 无边界
❌ "这个地方可以更好" → L3/L4
❌ "理论上可能出问题" → L4
❌ "为了一致性统一改掉" → L3

✅ "L1/L2 已清零，审计完成"
✅ "发现 N 个 L3 建议，是否需要修复？"

---

## 快速参考

```
/audit           → L2 审计（默认）
/audit deep      → L3 审计（用户明确要求）
/audit <路径>    → 指定范围
```
