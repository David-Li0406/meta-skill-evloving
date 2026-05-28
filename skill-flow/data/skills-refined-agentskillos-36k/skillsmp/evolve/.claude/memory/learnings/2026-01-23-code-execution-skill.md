# Code Execution Skill 開發記錄

**日期**: 2026-01-23
**類型**: Skill 創建
**標籤**: code-execution, mcp, token-optimization, skill-design

---

## 背景

研究 MCP 設計模式後，發現 **Code Execution 模式**（Anthropic 2025 提出）可大幅減少 Token 消耗（98%+）。決定將此模式封裝為獨立 Skill。

## 核心概念

### Code Execution 模式的本質

```
傳統 Tool Calling：
  Model → Tool → Model → Tool → Model → ...
  每次結果都傳回 Model，消耗大量 Context

Code Execution：
  Model → 生成程式碼 → 執行環境處理 → 精簡結果
  資料處理在執行環境中完成，只回傳最終結果
```

### 效率對比

| 場景 | 傳統 | Code Execution | 節省 |
|------|-----|---------------|------|
| 3 步驟 | 3x | 0.5x | 83% |
| 10 步驟 | 10x | 0.3x | 97% |
| 100 項迴圈 | 100x | 0.1x | 99% |

## Skill 設計決策

### 1. 觸發時機

明確定義何時使用：
- ✅ 3+ 步驟工作流程
- ✅ 迴圈處理多項目
- ✅ 條件分支邏輯
- ❌ 單一 Tool 呼叫
- ❌ 簡單 Q&A

### 2. 三種執行模式

1. **Claude Code 內建** — 直接撰寫 Python/Bash 處理
2. **Programmatic Tool Calling** — API beta 功能
3. **CLI 批次腳本** — 當 MCP Server 提供 CLI 時

### 3. 撰寫指南四原則

1. 資料處理在本地
2. 批次優於逐一
3. 提前過濾
4. 錯誤處理

## 與 evolve 整合

在 PDCA 各階段的應用：

```
Plan: 識別是否適合 Code Execution
Do: 撰寫批次處理程式碼
Check: 驗證結果，評估 Token 節省
Act: 記錄成功模式
```

## 學到的經驗

1. **Anthropic 已官方支援** — `advanced-tool-use-2025-11-20` beta
2. **Claude Code 本身就是執行環境** — 不需要額外建立
3. **安全性是關鍵** — 需要沙箱、限制、錯誤處理

## 產出

- Skill 檔案: `.claude/skills/code-execution/SKILL.md`
- 整合文檔: 更新 `05-integration/README.md`
- 研究報告: `.claude/memory/research/2026-01-23-mcp-advanced-patterns-detail.md`

## 參考資源

- [Code Execution with MCP - Anthropic](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [Programmatic Tool Calling - Claude Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)
- [Claude Code Sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing)
