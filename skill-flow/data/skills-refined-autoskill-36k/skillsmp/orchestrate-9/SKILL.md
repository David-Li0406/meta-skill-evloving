---
name: orchestrate
version: 3.1.0
description: 端到端工作流編排器 - 串聯 RESEARCH → PLAN → TASKS → IMPLEMENT → REVIEW → VERIFY
triggers: [orchestrate, workflow, 全流程, e2e]
allowed-tools: [Read, Write, Bash, Glob, Grep, Skill, Task, TaskCreate, TaskUpdate, TaskList, TaskGet]
---

# Multi-Agent Orchestrate v3.0.0

> 需求輸入 → 6 階段串聯 → 品質閘門 → 智慧回退 → 完成交付

## 使用方式

```bash
/orchestrate [需求描述]
/orchestrate 建立用戶認證系統，支援 JWT 和 OAuth2
```

**Flags**:
- `--profile <mode>` - 執行模式：`default`（預設）| `express`（快速）| `quality`（最高品質）
- `--start-from STAGE` - 從指定階段開始
- `--skip STAGE` - 跳過指定階段
- `--quick` - 快速模式（等同 `--profile express`）
- `--deep` - 深度模式（等同 `--profile quality`）

## 工作流階段

```
RESEARCH → PLAN → TASKS → IMPLEMENT → REVIEW → VERIFY
                                        ↑__________↓
                                      智慧回退機制
```

| 階段 | 輸入 | 輸出 | 閘門分數 |
|------|------|------|----------|
| RESEARCH | 需求 | synthesis.md | ≥70 |
| PLAN | 研究報告 | implementation-plan.md | ≥75 |
| TASKS | 實作計劃 | tasks.yaml | ≥80 |
| IMPLEMENT | 任務清單 | 程式碼 | ≥80 |
| REVIEW | 程式碼 | review-summary.md | ≥75 |
| VERIFY | 審查報告 | 驗證結果 | ≥85 |

## 執行流程

```
Phase 0: 初始化工作流
    ├── 生成 workflow-id
    ├── **【必要】執行 workflow-init.sh 初始化通訊環境**
    │   └── Bash: ./shared/tools/workflow-init.sh init <workflow-id> orchestrate "<需求摘要>"
    │   └── 這會創建 .claude/workflow/current.json（Hooks 依賴此檔案）
    ├── 載入執行模式配置
    │   └── 讀取 shared/config/execution-profiles.yaml
    │   └── 套用視角數和模型配置
    ├── 建立報告目錄
    └── 記錄開始時間
    ↓
For each stage in [RESEARCH, PLAN, TASKS, IMPLEMENT, REVIEW, VERIFY]:
    ↓
    Phase 1: 執行階段
    ├── 呼叫對應 skill
    └── 等待完成
    ↓
    Phase 2: 早期終止檢查
    ├── 滿足條件？→ 可跳過後續步驟
    └── 不滿足 → 繼續
    ↓
    Phase 3: 品質閘門
    ├── 通過 → 下一階段
    └── 失敗 → 智慧回退
    ↓
End for
    ↓
Phase 4: 完成
    ├── 生成報告
    └── 更新 Memory
```

## 智慧回退機制

根據迭代次數決定回退目標：

| 迭代 | 回退目標 | 原因 |
|------|----------|------|
| 1-2 | IMPLEMENT | 可能是實作問題 |
| 3 | TASKS | 可能是任務分解問題 |
| 4 | PLAN | 可能是設計問題 |
| 5+ | HUMAN | 超過自動修復能力 |

**循環偵測**：
- 相同錯誤兩次 → 升級回退層級
- 階段間振盪 → 暫停分析根因
- 總迭代 > 10 → 強制停止

→ 配置：[shared/quality/rollback-strategy.yaml](../../shared/quality/rollback-strategy.yaml)

## 早期終止

| 階段 | 條件 | 動作 |
|------|------|------|
| RESEARCH | consensus ≥ 0.9 | 跳過衝突解決 |
| PLAN | risk < 0.2 | 快速模式 |
| REVIEW | 無 BLOCKER/HIGH | 直接通過 |
| VERIFY | pass_rate ≥ 0.98 | 可發布 |

→ 配置：[shared/config/early-termination.yaml](../../shared/config/early-termination.yaml)

## 報告生成

完成後自動生成：
- `dashboard.md` - 總覽
- `timeline.md` - 時間線
- `quality-report.md` - 品質報告
- `decisions.md` - 決策記錄

→ 工具：[shared/tools/generate-report.sh](../../shared/tools/generate-report.sh)

## 輸出結構

```
.claude/memory/workflows/[workflow-id]/
├── dashboard.md        # 總覽報告
├── timeline.md         # 時間線
├── decisions.md        # 決策記錄
├── quality-report.md   # 品質報告
├── stages/             # 各階段報告
├── agents/             # Agent 記錄
└── exports/            # 匯出格式
```

## 共用模組

| 模組 | 用途 |
|------|------|
| [quality/gates.yaml](../../shared/quality/gates.yaml) | 品質閘門 |
| [quality/rollback-strategy.yaml](../../shared/quality/rollback-strategy.yaml) | 智慧回退 |
| [config/early-termination.yaml](../../shared/config/early-termination.yaml) | 早期終止 |
| [config/execution-profiles.yaml](../../shared/config/execution-profiles.yaml) | 執行模式 |
| [config/context-freshness.yaml](../../shared/config/context-freshness.yaml) | 上下文新鮮 |
| [tools/generate-report.sh](../../shared/tools/generate-report.sh) | 報告生成 |
| [tools/workflow-init.sh](../../shared/tools/workflow-init.sh) | 工作流初始化 |

## 【重要】初始化步驟

在執行任何階段之前，**必須**先初始化工作流環境：

```bash
# 1. 生成 workflow ID（格式：orchestrate_YYYYMMDD_HHMMSS_xxxx）
WORKFLOW_ID="orchestrate_$(date +%Y%m%d_%H%M%S)_$(openssl rand -hex 4)"

# 2. 執行初始化（創建 current.json，讓 Hooks 能記錄活動）
./shared/tools/workflow-init.sh init "$WORKFLOW_ID" orchestrate "需求摘要"
```

**為什麼這很重要？**
- Hooks（log-tool-pre.sh、log-tool-post.sh、log-agent-lifecycle.sh）依賴 `.claude/workflow/current.json`
- 如果沒有這個檔案，所有 Agent 活動都不會被記錄
- 這會導致 `/status` 和 statusline 無法顯示正確的工作流狀態
