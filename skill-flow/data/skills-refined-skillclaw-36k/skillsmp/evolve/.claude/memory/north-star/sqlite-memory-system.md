# 北極星：SQLite Memory 系統

> 建立日期：2026-01-16
> 狀態：✅ 已完成
> 完成日期：2026-01-16

## 願景

**讓整個 AI 助手生態系變得更聰明** — 透過統一的 SQLite Memory 系統，實現：
- 跨專案知識共享（學一次，處處可用）
- Token 使用優化（精確查詢取代全文載入）
- Context 無縫傳遞（Skill 間共享狀態）
- 集體智慧累積（失敗經驗共享、智能推薦）

## 完成標準（Definition of Done）

### 核心功能
- [x] SQLite 資料庫 schema 設計並初始化
- [x] Memory MCP Server 提供 tools (23 個工具)
- [x] FTS5 全文搜尋功能
- [x] Context 表支援跨 Skill 共享
- [x] 遷移現有 filesystem memory (22 筆)

### 整合
- [x] 更新 evolve skill CP1 使用 SQLite（memory_search + failure_search）
- [x] 更新 evolve skill CP3.5 使用 SQLite（memory_write）
- [x] 更新 evolve skill CP5 使用 SQLite（failure_record）
- [x] 建立整合指南（05-integration/_base/memory-mcp.md）
- [x] 提供 fallback 到 filesystem（離線支援）

### 生態系
- [x] 跨專案知識自動共享 (scope: global)
- [x] Skill 效果追蹤功能 (skill_usage_start/end)
- [x] 失敗經驗自動索引 (failure_record/search)

### 品質
- [x] 效能測試通過（FTS5 ~3.5ms vs Grep ~20ms）
- [x] 文檔完整 (05-integration/_base/memory-mcp.md)
- [x] npm 發布 (sqlite-memory-mcp v1.0.2)

## 不做清單（Out of Scope）

- ❌ 不使用 Redis（效能測試證明 SQLite 更適合）
- ❌ 不建立遠端同步（先專注本地）
- ❌ 不改變 filesystem memory 格式（保持相容）
- ❌ 不強制遷移（漸進式採用）

## 動機

### 問題
1. Token 浪費：每次搜尋載入完整文件（~2300 tokens）
2. Context 斷層：Skill 間無法共享狀態
3. 知識孤島：跨專案經驗無法自動共用
4. 重複學習：相同問題在不同專案重複解決

### 效益（已驗證）
- Token 節省：55-91%
- 搜尋速度：提升 5-6x
- Context Switch：根本解決
- 生態系智能化：集體學習、失敗共享、智能推薦

## 成功指標

| 指標 | 目標 |
|------|------|
| Memory 搜尋 token | < 200 (現況 ~2300) |
| FTS 搜尋速度 | < 5ms |
| Context 共享 | 跨 Skill 可用 |
| 跨專案共享 | 自動生效 |
