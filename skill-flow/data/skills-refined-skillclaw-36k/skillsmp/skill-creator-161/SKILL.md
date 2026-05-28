---
name: skill-creator
description: 提供建立有效 Claude Skills 的指導，包含結構、範本和品質要求。
---

# Claude Skills 建立指南

本文件提供建立 Claude Skills 的完整指導。

## 什麼是 Claude Skills？

Claude Skills 是可自訂的工作流程，教導 Claude 如何根據您的獨特需求執行特定任務。Skills 使 Claude 能夠在所有 Claude 平台上以可重複、標準化的方式執行任務。

## 儲存庫結構

```
skill-name/
├── SKILL.md              # 必要：指令 + YAML 前置資料 (name, description)
├── scripts/              # 選用：可執行程式碼 (Python/Bash)
├── references/           # 選用：依需求載入上下文的文件
└── assets/               # 選用：輸出時使用的範本、圖片、字型
```

## Skill 品質要求

- 解決**實際問題**，基於真實使用案例
- 文件完善，包含清楚的說明和範例
- 在執行破壞性操作前進行確認
- 經過測試，驗證在 Claude.ai / Claude Code 上運作正常
- 資料夾命名：**小寫、連字號分隔**（如 `my-skill-name`）
- 如基於他人工作流程，標註靈感來源：`**靈感來源：** [人名/來源]`

## SKILL.md 範本

```markdown
---
name: skill-name
description: 一句話描述這個 skill 做什麼以及何時使用它。
---

# Skill 名稱

詳細描述此 skill 以及它幫助用戶完成什麼任務。

## 何時使用此 Skill

- 使用案例 1
- 使用案例 2

## 如何使用

### 基本使用
簡單範例提示

### 進階使用
包含選項的更複雜範例提示

## 範例

**使用者**："範例提示"
**輸出**：展示 skill 產生的結果
```

## Skills 清單

### 文件處理
處理 Office 文件和 PDF 的 skills。

| Skill | 說明 |
|-------|------|
| docx | 建立、編輯、分析 Word 文件 |
| pdf | 擷取文字、表格、合併和標註 PDF |
| pptx | 讀取、產生和調整投影片 |
| xlsx | 試算表操作：公式、圖表、資料轉換 |

### 開發與程式碼工具
軟體開發、文件和技術工作流程的 skills。

| Skill | 說明 |
|-------|------|
| artifacts-builder | 使用 React、Tailwind CSS 建立 HTML 成品 |
| changelog-generator | 從 git 提交建立變更日誌 |
| mcp-builder | 建立 MCP 伺服器 |
| skill-creator | 建立 Claude Skills 的指導 |
| webapp-testing | 使用 Playwright 測試網頁應用程式 |

### 商業與行銷
潛在客戶開發、競爭研究、品牌建立的 skills。

| Skill | 說明 |
|-------|------|
| brand-guidelines | 應用 Anthropic 品牌顏色和排版 |
| competitive-ads-extractor | 擷取和分析競爭對手廣告 |
| domain-name-brainstormer | 產生網域名稱並檢查可用性 |
| internal-comms | 撰寫內部通訊和更新 |
| lead-research-assistant | 識別和篩選高品質潛在客戶 |

### 溝通與寫作
改善溝通、分析對話和創建內容的 skills。

| Skill | 說明 |
|-------|------|
| content-research-writer | 協助撰寫高品質內容 |
| meeting-insights-analyzer | 分析會議記錄發現行為模式 |

### 創意與媒體
處理圖片、影片、音訊和創意內容的 skills。

| Skill | 說明 |
|-------|------|
| canvas-design | 建立視覺藝術（海報、設計） |
| image-enhancer | 改善圖片品質 |
| slack-gif-creator | 建立 Slack 優化的動畫 GIF |
| theme-factory | 應用專業字型和顏色主題 |
| video-downloader | 下載 YouTube 影片 |

### 生產力與組織
整理檔案、管理任務和個人生產力的 skills。

| Skill | 說明 |
|-------|------|
| file-organizer | 智慧整理檔案和資料夾 |
| invoice-organizer | 自動整理發票和收據 |
| raffle-winner-picker | 隨機選擇獲獎者 |

### 開發流程（來自 hi-skills）
軟體開發流程、測試驅動開發和程式碼審查的 skills。

| Skill | 說明 |
|-------|------|
| brainstorming | 將粗略想法轉化為完整設計 |
| dispatching-parallel-agents | 分派獨立子代理處理任務 |
| executing-plans | 執行實作計畫 |
| finishing-a-development-branch | 指導完成開發工作 |
| receiving-code-review | 處理收到的程式碼審查 |
| requesting-code-review | 請求程式碼審查 |
| subagent-driven-development | 子代理驅動開發 |
| systematic-debugging | 系統化除錯 |
| test-driven-development | 測試驅動開發 |
| using-git-worktrees | 建立隔離的 git worktrees |
| verification-before-completion | 完成前驗證 |
| writing-plans | 撰寫實作計畫 |
| writing-skills | 撰寫新 skills |

## 快速開始

### 在 Claude Code 中使用

```bash
# Skills 位置
~/.claude/plugins/local/hi-skills/skills/

# 呼叫方式
hi-skills:skill-name
```

### 在 Claude.ai 中使用

1. 點擊聊天介面中的 skill 圖示
2. 從市集新增 skills 或上傳自訂 skills
3. Claude 會根據任務自動啟用相關 skills

## 貢獻新 Skill

1. 建立以 skill 名稱命名的資料夾（小寫、連字號分隔）
2. 新增包含正確前置資料的 `SKILL.md`
3. 將 skill 加入本文件的適當類別中
4. 跨平台測試您的 skill
5. **更新索引**：執行 `/update-skills-index` 或手動更新 `~/.claude/skills/README.md`

## 資源

- [Claude Skills 概述](https://www.anthropic.com/news/skills)
- [Skills 使用者指南](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [建立自訂 Skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [Anthropic Skills 儲存庫](https://github.com/anthropics/skills)

## 授權

Apache License 2.0
