---
name: commit-generate
description: Generate one-sentence commit message in Traditional Chinese from git diff output. Use when user provides git diff and requests a commit message.
---

# Commit Message Generator

從 git diff 產生單句繁體中文 commit message。

## Input

使用者提供 `git diff` 輸出。

## Classification Tags

| Tag | 適用情境 |
|-----|----------|
| `FEAT` | 新功能、新 endpoint、新元件 |
| `FIX` | Bug 修正、錯誤處理、nil check |
| `UPDATE` | 修改既有行為、參數調整 |
| `ADD` | 新增檔案/資源（非功能） |
| `REMOVE` | 刪除程式碼或檔案 |
| `REFACTOR` | 重構（行為不變） |
| `PERF` | 效能優化 |
| `STYLE` | 格式化、排版 |
| `DOC` | 文件、註解 |
| `TEST` | 測試相關 |
| `CHORE` | CI/CD、工具、依賴管理 |
| `SECURITY` | 安全性修補 |
| `BREAKING` | 破壞性變更 |

## Output Format
```
tag: 一句話描述變更內容（繁體中文）
```

## Rules

1. **單一 Tag** — 選擇最能代表本次變更核心意圖的 Tag
2. **Tag 優先序** — `BREAKING` > `FEAT` > `FIX` > `SECURITY` > `UPDATE` > `REFACTOR` > `PERF` > others
3. **簡潔** — 不超過 50 字，動詞開頭（新增、修正、重構、移除、優化）
4. **合併相關變更** — 多個小改動歸納為單一描述

## Examples
```
feat: 新增 Docker 環境自動偵測與資料庫路徑切換機制
fix: 修正使用者登入時 token 過期未正確處理的問題
refactor: 重構訂單模組並抽離共用驗證邏輯
update: 調整 API timeout 為 30 秒並加入 context 傳遞
chore: 升級 Go 版本至 1.22 並更新相依套件
breaking: 移除舊版 API v1 endpoint，需更新所有 client
security: 修補 SQL injection 漏洞並加入參數化查詢
perf: 優化批次查詢減少 N+1 問題
```
