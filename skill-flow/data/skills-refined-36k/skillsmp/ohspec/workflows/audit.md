# audit 阶段 - 工业级质量审查（专家视角）

## 概述

**目标**：从“高级技术专家 + 测试负责人”视角审查 RFC 是否满足工业级可开发/可验证标准。  
审查不是格式检查：必须验证与代码仓现状对齐、边界/依赖影响完备、测试闭环可执行。

**执行者**：质量审查员子代理（或编排器在 Codex 兼容模式下代行）

**输入**：
- `rfc.md`
- `findings.json`（scan-of-record：key_files/facts/依赖）
- `progress.json`（状态机/门禁/ASSESS 决策）

**输出**：
- 审查结论（pass | needs_discussion | reject）
- 阻断项清单（必须可定位到 RFC 章节/矩阵条目）
- `audit.md`（统一审查报告文件名，写入 RFC 目录）
- `progress.json` 更新（phases.audit / audit_log / gate）

---

## 审查清单（硬门禁）

以 `docs/quality-gates.md` 为准，额外强调：
- **证据链**：FACT/KEY_FILES 每条必须有证据锚点；禁止“设置键名/API/默认值按假设”
- **对齐与变更**：每条 CHG 必须 existing_ref 或 new_change_plan；跨仓影响/发布顺序明确
- **边界与异常**：并发/时序/权限/多用户/重启/超时/延迟至少覆盖到需求风险点
- **依赖影响**：外部依赖失败模式、回退目标、观测与影响范围齐全
- **测试闭环**：REQ→SCN→TST 可追溯，含故障注入与兼容回归
- **可读性**：审查速览能快速定位缺口；矩阵不应“难读到无法审”

> **阻断规则**：任何断链/缺矩阵/缺证据/未决项非空 → 一律 reject 或 needs_discussion（不得 approve）。

---

## 执行流程

### 步骤 0：强制执行可执行门禁（precheck）

审查员必须先确认 **precheck 已执行且通过**。若不确定，则直接运行脚本：

```bash
# 推荐（写报告 + 更新 progress）
python3 .ohspec/scripts/precheck_rfc.py RFC-... --write-report --update-progress

# COMPLEX 建议严格模式（warnings 也视为阻断）
python3 .ohspec/scripts/precheck_rfc.py RFC-... --strict --write-report --update-progress
```

判定规则：
- 若 precheck FAIL（存在 error）：**必须 reject**，不得给出“通过/需讨论”。
- 只有 precheck PASS 后，才进入下述“专家视角审查”（内容级审查）。

### 步骤 1：一致性与未决项检查（先于评分）

检查：
- `findings.working.pending_questions/pending_options` 是否为空
- RFC 引用的 ID（REQ/SCN/API/CHG/EDGE/DEP/TST/FIELD）是否存在断链
- Repo Manifest/锚点格式是否满足 `repo@rev:path#Lline`

### 步骤 2：按“可开发性/可测试性/可运维性”分组审查

每组输出：
- 发现的问题（带章节/条目 ID）
- 影响（为何会导致不可开发/不可测/不可运维）
- 修复建议（≤30字，尽量给可执行动作）

### 步骤 3：给出结论并写入 progress.json

更新：
- `phases.audit.status/completed_at/decision/score`
- `audit_log` 追加 `audit_completed`
- `state_machine.current_state` 推进到 APPROVED 或 REJECTED（或退回 DESIGNING）

同时在 RFC 目录输出 `audit.md`，并遵循：
- 先列 **阻断项**（带 RFC 章节/条目定位）
- 再列 **高风险项/建议**
- 最后给出 **结论**（pass/needs_discussion/reject）+ 分数 + 下一步动作

---

## 注意事项

1. **不要放水**：审查通过意味着“仅凭 RFC 就能做工业级交付”
2. **不要要求用户先给锚点**：优先用 rg/ag/grep 给候选锚点，再让用户确认
3. **不要写实现**：审查关注规格完备性与对齐，不给代码补丁
4. **不要输出 verification-report.md**：统一使用 `audit.md`，避免多种报告格式导致自动化误判
