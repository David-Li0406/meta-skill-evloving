# Quick Start Guide

> 3 分鐘快速上手 Multi-Agent Orchestrator

## 最簡用法

```bash
/multi-orchestrate "新增用戶認證功能"
```

這會：
1. 自動判斷應該從哪個階段開始
2. 按順序執行所需階段
3. 遇到問題自動回退修正
4. 最終產出完整工作流記錄

## 工作流階段

```
RESEARCH → PLAN → IMPLEMENT → REVIEW → VERIFY
   ↓         ↓         ↓          ↓        ↓
 研究      規劃      實作       審查     驗證
 (可選)                                   ↓
                                     SHIP IT ✅
```

## 常用模式

### 完整工作流

```bash
/multi-orchestrate "新增用戶認證功能"
```

系統會自動判斷從 RESEARCH 還是 PLAN 開始。

### 從已有計劃開始

```bash
/multi-orchestrate --from-plan user-auth
```

載入 `.claude/memory/plans/user-auth/`，從 IMPLEMENT 開始。

### 從已有研究開始

```bash
/multi-orchestrate --from-research user-auth
```

載入 `.claude/memory/research/user-auth/`，從 PLAN 開始。

### 指定起始階段

```bash
/multi-orchestrate --start-at implement --plan user-auth "用戶認證功能"
```

強制從 IMPLEMENT 開始。

### 部分執行

```bash
# 只執行到 IMPLEMENT（不審查驗證）
/multi-orchestrate --stop-at implement "用戶認證功能"

# 跳過 RESEARCH
/multi-orchestrate --skip research "用戶認證功能"
```

### 續接中斷的工作流

```bash
/multi-orchestrate --resume user-auth
```

從上次中斷處繼續。

## 階段判斷說明

### 自動判斷

系統會檢查 Memory 中是否有相關記錄：

| 存在記錄 | 起始階段 |
|----------|----------|
| 無任何記錄 | RESEARCH 或 PLAN |
| 有 research-report.md | PLAN |
| 有 implementation-plan.md | IMPLEMENT |
| 有 implementation-log.md | REVIEW |
| 有 review-summary.md (無 BLOCKER) | VERIFY |

### 手動指定

如果自動判斷不符合預期，可以手動指定：

```bash
# 強制從頭開始
/multi-orchestrate --start-at research "用戶認證功能"

# 強制從規劃開始（即使有研究報告）
/multi-orchestrate --start-at plan "用戶認證功能"
```

## 回退機制

### 自動回退

```
IMPLEMENT → REVIEW
              ↓
          有 BLOCKER
              ↓
         ← 回退 ←
         IMPLEMENT (修正)
              ↓
          REVIEW (重新審查)
              ↓
          通過 ✅
```

### 回退上限

預設最多回退 3 次。超過後會暫停並請求人工介入：

```
⚠️ 已達回退上限（3 次）
請人工審查後使用 --resume 繼續
```

### 禁用回退

```bash
/multi-orchestrate --no-rollback "用戶認證功能"
```

遇到問題直接停止，不嘗試回退。

## 演練模式

查看會執行哪些階段，但不實際執行：

```bash
/multi-orchestrate --dry-run "用戶認證功能"
```

輸出：

```
🔍 演練模式 - 以下是預計執行的階段：

1. PLAN
   輸入：需求描述
   輸出：implementation-plan.md, milestones.md

2. IMPLEMENT
   輸入：implementation-plan.md
   輸出：code changes, implementation-log.md

3. REVIEW
   輸入：code changes
   輸出：review-summary.md

4. VERIFY
   輸入：review-summary.md
   輸出：release-decision.md

預估階段數：4
（使用 --dry-run=false 實際執行）
```

## 輸出位置

所有產出物存儲在 `.claude/memory/`：

```
.claude/memory/
├── research/user-auth/          # RESEARCH 產出
│   └── research-report.md
├── plans/user-auth/             # PLAN 產出
│   ├── implementation-plan.md
│   └── milestones.md
├── implementations/user-auth/   # IMPLEMENT 產出
│   ├── implementation-log.md
│   └── perspectives/
├── reviews/user-auth/           # REVIEW 產出
│   └── review-summary.md
└── verifications/user-auth/     # VERIFY 產出
    └── release-decision.md
```

## 結果解讀

### ✅ SHIP IT

```
✅ 工作流完成：user-auth
🎯 最終結果：SHIP IT

所有階段通過，可以發布！
```

### ⚠️ 需要更多迭代

```
⚠️ 工作流暫停：user-auth
❌ 暫停原因：達到回退上限

需要人工介入後使用 --resume 繼續
```

### ❌ BLOCKED

```
❌ 工作流失敗：user-auth
失敗階段：VERIFY
原因：核心功能測試未通過

查看詳情：.claude/memory/verifications/user-auth/release-decision.md
```

## 進階技巧

### 調整回退上限

```bash
/multi-orchestrate --max-iterations 5 "複雜功能"
```

### 指定視角數量

會傳遞給各個子 skill：

```bash
/multi-orchestrate --perspectives 6 "核心功能"  # 深度模式
/multi-orchestrate --perspectives 2 "小功能"    # 快速模式
```

### 結合 evolve

工作流會自動與 evolve Checkpoint 同步：
- CP1: 開始時搜尋 Memory
- CP0.5: PLAN 完成後創建 Worktree（如啟用）
- CP2: IMPLEMENT 時 Build + Test
- CP3.5: 每階段完成更新 index.md
- CP5: 回退時驗屍分析
- CP6: VERIFY 完成時發布驗證
- CP6.5: Worktree 完成處理（合併/保留/清理）

## Git Worktree 模式

### 概述

Worktree 模式在隔離的分支/目錄中執行 IMPLEMENT/REVIEW/VERIFY，確保 main 分支始終穩定。

```
main (穩定)                    .worktrees/{id}/ (feature 開發)
    │                                │
    │  PLAN 完成                     │
    ├──────────────────────────────→│ 創建 worktree
    │                                │
    │                                │← IMPLEMENT
    │                                │← REVIEW
    │                                │← VERIFY
    │                                │
    │  SHIP IT                       │
    │←──────────────────────────────┤ 合併 + 清理
    │                                │
    ↓ 穩定推進                       (刪除)
```

### 基本使用

```bash
# 自動使用 worktree（預設）
/multi-orchestrate "新增用戶認證功能"

# 強制使用 worktree
/multi-orchestrate --worktree "新增功能"

# 禁用 worktree（直接在 main 工作）
/multi-orchestrate --no-worktree "快速修復"
```

### Worktree 目錄

程式碼變更在 `.worktrees/{feature-id}/` 中執行：

```
/project/
├── .worktrees/
│   └── user-auth/          # 隔離的工作目錄
│       ├── src/
│       ├── tests/
│       └── package.json
├── .claude/memory/         # Memory 仍在 main
│   └── implementations/
│       └── user-auth/
└── src/                    # main 保持穩定
```

### 完成處理

```bash
# SHIP IT → 自動合併並清理
# BLOCKED → 保留 worktree 繼續迭代

# 恢復 blocked 的工作流
/multi-orchestrate --resume user-auth

# 放棄工作流（保留 patch）
/multi-orchestrate --abandon user-auth --keep-patch

# 清理孤立的 worktrees
/multi-orchestrate --cleanup-worktrees
```

### 合併策略

```bash
# 壓縮為單一 commit（預設）
/multi-orchestrate --merge-strategy squash "功能"

# 保留完整歷史
/multi-orchestrate --merge-strategy merge "功能"

# Rebase
/multi-orchestrate --merge-strategy rebase "功能"
```

### 自訂 Worktree 目錄

```bash
/multi-orchestrate --worktree-dir ./dev-branches "功能"
```

## 下一步

- [階段判斷邏輯](../../01-stage-detection/_base/auto-detect.md)
- [數據傳遞](../../02-data-flow/_base/stage-handoff.md)
- [回退規則](../../03-error-handling/_base/rollback-rules.md)
- [Git Worktree 生命週期](../../04-git-worktree/_base/lifecycle.md)
