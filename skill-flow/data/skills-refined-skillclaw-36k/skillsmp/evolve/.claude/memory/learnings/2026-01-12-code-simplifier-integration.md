---
date: "2026-01-12"
tags: [code-simplifier, plugin, refactoring, technical-debt, boris-cherny, evolve-integration]
task: 安裝並整合 code-simplifier plugin 到 evolve 工作流程
status: resolved
source: https://x.com/bcherny/status/2009450715081789767
---

# code-simplifier Plugin 整合

## 情境
Boris Cherny (Claude Code 創作者) 開源了 Claude Code 團隊內部使用的 code-simplifier agent，可用於重構和清理技術債。

## 安裝方式

```bash
claude plugin install code-simplifier
```

## 核心功能

code-simplifier 是一個專注於程式碼簡化的 agent：

| 特性 | 說明 |
|------|------|
| **模型** | 使用 Opus（高品質推理） |
| **範圍** | 預設只處理最近修改的程式碼 |
| **原則** | 保持功能不變，只改善實作方式 |

### 簡化原則

1. **保持功能不變** - 只改「如何做」
2. **套用專案標準** - 讀取 CLAUDE.md 規範
3. **提升清晰度** - 減少複雜度、消除冗餘
4. **維持平衡** - 避免過度簡化

### 重要：避免的模式
- ❌ 巢狀三元運算 → 改用 switch/if-else
- ❌ 過度聰明的 one-liner
- ❌ 移除有助於組織的抽象

## 與 evolve 的整合

### 整合點：PDCA Check 階段

```
Do (寫程式碼)
    ↓
Check (功能驗證通過)
    ↓
呼叫 code-simplifier
    ↓
再次 Check (確保功能不變)
    ↓
Act (記錄)
```

### 使用時機

| 適合 | 不適合 |
|------|--------|
| 功能完成後 | 功能開發中 |
| 重構任務 | 緊急修復 |
| Code Review 前 | 不熟悉的程式碼 |
| Milestone 完成後 | - |

## 驗證結果

✅ Plugin 安裝成功
✅ 整合文件已建立：`skills/05-integration/_base/code-simplifier.md`
✅ 與現有 Boris Tips 記錄一致

## 注意事項

1. 先有測試覆蓋再簡化
2. 小範圍開始
3. 重大簡化前先 commit
4. 簡化前後都要驗證

## 相關檔案
- `skills/05-integration/_base/code-simplifier.md` - 完整整合指南
- `.claude/memory/learnings/2025-01-07-boris-cherny-claude-code-tips.md` - Boris 其他技巧
