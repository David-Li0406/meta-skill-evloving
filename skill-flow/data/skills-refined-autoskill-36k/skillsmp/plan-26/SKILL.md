---
name: plan
version: 3.2.0
description: 多 Agent 並行規劃框架 - 多視角同時設計，共識驅動實作計劃
triggers: [multi-plan, parallel-plan, 多角度規劃]
context: fork
agent: Plan
allowed-tools: [Read, Grep, Glob, Write, Bash]
model: sonnet
---

# Multi-Agent Plan v3.1.0

> 多視角並行規劃 → 風險評估 → 共識設計 → 實作計劃（自動 commit）

## 自動化機制

> ⚡ **本 skill 已整合 Claude Code Hooks**
>
> - Action logging、state tracking、git commit 均由 hooks 自動處理
> - 只需執行 CP1 初始化，其餘檢查點自動執行

## 使用方式

```bash
/multi-plan [功能需求]
/multi-plan 建立用戶認證系統 --from-research ID
```

**Flags**: `--perspectives N` | `--quick` | `--deep` | `--from-research ID`

## 預設 4 視角

| ID | 名稱 | 模型 | 聚焦 |
|----|------|------|------|
| `architect` | 系統架構師 | sonnet | 技術可行性、組件設計 |
| `risk-analyst` | 風險分析師 | sonnet | 潛在風險、失敗場景 |
| `estimator` | 估算專家 | haiku | 工作量評估、時程規劃 |
| `ux-advocate` | UX 倡導者 | haiku | 使用者體驗、API 設計 |

→ 模型路由配置：[shared/config/model-routing.yaml](../../shared/config/model-routing.yaml)

## 執行流程

```
CP1: 工作流初始化 ⚡ 手動執行
    python scripts/hooks/init_workflow.py --topic "{feature}" --stage PLAN
    ↓
Phase 0: 需求錨定 → 載入 research 上下文、確認驗收標準
    ↓
Phase 1: Memory 搜尋 → 識別可重用的設計決策
    ↓
Phase 2: 視角分解 → 早期安全/架構檢查
    ↓
Phase 3: MAP（並行規劃）✅ 自動追蹤
    ┌──────────┬──────────┬──────────┬──────────┐
    │ 架構師   │ 風險分析 │ 估算專家 │ UX 倡導  │
    └──────────┴──────────┴──────────┴──────────┘
    [CP2/CP3 由 hooks 自動處理 Agent 狀態追蹤]

    ⚠️ **並行執行關鍵**：
       在單一訊息中發送 4 個 Task 工具呼叫：
       - Task({description: "架構師視角", ...})
       - Task({description: "風險分析視角", ...})
       - Task({description: "估算專家視角", ...})
       - Task({description: "UX 倡導視角", ...})
       這樣才能真正並行執行！

    ⚠️ **強制**：每個 Agent 必須在完成前執行：
       1. mkdir -p .claude/memory/plans/{feature-id}/perspectives/
       2. Write → .claude/memory/plans/{feature-id}/perspectives/{perspective_id}.md
       未執行 Write = 任務失敗，工作流中止
    ↓
Phase 4: REDUCE（共識設計 + 風險緩解）
    ↓
Phase 5: 產出實作計劃 → 品質閘門檢查
    ↓
Phase 6: Memory 存檔
    ↓
CP4: Task Commit ✅ 自動執行
    [寫入 .claude/memory/ 時自動 git commit]
```

## 早期錯誤攔截

在 Phase 2 進行預防性檢查：

**安全性**（BLOCKER）：
- 認證機制已定義
- 授權模型已指定
- 資料驗證策略已定義

**架構**（HIGH）：
- 無循環依賴
- 模組邊界清晰

→ 配置：[shared/quality/early-detection.yaml](../../shared/quality/early-detection.yaml)

## CP4: Task Commit

Memory 存檔完成後，**必須執行 CP4 Task Commit**。

```
Phase 6: Memory 存檔
    ↓
CP4: Task Commit
    ├── git add .claude/memory/plans/{feature-id}/
    └── git commit -m "feat(plan): design {feature} implementation plan"
```

→ 協議：[shared/git/commit-protocol.md](../../shared/git/commit-protocol.md)

## 品質閘門

通過條件（PLAN 階段）：
- ✅ 所有必要組件有設計
- ✅ 風險評估完成
- ✅ 里程碑定義清晰
- ✅ 品質分數 ≥ 75

→ 閘門配置：[shared/quality/gates.yaml](../../shared/quality/gates.yaml)

## 輸出結構

```
.claude/memory/plans/[feature-id]/
├── meta.yaml               # 元數據
├── perspectives/           # 完整視角報告（MAP 產出，保留）
│   ├── architect.md
│   ├── risk-analyst.md
│   ├── estimator.md
│   └── ux-advocate.md
├── summaries/              # 結構化摘要（REDUCE 產出，供快速查閱）
│   ├── architect.yaml
│   ├── risk-analyst.yaml
│   ├── estimator.yaml
│   └── ux-advocate.yaml
├── synthesis.md            # 共識設計
├── implementation-plan.md  # 實作計劃（主輸出）
├── milestones.md           # 里程碑清單
└── risk-mitigation.md      # 風險緩解策略
```

> ⚠️ perspectives/ 保存完整報告，summaries/ 保存結構化摘要，兩者都必須保留。

## Agent 能力限制

**視角 Agent 不應該開啟 Task**：

| 允許的操作 | 說明 |
|-----------|------|
| ✅ Read | 讀取檔案 |
| ✅ Glob/Grep | 搜尋檔案和內容 |
| ✅ Explore agent | 輕量級探索 |
| ✅ Bash | 執行命令 |
| ✅ WebFetch | 抓取網頁 |
| ✅ Write | 寫入報告 |
| ❌ Task | 開子 Agent |

## 行動日誌

每個工具調用完成後，記錄到 `.claude/workflow/{workflow-id}/logs/actions.jsonl`。

**記錄時機**：
- 成功：記錄 `tool`、`input`、`output_preview`、`duration_ms`、`status: success`
- 失敗：記錄 `tool`、`input`、`error`、`stderr`（如有）、`status: failed`

**關鍵行動（PLAN 階段）**：
| 行動 | 記錄重點 |
|------|----------|
| Read（讀取研究報告） | `file_path`、`output_size` |
| Task（啟動 Agent） | `subagent_type`、`prompt` (truncated)、`agent_id` |
| Write（寫入計劃） | `file_path`、`content_size` |

**排查問題**：
```bash
# 查看 PLAN 階段所有失敗行動
jq 'select(.stage == "PLAN" and .status == "failed")' actions.jsonl

# 查看特定視角 Agent 的行動
jq 'select(.agent_id == "agent_architect")' actions.jsonl
```

→ 日誌規範：[shared/communication/execution-logs.md](../../shared/communication/execution-logs.md)

## 共用模組

| 模組 | 用途 |
|------|------|
| [coordination/map-phase.md](../../shared/coordination/map-phase.md) | 並行協調 |
| [coordination/reduce-phase.md](../../shared/coordination/reduce-phase.md) | 匯總整合、大檔案處理 |
| [synthesis/cross-validation.md](../../shared/synthesis/cross-validation.md) | 交叉驗證 |
| [quality/gates.yaml](../../shared/quality/gates.yaml) | 品質閘門 |
| [quality/early-detection.yaml](../../shared/quality/early-detection.yaml) | 早期攔截 |

## 工作流位置

```
RESEARCH → PLAN → TASKS → IMPLEMENT → REVIEW → VERIFY
             ↑
          你在這裡
```

- **輸入**：可從 `research` skill 載入研究報告
- **輸出**：`implementation-plan.md` 供 `tasks` skill 使用
