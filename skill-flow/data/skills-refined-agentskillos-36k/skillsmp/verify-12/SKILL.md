---
name: verify
version: 3.1.0
description: 多 Agent 並行驗證框架 - 多視角測試驗證，驗收標準確認
triggers: [multi-verify, verification, 驗證測試]
context: fork
agent: general-purpose
allowed-tools: [Read, Bash, Grep, Glob, Write]
model: sonnet
---

# Multi-Agent Verify v3.0.0

> 功能測試 → 邊界測試 → 回歸測試 → 驗收確認

## 使用方式

```bash
/multi-verify [審查路徑]
/multi-verify .claude/memory/review/user-auth/
```

**Flags**: `--from-review ID` | `--quick` | `--comprehensive`

## 預設 4 視角

| ID | 名稱 | 模型 | 聚焦 |
|----|------|------|------|
| `functional-tester` | 功能測試員 | haiku | 正常流程、功能驗證 |
| `edge-case-hunter` | 邊界獵人 | sonnet | 邊界條件、異常處理 |
| `regression-checker` | 回歸檢查員 | haiku | 回歸測試、副作用 |
| `acceptance-validator` | 驗收驗證員 | sonnet | 驗收標準、需求滿足 |

→ 模型路由配置：[shared/config/model-routing.yaml](../../shared/config/model-routing.yaml)

## 執行流程

```
Phase 0: 載入審查 → 收集待驗證項目
    ↓
Phase 1: MAP（並行驗證）
    ┌──────────┬──────────┬──────────┬──────────┐
    │功能測試員│邊界獵人  │回歸檢查員│驗收驗證員│
    └──────────┴──────────┴──────────┴──────────┘

    ⚠️ **並行執行關鍵**：
       在單一訊息中發送 4 個 Task 工具呼叫：
       - Task({description: "功能測試", ...})
       - Task({description: "邊界測試", ...})
       - Task({description: "回歸測試", ...})
       - Task({description: "驗收驗證", ...})
       這樣才能真正並行執行！
    ↓
Phase 2: REDUCE（結果匯總）
    ├── 測試結果統計
    ├── 失敗分析
    └── 驗收狀態
    ↓
Phase 3: 早期終止檢查 → 高通過率可提前完成
    ↓
Phase 4: 品質閘門 → 發布/回退決策
```

## 驗證類型

| 類型 | 重點 | 通過標準 |
|------|------|----------|
| 功能測試 | 正常操作流程 | 100% 通過 |
| 邊界測試 | 極端輸入、錯誤處理 | 95% 通過 |
| 回歸測試 | 既有功能不受影響 | 100% 通過 |
| 驗收驗證 | 滿足需求規格 | 所有標準達成 |

## 早期終止

當 `first_pass_rate >= 0.98` 時，可直接發布（ship_it）。

→ 配置：[shared/config/early-termination.yaml](../../shared/config/early-termination.yaml)

## CP4: Task Commit

品質閘門檢查完成後，**必須執行 CP4 Task Commit**。

```
Phase 4: 品質閘門 → 發布/回退決策
    ↓
CP4: Task Commit
    ├── git add .claude/memory/verify/{review-id}/
    └── git commit -m "test(verify): complete {feature} verification"
```

→ 協議：[shared/git/commit-protocol.md](../../shared/git/commit-protocol.md)

## 品質閘門

通過條件（VERIFY 階段）：
- ✅ 功能測試 100% 通過
- ✅ 回歸測試通過
- ✅ 驗收標準滿足
- ✅ 品質分數 ≥ 85

失敗處理：
- 功能測試失敗 → 回退到 IMPLEMENT
- 邊界測試失敗 → 記錄但可繼續
- 驗收標準未滿足 → 評估回退層級

→ 閘門配置：[shared/quality/gates.yaml](../../shared/quality/gates.yaml)

## 回退策略

根據迭代次數決定回退目標：
- 1-2 次：回退 IMPLEMENT（修復受影響任務）
- 3 次：回退 TASKS（重新評估分解）
- 4 次：回退 PLAN（重新評估設計）
- 5+ 次：人工介入

→ 配置：[shared/quality/rollback-strategy.yaml](../../shared/quality/rollback-strategy.yaml)

## 輸出結構

```
.claude/memory/verify/[review-id]/
├── meta.yaml           # 元數據
├── perspectives/       # 完整視角報告（MAP 產出，保留）
│   ├── functional-tester.md
│   ├── edge-case-hunter.md
│   ├── regression-checker.md
│   └── acceptance-validator.md
├── summaries/          # 結構化摘要（REDUCE 產出，供快速查閱）
│   ├── functional-tester.yaml
│   ├── edge-case-hunter.yaml
│   ├── regression-checker.yaml
│   └── acceptance-validator.yaml
├── test-results.yaml   # 測試結果
├── acceptance.yaml     # 驗收狀態
└── verify-summary.md   # 驗證摘要（主輸出）
```

> ⚠️ perspectives/ 保存完整報告，summaries/ 保存結構化摘要，兩者都必須保留。

## Agent 能力限制

**驗證 Agent 不應該開啟 Task**：

| 允許的操作 | 說明 |
|-----------|------|
| ✅ Read | 讀取測試結果 |
| ✅ Glob/Grep | 搜尋檔案和內容 |
| ✅ Bash | 執行測試 |
| ✅ Write | 寫入報告 |
| ❌ Task | 開子 Agent |

## 行動日誌

每個工具調用完成後，記錄到 `.claude/workflow/{workflow-id}/logs/actions.jsonl`。

**記錄時機**：
- 成功：記錄 `tool`、`input`、`output_preview`、`duration_ms`、`status: success`
- 失敗：記錄 `tool`、`input`、`error`、`stderr`（如有）、`status: failed`

**關鍵行動（VERIFY 階段）**：
| 行動 | 記錄重點 |
|------|----------|
| Read（讀取測試結果） | `file_path`、`output_size` |
| Bash（執行測試） | `command`、`exit_code`、`stdout`、`stderr` |
| Task（啟動驗證 Agent） | `subagent_type`、`prompt` (truncated)、`agent_id` |
| Write（寫入驗證報告） | `file_path`、`content_size` |

**排查問題**：
```bash
# 查看 VERIFY 階段所有失敗行動
jq 'select(.stage == "VERIFY" and .status == "failed")' actions.jsonl

# 查看測試執行失敗的詳情
jq 'select(.tool == "Bash" and .status == "failed" and .stage == "VERIFY")' actions.jsonl | jq '{command: .input.command, exit_code: .exit_code, stderr: .stderr}'

# 查看執行時間超過 10 秒的行動
jq 'select(.stage == "VERIFY" and .duration_ms > 10000)' actions.jsonl
```

→ 日誌規範：[shared/communication/execution-logs.md](../../shared/communication/execution-logs.md)

## 共用模組

| 模組 | 用途 |
|------|------|
| [coordination/map-phase.md](../../shared/coordination/map-phase.md) | 並行協調 |
| [coordination/reduce-phase.md](../../shared/coordination/reduce-phase.md) | 匯總整合、大檔案處理 |
| [quality/gates.yaml](../../shared/quality/gates.yaml) | 品質閘門 |
| [config/early-termination.yaml](../../shared/config/early-termination.yaml) | 早期終止 |
| [quality/rollback-strategy.yaml](../../shared/quality/rollback-strategy.yaml) | 回退策略 |
| [perspectives/expertise-frameworks/testing.yaml](../../shared/perspectives/expertise-frameworks/testing.yaml) | 測試框架 |

## 工作流位置

```
RESEARCH → PLAN → TASKS → IMPLEMENT → REVIEW → VERIFY
                                                  ↑
                                               你在這裡
```

- **輸入**：審查報告，來自 `review` skill
- **輸出**：驗證結果，工作流完成或回退
