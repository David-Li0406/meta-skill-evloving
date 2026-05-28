# 北極星：智能 Skill 生態系 MVP

> 建立日期：2026-01-16
> 狀態：✅ 已完成
> 完成日期：2026-01-16
> 版本：MVP (Phase 0.5)

## 願景

**讓 AI 自動發現、推薦、組合最適合的 skill** — 從「用戶選擇 skill」到「AI 智能推薦 skill」。

## 設計原則

- **不改 sqlite-memory-mcp**：使用現有 23 個 tools
- **只改 evolve skill**：降低風險和複雜度
- **用腳本達成同步**：不需要新的 MCP 功能
- **80% 效果，20% 工作量**

## 完成標準（Definition of Done）

### 核心功能
- [x] 自動判斷 scope（global vs project:xxx）
- [x] Skill 索引腳本（從 GitHub 同步到 sqlite-memory）
- [x] CP1 智能推薦（搜尋並顯示相關 skill）
- [x] 整合文檔更新

### 驗收標準
- [x] `/evolve 建立量化交易系統` 能自動推薦 `quant-trading` skill
- [x] 記錄經驗時能正確判斷 scope
- [x] 跨專案能搜尋到其他專案的 global 經驗

### 統計
- **已索引 Skills**: 78 個（54 software + 24 domain）
- **總記憶數**: 100 筆
- **Skill Repos**: 2 個（claude-software-skills, claude-domain-skills）

## 不做清單（Out of Scope）

- ❌ 不修改 sqlite-memory-mcp npm 包
- ❌ 不新增 MCP tools
- ❌ 不實作自動安裝 skill
- ❌ 不實作多 skill 並行執行
- ❌ 不建立 Web UI 儀表板

## 已完成的實作

### 1. Scope 自動判斷
- 文件：`skills/03-memory/_base/scope-detection.md`
- 判斷規則：專案專屬 vs 通用經驗
- 預設：global（寧可多分享）

### 2. Skill 同步腳本
- 文件：`scripts/sync-skills.sh`
- 功能：從 GitHub repos 同步 skill metadata 到 sqlite-memory
- 命令：`--software`, `--domain`, `--list`, `--clear`

### 3. CP1 推薦整合
- 文件：`skills/02-checkpoints/_base/cp1-memory-search.md`
- 新增：Skill 推薦顯示格式
- 搜尋：`memory_search({query: "skill:* 關鍵字"})`

### 4. 整合文檔
- 文件：`skills/05-integration/_base/skill-ecosystem.md`
- 完整說明生態系架構和使用方式

## 使用方式

```bash
# 同步 skill 索引
./scripts/sync-skills.sh

# 搜尋相關 skill
memory_search({query: "skill:* 量化 交易"})
```

## 未來擴展（Phase 1+）

MVP 驗證成功後，可考慮：
- 擴展 sqlite-memory schema（需發布新版）
- 自動安裝/更新 skill
- 多 skill 協作執行
- 效果度量儀表板
