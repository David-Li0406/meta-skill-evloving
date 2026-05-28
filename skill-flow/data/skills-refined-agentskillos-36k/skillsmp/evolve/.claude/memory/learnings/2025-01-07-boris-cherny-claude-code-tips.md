---
date: "2025-01-07"
updated: "2026-01-12"
tags: [claude-code, best-practices, boris-cherny, workflow, subagents, verification, teleport, permissions, large-codebase, file-suggestion]
task: 研究 Claude Code 創作者的使用技巧
status: resolved
source:
  - https://www.threads.com/@boris_cherny/post/DTBVlMIkpcm
  - https://x.com/bcherny/status/2009878642256691704
  - https://x.com/leocooout/status/2009337600742707335
---

# Boris Cherny 的 Claude Code 使用技巧

## 情境
Boris Cherny 是 Claude Code 的創作者，他分享了 13 條個人使用技巧。

## 核心洞察

### 最重要的一條（Tip #13）
**給 Claude 驗證工作的方式，能提升 2-3 倍品質**

Boris 使用 Chrome extension 讓 Claude 測試 UI，開啟瀏覽器、測試、迭代直到成功。

### 平行化策略（Tips #1, #2）
- 本地跑 5 個 Claude（終端分頁 1-5）
- 雲端 claude.ai/code 另外跑 5-10 個
- 每個專注不同任務
- **`--teleport` 命令**：在本地和網頁會話之間切換
- **iOS app**：早上透過手機啟動會話，稍後查看進度

### 團隊協作（Tips #4, #5）
- 單一 CLAUDE.md 存入 git，每週更新
- PR 上 @.claude tag 自動更新（GitHub Action）

### 模型選擇
**預設使用 Opus 4.5 + thinking 模式**：雖然較慢，但品質更高，減少返工反而更快完成。

### 工作流程優化
| 技巧 | 說明 |
|------|------|
| Plan mode | shift+tab 兩次起手，然後 auto-accept |
| Slash commands | /commit-push-pr 等內部工作流程 |
| Subagents | code-simplifier, verify-app, build-validator |
| PostToolUse hook | 自動格式化程式碼 |
| `/permissions` | 精細權限管理，預先允許安全常用命令，避免 `--dangerously-skip-permissions` |

### 長時間任務處理（Tip #12）
- Stop hook 驗證 background agent 工作
- ralph-wiggum plugin 做確定性處理
- --permission-mode=dontAsk 或 sandbox 避免阻塞

### MCP 整合（Tip #11）
```json
{
  "mcpServers": {
    "slack": {
      "type": "http",
      "url": "https://slack.mcp.anthropic.com/mcp"
    }
  }
}
```
整合 Slack, BigQuery, Sentry 等工具。

### 大型 Codebase 優化（Boris 轉推 by @leocooout）

> **Great tip for bigger codebases** - Boris Cherny, 2026-01-10

TikTok iOS 工程師分享的優化技巧：將檔案搜尋時間從 **8 秒降到 200 毫秒**。

**問題**：預設的 fast filesystem traversal 對小專案很好，但大型專案會變慢。

**解決方案**：使用自訂索引系統，透過 `settings.json` 配置：

```json
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

**效果**：在 Claude 中提及任何檔案都幾乎瞬間完成。

**適用場景**：
- 大型 monorepo（如 TikTok）
- 檔案數量超過數萬個的專案
- 檔案搜尋明顯變慢時

## 對 self-evolving-agent 的改進建議

1. **強化驗證迴圈**
   - PDCA Check 階段加入自動測試執行
   - 整合 verify-app 概念

2. **Subagents 策略池**
   - 加入 code-simplifier 策略
   - 加入 build-validator 策略

3. **Hooks 整合**
   - PostToolUse hook 自動格式化
   - Stop hook 處理長時間進化任務

4. **ralph-wiggum 整合**
   - 長時間任務使用 ralph-wiggum loop

## 核心哲學（2026-01-12 更新）

> **AI 是可調度的能力，而非單純的工具**

Boris 的核心理念：
- 像調度計算資源一樣分配認知
- 優化**吞吐量**而非僅僅是對話
- 將 AI 視為可調度的能力（schedulable capability）

這解釋了為什麼他會平行運行 5-10 個 Claude：不是為了「聊得更快」，而是為了**最大化整體產出**。

## 驗證
✅ 已記錄完整 13 條技巧
✅ 提出具體改進建議
✅ 2026-01-12 補充：teleport、permissions、Opus thinking、哲學觀
✅ 2026-01-12 補充：大型 codebase 優化（fileSuggestion 自訂配置）

## 相關檔案
- `SKILL.md` - self-evolving-agent 技能定義
- `.claude/memory/strategies/` - 策略記錄
- `.claude/memory/learnings/2026-01-12-code-simplifier-integration.md` - code-simplifier 整合
