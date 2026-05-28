---
name: new-skill
description: 引導式建立新 Skill - 完整工作流（訪談 → 生成 → 驗證 → 發布）
arguments:
  - name: name
    description: Skill 名稱
    required: true
---

# /new-skill

引導式建立新 Skill 的完整工作流。

## 別名

```bash
/evolve --new-skill <name>
```

## 流程

### Stage 1: 引導式訪談

我會問你以下問題：

1. **問題定義**：這個 skill 要解決什麼問題？
2. **目標使用者**：新手 / 進階 / 專家？
3. **前置需求**：需要什麼 MCP servers 或 CLI tools？
4. **參考來源**：有沒有類似的 skill 可以參考？

### Stage 2: 分析 + 生成

1. 搜尋類似 skills 作為參考
2. 選擇範本（basic / advanced）
3. 生成 SKILL.md 初稿
4. 建立目錄結構

### Stage 3: 驗證

執行驗證腳本檢查：
- SKILL.md frontmatter 格式
- 必要欄位存在
- scripts 可執行

### Stage 4: 發布到 GitHub

1. 建立新 repo 或加入現有 repo
2. 生成 README.md
3. git commit + push
4. 輸出安裝指令

## 範本

- `basic-skill.md` - 簡單指令，無依賴
- `advanced-skill.md` - 需要 MCP，複雜流程

## 使用範例

```bash
/new-skill "git commit helper"
/new-skill "api-documentation-generator"
```
