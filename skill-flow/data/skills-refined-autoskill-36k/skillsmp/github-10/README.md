# README.md 強制維護機制

## 🚨 核心原則

**任何變更完成後，必須立即執行以下強制流程：**

### 1️⃣ 立即檢查 README.md 影響範圍

#### 需要檢查的 README 檔案清單：

```bash
# 專案主要 README 檔案
README.md                           # 專案根目錄
.opencode/skills/README.md          # Skills 說明
docs/README.md                      # 文檔目錄
CONTRIBUTING.md                     # 貢獻指南
.github/README.md                   # GitHub 相關說明
```

#### 檢查指令：

```bash
# 檢查變更的檔案
git status --porcelain

# 檢查受影響的 README 區段
git diff --name-only HEAD~1 | grep -E "(README|\.md)"
```

### 2️⃣ 立即更新對應區段

#### 變更類型與對應更新：

| 變更類型             | 影響的 README                           | 必需更新內容                    |
| -------------------- | --------------------------------------- | ------------------------------- |
| **新增 Vue 組件**    | `README.md`                             | 組件列表、功能描述、使用範例    |
| **修改 Pinia Store** | `README.md`、`docs/state-management.md` | Store 結構、使用方式、API 變更  |
| **新增 Skill**       | `.opencode/skills/README.md`            | Skills 列表、使用說明、載入時機 |
| **更新依賴套件**     | `README.md`、`package.json`             | 安裝指令、版本要求、變更日誌    |
| **修改配置檔案**     | `README.md`、`docs/configuration.md`    | 配置說明、環境變數、範例檔案    |
| **新增 API 端點**    | `docs/api.md`、`README.md`              | API 列表、使用範例、錯誤處理    |
| **更新建置流程**     | `README.md`、`CONTRIBUTING.md`          | 建置指令、部署步驟、開發環境    |

#### 立即更新檢查清單：

- [ ] 確認哪些 README 檔案需要更新
- [ ] 識別受影響的具體區段
- [ ] 準備更新內容草稿
- [ ] 確認更新內容的準確性

### 3️⃣ 完整驗證更新內容

#### 格式驗證：

```bash
# Markdown 語法檢查
npx markdownlint README.md

# 連結有效性檢查
npx markdown-link-check README.md

# 拼寫檢查（可選）
npx cspell README.md
```

#### 內容驗證：

```bash
# 本地預覽（如果有預覽工具）
pnpm run docs:dev

# 或使用 VS Code 預覽
code README.md
```

#### 驗證項目清單：

- [ ] **功能對應性**：所有新增/修改功能都有說明
- [ ] **指令正確性**：安裝、運行、測試指令可正常執行
- [ ] **目錄同步**：README 中的目錄結構與實際一致
- [ ] **版本一致性**：所有地方的版本號同步更新
- [ ] **連結有效性**：所有內外部連結都能正常訪問
- [ ] **程式碼範例**：範例代碼可以複製貼上直接執行
- [ ] **格式統一性**：標題、列表、程式碼塊格式一致
- [ ] **語言一致性**：使用繁體中文，符合專案語境

### 4️⃣ 提交包含 README.md 更新的 Commit

#### 🚨 重要規則：絕不單獨提交 README.md！

**正確的 Commit 模式：**

```bash
# 功能開發 + README 更新
git add src/components/NewComponent.vue README.md
git commit -m "feat: 新增使用者認證組件並更新 README.md 說明"

# 修復問題 + README 更新
git add src/utils/validation.js docs/api.md
git commit -m "fix: 修復驗證邏輯錯誤並更新 API 文檔"

# Skill 更新 + README 更新
git add .opencode/skills/new-skill/ .opencode/skills/README.md
git commit -m "feat: 新增 vue skill 並更新 skills 說明文檔"
```

**❌ 錯誤的 Commit 模式：**

```bash
# 功能開發
git add src/components/NewComponent.vue
git commit -m "feat: 新增使用者認證組件"

# README 更新（單獨 commit - 禁止！）
git add README.md
git commit -m "docs: 更新 README.md"  # ❌ 這樣做會被 Git hooks 攔截
```

## 🔄 自動化檢查機制

### Git Hooks 整合

在現有的 Git hooks 中加入 README.md 強制檢查：

```bash
# .githooks/pre-commit
#!/bin/bash

# 檢查是否有程式碼變更但沒有 README 變更
CODE_CHANGED=$(git diff --cached --name-only | grep -E "\.(vue|ts|js|json)$" | wc -l)
README_CHANGED=$(git diff --cached --name-only | grep -E "README|\.md$" | wc -l)

if [ "$CODE_CHANGED" -gt 0 ] && [ "$README_CHANGED" -eq 0 ]; then
    echo "❌ 檢測到程式碼變更但沒有對應的 README.md 更新！"
    echo ""
    echo "🔥 請立即執行 README.md 強制維護流程："
    echo "   1️⃣ 檢查受影響的 README 檔案"
    echo "   2️⃣ 更新對應的說明區段"
    echo "   3️⃣ 驗證更新內容的正確性"
    echo "   4️⃣ 與程式碼變更一起提交"
    echo ""
    echo "📚 請參考：.opencode/skills/github/README.md"
    exit 1
fi

echo "✅ README.md 維護檢查通過"
```

### 持續整合（CI）檢查

在 GitHub Actions 中加入自動檢查：

```yaml
# .github/workflows/readme-check.yml
name: README.md 維護檢查

on:
  pull_request:
    paths:
      - 'src/**'
      - 'docs/**'
      - 'README.md'
      - '.opencode/skills/**'

jobs:
  readme-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: 檢查 README.md 與程式碼同步性
        run: |
          # 檢查是否有未更新的 README
          # 這裡可以加入更詳細的檢查邏輯
          echo "檢查 README.md 維護狀態..."
```

## 📋 緊急處理流程

### 忘記更新 README.md 怎麼辦？

**步驟 1：立即修正**

```bash
# 立即切換到對應分支
git checkout <feature-branch>

# 更新 README.md
# （編輯受影響的 README 檔案）

# 修正 commit（如果還沒推送）
git add README.md
git commit --amend -m "修正訊息：加上 README.md 更新說明"

# 如果已經推送，需要建立新的 commit
git add README.md
git commit -m "docs: 補充更新 README.md 說明"
git push origin <feature-branch>
```

**步驟 2：學習記錄**

- 在 team meeting 中分享經驗
- 更新開發流程檢查清單
- 考慮加入更多自動化檢查

## 🎯 最佳實踐總結

### 開發流程整合

**完整的開發流程：**

1. **規劃階段**：預估需要更新的 README 區段
2. **開發階段**：邊開發邊記錄變更點
3. **測試階段**：驗證新功能與文檔的一致性
4. **文檔更新**：立即更新所有受影響的 README
5. **最終驗證**：檢查格式、連結、內容正確性
6. **提交變更**：程式碼 + 文檔 在同一個 commit

### 團隊協作規範

**Code Review 重點：**

- ✅ 程式碼變更是否包含對應的 README 更新
- ✅ README 更新內容是否準確完整
- ✅ 所有連結和範例是否有效
- ✅ 符合繁體中文語境規範

**新人入職培訓：**

- 學習 README.md 強制維護機制
- 練習立即更新文檔的習慣
- 熟悉自動化檢查工具的使用

---

**記住：文檔不是事後補充，而是開發過程中不可或缺的一部分！** 🚀
