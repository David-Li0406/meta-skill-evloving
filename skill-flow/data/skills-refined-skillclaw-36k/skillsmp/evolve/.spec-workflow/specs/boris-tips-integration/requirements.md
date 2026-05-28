# Requirements: Boris Tips Integration

> 將 Boris Cherny 的 Claude Code 使用技巧整合到 self-evolving-agent 中

## 背景

Boris Cherny（Claude Code 創作者）分享了 13 條個人使用技巧，包括權限管理和大型 codebase 優化。這些技巧已記錄在 `.claude/memory/learnings/2025-01-07-boris-cherny-claude-code-tips.md`，但尚未整合到 skill 文檔中。

## 範圍

### In Scope (P0 + P1)

| 優先級 | 項目 | 說明 |
|--------|------|------|
| **P0** | Permissions 配置建議 | 在 PSB Setup 文檔中加入 `/permissions` 配置建議 |
| **P1** | Large Codebase 優化 | 新增 `large-codebase.md` 文檔，指導 `fileSuggestion` 配置 |

### Out of Scope

- P2/P3 項目（Opus thinking 模式、平行執行、ralph-wiggum 整合）
- 自動化腳本實作
- CI/CD 整合

## 使用者故事

### US-1: Permissions 配置建議 (P0)

**As a** self-evolving-agent 使用者
**I want** 在 PSB Setup 階段獲得 Claude Code 權限配置建議
**So that** 我可以預先允許安全的常用命令，避免頻繁的權限詢問

**驗收標準：**
- [ ] `psb-setup.md` 包含 permissions 配置段落
- [ ] 提供 `settings.local.json` 範例配置
- [ ] 說明何時使用 `/permissions` vs `--dangerously-skip-permissions`
- [ ] 與現有 PSB 7 步驟清單整合

### US-2: Large Codebase 優化文檔 (P1)

**As a** 在大型專案中使用 self-evolving-agent 的開發者
**I want** 了解如何優化 Claude Code 的檔案搜尋效能
**So that** 我可以在大型 monorepo 中獲得快速的檔案搜尋體驗（8秒 → 200ms）

**驗收標準：**
- [ ] 新增 `skills/06-scaling/_base/large-codebase.md`
- [ ] 包含問題診斷（何時需要優化）
- [ ] 提供 `fileSuggestion` 配置範例
- [ ] 包含 `file-suggestion.sh` 腳本模板
- [ ] 說明適用場景和限制

## 技術約束

1. 遵循現有 skill 目錄結構（`_base/` 目錄）
2. 使用 Markdown 格式，保持一致的文檔風格
3. 更新 `skills/SKILL.md` 主入口的模組列表

## 參考資料

- 來源：Boris Cherny Twitter/Threads + @leocooout 推文
- 記錄位置：`.claude/memory/learnings/2025-01-07-boris-cherny-claude-code-tips.md`
