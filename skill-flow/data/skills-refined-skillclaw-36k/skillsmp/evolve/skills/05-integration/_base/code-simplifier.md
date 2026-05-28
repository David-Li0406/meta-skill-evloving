# code-simplifier 整合

> Claude Code 官方 Plugin，用於簡化和重構程式碼

## 概述

| 屬性 | 說明 |
|------|------|
| **來源** | Claude Code 官方 Plugin (claude-plugins-official) |
| **作者** | Anthropic (Boris Cherny 團隊) |
| **模型** | Opus（高品質推理） |
| **用途** | 程式碼簡化、重構、技術債清理 |

## 安裝

```bash
claude plugin install code-simplifier
```

## 核心原則

### 1. 保持功能不變
- 只改「如何做」，不改「做什麼」
- 所有原始功能、輸出、行為必須保持不變

### 2. 套用專案標準
- 自動讀取 CLAUDE.md 的規範
- 遵循 ES modules、import 排序、命名規範
- 使用專案的錯誤處理模式

### 3. 提升清晰度
- 減少不必要的複雜度和巢狀
- 消除冗餘程式碼和抽象
- 改善變數和函數命名
- 移除描述明顯程式碼的註解
- **避免巢狀三元運算** - 改用 switch 或 if/else

### 4. 維持平衡
避免過度簡化：
- ❌ 過度聰明的解決方案
- ❌ 把太多關注點塞進單一函數
- ❌ 移除有助於組織的抽象
- ❌ 為了「更少行數」犧牲可讀性
- ❌ 讓程式碼更難除錯或擴展

## 與 evolve PDCA 的整合

```
┌─────────────────────────────────────────────────────────────────┐
│  PDCA 整合點                                                    │
│                                                                 │
│  Plan 階段                                                      │
│  └─ 無直接整合（code-simplifier 專注於已存在的程式碼）         │
│                                                                 │
│  Do 階段                                                        │
│  └─ 寫完程式碼後，可選擇性呼叫 code-simplifier 優化             │
│                                                                 │
│  Check 階段 ← 主要整合點                                        │
│  ├─ 功能驗證通過後                                              │
│  ├─ 呼叫 code-simplifier 簡化程式碼                             │
│  └─ 再次驗證確保功能不變                                        │
│                                                                 │
│  Act 階段                                                       │
│  └─ 記錄簡化前後的差異到 memory                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 使用時機

### 適合使用

| 場景 | 說明 |
|------|------|
| **功能完成後** | 程式碼能運作但不夠優雅 |
| **重構任務** | 專門清理技術債 |
| **Code Review 前** | 確保程式碼品質 |
| **Milestone 完成後** | 批次優化該階段的程式碼 |

### 不適合使用

| 場景 | 原因 |
|------|------|
| **功能開發中** | 程式碼還在變動，過早優化 |
| **緊急修復** | 簡化可能引入風險 |
| **不熟悉的程式碼** | 需要先理解再簡化 |

## 整合到 evolve 的建議流程

### 流程 A：單次任務後簡化

```
1. 執行 PDCA 完成任務
2. CP2 驗證通過（測試 + 編譯）
3. 呼叫 code-simplifier
4. 再次 CP2 驗證
5. 記錄到 memory（如有顯著改進）
```

### 流程 B：Milestone 批次簡化

```
1. 完成一個 Milestone 的多個任務
2. 執行 CP3（Milestone 確認）
3. 識別本階段修改的所有檔案
4. 對每個檔案呼叫 code-simplifier
5. 整體驗證
6. Commit：「refactor: simplify code after milestone X」
```

### 流程 C：技術債專項清理

```
1. 目標：清理特定目錄/模組的技術債
2. 先建立測試覆蓋率（如果沒有）
3. 逐檔呼叫 code-simplifier
4. 每次修改後執行測試
5. 記錄改進幅度到 memory
```

## 與其他工具的協作

```
┌─────────────────────────────────────────────────────────────────┐
│  工具鏈                                                         │
│                                                                 │
│  code-simplifier                                                │
│  ├─ 輸入：最近修改的程式碼                                      │
│  ├─ 處理：根據 CLAUDE.md 規範簡化                               │
│  └─ 輸出：更清晰、更一致的程式碼                                │
│                                                                 │
│  配合工具：                                                     │
│  ├─ PostToolUse Hook → 自動格式化（prettier, eslint）           │
│  ├─ CP2 (build/test) → 驗證功能不變                             │
│  ├─ code-review plugin → 審查簡化結果                           │
│  └─ PAL codereview → 多模型審查                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 注意事項

1. **先測試再簡化** - 確保有測試覆蓋，才能驗證功能不變
2. **小範圍開始** - 不要一次簡化太多檔案
3. **保留版本** - 重大簡化前先 commit
4. **驗證兩次** - 簡化前後都要驗證
5. **記錄學習** - 好的簡化模式記錄到 patterns/

## 策略記錄模板

```yaml
# .claude/memory/strategies/code-simplification.md
task_type: 程式碼簡化
last_updated: YYYY-MM-DD

strategies:
  - name: "code-simplifier plugin"
    priority: 1
    適用: "JavaScript/TypeScript 專案"
    success_rate: TBD
    notes: "使用 Opus 模型，品質高但較慢"

  - name: "手動重構 + PAL review"
    priority: 2
    適用: "複雜邏輯需要深度理解"
    success_rate: TBD
    notes: "先理解再簡化"
```

## 範例：呼叫 code-simplifier

```
用戶或 evolve：
「請使用 code-simplifier 簡化 src/utils/validator.ts」

或：
「使用 code simplifier 檢查最近修改的程式碼是否可以簡化」
```

## 相關資源

- [Boris Cherny 推文](https://x.com/bcherny/status/2009450715081789767)
- [Boris Cherny Tips](../.claude/memory/learnings/2025-01-07-boris-cherny-claude-code-tips.md)
