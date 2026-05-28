---
name: review
version: 3.1.0
description: 多 Agent 並行審查框架 - 多視角程式碼審查，問題分類與優先排序
triggers: [multi-review, code-review, 程式碼審查]
context: fork
agent: Explore
allowed-tools: [Read, Grep, Glob, Bash, Write]
model: sonnet
---

# Multi-Agent Review v3.0.0

> 多視角審查 → 問題分類 → 優先排序 → 修復建議

## 使用方式

```bash
/multi-review [實作路徑]
/multi-review .claude/memory/implement/user-auth/
```

**Flags**: `--from-implement ID` | `--focus security|quality|docs`

## 預設 4 視角

| ID | 名稱 | 模型 | 聚焦 |
|----|------|------|------|
| `code-quality` | 程式碼品質 | haiku | 命名、結構、可讀性 |
| `test-coverage` | 測試覆蓋 | haiku | 覆蓋率、測試品質 |
| `documentation` | 文檔檢查 | haiku | 註解、README、API 文檔 |
| `integration` | 整合分析 | sonnet | 整合問題、依賴衝突 |

→ 模型路由配置：[shared/config/model-routing.yaml](../../shared/config/model-routing.yaml)

## 執行流程

```
Phase 0: 載入實作 → 收集變更檔案、測試結果
    ↓
Phase 1: MAP（並行審查）
    ┌──────────┬──────────┬──────────┬──────────┐
    │程式碼品質│測試覆蓋  │文檔檢查  │整合分析  │
    └──────────┴──────────┴──────────┴──────────┘

    ⚠️ **並行執行關鍵**：
       在單一訊息中發送 4 個 Task 工具呼叫：
       - Task({description: "程式碼品質審查", ...})
       - Task({description: "測試覆蓋審查", ...})
       - Task({description: "文檔檢查", ...})
       - Task({description: "整合分析", ...})
       這樣才能真正並行執行！
    ↓
Phase 2: REDUCE（問題匯總）
    ├── 問題分類（BLOCKER/HIGH/MEDIUM/LOW）
    ├── 優先排序
    └── 修復建議
    ↓
Phase 3: 品質評分 → 各維度評分
    ↓
Phase 4: 品質閘門 → 通過/回退決策
```

## 問題分類

| 級別 | 定義 | 處理 |
|------|------|------|
| BLOCKER | 必須修復才能繼續 | 回退 IMPLEMENT |
| HIGH | 重要問題，應修復 | 限時修復 |
| MEDIUM | 建議改善 | 記錄追蹤 |
| LOW | 風格建議 | 可選 |

## 品質評分

三維度評分：
- **完整性** (30%): 功能完整、無遺漏
- **一致性** (30%): 風格一致、無矛盾
- **可操作性** (40%): 建議具體可執行

→ 評分配置：[shared/quality/scoring.yaml](../../shared/quality/scoring.yaml)

## CP4: Task Commit

品質閘門檢查完成後，**必須執行 CP4 Task Commit**。

```
Phase 4: 品質閘門 → 通過/回退決策
    ↓
CP4: Task Commit
    ├── git add .claude/memory/review/{implement-id}/
    └── git commit -m "docs(review): complete {feature} code review"
```

→ 協議：[shared/git/commit-protocol.md](../../shared/git/commit-protocol.md)

## 品質閘門

通過條件（REVIEW 階段）：
- ✅ 無 BLOCKER 問題
- ✅ HIGH 問題 ≤ 2
- ✅ 品質分數 ≥ 75

失敗處理：
- BLOCKER 存在 → 回退到 IMPLEMENT
- HIGH > 2 → 要求修復後重新審查

→ 閘門配置：[shared/quality/gates.yaml](../../shared/quality/gates.yaml)

## 輸出結構

```
.claude/memory/review/[implement-id]/
├── meta.yaml           # 元數據
├── perspectives/       # 完整視角報告（MAP 產出，保留）
│   ├── code-quality.md
│   ├── test-coverage.md
│   ├── documentation.md
│   └── integration.md
├── summaries/          # 結構化摘要（REDUCE 產出，供快速查閱）
│   ├── code-quality.yaml
│   ├── test-coverage.yaml
│   ├── documentation.yaml
│   └── integration.yaml
├── issues.yaml         # 問題清單
├── scoring.yaml        # 評分詳情
└── review-summary.md   # 審查摘要（主輸出）
```

> ⚠️ perspectives/ 保存完整報告，summaries/ 保存結構化摘要，兩者都必須保留。

## Agent 能力限制

**審查 Agent 不應該開啟 Task**：

| 允許的操作 | 說明 |
|-----------|------|
| ✅ Read | 讀取程式碼 |
| ✅ Glob/Grep | 搜尋檔案和內容 |
| ✅ Bash | 執行命令 |
| ✅ Write | 寫入報告 |
| ❌ Task | 開子 Agent |

## 行動日誌

每個工具調用完成後，記錄到 `.claude/workflow/{workflow-id}/logs/actions.jsonl`。

**記錄時機**：
- 成功：記錄 `tool`、`input`、`output_preview`、`duration_ms`、`status: success`
- 失敗：記錄 `tool`、`input`、`error`、`stderr`（如有）、`status: failed`

**關鍵行動（REVIEW 階段）**：
| 行動 | 記錄重點 |
|------|----------|
| Read（讀取程式碼） | `file_path`、`output_size` |
| Task（啟動審查 Agent） | `subagent_type`、`prompt` (truncated)、`agent_id` |
| Grep（搜尋問題模式） | `pattern`、`match_count` |
| Write（寫入審查報告） | `file_path`、`content_size` |

**排查問題**：
```bash
# 查看 REVIEW 階段所有失敗行動
jq 'select(.stage == "REVIEW" and .status == "failed")' actions.jsonl

# 查看特定審查視角的行動
jq 'select(.agent_id == "agent_code-quality")' actions.jsonl
```

→ 日誌規範：[shared/communication/execution-logs.md](../../shared/communication/execution-logs.md)

## 共用模組

| 模組 | 用途 |
|------|------|
| [coordination/map-phase.md](../../shared/coordination/map-phase.md) | 並行協調 |
| [coordination/reduce-phase.md](../../shared/coordination/reduce-phase.md) | 匯總整合、大檔案處理 |
| [quality/scoring.yaml](../../shared/quality/scoring.yaml) | 品質評分 |
| [quality/gates.yaml](../../shared/quality/gates.yaml) | 品質閘門 |
| [quality/rollback-strategy.yaml](../../shared/quality/rollback-strategy.yaml) | 回退策略 |
| [perspectives/expertise-frameworks/](../../shared/perspectives/expertise-frameworks/) | 專業框架 |

## 工作流位置

```
RESEARCH → PLAN → TASKS → IMPLEMENT → REVIEW → VERIFY
                                         ↑
                                      你在這裡
```

- **輸入**：已實作的程式碼，來自 `implement` skill
- **輸出**：審查報告，供 `verify` skill 驗證或回退 `implement`
