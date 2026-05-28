---
name: readme-generator
description: 建立高品質的 README.md 檔案。提供結構規範、格式指南與範例參考，確保 README 吸引人、資訊豐富且易讀。適用於開源專案或任何需要專業文件的場景。
---

# README Generator 技能

此技能提供建立專業 README.md 檔案的標準化流程與最佳實踐。

## 何時使用此技能

- 為新專案建立 README
- 改善現有 README 的結構與內容
- 確保 README 符合開源社群標準

## 核心原則

> [!IMPORTANT]
> README 是專案的「門面」，應讓讀者在 30 秒內了解專案價值。

- ✅ **吸引人**：清楚說明專案解決什麼問題
- ✅ **資訊豐富**：提供足夠的開始使用資訊
- ✅ **易讀**：結構清晰、段落簡潔

## 標準流程

### 步驟 1：分析專案 🔍

1. 瀏覽整個專案結構
2. 識別主要功能與技術棧
3. 找出專案 logo 或 icon（如有）

### 步驟 2：規劃結構 📋

建議的 README 結構：

```markdown
# 專案名稱

[簡短描述 - 一句話說明專案價值]

## Features / 功能特色

## Getting Started / 快速開始

### Prerequisites / 前置需求

### Installation / 安裝

### Usage / 使用方式

## Documentation / 文件（可選）

## Contributing / 貢獻指南（連結至 CONTRIBUTING.md）

## License（連結至 LICENSE）
```

### 步驟 3：撰寫內容 ✍️

#### 標題與描述
- 使用專案 logo（如有）
- 一句話描述專案價值
- 加入 badges（CI 狀態、版本、授權）

#### Features 區塊
- 使用列表呈現 3-5 個主要功能
- 避免技術術語，以使用者視角描述

#### Getting Started 區塊
- 提供可直接複製的指令
- 包含最小可行範例

### 步驟 4：格式檢查 ✅

- [ ] 使用 GFM（GitHub Flavored Markdown）
- [ ] 適當使用 GitHub admonitions（`> [!NOTE]`、`> [!WARNING]`）
- [ ] 避免過度使用 emoji
- [ ] 保持簡潔，避免冗長段落
- [ ] 不包含 LICENSE、CONTRIBUTING、CHANGELOG 等獨立檔案的內容

## 禁止事項 🚫

- ❌ 過度使用 emoji
- ❌ 冗長的段落（超過 3-4 行）
- ❌ 在 README 中重複 LICENSE 或 CONTRIBUTING 內容
- ❌ 使用過時的資訊或範例

## 參考文件

- [範例 README 清單](references/examples.md)
- [GitHub Admonitions 語法](https://github.com/orgs/community/discussions/16925)
