---
date: "2026-01-16"
tags: [memory, mcp, integration, sqlite, evolve]
---

# Memory MCP 整合設計

## 情境

需要將 claude-memory-mcp（SQLite Memory 系統）整合到 evolve skill 流程中，讓生態系更聰明、更專業。

## 問題

原本 evolve 的記憶系統是純 Git-based（.claude/memory/），搜尋依賴 Grep，存在以下問題：
1. 搜尋速度較慢（~20ms vs FTS5 的 ~3.5ms）
2. Token 消耗高（~2300 vs ~200）
3. 無法追蹤 Skill 使用成功率
4. 失敗經驗無法跨專案共享

## 解決方案

**Skill Script 整合**（最佳方案）：
- 在 `05-integration/_base/memory-mcp.md` 建立整合指南
- 更新關鍵檢查點（CP1, CP3.5, CP5）加入 Memory MCP 呼叫
- 保留 Git Memory 作為詳細記錄，Memory MCP 作為搜尋索引

**為什麼不用 CLI？**
- Claude Code 的 MCP 是 stdio 模式，CLI 無法共用連線
- AI 已經可以直接呼叫 MCP 工具，不需要額外中介

## 整合架構

```
CP0 ─► skill_usage_start()     # 開始追蹤
CP1 ─► memory_search()         # 搜尋經驗（取代 Grep）
    ─► failure_search()        # 搜尋失敗解法
CP3.5 ► memory_write()         # 記錄學習（雙重記錄）
CP5 ─► failure_record()        # 記錄失敗
結束 ─► skill_usage_end()      # 結束追蹤，計算成功率
```

## 驗證

- [x] 建立 `skills/05-integration/_base/memory-mcp.md`
- [x] 更新 CP1 加入 memory_search + failure_search
- [x] 更新 CP3.5 加入 memory_write
- [x] 更新 CP5 加入 failure_record
- [x] 更新 05-integration/README.md

## 注意事項

1. **雙重記錄**：Git Memory（詳細）+ Memory MCP（索引）並存
2. **回退機制**：若 MCP 不可用，回退到 Grep 搜尋
3. **Key 命名**：使用 `learning:YYYY-MM-DD:slug` 格式
4. **跨專案**：scope 設為 "global" 實現跨專案共享

## 相關檔案

- `skills/05-integration/_base/memory-mcp.md` - 整合指南
- `skills/02-checkpoints/_base/cp1-memory-search.md` - CP1 更新
- `skills/02-checkpoints/_base/cp3.5-memory-sync.md` - CP3.5 更新
- `skills/02-checkpoints/_base/cp5-failure-postmortem.md` - CP5 更新
