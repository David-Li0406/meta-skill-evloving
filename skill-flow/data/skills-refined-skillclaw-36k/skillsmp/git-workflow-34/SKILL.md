---
name: git-workflow
description: Git 分支命名與工作流程規範
license: MIT
compatibility: opencode
metadata:
  version: '1.2.0'
  updated: '2026-01-20'
  audience: developers
  workflow: git
  language: zh-TW
---

## 我的功能

- 提供標準化的 Git 分支命名規範
- 確保分支類型、開發者名稱和功能描述的一致性
- 協助團隊遵循最佳的 Git 工作流程

## ⚠️ 開始前必讀

**🔴 在任何程式碼修改前，必須先執行以下步驟：**

```bash
# 1. 確認當前在 main 分支
git branch

# 2. 如果不在 main，切換到 main
git checkout main

# 3. 拉取最新代碼
git pull origin main

# 4. 建立新的功能分支
git checkout -b <type>/<developer-name>/<feature-description>
```

**❌ 絕對禁止**：直接在 main 分支上進行任何修改！

**✅ 正確流程**：永遠從 main 建立新分支 → 在新分支上開發 → 提交 → 推送 → 建立 PR

## 何時使用我

在以下情況下使用此技能：

- **🔴 任何程式碼修改前**（檢查是否已建立分支）
- 建立新的 Git 分支時
- 需要確認分支命名是否符合規範
- 撰寫 Commit 訊息時
- 團隊協作需要統一的分支管理策略
- 進行 code review 時檢查分支命名

## 分支命名規範

### 標準格式

```
<type>/<developer-name>/<feature-description>
```

### 分支類型 (type)

- **feat**: 新功能開發
  - 例如: `feat/lip/user-authentication`
  - 用於: 開發全新的功能或特性

- **fix**: 錯誤修復
  - 例如: `fix/lip/login-button-error`
  - 用於: 修復現有功能的 bug

- **refactor**: 程式碼重構
  - 例如: `refactor/lip/optimize-state-management`
  - 用於: 改善程式碼結構，但不改變功能

- **docs**: 文件更新
  - 例如: `docs/lip/update-readme`
  - 用於: 更新專案文件、README、註解等

- **style**: 樣式調整
  - 例如: `style/lip/improve-button-design`
  - 用於: UI/UX 改進、CSS 調整

- **test**: 測試相關
  - 例如: `test/lip/add-unit-tests`
  - 用於: 新增或修改測試

- **chore**: 雜項任務
  - 例如: `chore/lip/update-dependencies`
  - 用於: 依賴更新、建置配置等

### 命名原則

1. **使用小寫字母**: 所有分支名稱使用小寫
2. **使用連字符**: 單詞之間使用 `-` 連接
3. **簡潔明確**: 功能描述應簡短但具描述性
4. **英文命名**: 統一使用英文命名
5. **避免特殊字符**: 只使用字母、數字和連字符

### 實際範例

```bash
# ✅ 正確範例
git checkout -b feat/lip/add-language-selector
git checkout -b fix/lip/fix-search-modal-crash
git checkout -b refactor/lip/improve-pinia-structure
git checkout -b docs/lip/update-api-documentation

# ❌ 錯誤範例
git checkout -b new-feature              # 缺少類型和開發者名稱
git checkout -b feat/AddFeature          # 使用大寫字母
git checkout -b feat/lip/新增功能     # 使用中文
git checkout -b feat-lip-feature      # 格式錯誤
```

## 工作流程

### 1. 建立新分支

```bash
# 從 main 分支建立新分支
git checkout main
git pull origin main
git checkout -b <type>/<name>/<description>
```

### 2. 開發過程

```bash
# 定期提交變更
git add .
git commit -m "feat: implement user authentication"

# 定期同步主分支
git fetch origin main
git rebase origin/main
```

### 3. 準備合併

```bash
# 推送分支到遠端
git push -u origin <branch-name>

# 建立 Pull Request
# 使用 GitHub/GitLab 介面建立 PR
```

### 4. 合併後清理

```bash
# 刪除本地分支
git branch -d <branch-name>

# 刪除遠端分支
git push origin --delete <branch-name>
```

## 提交訊息規範

### 格式

```
<type>: <subject>

<body>

<footer>
```

### 類型 (type)

與分支類型相同: `feat`, `fix`, `refactor`, `docs`, `style`, `test`, `chore`

### 語言規範

**🔴 重要：Lucky50 專案使用繁體中文作為 Commit 訊息的預設語言**

- **優先使用繁體中文**：除非特別要求或有特殊情況，Commit 訊息應使用繁體中文書寫
- **標題 (subject)**：使用中文簡潔描述
- **內文 (body)**：使用中文詳細說明變更內容
- **註解 (footer)**：使用中文標註相關 issue 或參考資料

### 範例

```bash
# ✅ 正確：使用繁體中文（推薦）
git commit -m "feat: 新增語言選擇器組件"

# ✅ 正確：詳細的中文提交訊息
git commit -m "feat: 新增語言選擇器組件

- 實作包含 5 種語言選項的下拉選單
- 新增語言偏好設定到 localStorage
- 更新 i18n 配置

關聯 issue #123"

# ⚠️ 可接受：英文提交（特殊情況或國際協作）
git commit -m "feat: add language selector component

- Implement dropdown with 5 language options
- Add language persistence to localStorage
- Update i18n configuration

Closes #123"

# ❌ 錯誤：混用中英文
git commit -m "feat: 新增 language selector component"
```

### 提交訊息最佳實踐

1. **使用繁體中文為主**：確保團隊成員都能快速理解
2. **標題簡潔明確**：50 字以內，說明「做了什麼」
3. **內文詳細說明**：解釋「為什麼」和「怎麼做」
4. **使用條列式**：清楚列出所有變更項目
5. **關聯相關 issue**：在 footer 標註相關的 issue 編號

## 注意事項

1. **絕不直接在 main 分支開發**: 永遠從 main 建立新分支
2. **保持分支生命週期短**: 盡快完成並合併分支
3. **定期同步主分支**: 避免合併衝突
4. **使用有意義的名稱**: 讓他人能理解分支目的
5. **一個分支一個功能**: 避免在單一分支混合多個不相關的變更
6. **🔴 Commit 訊息使用繁體中文**: Lucky50 專案預設使用中文撰寫 Commit 訊息

## 常見問題

### Q: 如何處理長期開發的功能？

A: 建立 feature 分支，定期從 main rebase，完成後再合併。

### Q: 可以在分支名稱中使用 issue 編號嗎？

A: 可以，格式: `feat/lip/add-feature-#123`

### Q: 如何處理緊急修復？

A: 使用 `hotfix` 類型: `hotfix/lip/critical-bug-fix`

## 參考資源

- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
