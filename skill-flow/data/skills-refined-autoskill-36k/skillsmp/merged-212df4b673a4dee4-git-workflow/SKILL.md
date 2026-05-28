---
name: git-workflow
description: 使用此技能以遵循標準化的 Git 分支命名和工作流程規範，確保團隊協作的有效性和一致性。
---

# Git Workflow Skill

> **版本控制是工程的基石**
> 清晰的提交歷史 = 可追溯的項目演進

---

## ⚠️ 開始前必讀

在任何程式碼修改前，必須先執行以下步驟：

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

---

## 🌿 分支策略

### 標準分支

| 分支 | 用途 | 保护 |
|:---|:---|:---|
| `main` | 生产代码 | ✅ 保护 |
| `develop` | 开发主线 | ✅ 保护 |
| `feature/*` | 功能开发 | ❌ |
| `bugfix/*` | Bug修复 | ❌ |
| `hotfix/*` | 紧急修复 | ❌ |
| `release/*` | 发布准备 | ❌ |

### 分支命名

標準格式：

```
<type>/<developer-name>/<feature-description>
```

### 分支類型 (type)

- **feat**: 新功能開發
- **fix**: 錯誤修復
- **refactor**: 程式碼重構
- **docs**: 文件更新
- **style**: 樣式調整
- **test**: 測試相關
- **chore**: 雜項任務

### 命名原則

1. 使用小寫字母
2. 使用連字符
3. 簡潔明確
4. 英文命名
5. 避免特殊字符

### 實際範例

```bash
# ✅ 正確範例
git checkout -b feat/lip/add-language-selector
git checkout -b fix/lip/fix-search-modal-crash

# ❌ 錯誤範例
git checkout -b new-feature              # 缺少類型和開發者名稱
```

---

## 📝 提交規範

### Conventional Commits

```
<type>: <subject>

<body>

<footer>
```

### 提交訊息最佳實踐

1. 使用繁體中文為主
2. 標題簡潔明確
3. 內文詳細說明
4. 使用條列式
5. 關聯相關 issue

### 範例

```bash
# ✅ 正確：使用繁體中文（推薦）
git commit -m "feat: 新增語言選擇器組件"
```

---

## 🔄 工作流程

### 1. 開始新功能

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
```

### 4. 合併後清理

```bash
# 刪除本地分支
git branch -d <branch-name>

# 刪除遠端分支
git push origin --delete <branch-name>
```

---

## 🔙 回滚策略

### 回滚单个提交

```bash
# 创建新提交来撤销
git revert <commit-hash>
```

### 回滚到特定版本

```bash
# 软回滚（保留修改）
git reset --soft <commit-hash>

# 硬回滚（丢弃修改）
git reset --hard <commit-hash>
```

---

## 📋 PR/MR 检查清单

创建 Pull Request 前：

- [ ] 代码已本地测试
- [ ] 提交历史清晰
- [ ] 无调试代码
- [ ] 已更新文档（如需要）
- [ ] 已添加测试（如需要）
- [ ] 符合代码规范

---

## ⚠️ 禁止操作

```bash
# ❌ 禁止在 main 上直接修改
git checkout main
git commit ...  # 禁止！

# ❌ 禁止 force push 保护分支
git push -f origin main  # 禁止！
```

---

## 常見問題

### Q: 如何處理長期開發的功能？

A: 建立 feature 分支，定期從 main rebase，完成後再合併。

### Q: 可以在分支名稱中使用 issue 編號嗎？

A: 可以，格式: `feat/lip/add-feature-#123`

### Q: 如何處理緊急修復？

A: 使用 `hotfix` 類型: `hotfix/lip/critical-bug-fix`

---

## 參考資源

- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

---

**核心**: 小步提交、清晰歷史、保護主幹 | **規範**: Conventional Commits