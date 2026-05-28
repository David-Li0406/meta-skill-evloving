---
name: research
version: 3.2.0
description: 多 Agent 並行研究框架 - 多視角同時研究，智能匯總成完整報告
triggers: [multi-research, parallel-research, 多角度研究]
context: fork
agent: Explore
allowed-tools: [Read, Grep, Glob, WebFetch, Write, Bash]
model: sonnet
---

# Multi-Agent Research v3.1.0

> 多視角並行研究 → 交叉驗證 → 智能匯總 → Memory 存檔（自動 commit）

## 自動化機制

> ⚡ **本 skill 已整合 Claude Code Hooks**
>
> - Action logging、state tracking、git commit 均由 hooks 自動處理
> - 只需執行 CP1 初始化，其餘檢查點自動執行

## 使用方式

```bash
/multi-research [研究主題]
/multi-research AI Agent 架構設計模式 --deep
```

**Flags**: `--perspectives N` | `--quick` | `--deep` | `--no-memory`

## 預設 4 視角

| ID | 名稱 | 模型 | 聚焦 |
|----|------|------|------|
| `architecture` | 架構分析師 | sonnet | 系統結構、設計模式 |
| `cognitive` | 認知研究員 | sonnet | 方法論、思維框架 |
| `workflow` | 工作流設計 | haiku | 執行流程、整合策略 |
| `industry` | 業界實踐 | haiku | 現有框架、最佳實踐 |

→ 模型路由配置：[shared/config/model-routing.yaml](../../shared/config/model-routing.yaml)

## 執行流程

```
CP1: 工作流初始化 ⚡ 手動執行
    python scripts/hooks/init_workflow.py --topic "{topic}" --stage RESEARCH
    ↓
Phase 0: 北極星錨定 → 定義研究目標、成功標準
    ↓
Phase 1: Memory 搜尋 → 避免重複研究
    ↓
Phase 2: 視角分解 → 為每視角生成專屬 prompt
    ↓
Phase 3: MAP（並行研究）✅ 自動追蹤
    ┌──────────┬──────────┬──────────┬──────────┐
    │架構分析師│認知研究員│工作流設計│業界實踐  │
    └──────────┴──────────┴──────────┴──────────┘
    [CP2/CP3 由 hooks 自動處理 Agent 狀態追蹤]

    ⚠️ **並行執行關鍵**：
       在單一訊息中發送 4 個 Task 工具呼叫：
       - Task({description: "架構視角", ...})
       - Task({description: "認知視角", ...})
       - Task({description: "工作流視角", ...})
       - Task({description: "業界視角", ...})
       這樣才能真正並行執行！

    ⚠️ **強制**：每個 Agent 必須在完成前執行：
       1. mkdir -p .claude/memory/research/{topic-id}/perspectives/
       2. Write → .claude/memory/research/{topic-id}/perspectives/{perspective_id}.md
       未執行 Write = 任務失敗，工作流中止
    ↓
Phase 4: REDUCE（交叉驗證 + 匯總）
    ↓
Phase 5: Memory 存檔 → 品質閘門檢查 → 存儲報告
    ↓
CP4: Task Commit ✅ 自動執行
    [寫入 .claude/memory/ 時自動 git commit]
```

## CP4: Task Commit ✅ 自動

> **由 `post_write.py` hook 自動處理**

當 Write 工具寫入 `.claude/memory/` 目錄時，hook 會自動：
1. `git add .claude/memory/research/{topic-id}/`
2. `git commit -m "docs(research): complete {topic} research"`
3. 記錄 action 到 `actions.jsonl`

→ Hook 設定：[.claude/settings.local.json.template](../../.claude/settings.local.json.template)
→ 協議：[shared/checkpoints/mandatory-checkpoints.md](../../shared/checkpoints/mandatory-checkpoints.md)

## 品質閘門

通過條件（RESEARCH 階段）：
- ✅ 至少 2 視角達成共識
- ✅ 無未解決的關鍵矛盾
- ✅ 品質分數 ≥ 70

→ 閘門配置：[shared/quality/gates.yaml](../../shared/quality/gates.yaml)

## 早期終止

當 `consensus_rate >= 0.9` 時，可跳過衝突解決。

→ 配置：[shared/config/early-termination.yaml](../../shared/config/early-termination.yaml)

## Context7 整合

自動偵測技術棧關鍵字（react, vue, fastapi 等）時，查詢最新文檔。

→ 配置：[shared/integration/context7.yaml](../../shared/integration/context7.yaml)

## 輸出結構

```
.claude/memory/research/[topic-id]/
├── meta.yaml           # 元數據
├── perspectives/       # 完整視角報告（MAP 產出，保留）
│   ├── architecture.md
│   ├── cognitive.md
│   ├── workflow.md
│   └── industry.md
├── summaries/          # 結構化摘要（REDUCE 產出，供快速查閱）
│   ├── architecture.yaml
│   ├── cognitive.yaml
│   ├── workflow.yaml
│   └── industry.yaml
├── synthesis.md        # 匯總報告（主輸出）
└── metrics.yaml        # 階段指標
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

## 網頁抓取策略

當需要抓取網頁時，使用以下順序：

1. **優先使用 WebFetch** - 快速、輕量
2. **如果 WebFetch 失敗**，使用 Chrome：
   ```
   a. mcp__claude-in-chrome__tabs_create_mcp → 建立新分頁
   b. mcp__claude-in-chrome__navigate → 導航到 URL
   c. mcp__claude-in-chrome__get_page_text → 讀取內容
   ```
3. **如果仍然失敗**，記錄 URL 供人工處理

## 行動日誌 ✅ 自動

> **由 Claude Code Hooks 自動處理**

工具調用自動記錄到 `.claude/workflow/{workflow-id}/logs/actions.jsonl`。

**自動記錄的工具**：
| 工具 | 觸發 Hook | 記錄內容 |
|------|-----------|----------|
| Task | pre_task.py / post_task.py | Agent 啟動/完成狀態 |
| Write | post_write.py | 檔案路徑、Memory commit |

**排查問題**：
```bash
# 查看 RESEARCH 階段所有失敗行動
jq 'select(.stage == "RESEARCH" and .status == "failed")' \
  .claude/workflow/{workflow-id}/logs/actions.jsonl

# 查看特定視角 Agent 的行動
jq 'select(.agent_id == "architecture")' \
  .claude/workflow/{workflow-id}/logs/actions.jsonl

# 查看即時狀態
cat .claude/workflow/{workflow-id}/current.json | jq .
```

→ Hook 腳本：[scripts/hooks/](../../scripts/hooks/)
→ 日誌規範：[shared/communication/execution-logs.md](../../shared/communication/execution-logs.md)

## 共用模組

| 模組 | 用途 |
|------|------|
| [coordination/map-phase.md](../../shared/coordination/map-phase.md) | 並行協調 |
| [coordination/reduce-phase.md](../../shared/coordination/reduce-phase.md) | 匯總整合、大檔案處理 |
| [synthesis/cross-validation.md](../../shared/synthesis/cross-validation.md) | 交叉驗證 |
| [quality/gates.yaml](../../shared/quality/gates.yaml) | 品質閘門 |
| [config/model-routing.yaml](../../shared/config/model-routing.yaml) | 模型路由 |

## 工作流位置

```
RESEARCH → PLAN → TASKS → IMPLEMENT → REVIEW → VERIFY
   ↑
  你在這裡
```

研究結果可被 `plan` skill 引用，作為規劃的輸入。
