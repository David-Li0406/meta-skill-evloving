---
name: tasks
version: 3.2.0
description: 多 Agent 任務分解框架 - 將計劃轉化為可執行的 DAG 任務清單
triggers: [multi-tasks, task-decomposition, 任務分解]
context: fork
agent: general-purpose
allowed-tools: [Read, Grep, Glob, Write, Bash, TaskCreate, TaskUpdate, TaskList, TaskGet]
model: sonnet
---

# Multi-Agent Tasks v3.2.0

> 計劃分解 → DAG 驗證 → TDD 對應 → 可執行任務清單

## Claude Code Tasks 整合

> v3.2.0 支援原生 Tasks API，實現跨 session 任務協作

本 Skill 可使用 Claude Code 原生 Tasks 系統：

```bash
# 建立任務（自動生成 taskId）
TaskCreate({ subject: "實作登入功能", description: "..." })

# 設定依賴關係
TaskUpdate({ taskId: "2", addBlockedBy: ["1"] })

# 跨 session 共享
export CLAUDE_CODE_TASK_LIST_ID=my-workflow
```

| API | 用途 |
|-----|------|
| `TaskCreate` | 建立任務 |
| `TaskUpdate` | 更新狀態、設定依賴（addBlockedBy） |
| `TaskList` | 列出所有任務 |
| `TaskGet` | 取得任務詳情 |

**優勢**：
- 跨 session 持久化
- 多 Agent 協作同一任務清單
- 自動依賴解除（完成時自動 unblock 下游任務）

## 使用方式

```bash
/multi-tasks [計劃路徑]
/multi-tasks .claude/memory/plans/user-auth/implementation-plan.md
```

**Flags**: `--from-plan ID` | `--validate-only` | `--no-tdd-check`

## 預設 4 視角

| ID | 名稱 | 模型 | 聚焦 |
|----|------|------|------|
| `dependency-analyst` | 依賴分析師 | sonnet | 任務依賴、執行順序 |
| `task-decomposer` | 任務分解師 | haiku | 粒度切分、並行識別 |
| `test-planner` | 測試規劃師 | haiku | TDD 對應、測試策略 |
| `risk-preventor` | 風險預防師 | haiku | 風險任務、預防措施 |

→ 模型路由配置：[shared/config/model-routing.yaml](../../shared/config/model-routing.yaml)

## 執行流程

```
Phase 0: 載入計劃 → 解析 implementation-plan.md
    ↓
Phase 1: MAP（並行分解）
    ┌──────────┬──────────┬──────────┬──────────┐
    │依賴分析師│任務分解師│測試規劃師│風險預防師│
    └──────────┴──────────┴──────────┴──────────┘

    ⚠️ **並行執行關鍵**：
       在單一訊息中發送 4 個 Task 工具呼叫：
       - Task({description: "依賴分析", ...})
       - Task({description: "任務分解", ...})
       - Task({description: "測試規劃", ...})
       - Task({description: "風險預防", ...})
       這樣才能真正並行執行！
    ↓
Phase 2: REDUCE（合併 + 排序）
    ↓
Phase 3: TDD 驗證 → 確保每個 T-F-* 有對應 TEST-*
    ↓
Phase 4: DAG 驗證 → 無循環、無孤立任務
    ↓
Phase 5: 依賴偵測 → 隱含依賴分析
    ↓
Phase 6: 品質閘門 → 輸出 tasks.yaml
```

## TDD 強制執行

**必要條件（BLOCKER）**：
- 所有 `T-F-*` 任務必須有對應的 `TEST-*` 任務
- `TEST-*` 任務必須 block 對應的 `T-F-*` 任務

**驗證腳本**：`shared/tools/tdd-validator.sh`

→ 配置：[shared/quality/tdd-enforcement.yaml](../../shared/quality/tdd-enforcement.yaml)

## 依賴偵測

四層依賴分析：
1. **L1_explicit**: 顯式聲明的依賴
2. **L2_file_overlap**: 修改相同檔案的任務
3. **L3_semantic**: 語意資料流依賴
4. **L4_environment**: 運行時環境依賴

**驗證腳本**：`shared/tools/dag-validator.py`

→ 配置：[shared/tasks/dependency-detection.yaml](../../shared/tasks/dependency-detection.yaml)

## CP4: Task Commit

品質閘門通過後，**必須執行 CP4 Task Commit**。

```
Phase 6: 品質閘門 → 輸出 tasks.yaml
    ↓
CP4: Task Commit
    ├── git add .claude/memory/tasks/{plan-id}/
    └── git commit -m "feat(tasks): decompose {plan} into executable tasks"
```

→ 協議：[shared/git/commit-protocol.md](../../shared/git/commit-protocol.md)

## 品質閘門

通過條件（TASKS 階段）：
- ✅ DAG 驗證通過（無循環）
- ✅ TDD 對應完整
- ✅ 所有任務有估算
- ✅ 品質分數 ≥ 80

→ 閘門配置：[shared/quality/gates.yaml](../../shared/quality/gates.yaml)

## 輸出結構

```
.claude/memory/tasks/[plan-id]/
├── meta.yaml               # 元數據
├── perspectives/           # 完整視角分析（MAP 產出，保留）
│   ├── dependency-analyst.md
│   ├── task-decomposer.md
│   ├── test-planner.md
│   └── risk-preventor.md
├── summaries/              # 結構化摘要（REDUCE 產出，供快速查閱）
│   ├── dependency-analyst.yaml
│   ├── task-decomposer.yaml
│   ├── test-planner.yaml
│   └── risk-preventor.yaml
└── tasks.yaml              # 任務清單（主輸出）
```

> ⚠️ perspectives/ 保存完整分析，summaries/ 保存結構化摘要，tasks.yaml 是最終可執行任務清單。

## Agent 能力限制

**視角 Agent 不應該開啟 Task**：

| 允許的操作 | 說明 |
|-----------|------|
| ✅ Read | 讀取檔案 |
| ✅ Glob/Grep | 搜尋檔案和內容 |
| ✅ Explore agent | 輕量級探索 |
| ✅ Bash | 執行命令 |
| ✅ Write | 寫入報告 |
| ❌ Task | 開子 Agent |

### tasks.yaml 格式

```yaml
version: "1.0"
plan_ref: "plans/user-auth"
waves:
  - id: wave-1
    tasks:
      - id: TEST-001
        type: test
        description: "登入功能測試"
        estimate: 15
      - id: T-F-001
        type: feature
        description: "實作登入功能"
        depends_on: [TEST-001]
        estimate: 30
        files: [src/auth/login.ts]
```

## 行動日誌

每個工具調用完成後，記錄到 `.claude/workflow/{workflow-id}/logs/actions.jsonl`。

**記錄時機**：
- 成功：記錄 `tool`、`input`、`output_preview`、`duration_ms`、`status: success`
- 失敗：記錄 `tool`、`input`、`error`、`stderr`（如有）、`status: failed`

**關鍵行動（TASKS 階段）**：
| 行動 | 記錄重點 |
|------|----------|
| Read（讀取計劃） | `file_path`、`output_size` |
| Task（啟動 Agent） | `subagent_type`、`prompt` (truncated)、`agent_id` |
| Bash（執行 DAG 驗證） | `command`、`exit_code`、`stderr` |
| Write（寫入 tasks.yaml） | `file_path`、`content_size` |

**排查問題**：
```bash
# 查看 TASKS 階段所有失敗行動
jq 'select(.stage == "TASKS" and .status == "failed")' actions.jsonl

# 查看 DAG 驗證失敗的詳情
jq 'select(.tool == "Bash" and .status == "failed")' actions.jsonl | jq '{command: .input.command, error: .error, stderr: .stderr}'
```

→ 日誌規範：[shared/communication/execution-logs.md](../../shared/communication/execution-logs.md)

## 共用模組

| 模組 | 用途 |
|------|------|
| [coordination/map-phase.md](../../shared/coordination/map-phase.md) | 並行協調 |
| [coordination/reduce-phase.md](../../shared/coordination/reduce-phase.md) | 匯總整合、大檔案處理 |
| [quality/tdd-enforcement.yaml](../../shared/quality/tdd-enforcement.yaml) | TDD 強制 |
| [tasks/dependency-detection.yaml](../../shared/tasks/dependency-detection.yaml) | 依賴偵測 |
| [quality/gates.yaml](../../shared/quality/gates.yaml) | 品質閘門 |
| [tools/dag-validator.py](../../shared/tools/dag-validator.py) | DAG 驗證器 |

## 工作流位置

```
RESEARCH → PLAN → TASKS → IMPLEMENT → REVIEW → VERIFY
                    ↑
                 你在這裡
```

- **輸入**：`implementation-plan.md` 來自 `plan` skill
- **輸出**：`tasks.yaml` 供 `implement` skill 使用
